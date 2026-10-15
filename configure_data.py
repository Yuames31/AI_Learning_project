md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./faiss_db"
chunk_size = 1000
chunk_overlap = 100
separators = ["。", "！", "?","\n\n","\n",".","!","？"," ",""]
max_split_char_number = 1000      # 文本分割阈值

#
similarity_threshold = 2           # 检索返回匹配的文档数量

embedding_model = "text-embedding-v4"
chat_model_name = "qwen-plus"

session_config = {
        "configurable":{
            "session_id": "user001",
        }
    }