import keras.models as ks
import method_rnn as rnn
import main_rnn as main


def get_bad_srcip(bad_index_list):

    bad_srcip_list, temp = [], []
    for index in bad_index_list:
        srcip = test_srcip[index]

        if temp.count(srcip) == 0:
            if test_srcip.count(srcip) >= 50:
                temp.append(srcip)
                bad_srcip_list.append(srcip)
        """ elif temp.count(srcip) != 0:
            print("exist before") """
        #have been counted, do nothing

    #print(bad_srcip_list)
    return bad_srcip_list

if __name__ == "__main__":
    test_path = "../pcap/DDos/DDos.csv"
    #test_path = "../pcap/Result.csv"
    #test_path = "../dataset/1_0-1_mix_time.csv"
    test_np, testlabel_np, testlabel_list = main.processed_data(test_path)

    model = ks.load_model('rnn_best.h5')

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])

    predictLabel = model.predict_classes(test_np)
    bad_index_list = rnn.detailAccuracyRNN(predictLabel, testlabel_list)
    #bad_srcip_list = get_bad_srcip(bad_index_list)
    #print(bad_srcip_list)
    #print(len(test_srcip), len(bad_index_list))


