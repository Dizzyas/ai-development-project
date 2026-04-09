import tkinter as tk
from tkinter import ttk
import pyperclip
import threading
import time
import requests
import re
from pynput import keyboard
import ctypes

# 启用高 DPI 支持
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class WordTranslator:
    def __init__(self):
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title("单词翻译工具")
        self.root.geometry("1300x1000")  # 增大初始窗口大小
        self.root.resizable(True, True)
        
        # 设置主题色彩（onedarkpro 风格）
        self.bg_color = "#282c34"  # 背景色（onedarkpro 主背景）
        self.primary_color = "#61afef"  # 主色（onedarkpro 蓝色）
        self.secondary_color = "#56b6c2"  # 次要色（onedarkpro 青色）
        self.cta_color = "#98c379"  # CTA按钮色（onedarkpro 绿色）
        self.text_color = "#abb2bf"  # 文本色（onedarkpro 文本）
        self.accent_color = "#c678dd"  # 强调色（onedarkpro 紫色）
        self.border_color = "#3e4451"  # 边框色（onedarkpro 边框）
        
        # 应用主题
        self.root.configure(bg=self.bg_color)
        
        # 创建界面元素
        self.create_widgets()
        
        # 初始化变量
        self.last_clipboard = ""
        self.floating_window = None
        
        # 启动剪贴板监控线程
        self.clipboard_thread = threading.Thread(target=self.monitor_clipboard, daemon=True)
        self.clipboard_thread.start()
        
        # 启动键盘监控
        self.keyboard_listener = keyboard.Listener(on_release=self.on_release)
        self.keyboard_listener.start()
        

    
    def create_widgets(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="40", style="Main.TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建样式
        style = ttk.Style()
        style.configure("Main.TFrame", background=self.bg_color)
        style.configure("Title.TLabel", font=("微软雅黑", 28, "bold"), background=self.bg_color, foreground=self.primary_color)
        style.configure("Subtitle.TLabel", font=("微软雅黑", 14), background=self.bg_color, foreground=self.text_color)
        style.configure("Info.TLabel", font=("微软雅黑", 11), background=self.bg_color, foreground=self.text_color)
        style.configure("TEntry", font=("微软雅黑", 14), padding=12, fieldbackground="#3e4451", foreground=self.text_color, bordercolor=self.border_color, lightcolor=self.border_color, darkcolor=self.border_color)
        style.configure("Focused.TEntry", font=("微软雅黑", 14), padding=12, fieldbackground="#3e4451", foreground=self.primary_color, bordercolor=self.primary_color, lightcolor=self.primary_color, darkcolor=self.primary_color)
        style.configure("Primary.TButton", font=("微软雅黑", 12, "bold"), foreground="white", background=self.cta_color, borderwidth=0)
        style.map("Primary.TButton", background=[("active", "#82b366")])
        style.configure("Secondary.TButton", font=("微软雅黑", 11), foreground=self.text_color, background=self.border_color, borderwidth=0)
        style.map("Secondary.TButton", background=[("active", "#4b5263")])
        
        # 标题和副标题
        title_frame = ttk.Frame(main_frame, style="Main.TFrame")
        title_frame.pack(pady=(0, 30))
        
        title_label = ttk.Label(title_frame, text="单词翻译工具", style="Title.TLabel")
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(title_frame, text="快速翻译单词和句子", style="Subtitle.TLabel")
        subtitle_label.pack()
        
        # 输入框
        input_frame = ttk.Frame(main_frame, style="Main.TFrame")
        input_frame.pack(pady=20, fill=tk.X)
        
        # 输入框容器
        entry_container = ttk.Frame(input_frame, style="Main.TFrame")
        entry_container.pack(fill=tk.X, expand=True)
        
        self.word_entry = ttk.Entry(entry_container, font=("微软雅黑", 14))
        self.word_entry.pack(fill=tk.X, expand=True, pady=2)
        self.word_entry.bind("<KeyRelease>", lambda event: self.on_key_release())  # 支持键入后自动翻译
        self.word_entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in())
        self.word_entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out())
        self.word_entry.focus()  # 自动聚焦输入框
        
        # 防抖定时器
        self.typing_timer = None
        self.typing_delay = 500  # 500毫秒防抖延迟
        
        # 翻译结果显示区域
        self.result_frame = ttk.Frame(main_frame, style="Main.TFrame")
        self.result_frame.pack(pady=10, fill=tk.X)
        
        # 结果标题
        self.result_title = ttk.Label(self.result_frame, text="翻译结果:", font=("微软雅黑", 14, "bold"), background=self.bg_color, foreground=self.secondary_color)
        self.result_title.pack(pady=(0, 10), anchor=tk.W)
        
        # 结果内容
        self.result_content = ttk.Label(self.result_frame, text="", font=("微软雅黑", 13), background=self.bg_color, foreground=self.text_color, wraplength=720)
        self.result_content.pack(anchor=tk.W, pady=6)
        
        # 功能说明卡片
        feature_frame = ttk.Frame(main_frame, style="Main.TFrame")
        feature_frame.pack(pady=30, fill=tk.X)
        
        feature_title = ttk.Label(feature_frame, text="✨ 功能特点", font=("微软雅黑", 16, "bold"), background=self.bg_color, foreground=self.primary_color)
        feature_title.pack(pady=(0, 20), anchor=tk.W)
        
        # 功能卡片容器
        features_container = ttk.Frame(feature_frame, style="Main.TFrame")
        features_container.pack(fill=tk.X)
        
        features = [
            {"icon": "🔍", "text": "输入翻译"},
            {"icon": "📋", "text": "复制翻译"},
            {"icon": "🔊", "text": "显示音标"},
            {"icon": "📝", "text": "句子翻译"}
        ]
        
        for i, feature in enumerate(features):
            feature_card = ttk.Frame(features_container, style="Main.TFrame")
            feature_card.pack(fill=tk.X, pady=8)
            
            icon_label = ttk.Label(feature_card, text=feature["icon"], font=("微软雅黑", 16), background=self.bg_color, foreground="white")
            icon_label.pack(side=tk.LEFT, padx=(0, 15))
            
            text_label = ttk.Label(feature_card, text=feature["text"], font=("微软雅黑", 12), background=self.bg_color, foreground=self.text_color)
            text_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # 退出按钮
        exit_frame = ttk.Frame(main_frame, style="Main.TFrame")
        exit_frame.pack(pady=40)
        
        exit_button = ttk.Button(exit_frame, text="退出", command=self.root.quit, style="Secondary.TButton")
        exit_button.pack(ipadx=30, ipady=10)
    
    def on_release(self, key):
        # 监听Ctrl+C组合键
        try:
            if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
                # 延迟一下，确保剪贴板已经更新
                time.sleep(0.1)
                self.check_clipboard()
        except Exception as e:
            print(f"键盘监听错误: {e}")
    
    def monitor_clipboard(self):
        # 监控剪贴板变化
        while True:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    self.check_clipboard()
                time.sleep(1)
            except Exception as e:
                print(f"剪贴板监控错误: {e}")
                time.sleep(1)
    
    def check_clipboard(self):
        # 检查剪贴板内容
        text = pyperclip.paste().strip()
        if text:
            # 无论单词还是句子，都进行查询
            self.query_word(text)
    
    def query_from_input(self):
        # 从输入框获取文本并查询
        text = self.word_entry.get().strip()
        if text:
            # 无论单词还是句子，都进行查询
            self.query_word(text)
        else:
            # 输入为空时，显示空白
            self.show_translation_result("", "")
    
    def is_chinese(self, text):
        # 判断文本是否包含中文
        for char in text:
            if '\u4e00' <= char <= '\u9fff':
                return True
        return False
    
    def is_number(self, text):
        # 判断文本是否是数字
        try:
            float(text)
            return True
        except ValueError:
            return False
    
    def translate_number(self, text):
        # 翻译数字为英文读法
        try:
            num = float(text)
            
            # 判断是否是整数
            if num.is_integer():
                num = int(num)
            
            # 无论用户输入什么语言，都将数字转换为英文读法
            return self.number_to_english(num)
        except Exception as e:
            print(f"数字翻译错误: {e}")
            return text
    
    def number_to_english(self, num):
        # 将数字转换为英文读法
        if num == 0:
            return "zero"
        
        # 定义数字的英文表示
        ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
        teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
        tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
        thousands = ["", "thousand", "million", "billion"]
        
        def helper(n):
            if n < 10:
                return ones[n]
            elif n < 20:
                return teens[n-10]
            elif n < 100:
                return tens[n//10] + ("-" + ones[n%10] if n%10 != 0 else "")
            elif n < 1000:
                return ones[n//100] + " hundred" + (" " + helper(n%100) if n%100 != 0 else "")
            else:
                for i, unit in enumerate(thousands):
                    if n < 1000**(i+1):
                        return helper(n//1000**i) + f" {unit}" + (" " + helper(n%1000**i) if n%1000**i != 0 else "")
        
        return helper(num)
    

    
    def translate_with_api(self, text):
        # 使用网络API进行翻译
        try:
            # 判断文本语言，确定翻译方向
            if self.is_chinese(text):
                # 中译英
                langpair = 'zh|en'
            else:
                # 英译中
                langpair = 'en|zh'
            
            # 使用备用接口进行翻译
            url = f"https://api.mymemory.translated.net/get?q={text}&langpair={langpair}"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if 'responseData' in data and 'translatedText' in data['responseData']:
                return data['responseData']['translatedText']
            
            return None
        except Exception as e:
            print(f"翻译API错误: {e}")
            return None
    

    
    def query_word(self, text):
        # 查询单词或句子信息
        try:
            # 检查是否是数字
            if self.is_number(text):
                # 数字，使用数字翻译功能
                translation = self.translate_number(text)
                self.show_translation_result(text, translation, "")
            else:
                # 检查是否是单个单词
                words = text.split()
                if len(words) == 1:
                    # 单个单词，先尝试本地词典
                    local_dict = {
                        # 英译中
                        'hello': '你好',
                        'world': '世界',
                        'apple': '苹果',
                        'banana': '香蕉',
                        'computer': '电脑',
                        'phone': '手机',
                        'book': '书',
                        'pen': '钢笔',
                        'cat': '猫',
                        'dog': '狗',
                        # 中译英
                        '你好': 'hello',
                        '世界': 'world',
                        '苹果': 'apple',
                        '香蕉': 'banana',
                        '电脑': 'computer',
                        '手机': 'phone',
                        '书': 'book',
                        '钢笔': 'pen',
                        '猫': 'cat',
                        '狗': 'dog'
                    }
                    
                    # 尝试使用本地词典
                    if text.lower() in local_dict:
                        translation = local_dict[text.lower()]
                        self.show_translation_result(text, translation)
                    else:
                        # 本地词典没有，使用网络API（在后台线程中执行）
                        threading.Thread(target=self.translate_in_background, args=(text,), daemon=True).start()
                else:
                    # 句子，使用网络API（在后台线程中执行）
                    threading.Thread(target=self.translate_in_background, args=(text,), daemon=True).start()
        except Exception as e:
            print(f"查询错误: {e}")
            # 显示错误信息
            self.show_translation_result(text, "抱歉，查询失败，请检查网络连接。")
    
    def translate_in_background(self, text):
        # 在后台线程中执行翻译
        try:
            translation = self.translate_with_api(text)
            if translation:
                # 使用 after 方法在主线程中更新 UI
                self.root.after(0, lambda: self.show_translation_result(text, translation))
            else:
                self.root.after(0, lambda: self.show_translation_result(text, "抱歉，无法连接到翻译服务，请检查网络连接。"))
        except Exception as e:
            print(f"翻译错误: {e}")
            self.root.after(0, lambda: self.show_translation_result(text, "抱歉，查询失败，请检查网络连接。"))
    

    
    def show_translation_result(self, original_text, translation):
        # 在输入框下方显示翻译结果
        if original_text and translation:
            # 只显示基本的翻译结果
            self.result_content.config(text=f"{translation}")
        else:
            # 输入为空时，显示空白
            self.result_content.config(text="")
    
    def close_floating_window(self):
        if self.floating_window:
            try:
                self.fade_out(self.floating_window)
            except:
                pass
    
    def on_entry_focus_in(self):
        # 输入框获得焦点时的效果
        self.word_entry.configure(style="Focused.TEntry")
    
    def on_entry_focus_out(self):
        # 输入框失去焦点时的效果
        self.word_entry.configure(style="TEntry")
    
    def on_key_release(self):
        # 处理按键释放事件，实现防抖和自动翻译
        if self.typing_timer:
            self.root.after_cancel(self.typing_timer)
        
        # 设置防抖定时器
        self.typing_timer = self.root.after(self.typing_delay, self.query_from_input)
    
    def fade_in(self, window, alpha=0.0, speed=0.05):
        # 淡入效果
        if alpha < 0.95:
            alpha += speed
            window.attributes("-alpha", alpha)
            self.root.after(20, lambda: self.fade_in(window, alpha, speed))
        else:
            window.attributes("-alpha", 0.95)
    
    def fade_out(self, window, alpha=0.95, speed=0.05):
        # 淡出效果
        if alpha > 0:
            alpha -= speed
            window.attributes("-alpha", alpha)
            self.root.after(20, lambda: self.fade_out(window, alpha, speed))
        else:
            try:
                window.destroy()
                self.floating_window = None
            except:
                pass
    
    def run(self):
        # 运行主循环
        self.root.mainloop()

if __name__ == "__main__":
    app = WordTranslator()
    app.run()