"""知识库"""

import os
import configure_data as config
import hashlib

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
        self.faiss = None     # 向量存储的实例 Faiss向量库对象
        self.spliter = None   #文本分割器对象

    def upload_by_str(self,data,filename):
        """将传入的字符串进行向量化，存入向量数据库中"""
        pass


if __name__ == '__main__':
    save_md5("7a8941058aaf4df5147042ce104568da")
    print(check_md5("7a8941058aaf4df5147042ce104568da"))