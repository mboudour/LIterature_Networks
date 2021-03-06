import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import random
import math
import numpy

# import community as community

def create_conn_random_graph(nodes,p):
    while  True:
        # G=nx.connected_watts_strogatz_graph(25, 2, 0.8, tries=100)
        G=nx.erdos_renyi_graph(nodes,p)
        if nx.is_connected(G):
            break
    G.remove_nodes_from(nx.isolates(G))
    sstt="Erdos-Renyi Random Graph with %i nodes and probability %.02f" %(nodes,p)
    return G, sstt


def draw_network(G,sstt,pos={},with_edgewidth=False,withLabels=True,pernode_dict={},labfs=10,valpha=0.4,ealpha=0.4):


# GI = graph_dic[ract_dic[cnum[3]]]
# print "The number of actors in Macbeth's Act IV is", len(GI.nodes())
# print "The number of conversational relationships in Macbeth's Act IV is", len(GI.edges())

    G.remove_nodes_from(nx.isolates(G))
    # if with_weights:
    #     weights={(i[0],i[1]):i[2]['weight'] for i in G.edges(data=True) }#if all((i[0],i[1])) in G.nodes() }
    plt.figure(figsize=(12,12))
    # try:
    #     f=open('positions_of_Mc_Shake.dmp')
    #     pos_dict=pickle.load(f)
    #     pos =pos_dict[3]
    # except:
        
    #     pos=nx.spring_layout(G,scale=50)
    #     pos_dict[3]=pos
    if len(pos)==0:
        pos=nx.spring_layout(G,scale=50)


# pos=nx.spring_layout(G,scale=50)
# pos_dict[3]=pos
    # if:
    #     labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
    # else:
    #     labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
    if with_edgewidth:
        edgewidth=[]
        for (u,v,d) in G.edges(data=True):
            edgewidth.append(d['weight'])
    else:
        edgewidth=[1 for i in G.edges()]
    nx.draw_networkx_nodes(G,pos=pos,with_labels=False,alpha=0.4)
    if withLabels:
        if len(pernode_dict)>0:
            labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
            labe=nx.draw_networkx_labels(G,pos=pos,labels=labels,font_size=20)
        else:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_edges(G,pos=pos,edge_color='b',width=edgewidth, alpha=0.5)#,edge_labels=weights,label_pos=0.2)


    # pos=nx.spring_layout(G,scale=50)
    # plt.figure(figsize=(12,12))
    # nx.draw_networkx_nodes(G,pos=pos,with_labels=withLabels,alpha=valpha)
    # if withLabels:
    #     labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    # # nx.draw_networkx_edges(G,pos=pos,edge_color='b',alpha=ealpha)
    plt.title(sstt,fontsize=20)
    kk=plt.axis('off')
    return pos


def draw_centralities(G,centr,pos,with_edgewidth=False,withLabels=True,pernode_dict={},title_st='', labfs=10,valpha=0.4,ealpha=0.4):

    plt.figure(figsize=(12,12))
    if centr=='degree_centrality':
        cent=nx.degree_centrality(G)
        sstt='Degree Centralities'
        ssttt='degree centrality'
    elif centr=='closeness_centrality':
        cent=nx.closeness_centrality(G)
        sstt='Closeness Centralities'
        ssttt='closeness centrality'
    elif centr=='betweenness_centrality':
        cent=nx.betweenness_centrality(G)
        sstt='Betweenness Centralities'
        ssttt='betweenness centrality'
    elif centr=='eigenvector_centrality':
        cent=nx.eigenvector_centrality(G,max_iter=1000)
        sstt='Eigenvector Centralities'
        ssttt='eigenvector centrality'
    elif centr=='katz_centrality':
        phi = (1+math.sqrt(5))/2.0 # largest eigenvalue of adj matrix
        cent=nx.katz_centrality_numpy(G,1/phi-0.01)
        sstt='Katz Centralities'
        ssttt='Katz centrality'
    elif centr=='page_rank':
        cent=nx.pagerank(G)
        sstt='PageRank'
        ssttt='pagerank'
    cs={}
    nods_dici={v:k for k,v in pernode_dict.items()}
    for k,v in cent.items():
        if v not in cs:
            cs[v]=[k]
        else:
            cs[v].append(k)
    for k in sorted(cs,reverse=True):
        for v in cs[k]:
            print 'Node %s has %s = %.4f' %(nods_dici[v],ssttt,k)

    if withLabels:
        if len(pernode_dict)>1:
            labels={i:v for v,i in pernode_dict.items() if i in G.nodes()}
            labe=nx.draw_networkx_labels(G,pos=pos,labels=labels,font_size=20)
        else:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
    nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(), #with_labels=withLabels,
                           node_size = [d*4000 for d in cent.values()],node_color=cent.values(),
                           cmap=plt.cm.Reds,alpha=valpha)
    if with_edgewidth:
        edgewidth=[]
        for (u,v,d) in G.edges(data=True):
            edgewidth.append(d['weight'])
    else:
        edgewidth=[1 for i in G.edges()]
    nx.draw_networkx_edges(G,pos=pos,edge_color='b',width=edgewidth, alpha=ealpha)
    plt.title(title_st+' '+ sstt,fontsize=20)
    kk=plt.axis('off')



def draw_centralities_subplots(G,pos,withLabels=True,labfs=10,valpha=0.4,ealpha=0.4):
    centList=['degree_centrality','closeness_centrality','betweenness_centrality',
    'eigenvector_centrality','katz_centrality','page_rank']
    cenLen=len(centList)
    plt.figure(figsize=(12,12))
    for uu,centr in enumerate(centList):
        if centr=='degree_centrality':
            cent=nx.degree_centrality(G)
            sstt='Degree Centralities'
            ssttt='degree centrality'
        elif centr=='closeness_centrality':
            cent=nx.closeness_centrality(G)
            sstt='Closeness Centralities'
            ssttt='closeness centrality'
        elif centr=='betweenness_centrality':
            cent=nx.betweenness_centrality(G)
            sstt='Betweenness Centralities'
            ssttt='betweenness centrality'
        elif centr=='eigenvector_centrality':
            cent=nx.eigenvector_centrality(G,max_iter=1000)
            sstt='Eigenvector Centralities'
            ssttt='eigenvector centrality'
        elif centr=='katz_centrality':
            phi = (1+math.sqrt(5))/2.0 # largest eigenvalue of adj matrix
            cent=nx.katz_centrality_numpy(G,1/phi-0.01)
            sstt='Katz Centralities'
            ssttt='Katz centrality'
        elif centr=='page_rank':
            cent=nx.pagerank(G)
            sstt='PageRank'
            ssttt='pagerank'
        cs={}
        for k,v in cent.items():
            if v not in cs:
                cs[v]=[k]
            else:
                cs[v].append(k)
        nodrank=[]
        uui=0
        for k in sorted(cs,reverse=True):
            for v in cs[k]:

                if uui<5:
                    nodrank.append(v)
                    uui+=1

        #         print 'Node %s has %s = %.4f' %(v,ssttt,k)
        nodeclo=[]
        for k,v in cent.items():
            if k in  nodrank :
                nodeclo.append(v)
            else:
                nodeclo.append(0.)
        plt.subplot(1+cenLen/2.,2,uu+1).set_title(sstt)
        if withLabels:
            labe=nx.draw_networkx_labels(G,pos=pos,font_size=labfs)
        
        # print uu,sstt
        nx.draw_networkx_nodes(G,pos=pos,nodelist=cent.keys(), #with_labels=withLabels,
                               # node_size = [d*4000 for d in cent.values()],
                               node_color=nodeclo,
                               cmap=plt.cm.Reds,alpha=valpha)
        
        nx.draw_networkx_edges(G,pos=pos,edge_color='b', alpha=ealpha)
        plt.title(sstt,fontsize=20)
        kk=plt.axis('off')