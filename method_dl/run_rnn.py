import keras.models as ks
import method_rnn as rnn
import main_rnn as main

if __name__ == "__main__":
    test_path = "../dataset/1_10-18_mix_time.csv"
    test_np, testlabel_np, testlabel_list = main.processed_data(test_path)

    model = ks.load_model('rnn_best.h5')

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])

    predictLabel = model.predict_classes(test_np)
    rnn.detailAccuracyRNN(predictLabel, testlabel_list)


