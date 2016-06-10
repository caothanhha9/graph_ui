from knowledge_network.utility.dao.neo4j_db import NeoFJ
from py2neo import Node, Relationship
import logging


class DataTransfer(object):
    """
    Class for transferring data from one db to another db
    """
    def __init__(self, src_address, des_address):
        """
        Initialize self.address
        :param src_address: source db address
        host address + db location.
        Format: http://account:password@host:port/db/data/ (db/data is the db location)
        E.g. http://localhost:7474/db/data/
        :param des_address: target db address
        :return: void
        """
        self.src_address = src_address
        self.des_address = des_address
        self.id_name = 'alias'
        # self.src_graph = get_db_connection(src_address)
        # self.des_graph = get_db_connection(des_address)

    def clone_nodes_by_label(self, _label):
        """
        Copy all nodes of one label from source db to destination db
        :param _label:
        :return: count - number of successful cloning, miss - number of miss
        """
        src_connector = NeoFJ(self.src_address)
        src_nodes = src_connector.get_all_nodes_by_label(_label)
        des_connector = NeoFJ(self.des_address)
        count = 0
        miss = 0
        for node in src_nodes:
            success = des_connector.create_node(name=node.properties["name"],
                                                alias=node.properties["alias"], label=_label)
            if success:
                count += 1
            else:
                count += 1
        return count, miss

    def clone_relations_for_node(self, _node, _f_label=None):
        """
        Copy all relations of one node from source db to destination db
        :param _node: Node to clone relations
        :param _f_label: filter label
        :return: True or false
        """
        src_connector = NeoFJ(self.src_address)
        relations = src_connector.get_all_relations_of_one_node(_id=_node.properties["alias"],
                                                                _f_label=_f_label)
        des_connector = NeoFJ(self.des_address)
        all_success = True
        for relation_tup in relations:
            success = des_connector.create_relation(_id1=_node.properties["alias"],
                                                    _id2=relation_tup[0],
                                                    _rel_type=relation_tup[1].type,
                                                    _rel_props=relation_tup[1].properties)
            if not success:
                all_success = False
        return all_success

    def clone_relations_for_all_node_by_label(self, _label):
        """
        Copy all relations of all nodes from source db to destination db
        :param _label: label of nodes
        :return: count - number of successful cloning, miss - number of miss
        """
        src_connector = NeoFJ(self.src_address)
        src_nodes = src_connector.get_all_nodes_by_label(_label)
        count = 0
        miss = 0
        for node in src_nodes:
            success = self.clone_relations_for_node(node)
            if success:
                count += 1
            else:
                miss += 1
        return count, miss
