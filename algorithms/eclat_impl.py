import math
from typing import List, Dict, Any, Iterable, Tuple, Set

from utils import compute_cosine


def run(transactions: List[List[str]], min_support: float, min_confidence: float) -> List[Dict[str, Any]]:
    """Simple Eclat implementation returning association rules."""
    n_tx = len(transactions)
    if n_tx == 0:
        return []
    min_sup_count = max(1, math.ceil(min_support * n_tx))

    # Build vertical format: item -> tidset
    tidsets: Dict[str, Set[int]] = {}
    for tid, tx in enumerate(transactions):
        for item in tx:
            tidsets.setdefault(item, set()).add(tid)

    # Filter infrequent singletons
    items = [(item, tids) for item, tids in tidsets.items() if len(tids) >= min_sup_count]
    # Sort by support for deterministic behavior
    items.sort(key=lambda x: (len(x[1]), x[0]))

    frequent: Dict[frozenset, Set[int]] = {}

    def eclat(prefix: Tuple[str, ...], items_list: List[Tuple[str, Set[int]]]):
        for i, (item, tids) in enumerate(items_list):
            new_itemset = frozenset(prefix + (item,))
            frequent[new_itemset] = tids
            suffix: List[Tuple[str, Set[int]]] = []
            for j in range(i + 1, len(items_list)):
                item2, tids2 = items_list[j]
                inter = tids & tids2
                if len(inter) >= min_sup_count:
                    suffix.append((item2, inter))
            if suffix:
                eclat(prefix + (item,), suffix)

    eclat((), items)

    if not frequent:
        return []

    # Cache supports
    support_cache: Dict[frozenset, float] = {fs: len(tids) / n_tx for fs, tids in frequent.items()}

    rules: List[Dict[str, Any]] = []
    for itemset, tids in frequent.items():
        if len(itemset) < 2:
            continue
        support_itemset = support_cache[itemset]
        items_list = list(itemset)
        for i in range(len(items_list)):
            antecedent = frozenset(item for idx, item in enumerate(items_list) if idx != i)
            consequent = frozenset({items_list[i]})
            support_ante = support_cache.get(antecedent)
            support_cons = support_cache.get(consequent)
            if not support_ante or support_ante == 0:
                continue
            confidence = support_itemset / support_ante
            if confidence + 1e-12 < min_confidence:
                continue
            lift = None
            leverage = None
            conviction = None
            if support_cons and support_cons > 0:
                lift = confidence / support_cons
                leverage = support_itemset - support_ante * support_cons
                if 1 - confidence != 0:
                    conviction = (1 - support_cons) / (1 - confidence)
            rules.append({
                "antecedent": tuple(sorted(antecedent)),
                "consequent": tuple(sorted(consequent)),
                "support": support_itemset,
                "confidence": confidence,
                "lift": lift,
                "leverage": leverage,
                "conviction": conviction,
                "cosine": compute_cosine(support_itemset, lift),
            })
    return rules
