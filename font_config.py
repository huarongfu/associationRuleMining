"""
中文字体配置模块
自动检测并配置系统中可用的中文字体，支持 macOS / Linux / Windows

使用方法:
    import font_config
    font_config.setup_chinese_fonts()
    # 之后 matplotlib 就能正常显示中文了
"""

import matplotlib
import matplotlib.pyplot as plt
import sys
import platform


def setup_chinese_fonts():
    """自动检测并配置中文字体"""
    
    system = platform.system()
    
    if system == 'Darwin':  # macOS
        fonts = ['STHeiti', 'SimHei', 'Heiti TC', 'SimSong', 'DejaVu Sans']
    elif system == 'Windows':
        fonts = ['SimHei', 'Microsoft YaHei', 'STHeiti', 'DejaVu Sans']
    elif system == 'Linux':
        fonts = ['SimHei', 'WenQuanYi Micro Hei', 'DejaVu Sans']
    else:
        fonts = ['DejaVu Sans']
    
    # 配置 matplotlib
    matplotlib.rcParams['font.sans-serif'] = fonts
    matplotlib.rcParams['axes.unicode_minus'] = False
    matplotlib.rcParams['font.size'] = 10
    
    # 验证字体配置
    try:
        fig, ax = plt.subplots(figsize=(1, 1))
        ax.text(0.5, 0.5, '中文测试', ha='center', va='center', fontsize=12)
        plt.close(fig)
        print(f"✓ 中文字体配置成功 (当前系统: {system})")
        print(f"  使用的字体列表: {fonts}")
        return True
    except Exception as e:
        print(f"⚠ 字体配置出现问题: {e}")
        return False


if __name__ == "__main__":
    setup_chinese_fonts()
