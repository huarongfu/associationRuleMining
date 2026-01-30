from typing import List, Dict, Any
from mlxtend.frequent_patterns import apriori, association_rules
from utils import transactions_to_df, compute_cosine


def run(transactions: List[List[str]], min_support: float, min_confidence: float) -> List[Dict[str, Any]]:
    """Run Apriori using mlxtend and return a list of rule dicts."""
    df = transactions_to_df(transactions)
    freq = apriori(df, min_support=min_support, use_colnames=True)
    if freq.empty:
        return []
    rules_df = association_rules(freq, metric="confidence", min_threshold=min_confidence)
    rules: List[Dict[str, Any]] = []
    for _, row in rules_df.iterrows():
        rules.append({
            "antecedent": tuple(sorted(row["antecedents"])),
            "consequent": tuple(sorted(row["consequents"])),
            "support": float(row["support"]),
            "confidence": float(row["confidence"]),
            "lift": float(row["lift"]),
            "leverage": float(row["leverage"]),
            "conviction": float(row["conviction"]),
            "cosine": compute_cosine(float(row["support"]), float(row["lift"])),
        })
    return rules
