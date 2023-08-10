import os
import sys
import json
import tkinter

from tkinter import filedialog
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import functools

W, H = 800, 800

qss = '/*\nMaterial Dark Style Sheet for QT Applications\nAuthor: Jaime A. Quiroga P.\nInspired on https://github.com/jxfwinter/qt-material-stylesheet\nCompany: GTRONICK\nLast updated: 04/12/2018, 15:00.\nAvailable at: https://github.com/GTRONICK/QSS/blob/master/MaterialDark.qss\n*/\nQMainWindow {\n\tbackground-color:#1e1d23;\n\tborder-radius:15px;\n\tfont-family:Segoe UI;\n}\nQDialog {\n\tbackground-color:#1e1d23;\n}\nQColorDialog {\n\tbackground-color:#1e1d23;\n\t\n}\nQTextEdit {\n\tbackground-color:#1e1d23;\n\tcolor: #a9b7c6;\n}\nQPlainTextEdit {\n\tselection-background-color:#007b50;\n\tbackground-color:#1e1d23;\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: transparent;\n\tborder-width: 1px;\n\tcolor: #a9b7c6;\n}\nQPushButton{\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: transparent;\n\tborder-width: 1px;\n\tborder-style: solid;\n\tcolor: #a9b7c6;\n\tpadding: 2px;\n\tbackground-color: #1e1d23;\n\tfont-size: 14px;\n}\nQPushButton::default{\n\tborder-style: inset;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #04b97f;\n\tborder-width: 1px;\n\tcolor: #a9b7c6;\n\tpadding: 2px;\n\tbackground-color: #1e1d23;\n}\nQToolButton {\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #04b97f;\n\tborder-bottom-width: 1px;\n\tborder-style: solid;\n\tcolor: #a9b7c6;\n\tpadding: 2px;\n\tbackground-color: #1e1d23;\n}\nQToolButton:hover{\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #37efba;\n\tborder-bottom-width: 2px;\n\tborder-style: solid;\n\tcolor: #FFFFFF;\n\tpadding-bottom: 1px;\n\tbackground-color: #1e1d23;\n}\nQPushButton:hover{\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #37efba;\n\tborder-bottom-width: 1px;\n\tborder-style: solid;\n\tcolor: #FFFFFF;\n\tpadding-bottom: 2px;\n\tbackground-color: #1e1d23;\n}\nQPushButton:pressed{\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #37efba;\n\tborder-bottom-width: 2px;\n\tborder-style: solid;\n\tcolor: #37efba;\n\tpadding-bottom: 1px;\n\tbackground-color: #1e1d23;\n}\nQPushButton:disabled{\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #808086;\n\tborder-bottom-width: 2px;\n\tborder-style: solid;\n\tcolor: #808086;\n\tpadding-bottom: 1px;\n\tbackground-color: #1e1d23;\n}\nQLineEdit {\n\tborder-width: 1px; border-radius: 4px;\n\tborder-color: rgb(58, 58, 58);\n\tborder-style: inset;\n\tpadding: 0 8px;\n\tcolor: #a9b7c6;\n\tbackground:#1e1d23;\n\tselection-background-color:#007b50;\n\tselection-color: #FFFFFF;\n}\nQLabel {\n\tcolor: #a9b7c6;\n\tfont-size: 14px;\n}\nQLCDNumber {\n\tcolor: #37e6b4;\n}\nQProgressBar {\n\ttext-align: center;\n\tcolor: rgb(240, 240, 240);\n\tborder-width: 1px; \n\tborder-radius: 10px;\n\tborder-color: rgb(58, 58, 58);\n\tborder-style: inset;\n\tbackground-color:#1e1d23;\n}\nQProgressBar::chunk {\n\tbackground-color: #04b97f;\n\tborder-radius: 5px;\n}\nQMenuBar {\n\tbackground-color: #1e1d23;\n}\nQMenuBar::item {\n\tcolor: #a9b7c6;\n  \tspacing: 3px;\n  \tpadding: 1px 4px;\n  \tbackground: #1e1d23;\n}\n\nQMenuBar::item:selected {\n  \tbackground:#1e1d23;\n\tcolor: #FFFFFF;\n}\nQMenu::item:selected {\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: #04b97f;\n\tborder-bottom-color: transparent;\n\tborder-left-width: 2px;\n\tcolor: #FFFFFF;\n\tpadding-left:15px;\n\tpadding-top:4px;\n\tpadding-bottom:4px;\n\tpadding-right:7px;\n\tbackground-color: #1e1d23;\n}\nQMenu::item {\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: transparent;\n\tborder-bottom-width: 1px;\n\tborder-style: solid;\n\tcolor: #a9b7c6;\n\tpadding-left:17px;\n\tpadding-top:4px;\n\tpadding-bottom:4px;\n\tpadding-right:7px;\n\tbackground-color: #1e1d23;\n}\nQMenu{\n\tbackground-color:#1e1d23;\n}\nQTabWidget {\n\tcolor:rgb(0,0,0);\n\tbackground-color:#1e1d23;\n}\nQTabWidget::pane {\n\t\tborder-color: rgb(77,77,77);\n\t\tbackground-color:#1e1d23;\n\t\tborder-style: solid;\n\t\tborder-width: 1px;\n    \tborder-radius: 6px;\n}\nQTabBar::tab {\n\tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: transparent;\n\tborder-bottom-width: 1px;\n\tborder-style: solid;\n\tcolor: #808086;\n\tpadding: 3px;\n\tmargin-left:3px;\n\tbackground-color: #1e1d23;\n}\nQTabBar::tab:selected, QTabBar::tab:last:selected, QTabBar::tab:hover {\n  \tborder-style: solid;\n\tborder-top-color: transparent;\n\tborder-right-color: transparent;\n\tborder-left-color: transparent;\n\tborder-bottom-color: #04b97f;\n\tborder-bottom-width: 2px;\n\tborder-style: solid;\n\tcolor: #FFFFFF;\n\tpadding-left: 3px;\n\tpadding-bottom: 2px;\n\tmargin-left:3px;\n\tbackground-color: #1e1d23;\n}\n\nQCheckBox {\n\tcolor: #a9b7c6;\n\tpadding: 2px;\n}\nQCheckBox:disabled {\n\tcolor: #808086;\n\tpadding: 2px;\n}\n\nQCheckBox:hover {\n\tborder-radius:4px;\n\tborder-style:solid;\n\tpadding-left: 1px;\n\tpadding-right: 1px;\n\tpadding-bottom: 1px;\n\tpadding-top: 1px;\n\tborder-width:1px;\n\tborder-color: rgb(87, 97, 106);\n\tbackground-color:#1e1d23;\n}\nQCheckBox::indicator:checked {\n\n\theight: 10px;\n\twidth: 10px;\n\tborder-style:solid;\n\tborder-width: 1px;\n\tborder-color: #04b97f;\n\tcolor: #a9b7c6;\n\tbackground-color: #04b97f;\n}\nQCheckBox::indicator:unchecked {\n\n\theight: 10px;\n\twidth: 10px;\n\tborder-style:solid;\n\tborder-width: 1px;\n\tborder-color: #04b97f;\n\tcolor: #a9b7c6;\n\tbackground-color: transparent;\n}\nQRadioButton {\n\tcolor: #a9b7c6;\n\tbackground-color: #1e1d23;\n\tpadding: 1px;\n}\nQRadioButton::indicator:checked {\n\theight: 10px;\n\twidth: 10px;\n\tborder-style:solid;\n\tborder-radius:5px;\n\tborder-width: 1px;\n\tborder-color: #04b97f;\n\tcolor: #a9b7c6;\n\tbackground-color: #04b97f;\n}\nQRadioButton::indicator:!checked {\n\theight: 10px;\n\twidth: 10px;\n\tborder-style:solid;\n\tborder-radius:5px;\n\tborder-width: 1px;\n\tborder-color: #04b97f;\n\tcolor: #a9b7c6;\n\tbackground-color: transparent;\n}\nQStatusBar {\n\tcolor:#027f7f;\n}\nQSpinBox {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQDoubleSpinBox {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQTimeEdit {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQDateTimeEdit {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQDateEdit {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQComboBox {\n\tcolor: #a9b7c6;\t\n\tbackground: #1e1d23;\n}\nQComboBox:editable {\n\tbackground: #1e1d23;\n\tcolor: #a9b7c6;\n\tselection-background-color: #1e1d23;\n}\nQComboBox QAbstractItemView {\n\tcolor: #a9b7c6;\t\n\tbackground: #1e1d23;\n\tselection-color: #FFFFFF;\n\tselection-background-color: #1e1d23;\n}\nQComboBox:!editable:on, QComboBox::drop-down:editable:on {\n\tcolor: #a9b7c6;\t\n\tbackground: #1e1d23;\n}\nQFontComboBox {\n\tcolor: #a9b7c6;\t\n\tbackground-color: #1e1d23;\n}\nQToolBox {\n\tcolor: #a9b7c6;\n\tbackground-color: #1e1d23;\n}\nQToolBox::tab {\n\tcolor: #a9b7c6;\n\tbackground-color: #1e1d23;\n}\nQToolBox::tab:selected {\n\tcolor: #FFFFFF;\n\tbackground-color: #1e1d23;\n}\nQScrollArea {\n\tcolor: #FFFFFF;\n\tbackground-color: #1e1d23;\n}\nQSlider::groove:horizontal {\n\theight: 5px;\n\tbackground: #04b97f;\n}\nQSlider::groove:vertical {\n\twidth: 5px;\n\tbackground: #04b97f;\n}\nQSlider::handle:horizontal {\n\tbackground: qlineargradient(x1:0, y1:0, x2:1, y2:1, stop:0 #b4b4b4, stop:1 #8f8f8f);\n\tborder: 0px solid #5c5c5c;\n\twidth: 14px;\n\tmargin: -5px 0;\n\tborder-radius: 7px;\n}\nQSlider::handle:vertical {\n\tbackground: qlineargradient(x1:1, y1:1, x2:0, y2:0, stop:0 #b4b4b4, stop:1 #8f8f8f);\n\tborder: 0px solid #5c5c5c;\n\theight: 14px;\n\tmargin: 0 -5px;\n\tborder-radius: 7px;\n}\nQSlider::add-page:horizontal {\n    background: white;\n}\nQSlider::add-page:vertical {\n    background: white;\n}\nQSlider::sub-page:horizontal {\n    background: #04b97f;\n}\nQSlider::sub-page:vertical {\n    background: #04b97f;\n}\n'

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.load_tree()
        self.init_widgets()
        self.init_tree()

    def load_tree(self):
        self.process_log = []
        root = tkinter.Tk()
        root.withdraw()
        print('Please select the root directory of the V3Det dataset!')
        self.root = filedialog.askdirectory()
        self.tree = {}
        self.visual_cat_list = []
        try:
            with open(os.path.join(self.root, 'annotations', 'v3det_2023_v1_category_tree.json'), encoding='utf-8') as f:
                self.tree = json.load(f)
            self.im_root = os.path.join(self.root, 'images')
            self.visual_cat_list = os.listdir(self.im_root)
            print('Images and category_tree.json are all loaded!')
        except:
            if len(self.tree) == 0:
                print('Error: There is no tree.json!')
            else:
                if len(self.visual_cat_list) == 0:
                    print('Warning: There is no images!')
            print('Please make sure the structure of files, and select the root directory:')
            print('| -- V3Det(root)')
            print('    | -- images')
            print('        | -- n00001234')
            print('            | -- ...jpg')
            print('    | -- annotations')
            print('        | -- v3det_2023_v1_category_tree.json')
            if len(self.tree) == 0:
                exit()

    def init_widgets(self):
        # main layout
        central_widget = QtWidgets.QWidget()
        main_layout = QtWidgets.QHBoxLayout()
        central_widget.setLayout(main_layout)

        left_layout = QtWidgets.QVBoxLayout()
        search_box = QtWidgets.QHBoxLayout()
        self.search_text = QLineEdit()
        self.search_text.textEdited.connect(self.text_change)
        self.search_button = QPushButton("Search")
        self.search_button.pressed.connect(self.search)
        search_box.addWidget(self.search_text)
        search_box.addWidget(self.search_button)
        left_layout.addLayout(search_box)

        self.visual_tree = QTreeWidget()
        self.visual_tree.setColumnCount(2)
        self.visual_tree.setHeaderLabels(['name_en', 'name_zh'])
        left_layout.addWidget(self.visual_tree)

        node_lay = QtWidgets.QHBoxLayout()
        self.current_node = QTreeWidget()
        self.current_node.setColumnCount(2)
        self.current_node.setHeaderLabels(['name_en', 'name_zh'])
        node_lay.addWidget(self.current_node)

        self.search_list = QTreeWidget()
        self.search_list.setColumnCount(2)
        self.search_list.setHeaderLabels(['name_en', 'name_zh/num'])
        node_lay.addWidget(self.search_list)
        left_layout.addLayout(node_lay)

        main_layout.addLayout(left_layout)

        right_layout = QtWidgets.QVBoxLayout()
        info_layout = QtWidgets.QVBoxLayout()
        self.class_id = QLabel("class_id")
        self.class_name_en = QLabel("class_name_en")
        self.class_desc_en = QLabel("class_desc_en")
        self.class_name_zh = QLabel("class_name_zh")
        self.class_desc_zh = QLabel("class_desc_zh")
        self.class_id.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.class_name_en.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.class_name_en.setWordWrap(True)
        self.class_desc_en.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.class_desc_en.setWordWrap(True)
        self.class_name_zh.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.class_name_zh.setWordWrap(True)
        self.class_desc_zh.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.class_desc_zh.setWordWrap(True)
        self.class_name_en.setFixedWidth(W)
        self.class_desc_en.setFixedWidth(W)
        self.class_name_zh.setFixedWidth(W)
        self.class_desc_zh.setFixedWidth(W)
        info_layout.addWidget(self.class_id, QtCore.Qt.AlignLeft)
        info_layout.addWidget(self.class_name_en, QtCore.Qt.AlignLeft)
        info_layout.addWidget(self.class_name_zh, QtCore.Qt.AlignLeft)
        info_layout.addWidget(self.class_desc_en, QtCore.Qt.AlignLeft)
        info_layout.addWidget(self.class_desc_zh, QtCore.Qt.AlignLeft)
        right_layout.addLayout(info_layout)

        self.class_images = []
        num_items = 4
        for num_im_i in range(num_items):
            img_layout = QtWidgets.QHBoxLayout()
            for num_im_j in range(num_items):
                image = CanvasImage(1 / num_items)
                self.class_images.append(image)
                img_layout.addWidget(image)
            right_layout.addLayout(img_layout)

        main_layout.addLayout(right_layout)

        self.setCentralWidget(central_widget)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyleSheet(qss)

        self.visual_tree.itemClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.visual_tree))
        self.current_node.itemClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.current_node))
        self.search_list.itemClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.search_list))

        self.visual_tree.itemSelectionChanged.connect(
            functools.partial(self.onitemSelectionChanged, self.visual_tree))
        self.current_node.itemSelectionChanged.connect(
            functools.partial(self.onitemSelectionChanged, self.current_node))
        self.search_list.itemSelectionChanged.connect(
            functools.partial(self.onitemSelectionChanged, self.search_list))

        self.visual_tree.itemDoubleClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.visual_tree))
        self.current_node.itemDoubleClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.current_node))
        self.search_list.itemDoubleClicked.connect(
            functools.partial(self.onitemSelectionChanged, self.search_list))

    def init_tree(self):
        child_num = {}

        def count_child(node):
            num = 1
            if node in self.tree['father2child']:
                for child in self.tree['father2child'][node]:
                    num += count_child(child)
            child_num[node] = num
            return num
        count_child('n00001740')
        self.child_num = child_num

        self.show_tree()

    def show_tree(self, node='n00001740', level=0, parent=None):
        name_en = self.tree['id2name'][node]
        name_en = name_en + '({})'.format(self.child_num[node])
        name_zh = str(self.tree['id2name_zh'][node]) if node in self.tree['id2name_zh'] else ''
        current = QtWidgets.QTreeWidgetItem(["{}-{}".format(level, name_en), name_zh])

        current.id = node
        if node == 'n00001740':
            self.visual_tree.addTopLevelItem(current)
        else:
            parent.addChild(current)
        if node in self.tree['father2child']:
            for child in self.tree['father2child'][node]:
                self.show_tree(child, level + 1, current)

    def text_change(self):
        if self.search_button.text() == 'Reset':
            self.search(False)
        if len(self.search_text.text().encode('utf-8')) > 1:
            self.search(False)

    def search(self, text_reset=True):
        if self.search_button.text() == 'Search':
            text = self.search_text.text()
            if len(text) != 0:
                searched_list = [class_id for class_id in self.tree['id2name'].keys() if class_id == text]
                for item in ['id2name', 'id2name_zh', 'id2desc', 'id2desc_zh']:
                    for k, v in self.tree[item].items():
                        if k not in self.tree.get('child2father'):
                            continue
                        if isinstance(v, list):
                            names = ''
                            for vi in v:
                                names += vi
                            v = names
                        if isinstance(v, str):
                            if (k not in searched_list) and (text.lower() in v.lower()):
                                if k in self.tree['id2name']:
                                    searched_list.append(k)

                self.insert_num = len(searched_list)
                self.show_list(searched_list)

            self.search_button.setText('Reset')

        elif self.search_button.text() == 'Reset':
            self.search_list.clear()
            self.insert_num = 0
            if text_reset:
                self.search_text.setText('')
            self.search_button.setText('Search')

    def show_list(self, show_list, insert_index=-1):
        num_id = 0
        for cat_id in show_list:
            if len(cat_id) == 0:
                continue
            num_id += 1
            name_en = self.tree['id2name'][cat_id] if len(self.tree['id2name'][cat_id]) else ''
            name_en = name_en + '({})'.format(len(self.tree['ancestor2descendant'].get(cat_id, set())))
            name_zh = self.tree['id2name_zh'].get(cat_id, '')
            cur = QtWidgets.QTreeWidgetItem(["{}-{}".format(num_id, name_en), name_zh])
            cur.id = cat_id

            insert_id = insert_index if insert_index >= 0 else self.search_list.topLevelItemCount()
            self.search_list.insertTopLevelItem(insert_id, cur)

    def onItemClicked(self, class_id):
        self.class_id.setText(class_id)
        self.class_name_en.setText(self.tree['id2name'][class_id])
        self.class_desc_en.setText(self.tree['id2desc'].get(class_id, ''))
        self.class_name_zh.setText(self.tree['id2name_zh'].get(class_id, ''))
        self.class_desc_zh.setText(self.tree['id2desc_zh'].get(class_id, ''))

        [im.clean() for im in self.class_images]
        if class_id in self.visual_cat_list:
            show_num = len(self.class_images)
            folder = os.path.join(self.im_root, class_id)
            im_names = os.listdir(folder)
            num_image = 0
            for im_i in im_names:
                if num_image == show_num:
                    break
                self.class_images[num_image].load_image(os.path.join(folder, im_i))
                num_image += 1

        self.add_current(class_id)

    def add_current(self, class_id):
        name_en = self.tree['id2name'][class_id]
        name_en = name_en + '({})'.format(len(self.tree['ancestor2descendant'].get(class_id, set())))
        name_zh = self.tree['id2name_zh'].get(class_id, '')
        self.current_node.clear()
        current = QtWidgets.QTreeWidgetItem([name_en, name_zh])
        current.id = class_id

        self.current_node.addTopLevelItem(current)
        for relation in ['father2child', 'child2father', 'id2synonym_list', 'ancestor2descendant', 'descendant2ancestor']:
            rel = QtWidgets.QTreeWidgetItem([relation, str(len(self.tree[relation].get(class_id, [])))])
            current.addChild(rel)
            for rel_class in self.tree[relation].get(class_id, []):
                name_en = self.tree['id2name'][rel_class]
                name_en = name_en + '({})'.format(
                    len(self.tree['ancestor2descendant'].get(rel_class, set())))
                name_zh = self.tree['id2name_zh'].get(rel_class, '')
                rel_node = QtWidgets.QTreeWidgetItem([name_en, name_zh])
                rel_node.id = rel_class
                rel.addChild(rel_node)
        self.current_node.expandAll()

    def onitemSelectionChanged(self, node_tree):
        if node_tree.selectedItems():
            if hasattr(node_tree.selectedItems()[0], 'id'):
                self.onItemClicked(node_tree.selectedItems()[0].id)

    def keyPressEvent(self, qKeyEvent):
        super().keyPressEvent(qKeyEvent)


class CanvasImage(QtWidgets.QLabel):
    def __init__(self, scale=1.):
        super().__init__()
        self.save_root = 'select'
        self.scale = scale
        self.clean()

    def load_image(self, path):
        pixmap = QPixmap(path)
        w, h = pixmap.width(), pixmap.height()
        r = min(self.scale * W / w, self.scale * H / h)
        w, h = int(r * w), int(r * h)
        pixmap = pixmap.scaled(w, h, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)

        self.setAlignment(Qt.AlignCenter | Qt.AlignCenter)
        self.setPixmap(pixmap)

    def clean(self):
        pixmap = QtGui.QPixmap(int(W * self.scale), int(H * self.scale))
        pixmap.fill(QColor("white"))
        self.setPixmap(pixmap)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('Material')
    window = MainWindow()
    window.show()
    app.exec_()

