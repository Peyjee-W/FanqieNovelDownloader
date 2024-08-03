import os
import json

def save_chapters_to_file(chapters, book_title, json_save_dir, txt_save_dir):
    """保存章节内容到 JSON 和 TXT 文件中，分别保存在不同的文件夹中"""
    json_path = os.path.join(json_save_dir, f'{book_title}.json')
    txt_path = os.path.join(txt_save_dir, f'{book_title}.txt')

    os.makedirs(json_save_dir, exist_ok=True)
    os.makedirs(txt_save_dir, exist_ok=True)

    with open(json_path, 'w', encoding='UTF-8') as json_file:
        json.dump(chapters, json_file)

    with open(txt_path, 'w', encoding='UTF-8') as txt_file:
        for chapter, content in chapters.items():
            txt_file.write(chapter + '\n')
            txt_file.write(content + '\n')

def load_existing_chapters(book_title, json_save_dir):
    """从 JSON 文件加载已存在的章节内容"""
    json_path = os.path.join(json_save_dir, f'{book_title}.json')
    if os.path.exists(json_path):
        with open(json_path, 'r', encoding='UTF-8') as json_file:
            return json.load(json_file)
    return {}
