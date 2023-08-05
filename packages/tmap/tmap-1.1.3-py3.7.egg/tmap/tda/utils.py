from __future__ import print_function

import csv
import os
import pickle
import json

import networkx as nx
import numpy as np
import pandas as pd
import scipy.stats as scs
from sklearn.neighbors import *
from sklearn.preprocessing import MinMaxScaler
from pandas.api.types import is_categorical_dtype,is_numeric_dtype
from tmap.tda import mapper
from tmap.tda.cover import Cover


def optimize_dbscan_eps(data, threshold=90, dm=None):
    if dm is not None:
        tmp = dm.where(dm != 0, np.inf)
        eps = np.percentile(np.min(tmp, axis=0), threshold)
        return eps
    # using metric='minkowski', p=2 (that is, a euclidean metric)
    tree = KDTree(data, leaf_size=30, metric='minkowski', p=2)
    # the first nearest neighbor is itself, set k=2 to get the second returned
    dist, ind = tree.query(data, k=2)
    # to have a percentage of the 'threshold' of points to have their nearest-neighbor covered
    eps = np.percentile(dist[:, 1], threshold)
    return eps


def optimal_r(X, projected_X, clusterer, mid, overlap, step=1):
    def get_y(r):
        tm = mapper.Mapper(verbose=0)
        cover = Cover(projected_data=MinMaxScaler().fit_transform(projected_X), resolution=r, overlap=overlap)
        graph = tm.map(data=X, cover=cover, clusterer=clusterer)
        if "adj_matrix" not in graph.keys():
            return np.inf
        return abs(scs.skew(graph["adj_matrix"].count()))

    mid_y = get_y(mid)
    mid_y_r = get_y(mid + 1)
    mid_y_l = get_y(mid - 1)
    while 1:
        min_r = sorted(zip([mid_y_l, mid_y, mid_y_r], [mid - 1, mid, mid + 1]))[0][1]
        if min_r == mid - step:
            mid -= step
            mid_y, mid_y_r = mid_y_l, mid_y
            mid_y_l = get_y(mid)
        elif min_r == mid + step:
            mid += step
            mid_y, mid_y_l = mid_y_r, mid_y
            mid_y_r = get_y(mid)
        else:
            break
    print("suitable resolution is ", mid)
    return mid

def unify_data(data):
    if 'iloc' in dir(data):
        # pd.DataFrame
        return data
    elif type(data) == list:
        # list
        return pd.DataFrame(data)
    elif isinstance(data,np.ndarray):
        return pd.DataFrame(data)
    elif type(data) == dict:
        return pd.DataFrame.from_dict(data,orient='index')
    else:
        print('Unkown data type')
        return

def transform2node_data(graph, data):
    nodes = graph.nodes.data()
    data = unify_data(data)
    if data is not None:
        node_data = {nid: data.iloc[attr['samples'], :].mean() for nid, attr in nodes.items()}
        node_data = pd.DataFrame.from_dict(node_data, orient='index', columns=data.columns)
        return node_data

def transform2sample_data(graph,data):
    nodes = graph.nodes.data()
    data = unify_data(data)
    datas = []
    if data is not None:
        for nid, attr in nodes.items():
            cache = [data.loc[nid,:]]* len(attr['samples'])
            cache = pd.concat(cache)
            cache.index = attr['samples']
            datas.append(cache)
        sample_data = pd.concat(data)
        # todo: average the same index id row. result is larger than the number of origin sample
        return sample_data

def prepare_metadata(graph,meta_data):
    if meta_data.shape[0] != len(graph['sample_names']) and meta_data.shape[1] == len(graph['sample_names']):
        print('It may be a transposited matrix. it should be samples X OTU/features. So we will transposited it for you.')
        meta_data = meta_data.T

    all_cat = np.array([is_categorical_dtype(meta_data.loc[:,col]) for col in meta_data])
    if any(all_cat):
        meta_data = meta_data.loc[:, ~all_cat]

    return meta_data

def node2samples(node2s, safe_dict):
    """
    get corresponding samples (samples in enriched nodes) at safe_dict.
    there are overlapped samples between nodes, and should be deduplicated.
    :param dict node2s: relationship between nodes and samples, as graph["nodes"]
    :param dict safe_dict: enrichment or decline SAFE score dict from SAFE_batch.
    :return: most contents are the same as safe_dict except for most inner ids are sample ids instead of node ids.
    """
    return {feature: list(set([sample_id for node_id in node_ids
                               for sample_id in safe_dict[node_id]]))
            for feature, node_ids in node2s.items()}


def get_pos(graph, strength):
    node_keys = graph["node_keys"]
    node_positions = graph["node_positions"]
    G = nx.Graph()
    G.add_nodes_from(graph['nodes'].keys())
    G.add_edges_from(graph['edges'])
    pos = {}
    for i, k in enumerate(node_keys):
        pos.update({int(k): node_positions[i, :2]})
    pos = nx.spring_layout(G, pos=pos, k=strength)
    return pos


## Access inner attribute

def cover_ratio(graph, data):
    nodes = graph['nodes']
    all_samples_in_nodes = [_ for vals in nodes.values() for _ in vals]
    n_all_sampels = data.shape[0]
    n_in_nodes = len(set(all_samples_in_nodes))
    return n_in_nodes / float(n_all_sampels) * 100


## Export data as file

def safe_scores_IO(arg, output_path=None, mode='w'):
    if mode == 'w':
        if not isinstance(arg, pd.DataFrame):
            safe_scores = pd.DataFrame.from_dict(arg, orient='index')
            safe_scores = safe_scores.T
        else:
            safe_scores = arg
        safe_scores.to_csv(output_path, index=True)
    elif mode == 'rd':
        safe_scores = pd.read_csv(arg, index_col=0)
        safe_scores = safe_scores.to_dict()
        return safe_scores
    elif mode == 'r':
        safe_scores = pd.read_csv(arg, index_col=0)
        safe_scores = safe_scores.to_dict('index')
        return safe_scores


def read_graph(path,method='pickle'):
    if method == 'pickle':
        graph = pickle.load(open(path, 'rb'))
    elif method == 'json':
        # currently it will raise error because json can't dump ndarry directly.
        json.load(path)
    else:
        print('Wrong method provided, currently acceptable method are [pickle|json].')
        return ''
    return graph


def dump_graph(graph, path,method='pickle'):
    # method must one of 'pickle' or 'json'.
    if method == 'pickle':
        pickle.dump(graph, open(path, "wb"))
    elif method =='json':
        # currently it will raise error because json can't dump ndarry directly.
        json.dump(graph,open(path,'w'))
    else:
        print('Wrong method provided, currently acceptable method are [pickle|json].')


def output_graph(graph, filepath, sep='\t'):
    """
    Export graph as a file with sep. The output file should be used with `Cytoscape <http://cytoscape.org/>`_ .

    It should be noticed that it will overwrite the file you provided.

    :param dict graph: Graph output from tda.mapper.map
    :param str filepath:
    :param str sep:
    """
    edges = graph['edges']
    with open(os.path.realpath(filepath), 'w') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=sep)
        spamwriter.writerow(['Source', 'Target'])
        for source, target in edges:
            spamwriter.writerow([source, target])
#
# def output_Node_data(graph,filepath,data,features = None,sep='\t',target_by='sample'):
#     """
#     Export Node data with provided filepath. The output file should be used with `Cytoscape <http://cytoscape.org/>`_ .
#
#     It should be noticed that it will overwrite the file you provided.
#
#     :param dict graph:
#     :param str filepath:
#     :param np.ndarray/pandas.Dataframe data: with shape [n_samples,n_features] or [n_nodes,n_features]
#     :param list features: It could be None and it will use count number as feature names.
#     :param str sep:
#     :param str target_by: target type of "sample" or "node"
#     """
#     if target_by not in ['sample','node']:
#         exit("target_by should is one of ['sample','node']")
#     nodes = graph['nodes']
#     node_keys = graph['node_keys']
#     if 'columns' in dir(data) and features is None:
#         features = list(data.columns)
#     elif 'columns' not in dir(data) and features is None:
#         features = list(range(data.shape[1]))
#     else:
#         features = list(features)
#
#     if type(data) != np.ndarray:
#         data = np.array(data)
#
#     if target_by == 'sample':
#         data = np.array([np.mean(data[nodes[_]],axis=0) for _ in node_keys])
#     else:
#         pass
#
#     with open(os.path.realpath(filepath),'w') as csvfile:
#         spamwriter = csv.writer(csvfile, delimiter=sep)
#         spamwriter.writerow(['NodeID'] + features)
#         for idx,v in enumerate(node_keys):
#             spamwriter.writerow([str(v)] + [str(_) for _ in data[idx,:]])
