"""
结果分析工具 - 汇总规则质量指标（表格展示）

使用方法:
    python analysis/analysis.py
"""

import os
import pandas as pd
from typing import Dict
import sys

# 获取结果目录（从 analysis 目录指向 results 目录）
RESULTS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')


def load_results():
    """加载所有结果文件"""
    results = {}
    
    # 按支持度的质量对比
    quality_by_support_file = os.path.join(RESULTS_DIR, "quality_by_support.csv")
    if os.path.exists(quality_by_support_file):
        results["quality_by_support"] = pd.read_csv(quality_by_support_file)
    
    # 按规模的质量对比
    quality_by_scale_file = os.path.join(RESULTS_DIR, "quality_by_scale.csv")
    if os.path.exists(quality_by_scale_file):
        results["quality_by_scale"] = pd.read_csv(quality_by_scale_file)
    
    return results


def print_quality_comparison(df: pd.DataFrame, title: str) -> None:
    """打印规则质量表格 - 使用纯文本格式"""
    print(f"\n{'='*130}")
    print(f"【{title}】")
    print(f"{'='*130}\n")
    
    # 按支持度或规模分组
    group_col = "min_support" if "min_support" in df.columns else "scale"
    
    for group_val in sorted(df[group_col].unique()):
        group_data = df[df[group_col] == group_val]
        
        if group_col == "min_support":
            print(f"\n最小支持度 = {group_val}")
        else:
            print(f"\n数据集规模 = {int(group_val*100)}%")
        print("-" * 130)
        
        # 构建表格数据
        header = "算法\t支持度(平)\t支持度(最小)\t支持度(最大)\t置信度(平)\t置信度(最小)\t置信度(最大)\t提升度(平)\t提升度(最小)\t提升度(最大)"
        print(header)
        print("-" * 130)
        
        for algo in sorted(group_data["algorithm"].unique()):
            algo_data = group_data[group_data["algorithm"] == algo].iloc[0]
            
            row_data = [
                algo,
                f"{algo_data.get('mean_support', 'N/A'):.6f}" if pd.notna(algo_data.get('mean_support')) else "N/A",
                f"{algo_data.get('min_support_val', 'N/A'):.6f}" if pd.notna(algo_data.get('min_support_val')) else "N/A",
                f"{algo_data.get('max_support_val', 'N/A'):.6f}" if pd.notna(algo_data.get('max_support_val')) else "N/A",
                f"{algo_data.get('mean_confidence', 'N/A'):.6f}" if pd.notna(algo_data.get('mean_confidence')) else "N/A",
                f"{algo_data.get('min_confidence_val', 'N/A'):.6f}" if pd.notna(algo_data.get('min_confidence_val')) else "N/A",
                f"{algo_data.get('max_confidence_val', 'N/A'):.6f}" if pd.notna(algo_data.get('max_confidence_val')) else "N/A",
                f"{algo_data.get('mean_lift', 'N/A'):.6f}" if pd.notna(algo_data.get('mean_lift')) else "N/A",
                f"{algo_data.get('min_lift', 'N/A'):.6f}" if pd.notna(algo_data.get('min_lift')) else "N/A",
                f"{algo_data.get('max_lift', 'N/A'):.6f}" if pd.notna(algo_data.get('max_lift')) else "N/A",
            ]
            print("\t".join(row_data))
        
        print()


def print_summary(results: Dict) -> None:
    """打印完整总结"""
    print("\n")
    print("=" * 130)
    print("【关联规则挖掘算法综合对比分析】")
    print("=" * 130)
    
    print("\n📊 统计指标说明:")
    print("-" * 130)
    print("  • 支持度:     规则在数据集中出现的频率（值域 [0, 1]，越高越好）")
    print("  • 置信度:     规则前件发生时后件也发生的概率（值域 [0, 1]，越高越好）")
    print("  • 提升度:     规则相对于独立情况的增强倍数（值域 [0, ∞)，>1表示正相关，越高越好）")
    print("  • 平均值:     该指标在所有规则中的平均水平")
    print("  • 最小值:     该指标的最小取值")
    print("  • 最大值:     该指标的最大取值")
    print("-" * 130)
    
    # 按支持度的质量对比
    if "quality_by_support" in results:
        print_quality_comparison(results["quality_by_support"], "按最小支持度的规则质量对比")
    
    # 按规模的质量对比
    if "quality_by_scale" in results:
        print_quality_comparison(results["quality_by_scale"], "按数据集规模的规则质量对比")
    
    print("\n")
    print("=" * 130)
    print("✓ 文件清单:")
    print("  【性能指标数据】- 已生成可视化图表")
    print("    • performance_by_support.csv  → performance_by_support.png")
    print("    • performance_by_scale.csv    → performance_by_scale.png")
    print("      运行: python plot_performance.py")
    print("\n  【规则质量数据】- 上述表格来自")
    print("    • quality_by_support.csv")
    print("    • quality_by_scale.csv")
    print("\n  【详细规则数据】")
    print("    • rules_by_support.csv  - 按支持度阈值的所有规则详情")
    print("    • rules_by_scale.csv    - 按数据集规模的所有规则详情")
    print("=" * 130)
    print()


if __name__ == "__main__":
    results = load_results()
    
    if not results:
        print("⚠ 未找到结果文件。请先运行:")
        print("   python ../experiments/run_by_support.py")
        print("   python ../experiments/run_by_scale.py")
        sys.exit(1)
    
    print_summary(results)
