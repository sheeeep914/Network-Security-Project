#import iptc
import sys
import os
import keras.models as ks
import method_rnn as rnn
import main_rnn as main

""" 
chain = iptc.Chain(table, "INPUT")
print chain.name
print len(chain.rules)
#print table.name
"""

def fit_testdata(test_path):
    test_np, testlabel_np, testlabel_list, test_srcip = main.processed_data(test_path)

    model = ks.load_model('./model/1-1-1.h5')

    result = model.evaluate(test_np,  testlabel_np)
    print("testing accuracy = ", result[1])

    predictLabel = model.predict_classes(test_np)
    #print(predictLabel)
    bad_index_list = rnn.detailAccuracyRNN(predictLabel, testlabel_list)

    return bad_index_list, test_srcip

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
    """os.system("sudo iptables -F")

    print("\n")
    print("IPTABLE(before exe)")
    print("===========================")
    os.system("sudo iptables -nL --line-number")
"""
    test_path = "../dataset/1_1-2_mix_time.csv"
    bad_index_list, test_srcip = fit_testdata(test_path)
    """bad_srcip_list = get_bad_srcip(bad_index_list)
    
    
    for ip_item in bad_srcip_list:

        rule = iptc.Rule()
        rule.in_interface = "eth+"
        rule.src  = ip_item
        target = rule.create_target("DROP")

        chain = iptc.Chain(iptc.Table(iptc.Table.FILTER), "INPUT")
        chain.insert_rule(rule)

    print("===========================")
    print("\n")
    print("IPTABLE(after exe)")
    print("===========================")
    
    os.system("sudo iptables -nL --line-number")

    
    """
    """
    table = iptc.Table(iptc.Table.FILTER)
    for chain in table.chains:
        print("=============")
        print("Chain", chain.name)
        for rule in chain.rules:
            print("Rule", "proto: ", rule.protocol, "src: ", rule.src, "dst: ", rule.dst, "in: ", rule.in_interface, "out: ", rule.out_interface)
            print("Matches: ")
            for match in rule.matches:
                print (match.name)
            print ("Target: ",rule.target.name)

        print("=============")
    """

    

