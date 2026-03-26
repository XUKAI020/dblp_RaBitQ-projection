import json
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import struct

def write_fvecs(file_path, data):
    d = data.shape[1]
    with open(file_path, 'wb') as f:
        for vec in data:
            f.write(struct.pack('i', d))
            f.write(vec.astype('float32').tobytes())

def write_ivecs(file_path, data):
    with open(file_path, 'wb') as f:
        for val in data:
            f.write(struct.pack('i', 1))
            f.write(struct.pack('I', val))

print("1. 加载文本并进行向量化 (CPU 将满载运行)...")
with open('dblp_sample.jsonl', 'r', encoding='utf-8') as f:
    texts = [json.loads(line)['title'] for line in f]

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts, show_progress_bar=True)

print("2. 执行 PCA 降维 (384 -> 128)...")
pca = PCA(n_components=128)
reduced_embeddings = pca.fit_transform(embeddings).astype(np.float32)

query_data = reduced_embeddings[:100]
base_data = reduced_embeddings[100:]

print("3. K-Means 物理空间切分 (100个抽屉)...")
kmeans = KMeans(n_clusters=100, random_state=42, n_init=10).fit(base_data)

print("4. 输出 C++ 底层二进制文件...")
write_fvecs('dblp_base.fvecs', base_data)
write_fvecs('dblp_query.fvecs', query_data)
write_fvecs('dblp_centroids.fvecs', kmeans.cluster_centers_)
write_ivecs('dblp_cluster_ids.ivecs', kmeans.labels_)
print("阶段二完成：底库、查询集、质心与倒排标签全量落盘！")
