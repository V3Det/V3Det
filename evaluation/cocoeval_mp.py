import copy
import itertools
import multiprocessing as mp
import time
from collections import defaultdict

import mmengine
import numpy as np
from mmengine.logging import MMLogger
from pycocotools.cocoeval import COCOeval, Params
from tqdm import tqdm


class COCOevalMP(COCOeval):

    def __init__(self, cocoGt=None, cocoDt=None, iouType='bbox', num_proc=8,
                 tree_ann_path='data/V3Det/annotations/v3det_2023_v1_category_tree.json',
                 ignore_parent_child_gts=True):
        '''
        Initialize CocoEval using coco APIs for gt and dt
        :param cocoGt: coco object with ground truth annotations
        :param cocoDt: coco object with detection results
        :return: None
        '''
        if not iouType:
            print('iouType not specified. use default iouType segm')
        self.cocoGt = cocoGt  # ground truth COCO API
        self.cocoDt = cocoDt  # detections COCO API
        self.evalImgs = defaultdict(list)  # per-image per-category evaluation results [KxAxI] elements
        self.eval = {}  # accumulated evaluation results
        self._gts = defaultdict(list)  # gt for evaluation
        self._dts = defaultdict(list)  # dt for evaluation
        self.params = Params(iouType=iouType)  # parameters
        self._paramsEval = {}  # parameters for evaluation
        self.stats = []  # result summarization
        self.ious = {}  # ious between all gts and dts
        self.num_proc = num_proc  # num of process
        self.tree_ann_path = tree_ann_path
        self.ignore_parent_child_gts = ignore_parent_child_gts
        if not mmengine.exists(tree_ann_path):
            print(f'{tree_ann_path} not exist')
            raise FileNotFoundError
        if not cocoGt is None:
            self.params.imgIds = sorted(cocoGt.getImgIds())
            self.params.catIds = sorted(cocoGt.getCatIds())
        # split base novel cat ids
        self.base_inds = []
        self.novel_inds = []
        for i, c in enumerate(self.cocoGt.dataset['categories']):
            if c['novel']:
                self.novel_inds.append(i)
            else:
                self.base_inds.append(i)

    def _prepare(self):
        '''
        Prepare ._gts and ._dts for evaluation based on params
        :return: None
        '''

        def _toMask(anns, coco):
            # modify ann['segmentation'] by reference
            for ann in anns:
                rle = coco.annToRLE(ann)
                ann['segmentation'] = rle

        p = self.params
        if p.useCats:
            gts = []
            dts = []
            img_ids = set(p.imgIds)
            cat_ids = set(p.catIds)
            for gt in self.cocoGt.dataset['annotations']:
                if (gt['category_id'] in cat_ids) and (gt['image_id']
                                                       in img_ids):
                    gts.append(gt)
            for dt in self.cocoDt.dataset['annotations']:
                if (dt['category_id'] in cat_ids) and (dt['image_id']
                                                       in img_ids):
                    dts.append(dt)
        else:
            gts = self.cocoGt.loadAnns(self.cocoGt.getAnnIds(imgIds=p.imgIds))
            dts = self.cocoDt.loadAnns(self.cocoDt.getAnnIds(imgIds=p.imgIds))

        # convert ground truth to mask if iouType == 'segm'
        if p.iouType == 'segm':
            _toMask(gts, self.cocoGt)
            _toMask(dts, self.cocoDt)
        # set ignore flag
        for gt in gts:
            gt['ignore'] = gt['ignore'] if 'ignore' in gt else 0
            gt['ignore'] = 'iscrowd' in gt and gt['iscrowd']
            if p.iouType == 'keypoints':
                gt['ignore'] = (gt['num_keypoints'] == 0) or gt['ignore']
        self._gts = defaultdict(list)  # gt for evaluation
        self._dts = defaultdict(list)  # dt for evaluation
        for gt in gts:
            self._gts[gt['image_id'], gt['category_id']].append(gt)
        for dt in dts:
            self._dts[dt['image_id'], dt['category_id']].append(dt)

        if self.ignore_parent_child_gts:
            # for each category, maintain its child categories
            cat_tree = mmengine.load(self.tree_ann_path)
            catid2treeid = cat_tree['categoryid2treeid']
            treeid2catid = {v: k for k, v in catid2treeid.items()}
            ori_ancestor2descendant = cat_tree['ancestor2descendant']
            ancestor2descendant = dict()
            for k, v in ori_ancestor2descendant.items():
                if k in treeid2catid:
                    ancestor2descendant[k] = v
            ancestor2descendant_catid = defaultdict(set)
            for tree_id in ancestor2descendant:
                cat_id = treeid2catid[tree_id]
                descendant_ids = ancestor2descendant[tree_id]
                for descendant_id in descendant_ids:
                    if descendant_id not in treeid2catid:
                        continue
                    descendant_catid = treeid2catid[descendant_id]
                    ancestor2descendant_catid[int(cat_id)].add(int(descendant_catid))
            self.ancestor2descendant_catid = ancestor2descendant_catid
            # If a gt has child category cat_A, and dts of this image has this category, add this gt to gt<img_id, cat_A>
            for gt in gts:
                ignore_cats = []
                for child_cat_id in self.ancestor2descendant_catid[gt['category_id']]:
                    if len(self._dts[gt['image_id'], child_cat_id]) > 0:
                        ignore_cats.append(child_cat_id)
                if len(ignore_cats) == 0:
                    continue
                ignore_gt = copy.deepcopy(gt)
                ignore_gt['category_id'] = ignore_cats
                ignore_gt['ignore'] = 1
                for child_cat_id in ignore_cats:
                    self._gts[gt['image_id'], child_cat_id].append(ignore_gt)

        self.evalImgs = defaultdict(
            list)  # per-image per-category evaluation results
        self.eval = {}  # accumulated evaluation results

    def evaluate(self):
        """Run per image evaluation on given images and store results (a list
        of dict) in self.evalImgs.

        :return: None
        """
        tic = time.time()
        print('Running per image evaluation...')
        p = self.params
        # add backward compatibility if useSegm is specified in params
        if p.useSegm is not None:
            p.iouType = 'segm' if p.useSegm == 1 else 'bbox'
            print('useSegm (deprecated) is not None. Running {} evaluation'.
                  format(p.iouType))
        print('Evaluate annotation type *{}*'.format(p.iouType))
        p.imgIds = list(np.unique(p.imgIds))
        if p.useCats:
            p.catIds = list(np.unique(p.catIds))
        p.maxDets = sorted(p.maxDets)
        self.params = p

        # loop through images, area range, max detection number
        catIds = p.catIds if p.useCats else [-1]

        nproc = self.num_proc
        split_size = len(catIds) // nproc
        mp_params = []
        for i in range(nproc):
            begin = i * split_size
            end = (i + 1) * split_size
            if i == nproc - 1:
                end = len(catIds)
            mp_params.append((catIds[begin:end], ))

        MMLogger.get_current_instance().info(
            f'start multi processing evaluation with nproc: {nproc}...')
        with mp.Pool(nproc) as pool:
            self.evalImgs = pool.starmap(self._evaluateImg, mp_params)

        self.evalImgs = list(itertools.chain(*self.evalImgs))

        self._paramsEval = copy.deepcopy(self.params)
        toc = time.time()
        print('DONE (t={:0.2f}s).'.format(toc - tic))

    def _evaluateImg(self, catids_chunk):
        self._prepare()
        p = self.params
        maxDet = max(p.maxDets)
        all_params = itertools.product(catids_chunk, p.areaRng, p.imgIds)
        all_params_len = len(catids_chunk) * len(p.areaRng) * len(p.imgIds)
        evalImgs = [
            self.evaluateImg(imgId, catId, areaRng, maxDet)
            for catId, areaRng, imgId in tqdm(all_params, total=all_params_len)
        ]
        return evalImgs

    def evaluateImg(self, imgId, catId, aRng, maxDet):
        p = self.params
        if p.useCats:
            gt = self._gts[imgId, catId]
            dt = self._dts[imgId, catId]
        else:
            gt = [_ for cId in p.catIds for _ in self._gts[imgId, cId]]
            dt = [_ for cId in p.catIds for _ in self._dts[imgId, cId]]
        if len(gt) == 0 and len(dt) == 0:
            return None

        for g in gt:
            if g['ignore'] or (g['area'] < aRng[0] or g['area'] > aRng[1]):
                g['_ignore'] = 1
            else:
                g['_ignore'] = 0

        # sort dt highest score first, sort gt ignore last
        gtind = np.argsort([g['_ignore'] for g in gt], kind='mergesort')
        gt = [gt[i] for i in gtind]
        dtind = np.argsort([-d['score'] for d in dt], kind='mergesort')
        dt = [dt[i] for i in dtind[0:maxDet]]
        iscrowd = [int(o['iscrowd']) for o in gt]
        # load computed ious
        # ious = self.ious[imgId, catId][:, gtind] if len(self.ious[imgId, catId]) > 0 else self.ious[imgId, catId] # noqa
        ious = self.computeIoU(imgId, catId)
        ious = ious[:, gtind] if len(ious) > 0 else ious

        T = len(p.iouThrs)
        G = len(gt)
        D = len(dt)
        gtm = np.zeros((T, G))
        dtm = np.zeros((T, D))
        gtIg = np.array([g['_ignore'] for g in gt])
        dtIg = np.zeros((T, D))
        if not len(ious) == 0:
            for tind, t in enumerate(p.iouThrs):
                for dind, d in enumerate(dt):
                    # information about best match so far (m=-1 -> unmatched)
                    iou = min([t, 1 - 1e-10])
                    m = -1
                    for gind, g in enumerate(gt):
                        # if this gt already matched, and not a crowd, continue
                        if gtm[tind, gind] > 0 and not iscrowd[gind]:
                            continue
                        # if dt matched to reg gt, and on ignore gt, stop
                        if m > -1 and gtIg[m] == 0 and gtIg[gind] == 1:
                            break
                        # continue to next gt unless better match made
                        if ious[dind, gind] < iou:
                            continue
                        # if match successful and best so far,
                        # store appropriately
                        iou = ious[dind, gind]
                        m = gind
                    # if match made store id of match for both dt and gt
                    if m == -1:
                        continue
                    dtIg[tind, dind] = gtIg[m]
                    dtm[tind, dind] = gt[m]['id']
                    gtm[tind, m] = d['id']
        # set unmatched detections outside of area range to ignore
        a = np.array([d['area'] < aRng[0] or d['area'] > aRng[1]
                      for d in dt]).reshape((1, len(dt)))
        dtIg = np.logical_or(dtIg, np.logical_and(dtm == 0, np.repeat(a, T,
                                                                      0)))
        # store results for given image and category

        return {
            'image_id': imgId,
            'category_id': catId,
            'aRng': aRng,
            'maxDet': maxDet,
            'dtIds': [d['id'] for d in dt],
            'gtIds': [g['id'] for g in gt],
            'dtMatches': dtm,
            'gtMatches': gtm,
            'dtScores': [d['score'] for d in dt],
            'gtIgnore': gtIg,
            'dtIgnore': dtIg,
        }

    def summarize(self, is_ovd=False):
        """Compute and display summary metrics for evaluation results.

        Note this function can *only* be applied on the default parameter
        setting
        """

        def _summarize(ap=1, iouThr=None, areaRng='all', maxDets=100):
            p = self.params
            iStr = ' {:<18} {} @[ IoU={:<9} | area={:>6s} | maxDets={:>3d} ] = {:0.3f}'  # noqa
            titleStr = 'Average Precision' if ap == 1 else 'Average Recall'
            typeStr = '(AP)' if ap == 1 else '(AR)'
            iouStr = '{:0.2f}:{:0.2f}'.format(p.iouThrs[0], p.iouThrs[-1]) \
                if iouThr is None else '{:0.2f}'.format(iouThr)

            aind = [
                i for i, aRng in enumerate(p.areaRngLbl) if aRng == areaRng
            ]
            mind = [i for i, mDet in enumerate(p.maxDets) if mDet == maxDets]
            if ap == 1:
                # dimension of precision: [TxRxKxAxM]
                s = self.eval['precision']
                # IoU
                if iouThr is not None:
                    t = np.where(iouThr == p.iouThrs)[0]
                    s = s[t]
                s = s[:, :, :, aind, mind]
            else:
                # dimension of recall: [TxKxAxM]
                s = self.eval['recall']
                if iouThr is not None:
                    t = np.where(iouThr == p.iouThrs)[0]
                    s = s[t]
                s = s[:, :, aind, mind]
            if len(s[s > -1]) == 0:
                mean_s = -1
            else:
                mean_s = np.mean(s[s > -1])
            print(
                iStr.format(titleStr, typeStr, iouStr, areaRng, maxDets,
                            mean_s))
            return mean_s

        def _summarizeDets():
            stats = []
            stats.append(_summarize(1, maxDets=self.params.maxDets[-1]))
            stats.append(
                _summarize(1, iouThr=.5, maxDets=self.params.maxDets[-1]))
            stats.append(
                _summarize(1, iouThr=.75, maxDets=self.params.maxDets[-1]))
            for area_rng in ('small', 'medium', 'large'):
                stats.append(
                    _summarize(
                        1, areaRng=area_rng, maxDets=self.params.maxDets[-1]))
            for max_det in self.params.maxDets:
                stats.append(_summarize(0, maxDets=max_det))
            for area_rng in ('small', 'medium', 'large'):
                stats.append(
                    _summarize(
                        0, areaRng=area_rng, maxDets=self.params.maxDets[-1]))
            stats = np.array(stats)
            return stats

        def _summarizeOVDs():
            def _summarize(ap=1, iouThr=None, areaRng='all', maxDets=100, cat_kind=None):
                assert cat_kind in ('Base', 'Novel')
                if cat_kind == 'Novel':
                    cat_inds = self.novel_inds
                else:
                    cat_inds = self.base_inds
                p = self.params
                iStr = ' {:<18} {} @[ IoU={:<9} | area={:>6s} | maxDets={:>3d} ] = {:0.3f}'  # noqa
                titleStr = f'{cat_kind} Average Precision' if ap == 1 else f'{cat_kind} Average Recall'
                typeStr = '(AP)' if ap == 1 else '(AR)'
                iouStr = '{:0.2f}:{:0.2f}'.format(p.iouThrs[0], p.iouThrs[-1]) \
                    if iouThr is None else '{:0.2f}'.format(iouThr)

                aind = [
                    i for i, aRng in enumerate(p.areaRngLbl) if aRng == areaRng
                ]
                mind = [i for i, mDet in enumerate(p.maxDets) if mDet == maxDets]
                if ap == 1:
                    # dimension of precision: [TxRxKxAxM]
                    s = self.eval['precision']
                    # IoU
                    if iouThr is not None:
                        t = np.where(iouThr == p.iouThrs)[0]
                        s = s[t]
                    s = s[:, :, cat_inds, aind, mind]
                else:
                    # dimension of recall: [TxKxAxM]
                    s = self.eval['recall']
                    if iouThr is not None:
                        t = np.where(iouThr == p.iouThrs)[0]
                        s = s[t]
                    s = s[:, cat_inds, aind, mind]
                if len(s[s > -1]) == 0:
                    mean_s = -1
                else:
                    mean_s = np.mean(s[s > -1])
                print(
                    iStr.format(titleStr, typeStr, iouStr, areaRng, maxDets,
                                mean_s))
                return mean_s

            stats = []
            for cat_kind in ('Base', 'Novel'):
                print(f'\nSummarize {cat_kind} Classes:')
                stats.append(_summarize(1, maxDets=self.params.maxDets[-1], cat_kind=cat_kind))
                stats.append(
                    _summarize(1, iouThr=.5, maxDets=self.params.maxDets[-1], cat_kind=cat_kind))
                stats.append(
                    _summarize(1, iouThr=.75, maxDets=self.params.maxDets[-1], cat_kind=cat_kind))
                for area_rng in ('small', 'medium', 'large'):
                    stats.append(
                        _summarize(
                            1, areaRng=area_rng, maxDets=self.params.maxDets[-1], cat_kind=cat_kind))
                for max_det in self.params.maxDets:
                    stats.append(_summarize(0, maxDets=max_det, cat_kind=cat_kind))
                for area_rng in ('small', 'medium', 'large'):
                    stats.append(
                        _summarize(
                            0, areaRng=area_rng, maxDets=self.params.maxDets[-1], cat_kind=cat_kind))
            stats = np.array(stats)

            print()
            print('-' * 45)
            print(f'Compute OVD AP: (bAP + 3 * nAP) / 4 = {(stats[0] + 3 * stats[10]) / 4.:.2f}')
            print('-' * 45)
            return stats


        def _summarizeKps():
            stats = np.zeros((10, ))
            stats[0] = _summarize(1, maxDets=20)
            stats[1] = _summarize(1, maxDets=20, iouThr=.5)
            stats[2] = _summarize(1, maxDets=20, iouThr=.75)
            stats[3] = _summarize(1, maxDets=20, areaRng='medium')
            stats[4] = _summarize(1, maxDets=20, areaRng='large')
            stats[5] = _summarize(0, maxDets=20)
            stats[6] = _summarize(0, maxDets=20, iouThr=.5)
            stats[7] = _summarize(0, maxDets=20, iouThr=.75)
            stats[8] = _summarize(0, maxDets=20, areaRng='medium')
            stats[9] = _summarize(0, maxDets=20, areaRng='large')
            return stats

        if not self.eval:
            raise Exception('Please run accumulate() first')
        iouType = self.params.iouType
        if iouType == 'segm' or iouType == 'bbox':
            summarize = _summarizeDets
        elif iouType == 'keypoints':
            summarize = _summarizeKps
        if is_ovd:
            assert iouType == 'bbox'
            summarize = _summarizeOVDs
        self.stats = summarize()
