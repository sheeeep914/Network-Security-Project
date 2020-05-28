import iptc
import keras.models as ks
import method_dnn as dnn
import main_dnn as main

""" 
chain = iptc.Chain(table, "INPUT")
print chain.name
print len(chain.rules)
#print table.name
"""

def fit_testdata(test_path):
    test_np, testlabel_np, testlabel_list, test_srcip, test_dstip = main.processed_data(test_path)

    model = ks.load_model('dnn_best.h5')

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])

    return model

def get_bad_srcip(model):
    predictLabel = model.predict_classes(test_np)
    #print(predictLabel)
    bad_index_list = dnn.detailAccuracyDNN(predictLabel, testlabel_list)

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

    test_path = "../dataset/1_0-1_mix_time.csv"
    model = fit_testdata(test_path)
    bad_srcip_list = get_bad_srcip(model)
    
    

    rule = iptc.Rule()
    rule.in_interface = "eth+"
    rule.src  = "127.0.0.1/255.0.0.0"
    target = rule.create_target("DROP")

    chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
    chain.insert_rule(rule)
   

    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        print("=============")
        print("Chain", chain.name)
        for rule in chain.rules:
            print("Rule", "proto: ", rule.protocol, "src: ", rule.src, "dst: ", rule.dst, "in: ", rule.in_interface, "out: ", rule.out_interface)
            print"Matches: ",
            for match in rule.matches:
                print match.name,
            print "Target: ",
            print rule.target.name

        print("=============")

    

