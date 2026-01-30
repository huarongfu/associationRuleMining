"""
项目配置和工具函数

运行实验前必须执行该模块来初始化项目路径
"""

import os
import sys

# 自动配置项目根路径
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

# 核心路径配置
PATHS = {
    "root": PROJECT_ROOT,
    "data": os.path.join(PROJECT_ROOT, "data"),
    "algorithms": os.path.join(PROJECT_ROOT, "algorithms"),
    "experiments": os.path.join(PROJECT_ROOT, "experiments"),
    "results": os.path.join(PROJECT_ROOT, "results"),
    "plots": os.path.join(PROJECT_ROOT, "plots"),
    "config": os.path.join(PROJECT_ROOT, "config"),
}

# 数据文件路径
DATA_FILES = {
    "transactions": os.path.join(PATHS["data"], "transactions.txt"),
    "preprocessed_transactions": os.path.join(PATHS["data"], "preprocessed_transactions.csv"),
    "jd_comments": os.path.join(PATHS["data"], "jd_cleaned_comments.csv"),
    "stopwords": os.path.join(PATHS["data"], "stopwords.txt"),
    "vocabulary": os.path.join(PATHS["data"], "vocabulary.txt"),
}

# 结果文件输出路径
RESULT_FILES = {
    "performance_by_support": os.path.join(PATHS["results"], "performance_by_support.csv"),
    "performance_by_scale": os.path.join(PATHS["results"], "performance_by_scale.csv"),
    "quality_by_support": os.path.join(PATHS["results"], "quality_by_support.csv"),
    "quality_by_scale": os.path.join(PATHS["results"], "quality_by_scale.csv"),
    "rules_by_support": os.path.join(PATHS["results"], "rules_by_support.csv"),
    "rules_by_scale": os.path.join(PATHS["results"], "rules_by_scale.csv"),
}


def print_config():
    """打印项目配置信息"""
    print("\n" + "="*80)
    print("【项目配置】")
    print("="*80)
    print(f"项目根目录: {PATHS['root']}")
    print(f"数据目录:   {PATHS['data']}")
    print(f"结果目录:   {PATHS['results']}")
    print("="*80 + "\n")
