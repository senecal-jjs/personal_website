title: The Influence of a Randomized SVD on the Subspace K-Means Algorithm
date: 2018-11-06
link: svd 

The k-means algorithm is a straight-forward and popular clustering technique. Vanilla k-means initializes some number of cluster centroids by randomly choosing points from our dataset of interest. Then, using a version of expectation-maximization, cluster centroids are updated iteratively until convergence. The process consists of assigning datapoints to the closest current centroid, then we recompute the new centroids of the clusters based on these assignments. 

It can be difficult to determine what structure k-means is finding and exploiting. Mautz et al. \citep{mautz2017towards} recently proposed *subspace k-means*, which simultaneously clusters the data and finds an optimal subspace for clustering. Subspace k-means makes the assumption that the features of a given dataset can be partitioned into a cluster subspace and a noise subspace. The features belonging to the cluster subspace are informative to the final clustering result, while the features belonging to the noise subspace are not.  

As subspace k-means progresses, a transformation matrix, \\( V \\), is repeatedly calculated. \\( V \\) rotates and reflects the original space so that the cluster space and noise space comprise the first \\( m \\) features and the last \\( d-m \\) features in the transformed space, respectively (where \\( d \\) is the dimensionality of the dataset and \\( m \\) is the dimensionality of the cluster space). The original algorithm's transformation matrix is determined through an eigenvalue decomposition that uses a Krylov subspace method in ARPACK with \\( O(d^3) \\) complexity \citep{golub2012matrix}; consequently, as the dimensionality of a dataset grows, calculating the transformation matrix represents a major bottleneck in terms of computational complexity and runtime. 

To create a trade-off between the cluster and noise subspaces, subspace k-means minimizes a modified k-means objective,

\\[
    \mathcal{J} = \bigg[\sum\_{i=1}^k \sum\_{x \in C_i} ||P_C^T V^T \mathbf{x} - P_C^T V^T \mathbf{\mu}_i||^2 \bigg] + \sum\_{\mathbf{x \in \mathcal{D}}} ||P_N^T V^T \mathbf{x} - P_N^T \mathbf{\mu}\_{\mathcal{D}}||^2
\\]

where \\( P\_C = \begin{bmatrix}\mathbf{I}\_m & \mathbf{0}\_{d-m,m} \end{bmatrix}^T \\) is the cluster space projection matrix, \\( P\_N = \begin{bmatrix} \mathbf{0}\_{m, d-m} & \mathbf{I}\_{d-m} \end{bmatrix}^T \\) is the noise space projection matrix, \\( V \\) is the transformation matrix, \\( \mathcal{D} \\) is the dataset, \\( C\_i \\) is cluster \\( i \\), \\( \mathbf{\mu}\_i \\) is the mean of cluster \\( i \\), and \\( \mathbf{\mu}\_\mathcal{D} \\) is the dataset mean. Informative features are better represented by the first term, while uninformative features are better represented by the second term. Following the derivation in \citep{mautz2017towards}, the objective function can be rewritten as,

\\[
\begin{split}
    \mathcal{J} & = \text{Tr} \bigg( P\_C P\_C^T V^T \underbrace{\bigg( \bigg[ \sum\_{i=1}^k S\_i \bigg] - S\_\mathcal{D} \bigg)}\_{=: \Sigma} V \bigg) + \underbrace{\text{Tr} (V^T S\_\mathcal{D} V)}\_{\text{const. w.r.t } V}
\end{split}
\\]

where \\( S\_i \\) is the scatter matrix for cluster \\( i \\), and \\(S\_\mathcal{D} \\) is the dataset scatter matrix. 

In the above cost function \\( P_C P_C^T \\) leaves the upper \\(m \times m\\) portion of the matrix unchanged and sets all other values to zero. Then, we minimize the cost function for a fixed cluster partition, fixed \\(\mathbf{\mu}\_i\\), and fixed cluster space dimensionality \\(m\\), by using the eigenvectors of \\(\Sigma\\) as columns in the transformation matrix \\(V\\), such that the eigenvectors are sorted in ascending order according to the corresponding eigenvalues, such that the \\(m\\) eigenvectors corresponding to the \\(m\\) smallest eigenvalues project the data onto the cluster subspace. 