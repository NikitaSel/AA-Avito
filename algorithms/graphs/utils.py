import os
import csv
import pickle
from typing import Optional
from collections import defaultdict, namedtuple


Edge = namedtuple('Edge', 'src dst distance')

Result = namedtuple('Result', 'least_number_of_jumps penultimate_link')

class BaseGraph:
    def __init__(self):
        self.neighbours = defaultdict(list)
        self.nodes = set()

    def add_edge(self, edge: Edge):
        self.neighbours[edge.src].append(edge)
        self.nodes.add(edge.src)
        self.nodes.add(edge.dst)

    def __getitem__(self, item):
        return self.neighbours.get(item, [])
 

def _load_pickle(path: str):
    py_object = None

    with open(path, 'rb') as f:
        py_object = pickle.load(f)

    return py_object


def _save_pickle(path: str, py_object):
    with open(path, 'wb') as f:
        pickle.dump(py_object, f)


def save_neighbours_and_nodes(csv_path: str,
                              src_col: str, dst_col: str, 
                              dist_col: Optional[str] = None,
                              save_to: str = './'):

    neighbours = defaultdict(list)
    nodes = set()

    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)

        header = next(reader)

        name2ind = {name: ind for ind, name in enumerate(header)}

        for row in reader:
            src, dst = row[name2ind[src_col]], row[name2ind[dst_col]]
            dist = row[name2ind[dist_col]] if dist_col is not None else 1

            neighbours[src].append(Edge(src, dst, dist))
            nodes.add(src)
            nodes.add(dst)

    path_neighbours = os.path.join(save_to, 'neighbours_dict')
    path_nodes =  os.path.join(save_to, 'nodes_dict')

    _save_pickle(path_neighbours, neighbours)
    _save_pickle(path_nodes, nodes)


def save_pages(csv_path: str, 
               id_col: str = 'page_id',
               title_col: str = 'page_title',
               save_to: str = './'):

    title2id = defaultdict(list)
    id2title = {}

    with open(csv_path, newline='') as csvfile:
        reader = csv.reader(csvfile, quoting=csv.QUOTE_ALL)

        header = next(reader)

        name2ind = {name: ind for ind, name in enumerate(header)}

        for row in reader:
            id, title = row[name2ind[id_col]], row[name2ind[title_col]]

            title2id[title].append(id)
            id2title[id] = title

    path_title_id = os.path.join(save_to, 'title_id_dict')
    path_id_title = os.path.join(save_to, 'id_title_dict')

    _save_pickle(path_title_id, title2id)
    _save_pickle(path_id_title, id2title)


def load_graph(path: str,
                neighbours_file_name, 
                nodes_file_name) -> tuple[dict, dict]:

    path_neighbours = os.path.join(path, neighbours_file_name)
    path_nodes =  os.path.join(path, nodes_file_name)

    neighbours = _load_pickle(path_neighbours)
    nodes = _load_pickle(path_nodes)

    return neighbours, nodes

def load_decoder_and_encoder(path: str) -> tuple[dict, dict]:
    path_title_to_ind = os.path.join(path, 'title_id_dict')
    path_ind_to_title = os.path.join(path, 'id_title_dict')

    decoder = _load_pickle(path_title_to_ind)
    encoder = _load_pickle(path_ind_to_title)

    return decoder, encoder
