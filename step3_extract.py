import numpy as np
import struct

def read_fvecs(file_path):
    a = np.fromfile(file_path, dtype='int32')
    d = a[0]
    return a.reshape(-1, d + 1)[:, 1:].copy().view('float32')

def write_ivecs(file_path, data):
    with open(file_path, 'wb') as f:
        for row in data:
            f.write(struct.pack('i', len(row)))
            f.write(row.astype('uint32').tobytes())

print("加载数据中...")
base = read_fvecs('dblp_base.fvecs')
query = read_fvecs('dblp_query.fvecs')

# 暴力计算 L2 距离 (100 条查询 vs 10万条底库)
print("开始暴力搜索标准答案 (Ground Truth)...")
# 使用广播计算欧式距离矩阵: (100, 100000)
dists = np.sum((query[:, np.newaxis, :] - base[np.newaxis, :, :]) ** 2, axis=2)

# 取距离最小的前 100 个索引 (通常评测取 Top-100 比较稳健)
gt_indices = np.argsort(dists, axis=1)[:, :100]

write_ivecs('dblp_groundtruth.ivecs', gt_indices)
print("Ground Truth 已生成：dblp_groundtruth.ivecs")
