from collections import Counter, defaultdict
from itertools import combinations
import math
from typing import List, Dict, Any, Tuple

from utils import compute_cosine


def _apriori_gen(prev_freq: List[Tuple[str, ...]]) -> List[Tuple[str, ...]]:
    """Join step to produce size-(k+1) candidates from size-k frequent itemsets."""
    if not prev_freq:
        return []
    k = len(prev_freq[0]) + 1
    prev_set = set(prev_freq)
    candidates = []
    prev_sorted = sorted(prev_freq)
    for i in range(len(prev_sorted)):
        for j in range(i + 1, len(prev_sorted)):
            a, b = prev_sorted[i], prev_sorted[j]
            if a[:-1] != b[:-1]:
                break
            candidate = tuple(sorted(set(a) | set(b)))
            if len(candidate) != k:
                continue
            # Apriori pruning: all (k-1) subsets must be frequent
            all_subsets_frequent = True
            for sub in combinations(candidate, k - 1):
                if sub not in prev_set:
                    all_subsets_frequent = False
                    break
            if all_subsets_frequent:
                candidates.append(candidate)
    return candidates


def run(transactions: List[List[str]], min_support: float, min_confidence: float) -> List[Dict[str, Any]]:
    """Apriori with hash-bucket pruning and recursive level expansion."""
    n_tx = len(transactions)
    if n_tx == 0:
        return []

    min_sup_count = max(1, math.ceil(min_support * n_tx))
    bucket_mod = 1009  # prime bucket size for hash-based pruning

    # Normalize transactions to de-duplicate items per transaction and sort for stable combinations
    norm_tx = [sorted(set(tx)) for tx in transactions if tx]

    # Count 1-itemsets
    counter = Counter()
    for tx in norm_tx:
        counter.update(tx)
    freq1 = {(item,): cnt for item, cnt in counter.items() if cnt >= min_sup_count}
    support_map: Dict[frozenset, float] = {frozenset(k): v / n_tx for k, v in freq1.items()}

    def count_with_hash(candidates: List[Tuple[str, ...]], k: int) -> Dict[Tuple[str, ...], int]:
        if not candidates:
            return {}
        cand_set = set(candidates)
        bucket_counts = defaultdict(int)
        support_counts = defaultdict(int)
        for tx in norm_tx:
            if len(tx) < k:
                continue
            for comb in combinations(tx, k):
                h = hash(comb) % bucket_mod
                bucket_counts[h] += 1
                if comb in cand_set:
                    support_counts[comb] += 1
        # Hash-bucket pruning before applying min_sup
        pruned_candidates = {c for c in candidates if bucket_counts[hash(c) % bucket_mod] >= min_sup_count}
        return {c: cnt for c, cnt in support_counts.items() if cnt >= min_sup_count and c in pruned_candidates}

    def mine(prev_freq: Dict[Tuple[str, ...], int], k: int) -> None:
        if not prev_freq:
            return
        candidates = _apriori_gen(list(prev_freq.keys()))
        if not candidates:
            return
        freq_k = count_with_hash(candidates, k)
        if not freq_k:
            return
        for itemset, cnt in freq_k.items():
            support_map[frozenset(itemset)] = cnt / n_tx
        mine(freq_k, k + 1)

    mine(freq1, 2)

    # Generate association rules from support map
    rules: List[Dict[str, Any]] = []
    for itemset, supp in support_map.items():
        if len(itemset) < 2:
            continue
        items = tuple(sorted(itemset))
        for r in range(1, len(items)):
            for antecedent in combinations(items, r):
                antecedent_fs = frozenset(antecedent)
                consequent_fs = itemset - antecedent_fs
                if not consequent_fs:
                    continue
                supp_ante = support_map.get(antecedent_fs)
                supp_cons = support_map.get(consequent_fs)
                if not supp_ante or supp_ante == 0:
                    continue
                confidence = supp / supp_ante
                if confidence + 1e-12 < min_confidence:
                    continue
                lift = None
                leverage = None
                conviction = None
                if supp_cons and supp_cons > 0:
                    lift = confidence / supp_cons
                    leverage = supp - supp_ante * supp_cons
                    if 1 - confidence != 0:
                        conviction = (1 - supp_cons) / (1 - confidence)
                rules.append({
                    "antecedent": tuple(sorted(antecedent_fs)),
                    "consequent": tuple(sorted(consequent_fs)),
                    "support": supp,
                    "confidence": confidence,
                    "lift": lift,
                    "leverage": leverage,
                    "conviction": conviction,
                    "cosine": compute_cosine(supp, lift),
                })
    return rules
