import keras.models as ks
import method_dnn as dnn
import main_rnn as main

if __name__ == "__main__":
    test_path = "../dataset/1_0-1_mix_time.csv"
    test_np, testlabel_np, testlabel_list = main.processed_data(test_path)

    model = ks.load_model('dnn_best.h5')
