import cv2
import numpy as np
import pydirectinput
import pyautogui
import time
import os

# DirectInput类
class DirectInput:
    def __init__(self):
        pass
    
    def press(self, key):
        pydirectinput.press(key)
        print(f"Pressed {key} key using DirectInput")

# 加载模板图像
def load_templates(template_dir):
    templates = []
    for filename in os.listdir(template_dir):
        if filename.endswith(('.png', '.jpg', '.jpeg')):
            template_path = os.path.join(template_dir, filename)
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is not None:
                templates.append((filename, template))
                print(f"Loaded template: {filename}")
    return templates

# 屏幕截图
def capture_screen():
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2BGR)
    return screenshot

# 模板匹配
def match_templates(screen, templates, threshold=0.8):
    matches = []
    for template_name, template in templates:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        for pt in zip(*loc[::-1]):
            matches.append((template_name, pt, result.max()))
    return matches

# 主函数
def main():
    template_dir = "template"
    templates = load_templates(template_dir)
    
    if not templates:  
        print("No templates found in the template directory.")
        return
    
    # 创建DirectInput类对象
    direct_input = DirectInput()
    
    print("Starting screen monitoring...")
    last_press_time = time.time()
    press_interval = 2  # 每2秒按一次键
    press_key1 = "space"  # 默认按空格键
    press_key2 = "f"
    
    try:
        while True:
            # 捕获屏幕
            screen = capture_screen()
            
            # 模板匹配
            matches = match_templates(screen, templates)
            
            # 处理匹配结果
            if matches:
                print(f"Found {len(matches)} matches:")
                for match in matches:
                    template_name, pt, score = match
                    print(f"Template: {template_name}, Location: {pt}, Score: {score:.2f}")

                direct_input.press(press_key1)
                time.sleep(0.1)
                direct_input.press(press_key2)
            # 定时按键
            """current_time = time.time()
            if current_time - last_press_time >= press_interval:
                direct_input.press(press_key)
                # 切换按键
                press_key = "f" if press_key == "space" else "space"
                last_press_time = current_time
            """
            # 短暂延迟，避免CPU占用过高
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("Monitoring stopped by user.")

if __name__ == "__main__":
    main()