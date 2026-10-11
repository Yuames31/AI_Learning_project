import os
from langchain_community.vectorstores import FAISS
import configure_data as config

class VectorStoreService(object):
    def __init__(self, embedding):
        """
        Initialize the vector store service.
        :param embedding:  嵌入模型的传入
        """
        self.embedding = embedding
        # 与 knowledge_base.py 保持一致
        self.faiss_index_path = os.path.join(config.persist_directory, "index")

        self.vector_store = FAISS.load_local(
            folder_path=self.faiss_index_path,
            embeddings=self.embedding,
            allow_dangerous_deserialization=True  # LangChain 加载本地文件的安全校验开关
        )

    def get_retriever(self):
        """返回向量检索器，方便加入chain"""
        return self.vector_store.as_retriever(search_kwargs={"k": config.similarity_threshold})


if __name__ == '__main__':
    from langchain_community.embeddings import DashScopeEmbeddings
    retriever = VectorStoreService(DashScopeEmbeddings(model="text-embedding-v4")).get_retriever()
    res = retriever.invoke("我的体重180斤，尺码推荐")
    print(res)
