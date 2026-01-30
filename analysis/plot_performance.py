"""
可视化脚本 - 生成性能指标图表（运行时间 & 内存占用）

使用方法:
    python analysis/plot_performance.py
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Dict, List
import sys

# 导入字体配置
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import font_config
font_config.setup_chinese_fonts()

# 结果目录（从 analysis 目录指向 results 目录）
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')


def plot_performance_by_support() -> None:
    """按支持度阈值绘制性能对比图"""
    perf_file = os.path.join(RESULTS_DIR, "performance_by_support.csv")
    
    if not os.path.exists(perf_file):
        print(f"⚠ 未找到文件: {perf_file}")
        return
    
    df = pd.read_csv(perf_file)
    
    # 创建 2x2 子图
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('按最小支持度的性能对比', fontsize=16, fontweight='bold')
    
    # 1. 运行时间柱状图
    ax1 = axes[0, 0]
    pivot_time = df.pivot_table(values='runtime_sec', index='min_support', columns='algorithm')
    pivot_time.plot(kind='bar', ax=ax1, width=0.8)
    ax1.set_title('运行时间', fontsize=12, fontweight='bold')
    ax1.set_xlabel('最小支持度')
    ax1.set_ylabel('时间 (秒)')
    ax1.legend(title='算法')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    
    # 2. 运行时间折线图
    ax2 = axes[0, 1]
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo].sort_values('min_support')
        ax2.plot(algo_data['min_support'], algo_data['runtime_sec'], 
                marker='o', label=algo, linewidth=2)
    ax2.set_title('运行时间趋势', fontsize=12, fontweight='bold')
    ax2.set_xlabel('最小支持度')
    ax2.set_ylabel('时间 (秒)')
    ax2.legend(title='算法')
    ax2.grid(alpha=0.3)
    
    # 3. 内存占用柱状图
    ax3 = axes[1, 0]
    pivot_mem = df.pivot_table(values='memory_mb', index='min_support', columns='algorithm')
    pivot_mem.plot(kind='bar', ax=ax3, width=0.8)
    ax3.set_title('内存占用', fontsize=12, fontweight='bold')
    ax3.set_xlabel('最小支持度')
    ax3.set_ylabel('内存 (MB)')
    ax3.legend(title='算法')
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=45)
    
    # 4. 内存占用折线图
    ax4 = axes[1, 1]
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo].sort_values('min_support')
        ax4.plot(algo_data['min_support'], algo_data['memory_mb'], 
                marker='s', label=algo, linewidth=2)
    ax4.set_title('内存占用趋势', fontsize=12, fontweight='bold')
    ax4.set_xlabel('最小支持度')
    ax4.set_ylabel('内存 (MB)')
    ax4.legend(title='算法')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(RESULTS_DIR, "performance_by_support.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 已保存: {output_path}")
    plt.close()


def plot_performance_by_scale() -> None:
    """按数据集规模绘制性能对比图"""
    perf_file = os.path.join(RESULTS_DIR, "performance_by_scale.csv")
    
    if not os.path.exists(perf_file):
        print(f"⚠ 未找到文件: {perf_file}")
        return
    
    df = pd.read_csv(perf_file)
    
    # 创建 2x2 子图
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('按数据集规模的性能对比', fontsize=16, fontweight='bold')
    
    # 1. 运行时间柱状图
    ax1 = axes[0, 0]
    pivot_time = df.pivot_table(values='runtime_sec', index='scale', columns='algorithm')
    pivot_time.plot(kind='bar', ax=ax1, width=0.8)
    ax1.set_title('运行时间', fontsize=12, fontweight='bold')
    ax1.set_xlabel('数据集规模 (%)')
    ax1.set_ylabel('时间 (秒)')
    ax1.legend(title='算法')
    ax1.grid(axis='y', alpha=0.3)
    ax1.set_xticklabels([f"{int(x*100)}%" for x in pivot_time.index], rotation=0)
    
    # 2. 运行时间折线图
    ax2 = axes[0, 1]
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo].sort_values('scale')
        ax2.plot(algo_data['scale'] * 100, algo_data['runtime_sec'], 
                marker='o', label=algo, linewidth=2)
    ax2.set_title('运行时间趋势', fontsize=12, fontweight='bold')
    ax2.set_xlabel('数据集规模 (%)')
    ax2.set_ylabel('时间 (秒)')
    ax2.legend(title='算法')
    ax2.grid(alpha=0.3)
    
    # 3. 内存占用柱状图
    ax3 = axes[1, 0]
    pivot_mem = df.pivot_table(values='memory_mb', index='scale', columns='algorithm')
    pivot_mem.plot(kind='bar', ax=ax3, width=0.8)
    ax3.set_title('内存占用', fontsize=12, fontweight='bold')
    ax3.set_xlabel('数据集规模 (%)')
    ax3.set_ylabel('内存 (MB)')
    ax3.legend(title='算法')
    ax3.grid(axis='y', alpha=0.3)
    ax3.set_xticklabels([f"{int(x*100)}%" for x in pivot_mem.index], rotation=0)
    
    # 4. 内存占用折线图
    ax4 = axes[1, 1]
    for algo in df['algorithm'].unique():
        algo_data = df[df['algorithm'] == algo].sort_values('scale')
        ax4.plot(algo_data['scale'] * 100, algo_data['memory_mb'], 
                marker='s', label=algo, linewidth=2)
    ax4.set_title('内存占用趋势', fontsize=12, fontweight='bold')
    ax4.set_xlabel('数据集规模 (%)')
    ax4.set_ylabel('内存 (MB)')
    ax4.legend(title='算法')
    ax4.grid(alpha=0.3)
    
    plt.tight_layout()
    output_path = os.path.join(RESULTS_DIR, "performance_by_scale.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ 已保存: {output_path}")
    plt.close()


if __name__ == "__main__":
    print("📊 生成性能对比图表...\n")
    plot_performance_by_support()
    plot_performance_by_scale()
    print("\n✓ 所有图表已生成完毕！")
