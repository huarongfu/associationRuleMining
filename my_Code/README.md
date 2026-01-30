# 关联规则挖掘算法对比框架

基于多个经典算法（Apriori、FP-Growth、Eclat）的关联规则挖掘实现与性能对比。

## 📂 项目结构

```
my_Code/
├── README.md                    # 项目说明（本文件）
├── requirements.txt             # 依赖包列表
├── setup.py                     # 环境验证脚本
├── utils.py                     # 公共工具函数
├── font_config.py               # 中文字体配置（matplotlib）
│
├── algorithms/                  # 算法实现
│   ├── __init__.py
│   ├── apriori_impl.py         # 标准 Apriori（基于 mlxtend）
│   ├── apriori_improved_impl.py # 改进的 Apriori（哈希表+剪枝）
│   ├── apriori_hash_trie_impl.py # 哈希表+十字链表 Apriori
│   ├── fpgrowth_impl.py        # FP-Growth 算法
│   └── eclat_impl.py           # Eclat 算法
│
├── config/                      # 配置和预处理
│   └── data_preprocessing.py    # 数据预处理脚本
│
├── data/                        # 数据文件
│   ├── transactions.txt         # 交易数据（主数据集）
│   ├── preprocessed_transactions.csv  # 预处理后的交易
│   ├── jd_cleaned_comments.csv  # 评论数据
│   ├── stopwords.txt            # 停用词表
│   └── vocabulary.txt           # 词汇表
│
├── experiments/                 # 实验脚本
│   ├── run_by_support.py        # 按支持度阈值对比
│   └── run_by_scale.py          # 按数据集规模对比
│
├── analysis/                    # 结果分析脚本
│   ├── README.md                # 分析工具说明
│   ├── analysis.py              # 规则质量分析（表格展示）
│   └── plot_performance.py      # 性能对比可视化
│
└── results/                     # 实验结果（CSV & PNG）
    ├── performance_by_support.csv    # 性能指标（按支持度）
    ├── performance_by_support.png    # 性能图表（按支持度）
    ├── quality_by_support.csv        # 规则质量（按支持度）
    ├── rules_by_support.csv          # 规则详情（按支持度）
    │
    ├── performance_by_scale.csv      # 性能指标（按规模）
    ├── performance_by_scale.png      # 性能图表（按规模）
    ├── quality_by_scale.csv          # 规则质量（按规模）
    └── rules_by_scale.csv            # 规则详情（按规模）
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 运行实验

```bash
# 按最小支持度对比算法
python experiments/run_by_support.py

# 按数据集规模对比算法
python experiments/run_by_scale.py
```

### 3. 查看结果

```bash
# 查看规则质量表格
python analysis/analysis.py

# 生成性能对比图表
python analysis/plot_performance.py
```

结果文件保存在 `results/` 目录。

## 📊 输出文件说明

### 性能指标（Performance）
- **CSV格式**: 运行时间 + 内存占用
- **图表格式**: 柱状图 + 折线图对比
- **用途**: 展示算法的效率优劣

### 规则质量（Quality）
- **表格格式**: 支持度、置信度、提升度的统计
- **用途**: 展示算法挖掘的规则质量

### 规则详情（Rules）
- **CSV格式**: 所有发现的关联规则详情
- **用途**: 数据查询和进一步分析

## 📈 算法对比

| 算法 | 数据结构 | 时间复杂度 | 空间复杂度 | 特点 |
|------|---------|-----------|-----------|------|
| Apriori | 前缀树/哈希表 | O(2^n) | O(n) | 基础实现，多次扫描 |
| 改进Apriori | 哈希表+剪枝 | O(2^n) | O(n) | 优化剪枝，减少候选集 |
| 哈希Apriori | 哈希表+十字链表 | O(2^n) | O(n) | 十字链表加速计数 |
| FP-Growth | FP树 | O(n log n) | O(n) | 无候选集生成，最优 |
| Eclat | 垂直数据格式 | O(2^n) | O(n) | 深度优先搜索 |

## 🔧 主要功能函数

### utils.py
```python
profile_execution(fn, *args, **kwargs)
  # 执行函数并收集性能指标（运行时间、内存占用）

eval_rules_comprehensive(rules)
  # 综合评估规则质量（支持度、置信度、提升度）

load_transactions(path)
  # 加载交易数据

compute_cosine(support, lift)
  # 计算Cosine相似度
```

### algorithms/*.py
```python
run(transactions, min_support, min_confidence)
  # 运行关联规则挖掘算法
  # 返回: List[Dict] - 规则列表
```

## 📝 数据格式

### 交易数据 (transactions.txt)
```
item1 item2 item3 ...
item4 item5 ...
...
```

### 规则输出 (rules_by_*.csv)
```csv
algorithm,min_support,min_conf,antecedent,consequent,support,confidence,lift,leverage,conviction,cosine
apriori,0.003,0.4,item1 item2,item3,0.008234,0.721345,2.345678,0.002341,1.234567,0.154321
...
```

## 📌 参数说明

- **min_support**: 最小支持度（0~1），项集频率阈值
- **min_confidence**: 最小置信度（0~1），规则强度阈值
- **support**: 规则支持度 = (A∪B) / 总交易数
- **confidence**: 规则置信度 = (A∪B) / A
- **lift**: 提升度 = P(A∪B) / (P(A) × P(B))

## 💡 使用场景

- **性能评估**: 对比不同算法的运行时间和内存占用
- **规则质量**: 评估不同支持度阈值下的规则质量
- **可扩展性**: 测试算法在不同数据规模下的表现
- **参数调优**: 找到最优的支持度和置信度设置

## 📚 相关论文

- Agrawal, R., & Srikant, R. (1994). Fast algorithms for mining association rules
- Han, J., et al. (2000). Mining frequent patterns without candidate generation
- Zaki, M. J., et al. (2003). Scalable algorithms for association mining

## 📄 许可证

MIT License
