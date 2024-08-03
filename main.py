import sys
import json
import os
import threading
import time
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QDesktopWidget, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QTextCursor
from PyQt5.QtCore import Qt
import webbrowser
from download_utils import download_chapter_list, download_chapter_content
from file_utils import save_chapters_to_file, load_existing_chapters
from fun_facts import get_random_fun_fact
from agreement import show_agreement

class CustomLineEdit(QLineEdit):
    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()
        menu.clear()  # 清除默认菜单项

        # 添加自定义的中文菜单项和快捷键提示
        menu.addAction("剪切", self.cut).setShortcut("Ctrl+X")
        menu.addAction("复制", self.copy).setShortcut("Ctrl+C")
        menu.addAction("粘贴", self.paste).setShortcut("Ctrl+V")
        menu.addAction("删除", self.clear).setShortcut("Del")
        menu.addAction("全选", self.selectAll).setShortcut("Ctrl+A")
        menu.exec_(event.globalPos())

class NovelDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()
        self.records = self.load_records()
        self.downloading = False
        self.paused = False
        self.pause_event = threading.Event()

        if not show_agreement(self):
            QApplication.quit()  # 关闭整个应用程序
            return

        self.tray_icon = None  # 初始化托盘图标变量
        self.initUI()
        self.createTrayIcon()  # 创建托盘图标

    def initUI(self):
        self.setWindowTitle('小说下载助手')
        self.setGeometry(300, 300, 600, 480)
        self.setWindowIcon(QIcon('path_to_icon.ico'))  # 设置窗口图标

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)

        self.entry = CustomLineEdit(self)
        self.entry.setPlaceholderText("在此输入书籍ID...")
        self.entry.returnPressed.connect(self.process_input)

        self.confirm_button = QPushButton("确定", self)
        self.confirm_button.clicked.connect(self.process_input)

        self.funfact_button = QPushButton("获取有趣的小知识", self)
        self.funfact_button.clicked.connect(self.show_fun_fact)

        self.github_button = QPushButton("GitHub主页", self)
        self.github_button.clicked.connect(self.open_github)

        self.refresh_button = QPushButton("更新书籍状态", self)
        self.refresh_button.clicked.connect(self.refresh_books)

        self.pause_button = QPushButton("暂停", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setEnabled(False)

        self.exit_button = QPushButton("退出", self)
        self.exit_button.clicked.connect(self.close)

        entry_layout = QHBoxLayout()
        entry_layout.addWidget(self.entry)
        entry_layout.addWidget(self.confirm_button)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.funfact_button)
        button_layout.addWidget(self.github_button)
        button_layout.addWidget(self.refresh_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.exit_button)

        layout = QVBoxLayout()
        layout.addWidget(self.text_area)
        layout.addLayout(entry_layout)
        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.center()
        self.show_initial_message()

    def createTrayIcon(self):
        """创建系统托盘图标和菜单"""
        self.tray_icon = QSystemTrayIcon(QIcon('path_to_icon.ico'), self)  # 使用相同的图标文件
        tray_menu = QMenu(self)

        show_action = QAction("显示", self)
        quit_action = QAction("退出", self)

        show_action.triggered.connect(self.show)
        quit_action.triggered.connect(self.close)

        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)

        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

    def center(self):
        """将窗口移动到屏幕中央"""
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def show_initial_message(self):
        initial_message = (
            "🌟 欢迎使用小说下载助手！🌟\n"
            "📚 你可以通过输入书籍ID来下载小说。\n"
            "🔗 点按下方 GitHub 按钮获取源码\n"
        )
        self.text_area.append(initial_message)

    def process_input(self):
        user_input = self.entry.text().strip()
        self.entry.clear()

        if user_input.lower() == 'exit':
            self.text_area.append('👋 再见！期待下次见到你！')
            self.close()
        elif user_input.lower() == 'refresh':
            self.refresh_books()
        elif user_input.lower() == 'funfact':
            self.show_fun_fact()
        else:
            try:
                book_id = str(int(user_input))
                self.text_area.append(f'🔍 输入书籍ID: {book_id}')
                self.pause_button.setEnabled(True)
                self.downloading = True

                book_title, _, _ = download_chapter_list(book_id)
                if book_title == 'err':
                    self.text_area.append('❌ 找不到此书')
                    self.downloading = False
                    self.pause_button.setEnabled(False)
                else:
                    if book_id not in self.records:
                        self.records.append(book_id)
                        self.save_records()
                    threading.Thread(target=self.download_book, args=(book_id,)).start()
            except ValueError:
                self.text_area.append('🚫 请输入有效的数字书籍ID！')

    def show_fun_fact(self):
        fact = get_random_fun_fact()
        text = f'🎉 有趣的小知识：{fact}\n'
        self.type_effect(text)

    def type_effect(self, text, speed=0.05):
        """在文本区域中显示带有打字效果的文本"""
        for char in text:
            self.text_area.moveCursor(QTextCursor.End)
            self.text_area.insertPlainText(char)
            QApplication.processEvents()
            time.sleep(speed)

    def open_github(self):
        try:
            webbrowser.open("https://github.com/Peyjee-W")
        except Exception as e:
            self.text_area.append(f"⚠️ 打开 GitHub 页面时发生错误：{e}")

    def refresh_books(self):
        self.type_effect('🔄 正在更新书籍状态...\n')
        if os.path.exists('record.json'):
            try:
                with open('record.json', 'r', encoding='UTF-8') as file:
                    self.records = json.load(file)
            except (IOError, ValueError) as e:
                self.type_effect(f'⚠️ 无法读取record.json: {e}\n')
                self.records = []
                self.save_records()
                return

            for book_id in self.records:
                self.type_effect(f'\n🔍 检查书籍ID {book_id}...\n')
                status = self.download_book(book_id)
                if status == '未更新':
                    self.type_effect(f'📙 书籍ID {book_id} 没有新的更新。\n')
                elif status == '已完结':
                    self.records.remove(book_id)
                    self.type_effect(f'🛑 书籍ID {book_id} 已完结并从记录中移除\n')

            self.save_records()
            self.type_effect('✅ 更新完成！\n')
        else:
            self.type_effect('⚠️ record.json文件不存在。\n')

    def toggle_pause(self):
        if self.downloading:
            if self.paused:
                self.paused = False
                self.pause_event.set()
                self.pause_button.setText("暂停")
                self.text_area.append("▶️ 继续下载...")
            else:
                self.paused = True
                self.pause_event.clear()
                self.pause_button.setText("继续")
                self.text_area.append("⏸️ 下载暂停。")

    def download_book(self, book_id, json_save_dir="json_files", txt_save_dir="txt_files"):
        book_title, chapters, book_status = download_chapter_list(book_id)
        if book_title == 'err':
            self.text_area.append('❌ 找不到此书')
            self.downloading = False
            self.pause_button.setEnabled(False)
            return '未更新'

        self.text_area.append(f'🍀 正在下载《{book_title}》，当前状态: “{book_status}”')
        old_chapters = load_existing_chapters(book_title, json_save_dir)

        if chapters == old_chapters:
            self.text_area.append('📙 没有新的章节更新。')
            return '未更新'

        for chapter in chapters:
            if chapter in old_chapters and len(old_chapters[chapter]) > 30:
                chapters[chapter] = old_chapters[chapter]
            else:
                while self.paused:
                    self.pause_event.wait()
                self.text_area.append(f'📥 正在下载章节：{chapter}')
                chapters[chapter] = download_chapter_content(chapters[chapter])
                save_chapters_to_file(chapters, book_title, json_save_dir, txt_save_dir)

        self.text_area.append('📥 下载完成！\n')
        self.downloading = False
        self.pause_button.setEnabled(False)
        return book_status

    def load_records(self):
        if os.path.exists('record.json'):
            try:
                with open('record.json', 'r', encoding='UTF-8') as file:
                    return json.load(file)
            except (IOError, ValueError):
                return []
        return []

    def save_records(self):
        try:
            with open('record.json', 'w', encoding='UTF-8') as file:
                json.dump(self.records, file)
        except IOError as e:
            self.text_area.append(f'⚠️ 无法写入record.json: {e}')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NovelDownloaderApp()
    window.show()
    sys.exit(app.exec_())
