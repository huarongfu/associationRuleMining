# 结果分析工具

本目录包含实验结果的分析和可视化脚本。

## 📁 文件说明

- `analysis.py` - 规则质量指标分析（表格展示）
- `plot_performance.py` - 性能指标可视化（图表生成）

## 🚀 使用方法

### 1. 查看规则质量分析

```bash
python analysis/analysis.py
```

输出：
- 按最小支持度的规则质量对比表
- 按数据集规模的规则质量对比表
- 包括支持度、置信度、提升度等统计指标

### 2. 生成性能对比图表

```bash
python analysis/plot_performance.py
```

生成图表：
- `results/performance_by_support.png` - 按支持度的性能对比
- `results/performance_by_scale.png` - 按数据集规模的性能对比

每个图表包含 4 个子图：
- 运行时间柱状图
- 运行时间趋势折线图
- 内存占用柱状图
- 内存占用趋势折线图

## 📊 分析指标说明

**性能指标：**
- 运行时间 (秒)
- 内存占用 (MB)

**规则质量指标：**
- 支持度 (Support)：规则在数据集中出现的频率
- 置信度 (Confidence)：规则前件发生时后件也发生的概率
- 提升度 (Lift)：规则相对于独立情况的增强倍数

## ⚠️ 注意事项

- 需要先运行实验脚本生成结果数据
- 图表生成依赖 matplotlib 和中文字体配置
- 所有分析结果基于 `results/` 目录中的 CSV 文件
