#!/usr/bin/env python3
"""
项目快速启动脚本
"""

import os
import sys

# 配置项目路径
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, PROJECT_ROOT)

def print_welcome():
    """打印欢迎信息"""
    print("\n" + "="*80)
    print("  关联规则挖掘算法对比框架 v1.0")
    print("="*80)
    print("\n📚 项目结构:")
    print("  ├─ algorithms/      算法实现（Apriori、FP-Growth、Eclat）")
    print("  ├─ experiments/     实验脚本（按支持度、按规模）")
    print("  ├─ results/         结果分析和可视化工具")
    print("  ├─ data/            数据文件")
    print("  └─ config/          配置文件")
    print("\n🚀 快速开始:")
    print("  1. 安装依赖: pip install -r requirements.txt")
    print("  2. 运行实验: python experiments/run_by_support.py")
    print("             python experiments/run_by_scale.py")
    print("  3. 查看结果: python results/analysis.py")
    print("  4. 生成图表: python results/plot_performance.py")
    print("\n📁 文件说明:")
    print("  • performance_by_*.csv  → 运行时间和内存占用数据")
    print("  • quality_by_*.csv      → 规则质量统计（支持度、置信度、提升度）")
    print("  • rules_by_*.csv        → 详细规则信息")
    print("  • *.png                 → 性能对比图表")
    print("\n" + "="*80 + "\n")

def check_environment():
    """检查项目环境"""
    print("🔍 检查项目环境...\n")
    
    # 检查目录结构
    required_dirs = ["algorithms", "experiments", "data", "results", "config"]
    missing_dirs = []
    
    for d in required_dirs:
        path = os.path.join(PROJECT_ROOT, d)
        if os.path.isdir(path):
            print(f"  ✓ {d}/")
        else:
            print(f"  ✗ {d}/ (缺失)")
            missing_dirs.append(d)
    
    # 检查关键文件
    print()
    key_files = [
        "utils.py",
        "requirements.txt",
        "README.md",
        "algorithms/__init__.py",
        "experiments/run_by_support.py",
        "experiments/run_by_scale.py",
        "results/analysis.py",
    ]
    
    missing_files = []
    for f in key_files:
        path = os.path.join(PROJECT_ROOT, f)
        if os.path.isfile(path):
            print(f"  ✓ {f}")
        else:
            print(f"  ✗ {f} (缺失)")
            missing_files.append(f)
    
    if missing_dirs or missing_files:
        print(f"\n⚠ 警告: 发现缺失的文件或目录")
        return False
    else:
        print("\n✓ 项目结构完整！")
        return True

if __name__ == "__main__":
    print_welcome()
    
    if check_environment():
        print("\n✨ 项目已就绪，可以开始使用！\n")
    else:
        print("\n请确保所有必需的文件和目录都存在。\n")
        sys.exit(1)
