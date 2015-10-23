# import nltk
import re
import networkx as nx
from collections import Counter
def create_diction_of_actors(path):
    pers_l={}
    fifi=open(path)
    u=0
    while True:
        u+=1
        i=fifi.readline()
        if i=='':
            break
        else:
            i=i.strip()
        # ii=i.split()
        ii=re.split(r'[A-Z]+', i)
        print ii,len(ii)
        if len(ii)>0 and len(ii) <= 2 and i[-1]=='.':
            if i[:-1] not in pers_l:
                pers_l[i[:-1]]=[u]
            else:
                pers_l[i[:-1]].append(u)
    return pers_l

def create_dict_of_acts(path):
    fifi = open(path)
    # fifi = open('/home/sergios-len/Dropbox/Python Projects (1)/LiteratureNetworks/corpora/HamletShakespeare.txt')
    persons = False
    acting=False
    pers_l=[]
    pers_dict={}
    act_dict={}
    scen_dict={}
    lact=[]
    lscen=[]
    checked=set()
    u=0
    while True:
        u+=1
        i=fifi.readline()
        if i=='':
            break
        else:
            i=i.strip()

        # print i ,u,i.strip()
        # if u>410:
        #     break
        if i.strip()=='PERSONS REPRESENTED.':
            # print persons
            persons =True
            continue
        if i == 'SCENE. Elsinore.':

            acting=True
            continue
        if persons and acting :
            # print i,'hehe'
            spers_l=set(pers_l)
            # print i,'hehe',spers_l,checked
            # break
            if i[:3].lower()=='Act'.lower():
                ikl=i.split()[1][:-1]
                # print i,ikl
                if ikl not in act_dict:
                    act_dict[ikl]=u

                    if len(lact)==0:
                        pact=[ikl]
                        lact.append(u)
                    else:
                        pu=lact[-1]
                        ppu=pact[-1]
                        act_dict[ppu]=(pu,u-1)
                        pact.append(ikl)
                        lact.append(u)
                    
            if i[:5].lower()=='Scene'.lower():
                ikls=i.split()[1][:-1]
                # print i,u
                # print ikl+' '+ikls,pact[-1]+' '+ ikls
                if pact[-1]+'.'+ ikls in scen_dict:
                    scen_dict[pact[-1]+'.'+ ikls]=u
                if len(lscen)==0:
                    pscen=[pact[-1]+'.'+ ikls]
                    lscen.append(u)
                else:
                    puu=lscen[-1]
                    ppuu=pscen[-1]
                    scen_dict[ppuu]=(puu,u-1)
                    pscen.append(pact[-1]+'.'+ ikls)
                    lscen.append(u)
                # print i
                # act_dict[ikl][i.split()[1][:-1]]=u
                # lact.append(u)

            if len(i)>=4 :#and len(i)<=8:
                if i[0]!='[' :#and i[-1]=='.':
                    # print i,'aaaaaaaaaaaaaaaaaaaaaaa'
                    # if i not in pers_dict:
                        # print i
                    if i in pers_l:
                        j=fifi.readline().strip()
                        u+=1
                        while j !='':
                            # j=j.strip()
                            if i not in pers_dict:
                        # for j in set(pers_l) - checked:
                            # print j,i,i[:-1]
                            # if j.find(i[:-1])==0 and j not in checked:
                                pers_dict[i]={u:j}
                                checked.add(j)
                            else:
                                pers_dict[i][u]=j
                            j=fifi.readline().strip()
                            u+=1
                   
        elif persons and len(i)>1 and not acting:
            # print i.split(', ')[0]
            pers_l.append(i.split(', ')[0])
            # spers_l=

        else:
            continue

    fifi.close()

    return act_dict,u,pers_l,pers_dict,pact,lact,scen_dict,lscen,pscen
    # act_dict,u,pers_l,pers_dict,pact,lact
# print act_dict
# print pact
# print lact
# print u
# print aaa
def create_per_nod_dict(pers_dict):
    pernode_dict={}
    nodper_dic={}
    for i,v in enumerate(pers_dict.keys()):
        pernode_dict[v]=i
        nodper_dic[i]=v
    return pernode_dict,nodper_dic
def create_graph_dict(act_dict,pers_l,pers_dict,u):
    ract_dic={}
    graph_dic={}
    pernode_dict,nodper_dic=create_per_nod_dict(pers_dict)
    # lact=sorted(lact)
    # print lact
    for k,v in act_dict.items():
        try:
            vv=int(v)
            va=(v,u)
        except:
            va=v
        ract_dic[va]=k
        G=nx.Graph()
        graph_dic[k]=G

    # print ract_dic
    # print graph_dic
    # print aaaa
    sractd=sorted(ract_dic.keys())
    # print sractd

    # G=nx.Graph()
    for k,v in pers_dict.items():
        for kk ,vv in v.items():
            for tok in re.split(r'\W+', vv):
                if tok in pers_dict:
                    # print sractd
                    for act_interv in sractd:
                        # print kk,act_interv
                        if act_interv[0]<=kk and kk<act_interv[1]:
                            G=graph_dic[ract_dic[act_interv]]
                            # print type(G)
                            ed=pernode_dict[k]
                            de=pernode_dict[tok]
                            if G.has_edge(ed,de):
                                wei=G[ed][de]['weight']
                            else:
                                wei=0
                else:
                    for act_interv in sractd:
                        # print kk,act_interv
                        if act_interv[0]<=kk and kk<act_interv[1]:
                            aasscen[ract_dic[act_interv]].add(k)
    for k,g in graph_dic.items():
        for nd in g.nodes():
            if len(attribute_dict)>1:
                label_na=nodper_dic[nd]
                attributt=attribute_dict[label_na]
                numattr=actors_words_dic[label_na]
                g.add_node(nd,label=label_na,count_of_speech_characters=numattr,gender=attributt[0],social_status=attributt[1],alliance=attributt[2],drive=attributt[3])
            else:
                g.add_node(nd,label=nodper_dic[nd])
        g.name='Act %s' %k    
        graph_dic[k]=g


    return graph_dic,ract_dic,pernode_dict,nodper_dic,sractd,aasscen
# def relabel_graph_nodes(graph_dic,ract_dic):
#     ngraph_dic={}
#     for kk

# act_dict,u,pers_l,pers_dict,pact,lact=create_dict_of_acts('/home/sergios-len/Dropbox/Python Projects (1)/LiteratureNetworks/corpora/HamletShakespeare.txt')

# graph_dic,ract_dic=create_graph_dict(act_dict,pers_l,pers_dict)
# for k,v in graph_dic.items():
    # print k,nx.info(v)
def create_two_mode_act_scene_graph(actors_dict):
    G=nx.Graph()
    for k,v in actors_dict.items():
        for actor in v:
            G.add_edge(k,actor)
    return G