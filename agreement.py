import os
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QDesktopWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt

class AgreementDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("用户协议")
        self.setWindowFlag(Qt.WindowCloseButtonHint, False)  # 移除关闭按钮
        self.setModal(True)
        self.setWindowIcon(QIcon('path_to_icon.ico'))  # 设置窗口图标
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        agreement_text = (
            "用户协议\n\n"
            "1. 本软件仅供个人学习和研究使用。\n"
            "2. 请勿用于商业用途或其他非法用途。\n"
            "3. 使用本软件即表示同意遵守相关法律法规。\n\n"
            "同意协议即可继续使用本软件，不同意将退出程序。"
        )

        label = QLabel(agreement_text)
        label.setWordWrap(True)
        layout.addWidget(label)

        button_layout = QVBoxLayout()

        agree_button = QPushButton("同意", self)
        agree_button.clicked.connect(self.accept)
        button_layout.addWidget(agree_button)

        disagree_button = QPushButton("不同意", self)
        disagree_button.clicked.connect(self.reject_and_exit)
        button_layout.addWidget(disagree_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def showEvent(self, event):
        """在显示窗口时将其移动到屏幕中央"""
        self.center()
        super().showEvent(event)

    def center(self):
        """将窗口移动到屏幕中央"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def reject_and_exit(self):
        self.reject()
        os._exit(0)  # 强制退出整个Python进程

def show_agreement(parent):
    dialog = AgreementDialog(parent)
    return dialog.exec_() == QDialog.Accepted
