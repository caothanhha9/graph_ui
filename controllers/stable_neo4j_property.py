import bisect
from knowledge_network.config.config import Neo4JFilePath

edge_properties = ["value", "rating"]
edge_properties_data = dict(rating=["0.5", "0.75", "1.0"])


def label_validate(_label):
    node_labels = get_node_labels()
    f_id = bisect.bisect_left(node_labels, _label)
    if node_labels[f_id] == _label:
        return True
    else:
        return False


def get_node_labels(file_path=Neo4JFilePath.node_label):
    return [str.strip(s) for s in open(file_path).readlines()]


def get_edge_names(file_path=Neo4JFilePath.edge_name):
    return [str.strip(s) for s in open(file_path).readlines()]


def get_edge_properties():
    return edge_properties, edge_properties_data
