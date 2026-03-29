#!/usr/bin/env python3
"""Gossip protocol — epidemic broadcast simulator."""
import random, sys

class Node:
    def __init__(self, nid):
        self.id = nid
        self.data = set()
        self.infected = False
    def receive(self, msg):
        if msg not in self.data:
            self.data.add(msg)
            self.infected = True
            return True
        return False

def simulate(n=50, fanout=3, rounds=20):
    nodes = [Node(i) for i in range(n)]
    nodes[0].receive("secret")
    print(f"Gossip: {n} nodes, fanout={fanout}\n")
    for r in range(rounds):
        spreaders = [nd for nd in nodes if nd.infected]
        if not spreaders: break
        for nd in spreaders:
            targets = random.sample([x for x in nodes if x.id != nd.id], min(fanout, n-1))
            for t in targets:
                t.receive("secret")
            nd.infected = False
        informed = sum(1 for nd in nodes if nd.data)
        print(f"Round {r+1}: {informed}/{n} informed ({informed*100//n}%)")
        if informed == n:
            print(f"\nFull convergence in {r+1} rounds!")
            return
    informed = sum(1 for nd in nodes if nd.data)
    print(f"\nAfter {rounds} rounds: {informed}/{n} informed")

if __name__ == "__main__":
    simulate(int(sys.argv[1]) if len(sys.argv) > 1 else 50)
