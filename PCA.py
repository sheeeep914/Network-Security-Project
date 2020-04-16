#PCA
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
pca = PCA(n_components=48).fit(packets)
print(pca.explained_variance_ratio_)

fig, ax = plt.subplots(1,2,figsize=(12,6))

ax[0].scatter(pca[:,0], pca[:,1],c=km)
ax[0].set_title("Predicted Training Labels")


plt.show()
