"""知识库"""

import os
import configure_data as config
import hashlib
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from datetime import datetime

def check_md5(md5_str: str):
    """检查传入的 md5字符串是否已经被处理过了"""
    if not os.path.exists(config.md5_path):
        open(config.md5_path,"w",encoding="utf-8").close()
        return False     # 表示未处理过
    else:
        with open(config.md5_path,"r",encoding="utf-8") as f:
            for line in f.readlines():
                line = line.strip()
                if line == md5_str:
                    return True     # 表示已处理过
        return False

def save_md5(md5_str: str):
    """将传入的 md5字符串，记录到文件内保存"""
    with open(config.md5_path,"a",encoding="utf-8") as f:
        f.write(md5_str + '\n')

def get_string_md5(input_str: str, encoding="utf-8"):
    """将传入的字符串转换为 md5字符串"""
    # 将字符串转换为 bytes字节数据
    str_bytes = input_str.encode(encoding=encoding)

    # 创建 md5 对象
    md5_obj = hashlib.md5()     # 得到 md5对象
    md5_obj.update(str_bytes)   # 更新内容（传入即将转换的字符）
    md5_hex = md5_obj.hexdigest()      # 得到 md5的十六进制字符串

    return md5_hex

class KnowledgeBaseService(object):
    def __init__(self):
        # 如果文件夹不存在，则创建
        os.makedirs(config.persist_directory, exist_ok=True)
        self.faiss_index_path = os.path.join(config.persist_directory, "index")   #数据库本地存储文件夹
        self.embedding = DashScopeEmbeddings(model="text-embedding-v4")

        # 判断本地是否存在 faiss索引，存在就加载；不存在新建空索引
        if os.path.exists(self.faiss_index_path):
            self.faiss = FAISS.load_local(
                self.faiss_index_path,
                self.embedding,
                allow_dangerous_deserialization=True
            )    # 向量存储的实例 FAISS向量库对象
        else:
            # 新建空 FAISS向量库
            self.faiss = FAISS.from_texts(       # 用占位文本创建索引
                texts=["placeholder"],
                embedding=self.embedding,
                metadatas=[{"source": "placeholder"}]
            )
            # 删除占位数据
            self.faiss.delete([self.faiss.index_to_docstore_id[0]])
            self.faiss.save_local(self.faiss_index_path)     # 保存空索引文件

        self.spliter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,             # 分割后文本段最大长度
            chunk_overlap=config.chunk_overlap,       # 连续文本段允许重叠的最大数量
            separators=config.separators,             # 自然段落划分的符号
            length_function=len,                      # 使用 Python自带的 len函数做长度统计的依据
        )   #文本分割器对象

    def upload_by_str(self,data: str,filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        # 先得到传入字符串的 md5值
        md5_hex = get_string_md5(data)

        if check_md5(md5_hex):
            return "[内容已存在知识库中]"

        if len(data) > config.max_split_char_number:
            knowledge_chunks: list[str] = self.spliter.split_text(data)
        else:
            knowledge_chunks = [data]

        metadata = {
            "source": filename,
            "create_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "operator": "Yuames",
        }
        self.faiss.add_texts(        # 内容加载到向量库中
            # iterable -> list \ tuple
            texts=knowledge_chunks,
            metadatas=[metadata for _ in knowledge_chunks]
        )

        # FAISS新增向量后必须手动持久化保存到本地磁盘
        self.faiss.save_local(self.faiss_index_path)

        save_md5(md5_hex)

        return "[内容已成功载入向量库]"

if __name__ == '__main__':
    service = KnowledgeBaseService()
    res = service.upload_by_str("周杰伦","testfile")
    print(res)