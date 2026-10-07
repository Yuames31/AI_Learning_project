md5_path = "./md5.text"

# Chroma
collection_name = "rag"
persist_directory = "./faiss_db"
chunk_size = 1000
chunk_overlap = 100
separators = ["。", "！", "?","\n\n","\n",".","!","？"," ",""]
max_split_char_number = 1000      # 文本分割阈值
