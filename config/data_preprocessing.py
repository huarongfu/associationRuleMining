# data_preprocessing.py
"""
手机评论数据预处理脚本
功能：数据清洗 -> 中文分词 -> TF-IDF关键词提取 -> 构建事务数据库
"""

import pandas as pd
import jieba
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import warnings
warnings.filterwarnings('ignore')

class CommentPreprocessor:
    """评论数据预处理器"""
    
    def __init__(self, stopwords_file='stopwords.txt'):
        """
        初始化预处理器
        
        Args:
            stopwords_file: 停用词文件路径
        """
        self.stopwords_file = stopwords_file
        self.stopwords = set()
        self.load_stopwords()
        self.extend_domain_stopwords()
        self.init_jieba()
        
    def load_stopwords(self):
        """加载停用词表"""
        try:
            with open(self.stopwords_file, 'r', encoding='utf-8') as f:
                self.stopwords = set([line.strip() for line in f if line.strip()])
            print(f"成功加载停用词 {len(self.stopwords)} 个")
        except FileNotFoundError:
            print(f"警告：停用词文件 {self.stopwords_file} 未找到，使用空停用词表")
            self.stopwords = set()
    
    def extend_domain_stopwords(self):
        """扩展手机评论场景下的领域停用词，过滤明显无用的词"""
        domain_stopwords = {
            # 人称/群体
            '家人', '学生', '小伙伴', '小哥',
            # 时间相关
            '今后', '目前', '已经', '现在', '当时', '后来', '以前', '之后',
            '今天', '昨天', '头天', '当天', '昨晚', '早上',
            # 次数/程度等
            '一次', '两次', '三次', '不多', '稍微', '有点', '有点儿', '有些',
            # 语气/连接词
            '比如', '反正', '其实', '然后', '因为', '所以', '但是',
            # 总结性词
            '总体', '总的来说'
        }
        before = len(self.stopwords)
        self.stopwords |= domain_stopwords
        added = len(self.stopwords) - before
        if added > 0:
            print(f"已额外添加 {added} 个领域停用词")
    
    def init_jieba(self):
        """初始化jieba分词器，添加手机领域专业词汇"""
        # 手机领域专业词典（可以扩展）
        professional_words = [
            '全面屏', '刘海屏', '水滴屏', '曲面屏', '2K屏', 'OLED', 'LCD', 
            '骁龙', '麒麟', '联发科', '苹果A', 'Exynos', '高通', 'MTK',
            '麒麟970', '骁龙845', '骁龙835', 'A11', 'A12', 'P60',
            '人脸识别', '指纹识别', '屏下指纹', '面部解锁', '虹膜识别',
            '双摄', '三摄', '四摄', '像素', '拍照', '摄影', '美颜', 'AI摄影',
            '快充', '无线充电', '闪充', '续航', '电池', '毫安', 'mAh',
            '运行内存', '存储', 'RAM', 'ROM', '6GB', '8GB', '128GB', '256GB',
            'HiFi', '音质', '立体声', '双扬声器', '杜比',
            '游戏模式', '吃鸡', '王者荣耀', '帧率', '画质',
            '京东', '自营', '物流', '快递', '客服', '售后',
            '性价比', '颜值', '手感', '轻薄', '厚重', '边框', '下巴',
            '发烫', '发热', '卡顿', '流畅', '死机', '重启',
            '华为', '小米', '苹果', 'iPhone', 'vivo', 'OPPO', '荣耀', '红米',
            '三星', '魅族', '一加', '坚果', '夏普', '酷派', '小辣椒'
        ]
        
        # 添加专业词汇到jieba词典，显式指定 freq 兼容所有版本
        for word in professional_words:
            jieba.add_word(word, freq=10)
        
        print(f"已添加 {len(professional_words)} 个手机领域专业词汇到jieba词典")
    
    def clean_text(self, text):
        """
        清洗文本数据
        
        Args:
            text: 原始文本
            
        Returns:
            清洗后的文本
        """
        if not isinstance(text, str):
            return ""
        
        # 1. 去除HTML实体
        text = re.sub(r'&[a-z]+;', '', text)
        text = re.sub(r'&hellip;', '', text)
        text = re.sub(r'&nbsp;', '', text)
        text = re.sub(r'&mdash;', '', text)
        text = re.sub(r'&ldquo;|&rdquo;', '', text)
        
        # 2. 去除URL链接
        text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', text)
        
        # 3. 去除除中文和空白以外的所有字符（包括数字和字母）
        #   只保留中文和空格/换行等空白符
        text = re.sub(r'[^\u4e00-\u9fa5\s]', '', text)
        
        # 4. 此时数字和字母已经被移除，无需再单独处理
        
        # 5. 去除多余空白字符
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    def segment_text(self, text):
        """
        中文分词并过滤停用词
        
        Args:
            text: 清洗后的文本
            
        Returns:
            分词后的词列表
        """
        if not text:
            return []
        
        # 使用jieba分词，兼容无 lcut 的版本
        try:
            words = jieba.lcut(text)
        except AttributeError:
            # 旧版本只有 cut 接口
            words = list(jieba.cut(text))
        
        # 过滤停用词和单字词
        filtered_words = []
        for word in words:
            word = word.strip()
            if (word and 
                len(word) > 1 and  # 过滤单字词
                word not in self.stopwords and  # 过滤停用词
                not word.isdigit() and  # 过滤纯数字
                not re.match(r'^[a-zA-Z]+$', word)):  # 过滤纯英文
                filtered_words.append(word)
        
        return filtered_words
    
    def extract_keywords_tfidf(self, documents, top_k=15):
        """
        使用TF-IDF提取每条评论的关键词
        
        Args:
            documents: 分词后的文档列表（每个文档是词列表）
            top_k: 每条评论提取的关键词数量
            
        Returns:
            keywords_list: 每条评论的关键词列表
            vocabulary: 词汇表
            tfidf_matrix: TF-IDF矩阵
        """
        # 将词列表转换为空格分隔的字符串
        text_docs = [' '.join(doc) for doc in documents]
        
        # 创建TF-IDF向量化器
        vectorizer = TfidfVectorizer(
            max_features=1000,  # 限制词汇表大小
            min_df=2,  # 最小文档频率
            max_df=0.8  # 最大文档频率
        )
        
        # 拟合并转换
        tfidf_matrix = vectorizer.fit_transform(text_docs)
        
        # 获取词汇表
        vocabulary = vectorizer.get_feature_names_out()
        
        # 提取每条评论的top_k关键词
        keywords_list = []
        for i in range(len(documents)):
            # 获取当前文档的TF-IDF向量
            doc_vector = tfidf_matrix[i].toarray()[0]
            
            # 获取非零特征的索引和值
            nonzero_indices = np.nonzero(doc_vector)[0]
            if len(nonzero_indices) > 0:
                # 按TF-IDF值排序
                sorted_indices = nonzero_indices[np.argsort(doc_vector[nonzero_indices])[::-1]]
                # 取top_k个关键词
                top_indices = sorted_indices[:min(top_k, len(sorted_indices))]
                keywords = [vocabulary[idx] for idx in top_indices]
            else:
                keywords = []
            
            keywords_list.append(keywords)
        
        return keywords_list, vocabulary, tfidf_matrix
    
    def process(self, input_file, output_file='preprocessed_transactions.csv', top_k=15):
        """
        完整的数据预处理流程
        
        Args:
            input_file: 输入数据文件路径
            output_file: 输出文件路径
            top_k: 每条评论提取的关键词数量
            
        Returns:
            DataFrame: 包含原始数据和处理结果
        """
        print(f"开始处理数据文件: {input_file}")
        
        # 1. 加载数据
        try:
            df = pd.read_csv(input_file)
            print(f"成功加载数据，共 {len(df)} 条记录")
        except Exception as e:
            print(f"加载数据失败: {e}")
            return None
        
        # 2. 数据清洗
        print("开始数据清洗...")
        df['cleaned_content'] = df['content'].apply(self.clean_text)
        
        # 3. 中文分词
        print("开始中文分词...")
        df['segmented_words'] = df['cleaned_content'].apply(self.segment_text)
        
        # 统计分词结果
        word_counts = df['segmented_words'].apply(len)
        print(f"分词完成，平均每条评论 {word_counts.mean():.2f} 个词")
        print(f"最长评论 {word_counts.max()} 个词，最短评论 {word_counts.min()} 个词")
        
        # 4. TF-IDF关键词提取
        print("开始TF-IDF关键词提取...")
        documents = df['segmented_words'].tolist()
        keywords_list, vocabulary, tfidf_matrix = self.extract_keywords_tfidf(documents, top_k)
        
        df['keywords'] = keywords_list
        df['keywords_str'] = df['keywords'].apply(lambda x: ' '.join(x))
        
        print(f"关键词提取完成，词汇表大小: {len(vocabulary)}")
        print(f"平均每条评论 {df['keywords'].apply(len).mean():.2f} 个关键词")
        
        # 5. 构建事务数据库
        print("构建事务数据库...")
        transactions = df['keywords'].tolist()
        
        # 6. 保存结果
        print(f"保存结果到: {output_file}")
        
        # 保存完整的处理结果
        result_df = df[['id', 'content', 'score', 'content_length', 
                       'cleaned_content', 'keywords_str']].copy()
        result_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        
        # 单独保存事务数据库（用于关联规则挖掘）
        transactions_file = 'data/transactions.txt'
        with open(transactions_file, 'w', encoding='utf-8') as f:
            for i, transaction in enumerate(transactions):
                if transaction:  # 跳过空事务
                    f.write(f"{' '.join(transaction)}\n")
        print(f"事务数据库保存到: {transactions_file}")
        
        # 保存词汇表
        vocab_file = 'data/vocabulary.txt'
        with open(vocab_file, 'w', encoding='utf-8') as f:
            for word in vocabulary:
                f.write(f"{word}\n")
        print(f"词汇表保存到: {vocab_file}")
        
        # 7. 统计信息
        print("\n=== 预处理完成 ===")
        print(f"原始评论数: {len(df)}")
        print(f"有效事务数: {len([t for t in transactions if t])}")
        
        # 统计高频关键词
        all_keywords = []
        for keywords in transactions:
            all_keywords.extend(keywords)
        
        if all_keywords:
            from collections import Counter
            keyword_counter = Counter(all_keywords)
            top_keywords = keyword_counter.most_common(20)
            
            print("\nTop 20高频关键词:")
            for word, count in top_keywords:
                print(f"  {word}: {count}次")
        
        return df, transactions, vocabulary

def main():
    """主函数"""
    # 配置参数
    INPUT_FILE = 'data/jd_cleaned_comments.csv'  # 输入文件
    STOPWORDS_FILE = 'data/stopwords.txt'        # 停用词文件
    OUTPUT_FILE = 'data/preprocessed_transactions.csv'  # 输出文件
    TOP_K = 15  # 每条评论提取的关键词数量
    
    # 创建预处理器
    preprocessor = CommentPreprocessor(stopwords_file=STOPWORDS_FILE)
    
    # 执行预处理
    result = preprocessor.process(
        input_file=INPUT_FILE,
        output_file=OUTPUT_FILE,
        top_k=TOP_K
    )
    if result is None:
        return
    df, transactions, vocabulary = result
    
    # 打印示例结果
    if df is not None:
        print("\n=== 示例结果 ===")
        print("原始评论示例:")
        print(df.iloc[0]['content'])
        print("\n清洗后文本:")
        print(df.iloc[0]['cleaned_content'])
        print("\n关键词提取结果:")
        print(df.iloc[0]['keywords'])
        
        print(f"\n事务数据库大小: {len(transactions)} 条事务")
        print(f"词汇表大小: {len(vocabulary)} 个词")

if __name__ == "__main__":
    main()
