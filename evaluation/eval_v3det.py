from pycocotools.coco import COCO
from cocoeval_mp import COCOevalMP


v3det_gt = COCO('data/V3Det/annotations/v3det_2023_v1_val.json')  # GT annotation file

# Load supervised det result in COCO format
# v3det_dt = v3det_gt.loadRes('det_res.json')

# Load OVD det result in COCO format
v3det_dt = v3det_gt.loadRes('det_res.json')

# Start multiprocess evaluation
v3det_eval = COCOevalMP(v3det_gt, v3det_dt, 'bbox', num_proc=8)
v3det_eval.params.maxDets = [300]

v3det_eval.evaluate()
v3det_eval.accumulate()

# Supervised eval
# v3det_eval.summarize()

# OVD eval, set is_ovd=True
v3det_eval.summarize(is_ovd=True)

