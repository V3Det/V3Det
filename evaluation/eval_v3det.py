import argparse

from pycocotools.coco import COCO

from cocoeval_mp import COCOevalMP

parser = argparse.ArgumentParser()
parser.add_argument('dt_json_path', help='COCO JSON format det result')
parser.add_argument('--ovd', action='store_true', default=False, help='Whether evaluate OVD metric')
parser.add_argument('--gt_json_path', default='data/V3Det/annotations/v3det_2023_v1_val.json')
args = parser.parse_args()

v3det_gt = COCO(args.gt_json_path)

v3det_dt = v3det_gt.loadRes(args.dt_json_path)

v3det_eval = COCOevalMP(v3det_gt, v3det_dt, 'bbox', num_proc=8)
v3det_eval.params.maxDets = [300]

v3det_eval.evaluate()
v3det_eval.accumulate()

if args.ovd:
    v3det_eval.summarize(is_ovd=True)
else:
    v3det_eval.summarize()


