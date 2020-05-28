import iptc

""" 
chain = iptc.Chain(table, "INPUT")
print chain.name
print len(chain.rules)
#print table.name
 """

def test():
    print("hellooooooooo!")

""" if __name__ == "__main__":
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

    
 """
