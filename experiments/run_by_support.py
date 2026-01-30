import os
import sys
import csv
from typing import Dict, Callable, List

# 自动配置项目路径
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from utils import load_transactions, eval_rules_comprehensive, profile_execution
from algorithms import apriori_impl, fpgrowth_impl, eclat_impl, apriori_improved_impl


def main():
    data_path = os.path.join(ROOT, "data", "transactions.txt")
    transactions = load_transactions(data_path)

    # 数据集较稀疏，进一步降低阈值以产生更多规则
    min_conf = 0.4
    support_list = [0.003, 0.004, 0.005, 0.007, 0.01]

    algos: Dict[str, Callable] = {
        "apriori": apriori_impl.run,
        "fpgrowth": fpgrowth_impl.run,
        "eclat": eclat_impl.run,
        "apriori_improved": apriori_improved_impl.run,
    }

    results_dir = os.path.join(ROOT, "results")
    os.makedirs(results_dir, exist_ok=True)

    # ==================== 性能指标 CSV ====================
    perf_csv = os.path.join(results_dir, "performance_by_support.csv")
    
    # ==================== 规则质量 CSV ====================
    quality_csv = os.path.join(results_dir, "quality_by_support.csv")
    
    # ==================== 规则详情 CSV ====================
    rules_detail_csv = os.path.join(results_dir, "rules_by_support.csv")

    with open(perf_csv, "w", newline="", encoding="utf-8") as fperf, \
         open(quality_csv, "w", newline="", encoding="utf-8") as fquality, \
         open(rules_detail_csv, "w", newline="", encoding="utf-8") as frules:
        
        # 性能指标 CSV 头部
        pw = csv.writer(fperf)
        pw.writerow([
            "algorithm", "min_support", "min_conf", 
            "runtime_sec", "memory_mb"
        ])

        # 规则质量 CSV 头部
        qw = csv.writer(fquality)
        qw.writerow([
            "algorithm", "min_support", "min_conf", 
            "mean_support", "min_support_val", "max_support_val",
            "mean_confidence", "min_confidence_val", "max_confidence_val",
            "mean_lift", "min_lift", "max_lift"
        ])

        # 规则详情 CSV 头部
        rdetail = csv.writer(frules)
        rdetail.writerow([
            "algorithm", "min_support", "min_conf",
            "antecedent", "consequent", "support", "confidence", "lift", "leverage", "conviction", "cosine",
        ])

        # 运行实验
        for s in support_list:
            for name, fn in algos.items():
                # 执行算法并收集性能和规则数据
                rules, metrics = profile_execution(fn, transactions, min_support=s, min_confidence=min_conf)
                stats = eval_rules_comprehensive(rules)
                
                # 写性能指标
                pw.writerow([
                    name, s, min_conf,
                    f"{metrics['runtime_sec']:.6f}", 
                    f"{metrics['memory_mb']:.2f}"
                ])
                # 写规则质量指标
                qw.writerow([
                    name, s, min_conf,
                    f"{stats['mean_support']:.6f}" if stats['mean_support'] else None,
                    f"{stats['min_support']:.6f}" if stats['min_support'] else None,
                    f"{stats['max_support']:.6f}" if stats['max_support'] else None,
                    f"{stats['mean_confidence']:.6f}" if stats['mean_confidence'] else None,
                    f"{stats['min_confidence']:.6f}" if stats['min_confidence'] else None,
                    f"{stats['max_confidence']:.6f}" if stats['max_confidence'] else None,
                    f"{stats['mean_lift']:.6f}" if stats['mean_lift'] else None,
                    f"{stats['min_lift']:.6f}" if stats['min_lift'] else None,
                    f"{stats['max_lift']:.6f}" if stats['max_lift'] else None
                ])
                
                # 逐条保存挖掘出的规则，便于后续查看
                for r in rules:
                    rdetail.writerow([
                        name, s, min_conf,
                        " ".join(r.get("antecedent", ())),
                        " ".join(r.get("consequent", ())),
                        f"{r.get('support'):.6f}" if r.get("support") is not None else None,
                        f"{r.get('confidence'):.6f}" if r.get("confidence") is not None else None,
                        f"{r.get('lift'):.6f}" if r.get("lift") is not None else None,
                        f"{r.get('leverage'):.6f}" if r.get("leverage") is not None else None,
                        f"{r.get('conviction'):.6f}" if r.get("conviction") is not None else None,
                        f"{r.get('cosine'):.6f}" if r.get("cosine") is not None else None,
                    ])
    
    print(f"✓ 性能指标已保存: {perf_csv}")
    print(f"✓ 规则质量已保存: {quality_csv}")
    print(f"✓ 规则详情已保存: {rules_detail_csv}")


if __name__ == "__main__":
    main()
