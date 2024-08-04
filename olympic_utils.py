# olympic_utils.py

import requests
import time
from PyQt5.QtGui import QTextCursor
from PyQt5.QtWidgets import QApplication

def fetch_top_5_olympic_medals():
    url = "https://60s.viki.moe/olympic?e=text"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.text.splitlines()
        top_5 = []

        for line in data:
            if len(top_5) >= 5:
                break
            if '.' in line:
                parts = line.split('.')
                if len(parts) > 1:
                    country_info = parts[1].split()
                    if len(country_info) >= 4:
                        country = country_info[0]
                        gold = country_info[1]
                        silver = country_info[2]
                        bronze = country_info[3]
                        total = country_info[4].strip('（）')
                        top_5.append({
                            '排名': parts[0],
                            '国家/地区': country,
                            '金牌数量': gold,
                            '银牌数量': silver,
                            '铜牌数量': bronze,
                            '奖牌总数': total
                        })
        return top_5
    else:
        return None

def display_top_5_olympic_medals(text_area):
    top_5 = fetch_top_5_olympic_medals()
    if top_5:
        for entry in top_5:
            text = (f"排名: {entry['排名']}, 国家/地区: {entry['国家/地区']}, "
                    f"金牌: {entry['金牌数量']}, 银牌: {entry['银牌数量']}, "
                    f"铜牌: {entry['铜牌数量']}, 总数: {entry['奖牌总数']}\n")
            type_effect(text_area, text)
    else:
        type_effect(text_area, "⚠️ 无法获取奥运金牌榜数据。\n")

def type_effect(text_area, text, speed=0.05):
    """在文本区域中显示带有打字效果的文本"""
    for char in text:
        text_area.moveCursor(QTextCursor.End)
        text_area.insertPlainText(char)
        QApplication.processEvents()
        time.sleep(speed)
