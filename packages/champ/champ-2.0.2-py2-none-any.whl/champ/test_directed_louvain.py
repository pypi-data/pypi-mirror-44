import igraph as ig
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
import champ



def main():
    pol_blogs = "/Users/whweir/Documents/UNC_SOM_docs/MATH890_networks_course/notebooks/data/polblogs/polblogs.gml"
    mygraph=ig.Graph.Read_GML(pol_blogs)
    # mygraph.to_undirected()
    print("num nodes",mygraph.vcount())
    print("num edges",mygraph.ecount())
    print('node attributes',mygraph.vs.attributes())
    print('edge attributes',mygraph.es.attributes())
    part_ens = champ.parallel_louvain(graph=mygraph, start=0, fin=2, numruns=10, numprocesses=1)
    print("Champ set= {:d}/{:d}".format(len(part_ens.ind2doms.keys()), part_ens.numparts))

    return 0

if __name__=='__main__':
    sys.exit(main())