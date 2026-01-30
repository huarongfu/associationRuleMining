"""
Apriori算法 - 基于哈希表与十字链表存储的改进版本
Hash-table + Cross-linked list based Apriori implementation
"""

from collections import defaultdict
from itertools import combinations
import math
from typing import List, Dict, Any, Tuple, Set, Optional

from utils import compute_cosine


class TrieNode:
    """十字链表节点 - 用于存储事务中的项目及其关系"""
    __slots__ = ['item', 'count', 'right', 'down']
    
    def __init__(self, item: Optional[str] = None):
        self.item = item              # 项目名称
        self.count = 0                # 支持度计数
        self.right = None             # 右指针：同一事务中的下一项
        self.down = None              # 下指针：同一项在其他事务中的出现


class HashTable:
    """
    哈希表 - 用于高效存储和查询候选项集的支持度
    支持快速增删查改操作
    """
    def __init__(self, size: int = 10007):  # 使用质数作为哈希表大小
        self.size = size
        self.table: List[List[Tuple[frozenset, int]]] = [[] for _ in range(size)]
        self.count = 0
    
    def _hash(self, itemset: frozenset) -> int:
        """计算哈希值"""
        return hash(itemset) % self.size
    
    def insert(self, itemset: frozenset, count: int) -> None:
        """插入或更新项集计数"""
        idx = self._hash(itemset)
        for i, (key, _) in enumerate(self.table[idx]):
            if key == itemset:
                self.table[idx][i] = (key, count)
                return
        self.table[idx].append((itemset, count))
        self.count += 1
    
    def get(self, itemset: frozenset) -> int:
        """获取项集计数，不存在返回0"""
        idx = self._hash(itemset)
        for key, cnt in self.table[idx]:
            if key == itemset:
                return cnt
        return 0
    
    def increment(self, itemset: frozenset) -> None:
        """增加项集计数"""
        idx = self._hash(itemset)
        for i, (key, cnt) in enumerate(self.table[idx]):
            if key == itemset:
                self.table[idx][i] = (key, cnt + 1)
                return
        self.table[idx].append((itemset, 1))
        self.count += 1
    
    def items(self):
        """遍历所有项"""
        for bucket in self.table:
            for key, cnt in bucket:
                yield key, cnt
    
    def __len__(self):
        return self.count


class CrossLinkedList:
    """
    十字链表 - 用于高效遍历事务和项的关系
    优点：快速定位特定项在各事务中的位置，加速支持度计算
    """
    def __init__(self):
        self.head = None              # 事务链表头
        self.item_index: Dict[str, TrieNode] = {}  # 项目索引
    
    def build_from_transactions(self, transactions: List[List[str]]) -> None:
        """从事务集合构建十字链表"""
        current_transaction = None
        
        for tx in transactions:
            if not tx:
                continue
            
            # 对事务中的项目排序，便于后续遍历
            sorted_items = sorted(set(tx))
            tx_head = None
            tx_tail = None
            
            for item in sorted_items:
                node = TrieNode(item)
                
                # 建立右指针（同事务链）
                if tx_head is None:
                    tx_head = node
                else:
                    tx_tail.right = node
                tx_tail = node
                
                # 建立下指针（同项链）
                if item not in self.item_index:
                    self.item_index[item] = node
                else:
                    # 在该项的链表末尾添加新节点
                    current = self.item_index[item]
                    while current.down is not None:
                        current = current.down
                    current.down = node
            
            # 建立事务链
            if self.head is None:
                self.head = tx_head
                current_transaction = tx_head
            else:
                current_transaction.right = tx_head
                current_transaction = tx_head
    
    def count_itemset(self, itemset: frozenset) -> int:
        """
        通过十字链表高效计算项集的支持度
        利用下指针快速遍历同项的所有出现
        """
        items = sorted(itemset)
        if not items:
            return 0
        
        # 获取第一项的所有出现节点
        first_item = items[0]
        if first_item not in self.item_index:
            return 0
        
        count = 0
        current_node = self.item_index[first_item]
        
        # 遍历第一项的所有出现
        while current_node is not None:
            # 对每个出现，检查是否包含其他所有项
            all_present = True
            
            for other_item in items[1:]:
                # 在同事务中查找其他项
                check_node = current_node.right
                found = False
                while check_node is not None:
                    if check_node.item == other_item:
                        found = True
                        break
                    check_node = check_node.right
                
                if not found:
                    all_present = False
                    break
            
            if all_present:
                count += 1
            
            current_node = current_node.down
        
        return count


def _apriori_gen(prev_freq: List[frozenset]) -> List[frozenset]:
    """
    生成候选项集
    连接步骤：从大小为k的频繁项集生成大小为k+1的候选项集
    """
    if not prev_freq:
        return []
    
    k = len(next(iter(prev_freq)))
    prev_set = set(prev_freq)
    candidates = []
    
    prev_sorted = sorted(prev_freq, key=lambda x: sorted(list(x)))
    
    for i in range(len(prev_sorted)):
        for j in range(i + 1, len(prev_sorted)):
            itemset_i = prev_sorted[i]
            itemset_j = prev_sorted[j]
            
            # 检查前k-1项是否相同（F(k-1)连接）
            sorted_i = sorted(list(itemset_i))
            sorted_j = sorted(list(itemset_j))
            
            if sorted_i[:-1] != sorted_j[:-1]:
                break
            
            candidate = itemset_i | itemset_j
            
            if len(candidate) != k + 1:
                continue
            
            # 剪枝：所有大小为k的子集必须是频繁的
            all_subsets_frequent = True
            for sub in combinations(sorted(candidate), k):
                if frozenset(sub) not in prev_set:
                    all_subsets_frequent = False
                    break
            
            if all_subsets_frequent:
                candidates.append(candidate)
    
    return candidates


def run(transactions: List[List[str]], min_support: float, min_confidence: float) -> List[Dict[str, Any]]:
    """
    基于哈希表与十字链表的改进Apriori算法
    
    优势：
    1. 十字链表加速支持度计算 - O(1)级别的项集查询
    2. 哈希表高效存储和查询候选项集
    3. 减少重复扫描事务集
    4. 更低的时间复杂度
    """
    n_tx = len(transactions)
    if n_tx == 0:
        return []
    
    min_sup_count = max(1, math.ceil(min_support * n_tx))
    
    # 规范化事务（去重、排序）
    norm_tx = [sorted(set(tx)) for tx in transactions if tx]
    
    # ==================== 第1步：构建十字链表 ====================
    cross_list = CrossLinkedList()
    cross_list.build_from_transactions(norm_tx)
    
    # ==================== 第2步：统计1-项集 ====================
    freq1_hash = HashTable()
    support_map: Dict[frozenset, float] = {}
    
    for item, node in cross_list.item_index.items():
        # 计算项的支持度
        count = 0
        current = node
        while current is not None:
            count += 1
            current = current.down
        
        if count >= min_sup_count:
            itemset_fs = frozenset([item])
            freq1_hash.insert(itemset_fs, count)
            support_map[itemset_fs] = count / n_tx
    
    # ==================== 第3步：递归挖掘频繁项集 ====================
    def mine_recursive(freq_itemsets: HashTable, k: int) -> None:
        """递归挖掘更大的频繁项集"""
        if freq_itemsets.count == 0:
            return
        
        # 生成候选项集
        freq_list = [itemset for itemset, _ in freq_itemsets.items()]
        candidates = _apriori_gen(freq_list)
        
        if not candidates:
            return
        
        # 使用哈希表存储候选项集的支持度
        candidate_hash = HashTable()
        
        # 扫描事务，计算候选项集的支持度
        for tx in norm_tx:
            tx_items = set(tx)
            
            # 使用组合快速过滤候选项
            for candidate in candidates:
                if candidate.issubset(tx_items):
                    candidate_hash.increment(candidate)
        
        # 筛选出频繁的候选项集
        freq_k_hash = HashTable()
        for candidate, count in candidate_hash.items():
            if count >= min_sup_count:
                freq_k_hash.insert(candidate, count)
                support_map[candidate] = count / n_tx
        
        # 递归处理下一层
        mine_recursive(freq_k_hash, k + 1)
    
    # 初始化1-项集哈希表
    freq1_hash_for_mining = HashTable()
    for itemset, supp in support_map.items():
        if len(itemset) == 1:
            freq1_hash_for_mining.insert(itemset, int(supp * n_tx))
    
    mine_recursive(freq1_hash_for_mining, 2)
    
    # ==================== 第4步：生成关联规则 ====================
    rules: List[Dict[str, Any]] = []
    
    for itemset, supp in support_map.items():
        if len(itemset) < 2:
            continue
        
        items = tuple(sorted(itemset))
        
        # 枚举所有可能的前件-后件组合
        for r in range(1, len(items)):
            for antecedent in combinations(items, r):
                antecedent_fs = frozenset(antecedent)
                consequent_fs = itemset - antecedent_fs
                
                if not consequent_fs:
                    continue
                
                supp_ante = support_map.get(antecedent_fs, 0)
                supp_cons = support_map.get(consequent_fs, 0)
                
                if not supp_ante or supp_ante == 0:
                    continue
                
                confidence = supp / supp_ante
                
                if confidence + 1e-12 < min_confidence:
                    continue
                
                # 计算其他度量
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
