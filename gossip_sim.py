#!/usr/bin/env python3
"""gossip_sim - Gossip protocol simulation."""
import sys,random
class Node:
    def __init__(s,nid):s.id=nid;s.data={};s.peers=[]
    def update(s,key,val,version=0):s.data[key]={"val":val,"ver":version}
    def gossip(s):
        if not s.peers:return 0
        target=random.choice(s.peers);changes=0
        for key,info in s.data.items():
            if key not in target.data or target.data[key]["ver"]<info["ver"]:
                target.data[key]=dict(info);changes+=1
        return changes
def simulate(n_nodes=10,rounds=20):
    nodes=[Node(i) for i in range(n_nodes)]
    for nd in nodes:nd.peers=[p for p in nodes if p.id!=nd.id]
    nodes[0].update("secret","hello",1)
    for r in range(rounds):
        total=0
        for nd in nodes:total+=nd.gossip()
        informed=sum(1 for nd in nodes if "secret" in nd.data)
        print(f"  Round {r}: {informed}/{n_nodes} nodes informed, {total} propagations")
        if informed==n_nodes:print(f"  Convergence at round {r}!");return r
    return rounds
if __name__=="__main__":
    n=int(sys.argv[1]) if len(sys.argv)>1 else 20
    simulate(n)
