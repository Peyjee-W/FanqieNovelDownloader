import random
import requests
from googletrans import Translator

FUN_FACTS = [
    "🌈 知道吗？章鱼有三个心脏！两个为鳃供血，一个为身体供血。",
    "🦉 猫头鹰的眼睛并不是球形的，而是管状的，这使它们在看远处时非常清晰。",
    # 其他本地备用小知识...
]

def get_online_fun_fact():
    """从网络获取一个有趣的小知识并翻译成中文"""
    try:
        response = requests.get("https://uselessfacts.jsph.pl/random.json?language=en")
        if response.status_code == 200:
            data = response.json()
            english_fact = data['text']
            translated_fact = translate_to_chinese(english_fact)
            return translated_fact
        else:
            return "无法获取有趣的小知识，请稍后再试。"
    except Exception as e:
        return f"发生错误：{e}"

def translate_to_chinese(text):
    """使用 googletrans 将文本翻译为中文"""
    try:
        translator = Translator()
        translated = translator.translate(text, src='en', dest='zh-cn')
        return translated.text
    except Exception as e:
        return f"翻译时发生错误：{e}"

def get_random_fun_fact():
    """随机选择并返回一个有趣的小知识，优先从网络获取"""
    online_fact = get_online_fun_fact()
    if online_fact.startswith("发生错误") or online_fact in ["无法获取有趣的小知识，请稍后再试。", "翻译失败，请稍后再试。"]:
        # 如果在线获取或翻译失败，则从本地备用数据库中随机选择
        return random.choice(FUN_FACTS)
    return online_fact
