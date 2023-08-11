<p>
<div align="center">
    
# <img src="images/v3det_icon.jpg" height="25"> V3Det: Vast Vocabulary Visual Detection Dataset

<div>
    <a href='https://myownskyw7.github.io/' target='_blank'>Jiaqi Wang</a>*,
    <a href='https://panzhang0212.github.io/' target='_blank'>Pan Zhang</a>*,
    Tao Chu*,
    Yuhang Cao*, </br>
    Yujie Zhou,
    <a href='https://wutong16.github.io/' target='_blank'>Tong Wu</a>,
    Bin Wang,
    Conghui He,
    <a href='http://dahua.site/' target='_blank'>Dahua Lin</a></br>
    (* equal contribution)</br>
    <strong>Accepted to ICCV 2023</strong>
</div>
</p>
<p>
<div>
    <strong>
        <a href='https://arxiv.org/pdf/2304.03752.pdf' target='_blank'>Paper</a>, 
        <a href='https://v3det.openxlab.org.cn/' target='_blank'>Dataset</a></br>
    </strong>
</div>
</div>
</p>

<p align="left">
    <img width=960 src="images/introduction.jpg"/>
</p>

## Data Format

The data includes a training set, a validation set, comprising 13,204 categories. The training set consists of 183,354 images, while the validation set has 29,821 images. The data organization is:
```
V3Det/
    images/
        <category_node>/
            |────<image_name>.png
            ...
        ...
    annotations/
        |────v3det_2023_v1_category_tree.json       # Category tree
        |────category_name_13204_v3det_2023_v1.txt  # Category name
        |────v3det_2023_v1_train.json               # Train set
        |────v3det_2023_v1_val.json                 # Validation set
```

## Annotation Files

### Train/Val
The annotation files are provided in dictionary format and contain the keywords "images," "categories," and "annotations."

- images : store a list containing image information, where each element is a dictionary representing an image.
```
    file_name            # The relative image path, eg. images/n07745046/21_371_29405651261_633d076053_c.jpg.
    height               # The height of the image
    width                # The width of the image
    id                   # Unique identifier of the image.
```

- categories : store a list containing category information, where each element is a dictionary representing a category.
```
    name                 # English name of the category.
    name_zh              # Chinese name of the category.
    cat_info             # The format for the description information of categories is a list.
    novel                # For open-vocabulary detection, indicate whether the current category belongs to the 'novel' category.
    id                   # Unique identifier of the category.
```

- annotations : store a list containing annotation information, where each element is a dictionary representing a bounding box annotation.
```
    image_id             # The unique identifier of the image where the bounding box is located.
    category_id          # The unique identifier of the category corresponding to the bounding box.
    bbox                 # The coordinates of the bounding box, in the format [x, y, w, h], representing the top-left corner coordinates and the width and height of the box.
    iscrowd              # Whether the bounding box is a crowd box.
    area                 # The area of the bounding box
```

### Category Tree
- The category tree stores information about dataset category mappings and relationships in dictionary format.
```
    categoryid2treeid    # Unique identifier of node in the category tree corresponding to the category identifier in dataset
    id2name              # English name corresponding to each node in the category tree
    id2name_zh           # Chinese name corresponding to each node in the category tree
    id2desc              # English description corresponding to each node in the category tree
    id2desc_zh           # Chinese description corresponding to each node in the category tree
    id2synonym_list      # List of synonyms corresponding to each node in the category tree
    id2center_synonym    # Center synonym corresponding to each node in the category tree
    father2child         # All direct child categories corresponding to each node in the category tree
    child2father         # All direct parent categories corresponding to each node in the category tree
    ancestor2descendant  # All descendant nodes corresponding to each node in the category tree
    descendant2ancestor  # All ancestor nodes corresponding to each node in the category tree
```

## Image Download

- Run the command to crawl the images. By default, the images will be stored in the './V3Det/' directory.
```
python v3det_image_download.py
```
- If you want to change the storage location, you can specify the desired folder by adding the option '--output_folder' when executing the script.
```
python v3det_image_download.py --output_folder our_folder
```

## Category Tree Visualization

- Run the command and then select dataset path `path/to/V3Det` to visualize the category tree.
```
python v3det_visualize_tree.py
```

Please refer to the [TreeUI Operation Guide](VisualTree.md) for more information.

## Codebase
- [x] mmdetection: https://github.com/V3Det/mmdetection-V3Det/tree/main/configs/v3det
- [x] Detectron2： https://github.com/V3Det/Detectron2-V3Det/tree/main/det/projects/ViTDet/configs/V3Det

## Citation

```bibtex
@article{wang2023v3det,
  title={V3det: Vast vocabulary visual detection dataset},
  author={Wang, Jiaqi and Zhang, Pan and Chu, Tao and Cao, Yuhang and Zhou, Yujie and Wu, Tong and Wang, Bin and He, Conghui and Lin, Dahua},
  journal={arXiv preprint arXiv:2304.03752},
  year={2023}
}
```
