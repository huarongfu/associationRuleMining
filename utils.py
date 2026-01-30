import math
import random
import time
import tracemalloc
from typing import List, Sequence, Tuple, Dict, Any, Callable
from collections import defaultdict
import pandas as pd


Transaction = List[str]
Rule = Dict[str, Any]


def load_transactions(path: str) -> List[Transaction]:
    """Load transactions from a plain text file (one space-separated transaction per line)."""
    with open(path, "r", encoding="utf-8") as f:
        return [line.strip().split() for line in f if line.strip()]


def sample_transactions(transactions: List[Transaction], ratio: float, seed: int = 42) -> List[Transaction]:
    """Sample a proportion of transactions (without replacement)."""
    n = max(1, int(len(transactions) * ratio))
    random.seed(seed)
    return random.sample(transactions, n)


def transactions_to_df(transactions: List[Transaction]) -> pd.DataFrame:
    """Convert list of transactions to one-hot DataFrame for mlxtend."""
    # Build item universe
    items = sorted({item for tx in transactions for item in tx})
    data = []
    for tx in transactions:
        row = {item: (item in tx) for item in items}
        data.append(row)
    return pd.DataFrame(data)


def compute_cosine(support: float, lift: float):
    """Cosine similarity between itemsets derived from support and lift."""
    if support is None or lift is None:
        return None
    if support <= 0 or lift <= 0:
        return None
    return math.sqrt(support * lift)


def eval_rules(rules: Sequence[Rule]) -> Dict[str, Any]:
    """Aggregate basic quality metrics from a rule list."""
    if not rules:
        return {
            "count": 0,
            "mean_support": None,
            "mean_conf": None,
            "mean_lift": None,
            "mean_cosine": None,
        }
    supports = [r.get("support") for r in rules if r.get("support") is not None]
    confs = [r.get("confidence") for r in rules if r.get("confidence") is not None]
    lifts = [r.get("lift") for r in rules if r.get("lift") is not None]
    cosines = []
    for r in rules:
        c = r.get("cosine")
        if c is None:
            c = compute_cosine(r.get("support"), r.get("lift"))
        if c is not None:
            cosines.append(c)
    return {
        "count": len(rules),
        "mean_support": sum(supports) / len(supports) if supports else None,
        "mean_conf": sum(confs) / len(confs) if confs else None,
        "mean_lift": sum(lifts) / len(lifts) if lifts else None,
        "mean_cosine": sum(cosines) / len(cosines) if cosines else None,
    }


def time_it(fn, *args, **kwargs):
    """Measure runtime of a function call, returning (result, seconds)."""
    t0 = time.perf_counter()
    result = fn(*args, **kwargs)
    dt = time.perf_counter() - t0
    return result, dt


def profile_execution(fn: Callable, *args, **kwargs) -> Tuple[Any, Dict[str, Any]]:
    """
    执行函数并收集性能指标
    
    Returns:
        (result, metrics) - 其中 metrics 包含:
            - runtime_sec: 执行时间（秒）
            - memory_mb: 峰值内存占用（MB）
            - memory_peak: 峰值内存占用（字节）
    """
    tracemalloc.start()
    t0 = time.perf_counter()
    
    result = fn(*args, **kwargs)
    
    dt = time.perf_counter() - t0
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    
    metrics = {
        "runtime_sec": dt,
        "memory_mb": peak / (1024 * 1024),
        "memory_peak": peak,
    }
    
    return result, metrics


def eval_rules_comprehensive(rules: Sequence[Rule]) -> Dict[str, Any]:
    """
    综合评估规则质量，返回统一的质量指标
    
    指标包括：
    - count: 规则总数
    - mean_support: 平均支持度
    - min_support / max_support: 支持度范围
    - mean_confidence: 平均置信度
    - min_confidence / max_confidence: 置信度范围
    - mean_lift: 平均提升度
    - min_lift / max_lift: 提升度范围
    - mean_cosine: 平均cosine相似度
    """
    if not rules:
        return {
            "count": 0,
            "mean_support": None,
            "min_support": None,
            "max_support": None,
            "mean_confidence": None,
            "min_confidence": None,
            "max_confidence": None,
            "mean_lift": None,
            "min_lift": None,
            "max_lift": None,
            "mean_cosine": None,
        }
    
    supports = [r.get("support") for r in rules if r.get("support") is not None]
    confs = [r.get("confidence") for r in rules if r.get("confidence") is not None]
    lifts = [r.get("lift") for r in rules if r.get("lift") is not None]
    
    cosines = []
    for r in rules:
        c = r.get("cosine")
        if c is None:
            c = compute_cosine(r.get("support"), r.get("lift"))
        if c is not None:
            cosines.append(c)
    
    return {
        "count": len(rules),
        # 支持度指标
        "mean_support": sum(supports) / len(supports) if supports else None,
        "min_support": min(supports) if supports else None,
        "max_support": max(supports) if supports else None,
        # 置信度指标
        "mean_confidence": sum(confs) / len(confs) if confs else None,
        "min_confidence": min(confs) if confs else None,
        "max_confidence": max(confs) if confs else None,
        # 提升度指标
        "mean_lift": sum(lifts) / len(lifts) if lifts else None,
        "min_lift": min(lifts) if lifts else None,
        "max_lift": max(lifts) if lifts else None,
        # cosine相似度
        "mean_cosine": sum(cosines) / len(cosines) if cosines else None,
    }


def eval_rules(rules: Sequence[Rule]) -> Dict[str, Any]:
    """向后兼容的简化版本"""
    comprehensive = eval_rules_comprehensive(rules)
    return {
        "count": comprehensive["count"],
        "mean_support": comprehensive["mean_support"],
        "mean_conf": comprehensive["mean_confidence"],
        "mean_lift": comprehensive["mean_lift"],
        "mean_cosine": comprehensive["mean_cosine"],
    }
