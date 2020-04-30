from sklearn.decomposition import PCA
from sklearn.manifold import Isomap
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

dimension = 2

def pca(packets, clusters):
    pca = PCA(n_components=dimension)
    packets_pca = pca.fit_transform(packets)

    plt.scatter(packets_pca[:,0], packets_pca[:,1], s = 2, c = clusters, cmap = cm.hsv, alpha = 0.75)
    plt.title("PCA")
    plt.show()

def isomap(packets, clusters):
    isomap = Isomap(n_components=dimension)
    packets_isomap = isomap.fit_transform(packets)

    plt.scatter(packets_isomap[:,0], packets_isomap[:,1], s = 2, c = clusters, cmap = cm.hsv, alpha=0.75)
    plt.title("Isomap")
    plt.show()

def LDA(packets, clusters):
    lda = LinearDiscriminantAnalysis(n_components=dimension)
    packets_LDA = lda.fit(packets, clusters).transform(packets)
    print(packets_LDA.shape)

    plt.scatter(packets_LDA[:,0], packets_LDA[:,1], s = 2, c = clusters, cmap = cm.hsv, alpha=0.75)
    plt.title("LDA")
    plt.show()