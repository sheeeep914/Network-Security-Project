from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

def pca(packets, number):
    pca = PCA(n_components=number)
    model = pca.fit(packets)
    X_pcs = model.transform(packets)
    #pca.fit_transform(packets)

    n_pcs = model.components_.shape[0]  # -> ç¸½å…±å¹¾ç¶­ == number
    #print(n_pcs)

    most_imp = [np.abs(model.components_[i]).argmax() for i in range(n_pcs)]
    initial_feature_names = packets.keys()

    print(most_imp)
    """ # get the names
    most_important_names = [initial_feature_names[most_imp[i]] for i in range(n_pcs)]

    # using LIST COMPREHENSION HERE AGAIN
    dic = {'PC{}'.format(i+1): most_important_names[i] for i in range(n_pcs)}

    # build the dataframe
    df = pd.DataFrame(sorted(dic.items()))
    print(df) """

    #print(type(initial_feature_names))
    """ # Dump components relations with features:
    column_index = []
    for i in range (number):
        column_index.append('PCA-' + str(i))

    test = pd.DataFrame(
        pca.components_, columns=packets.columns, index=column_index)
    print (test) """
