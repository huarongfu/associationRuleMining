# 关联规则挖掘算法对比框架

基于多个经典算法（Apriori、FP-Growth、Eclat）的关联规则挖掘实现与性能对比。

## 📂 项目结构

```
associationRuleMining/
├── README.md                    # 项目说明（本文件）
├── requirements.txt             # 依赖包列表
├── quick_start.py               # 交互式快速入口（可选）
├── setup.py                     # 环境验证脚本
├── utils.py                     # 公共工具函数
├── font_config.py               # 中文字体配置（matplotlib）
│
├── algorithms/                  # 算法实现
│   ├── __init__.py
│   ├── apriori_impl.py           # 标准 Apriori（基于 mlxtend）
│   ├── apriori_improved_impl.py  # 改进的 Apriori（哈希表+剪枝）
│   ├── apriori_hash_trie_impl.py # 哈希表+十字链表 Apriori
│   ├── fpgrowth_impl.py          # FP-Growth 算法
│   └── eclat_impl.py             # Eclat 算法
│
├── config/                      # 配置和预处理
│   └── data_preprocessing.py     # 数据预处理脚本
│
├── data/                        # 数据文件
│   ├── jd_cleaned_comments.csv   # 原始评论数据
│   ├── stopwords.txt             # 停用词表
│   ├── preprocessed_transactions.csv  # 预处理结果
│   ├── transactions.txt          # 事务数据库（挖掘输入）
│   └── vocabulary.txt            # 词汇表
│
├── experiments/                 # 实验脚本
│   ├── run_by_support.py         # 按支持度阈值对比
│   └── run_by_scale.py           # 按数据集规模对比
│
├── analysis/                    # 结果分析脚本
│   ├── analysis.py               # 规则质量分析（表格展示）
│   └── plot_performance.py       # 性能对比可视化
│
└── results/                     # 实验结果（CSV & PNG）
    ├── performance_by_support.csv
    ├── performance_by_support.png
    ├── quality_by_support.csv
    ├── rules_by_support.csv
    ├── performance_by_scale.csv
    ├── performance_by_scale.png
    ├── quality_by_scale.csv
    └── rules_by_scale.csv
```

## ▶️ 运行顺序（使用本地 Python 解释器）

### 1. 安装依赖

使用本地 Python（不使用虚拟环境）：

```bash
python3 -m pip install -r requirements.txt
```

### 2. 数据预处理（从原始评论生成事务）

```bash
python3 config/data_preprocessing.py
```

输出：
- data/preprocessed_transactions.csv
- data/transactions.txt
- data/vocabulary.txt

### 3. 运行关联规则挖掘

```bash
python3 experiments/run_by_support.py
```

可选：按规模对比

```bash
python3 experiments/run_by_scale.py
```

### 4. 结果分析与可视化

```bash
python3 analysis/analysis.py
python3 analysis/plot_performance.py
```

结果在 results/ 目录。

## 📌 结果文件说明

- results/rules_by_support.csv：规则详情（最重要）
- results/quality_by_support.csv：规则质量统计
- results/performance_by_support.csv：性能指标统计
- results/performance_by_support.png：性能图表

## 📝 数据格式

### 交易数据（data/transactions.txt）

```
item1 item2 item3 ...
item4 item5 ...
...
```

### 规则输出（results/rules_by_*.csv）

```csv
algorithm,min_support,min_conf,antecedent,consequent,support,confidence,lift,leverage,conviction,cosine
apriori,0.003,0.4,item1 item2,item3,0.008234,0.721345,2.345678,0.002341,1.234567,0.154321
...
```
