Ubuntu 22.04
1.clone the RaBitQlib and the datasets
git clone https://github.com/VectorDB-NTU/RaBitQ-Library.git
git clone https://github.com/XUKAI020/dblp_RaBitQ-projection.git
2.download the tools for py and multithreading of C++
sudo apt update && sudo apt install build-essential libomp-dev python3-pip -y    
3.download the tool for math
pip3 install numpy scikit-learn
4.move the .fvecs files and .ivecs files into the RaBitQlib
5.create the build file
mkdir -p build
6.compile the index and test tools
g++ -O3 -march=native -fopenmp -Iinclude sample/ivf_rabitq_indexing.cpp -o build/rabitq_ivf_build
g++ -O3 -march=native -fopenmp -Iinclude sample/ivf_rabitq_querying.cpp -o build/rabitq_ivf_query
7.build index
./build/rabitq_ivf_build dblp_base.fvecs dblp_centroids.fvecs dblp_cluster_ids.ivecs 8 dblp_index.bin l2 true
8.performance search
./build/rabitq_ivf_query dblp_index.bin dblp_query.fvecs dblp_groundtruth.ivecs true

Attention:the command should run in the RaBitQ-Library file
