# TreeUI Operation Guide

## 1. Data and Environment Setup

Use `v3det_image_download.py` to download the dataset images into `images` in the `/path/to/V3Det` directory. 
Download `v3det_2023_v1_category_tree.json` into the `annotations` directory.

Install the required package: `pip install pyqt5`

## 2. Visualization Tool and Instructions
After running `python v3det_visualize_tree.py`, a dialog box will pop up. Select the downloaded dataset folder `/path/to/V3Det`. Following this, the visualization tool interface will appear:
![view.png](../TreeUI.png)

Description of functions and operations:\
① Search box: Enter English or Chinese text for searching. The results will be displayed in ⑤.\
② Reset button: This is used to reset the search box (①) and the search display area (⑤).\
③ Category tree display area: Here you can expand the category tree, select categories, and view the structure and information of the current category in ④, ⑥, and ⑦.\
④ Category relationship display area: This shows the relationships of the categories selected in ③/⑤.\
⑤ Category search area: Displays the categories searched.\
⑥ Category information area: Shows the information of the selected category, including English category name, Chinese category name, English category description, and Chinese category description.\
⑦ Image area: Displays related images of the selected category, with a maximum of 16 images displayed at a time.
