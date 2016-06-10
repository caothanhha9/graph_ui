# -*- coding: utf-8 -*-
from py2neo import authenticate, Graph, Path
from py2neo import Node, Relationship
import logging


class NeoFJ(object):
    """
    Class for accessing neo4j data from clients
    __init__ define address and get graph
    get_db_connection get graph object linked with address
    get_all_nodes_by_label get all nodes of one type
    get_two_node_relations get all relations of two nodes
    """
    def __init__(self, address):
        """
        Initialize self.address
        :param address: host address + db location.
        Format: http://account:password@host:port/db/data/ (db/data is the db location)
        E.g. http://localhost:7474/db/data/
        :return: void
        """
        self.address = address
        self.id_name = 'alias'
        self.graph = self.get_db_connection()

    def get_db_connection(self):
        """
        get graph object which links to the address
        :return: instance of Graph class
        """
        graph = Graph(self.address)
        return graph

    def create_node(self, name, alias, label):
        """
        Create a node with name, alias and label
        :param name: name of node
        :param alias: alias or id of node
        :param label: label of node
        :return: True or False
        """
        try:
            a_node = Node(label, name=name, alias=alias)
            self.graph.create(a_node)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def update_node(self, name, alias, label):
        """
        Update a node with name, alias and label
        :param name: name of node
        :param alias: alias or id of node
        :param label: label of node
        :return: True or False
        """
        try:
            update_sql = 'MATCH (n) WHERE n.alias = {alias} SET n: ' + label + ', n.name = {name}'
            self.graph.cypher.execute(update_sql, name=name, alias=alias)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def delete_node(self, alias, label=None):
        """
        delete a node by alias
        :param alias: alias of node, type: str
        :param label: label type, type: str
        :return: result of transaction (True or False)
        """
        try:
            if label is None:
                f_label_str = ""
            else:
                f_label_str = ":" + label
            delete_node_sql = "MATCH (n" + f_label_str + ") WHERE n." + self.id_name + " = {alias} \
            OPTIONAL MATCH (n)-[r]-() DELETE r,n"
            self.graph.cypher.execute(delete_node_sql, alias=alias)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def get_node(self, alias, label=None):
        """
        get one node by alias
        :param alias: alias of node, type: str
        :param label: label of node, type: str
        :return: node
        """
        if label is None:
            f_label_str = ''
        else:
            f_label_str = ':' + label
        find_node_sql = 'MATCH (n' + f_label_str + ') WHERE n.' + self.id_name + '={alias} return n AS node'
        result = self.graph.cypher.execute_one(find_node_sql, alias=alias)
        return result

    def search_node(self, _keyword, label=None):
        """
        search node by keyword
        :param _keyword: keyword to search
        :param label: label of node
        :return: list of nodes
        """
        name = '(?iu).*' + _keyword.encode('utf-8') + '.*'
        if label is None:
            f_label_str = ''
        else:
            f_label_str = ':' + label
        find_node_sql = 'MATCH (n' + f_label_str + ') WHERE n.name' + '=~{name} return n AS node'
        nodes = []
        for result in self.graph.cypher.execute(find_node_sql, name=name):
            nodes.append(result.node)
        return nodes

    def get_all_nodes_by_label(self, _label):
        """
        get all nodes of one label type
        :param _label: str - type of label
        :return: list of nodes
        """
        find_nodes_sql = 'MATCH (n:' + _label + ') RETURN DISTINCT n AS node'
        nodes = []
        for result in self.graph.cypher.execute(find_nodes_sql):
            nodes.append(result.node)
        return nodes

    def create_relation(self, _id1, _id2, _rel_type, _rel_props, _label1=None, _label2=None):
        """
        Create relations for two nodes
        :param _id1: (str) id or alias of node 1
        :param _id2: (str)  id or alias of node 2
        :param _rel_type: (str) relation type
        :param _rel_props: (dict) key, val of relation
        :param _label1: (str) label of node 1
        :param _label2: (str) label of node 2
        :return: True or False
        """
        try:
            if _label1 is None:
                f_label_str1 = ''
            else:
                f_label_str1 = ':' + _label1
            if _label2 is None:
                f_label_str2 = ''
            else:
                f_label_str2 = ':' + _label2
            create_relation_sql = 'MATCH (a' + f_label_str1 + '),(b' + f_label_str2 + ') \
            WHERE a.' + self.id_name + ' =~ {a_alias}  AND b.' + self.id_name + ' =~ {b_alias} \
            CREATE (a)-[r:' + _rel_type + ' ' + '{rel_props}' + ']->(b) '
            self.graph.cypher.execute(create_relation_sql, a_alias='(?iu)' + _id1,
                                      b_alias='(?iu)' + _id2, rel_props=_rel_props)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def delete_relation(self, _id1, _id2, _rel_type=None, _label1=None, _label2=None):
        """
        delete one or all relations between two nodes
        :param _id1: (str) id of node 1
        :param _id2: (str) id of node 2
        :param _rel_type: (str) relation type
        :param _label1: (str) label of node 1
        :param _label2: (str) label of node 2
        :return: True or False
        """
        if _label1 is None:
            f_label_str1 = ''
        else:
            f_label_str1 = ':' + _label1
        if _label2 is None:
            f_label_str2 = ''
        else:
            f_label_str2 = ':' + _label2
        if _rel_type is None:
            f_rel_type_str = ''
        else:
            f_rel_type_str = ':' + _rel_type
        try:
            delete_relation_sql = 'MATCH (a' + f_label_str1 + ')-[r' + f_rel_type_str + ']->(b' + f_label_str2 + ') \
            WHERE a.' + self.id_name + ' =~ {a_alias}  AND b.' + self.id_name + ' =~ {b_alias} \
            DELETE r'
            self.graph.cypher.execute(delete_relation_sql, a_alias='(?iu)' + _id1, b_alias='(?iu)' + _id2)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def update_relation(self, _id1, _id2, _rel_type, _rel_props, _label1=None, _label2=None, _new_type=None):
        if _label1 is None:
            f_label_str1 = ''
        else:
            f_label_str1 = ':' + _label1
        if _label2 is None:
            f_label_str2 = ''
        else:
            f_label_str2 = ':' + _label2
        update_prop_arr = []
        for key, val in _rel_props.iteritems():
            update_prop_arr.append('r.' + str(key) + '=' + str(val))
        if len(update_prop_arr) > 0:
            set_props_str = ' SET ' + ','.join(update_prop_arr)
        else:
            set_props_str = ''

        try:
            if _new_type is None:
                update_relation_sql = 'MATCH (a' + f_label_str1 + ')-[r:' + _rel_type + ']->(b' + f_label_str2 + ') \
                WHERE a.' + self.id_name + ' =~ {a_alias}  AND b.' + self.id_name + ' =~ {b_alias} \
                ' + set_props_str
            else:
                update_relation_sql = 'MATCH (a' + f_label_str1 + ')-[r:' + _rel_type + ']->(b' + f_label_str2 + ') \
                WHERE a.' + self.id_name + ' =~ {a_alias}  AND b.' + self.id_name + ' =~ {b_alias} \
                CREATE (a)-[r2:' + _new_type + ']->(b) \
                SET r2 = r' + set_props_str + ' \
                WITH r DELETE r'
            self.graph.cypher.execute(update_relation_sql, a_alias='(?iu)' + _id1,
                                      b_alias='(?iu)' + _id2)
            return True
        except Exception as inst:
            logging.error(inst)
            return False

    def get_two_node_relations(self, _id1, _label1=None, _id2=None, _label2=None, _f_relation=None):
        """
        get all relations of two specific nodes
        :param _id1: id of label 1, type: str
        :param _label1: label type of label 1, type: str
        :param _id2:  id of label 2, type: str
        :param _label2: label type of label 2, type: str
        :param _f_relation: relation type, type: str
        :return: list of relations
        """

        if _label1 is None:
            f_label_str1 = ''
        else:
            f_label_str1 = ':' + _label1
        if _label2 is None:
            f_label_str2 = ''
        else:
            f_label_str2 = ':' + _label2
        if _f_relation is None:
            f_relation_str = ''
        else:
            f_relation_str = ':' + _f_relation
        find_relationship_sql = 'MATCH (a' + f_label_str1 + ')-[r' + f_relation_str + ']->(b' + f_label_str2 + ') \
        WHERE a.' + self.id_name + ' =~ {a_alias}  AND b.' + self.id_name + ' =~ {b_alias} \
        RETURN DISTINCT r AS relation'
        relations = []
        for result in self.graph.cypher.execute(find_relationship_sql, a_alias='(?iu)' + _id1, b_alias='(?iu)' + _id2):
            relations.append(result.relation)
        return relations

    def get_all_relations_of_one_node(self, _id, _label=None, _f_label=None, _f_relation=None):
        """
        get all relations linked to one node
        :param _id: id of target node, type: str
        :param _label: label of target node, type: str
        :param _f_label: label of related nodes, type: str
        :param _f_relation: type of relation, type: str
        :return: list of tuples (relation, id)
        """
        if _label is None:
            label_str = ''
        else:
            label_str = ':' + _label
        if _f_label is None:
            f_label_str = ''
        else:
            f_label_str = ':' + _f_label
        if _f_relation is None:
            f_relation_str = ''
        else:
            f_relation_str = ':' + _f_relation
        find_relationship_sql = 'MATCH (a' + label_str + ')-[r' + f_relation_str + ']->(b' + f_label_str + ') \
        WHERE a.' + self.id_name + ' =~ {a_alias} \
        RETURN b.' + self.id_name + ' AS b_alias, r AS relation, b as b_node'

        relations_ids = []
        nodes = []
        for result in self.graph.cypher.execute(find_relationship_sql, a_alias='(?iu)' + _id):
            relations_ids.append((result.b_alias, result.relation))
            nodes.append(result.b_node)
        return relations_ids, nodes

    def get_all_nodes_and_relations(self, _label=None, _limit=None):
        """
        get all nodes and relations
        :param _label: str - type of label
        :param _limit: str - limit number of nodes
        :return: list of nodes
        """
        if _label is None:
            label_str = ''
        else:
            label_str = ':' + _label
        if _limit is None:
            limit_str = ''
        else:
            limit_str = ' LIMIT ' + _limit
        find_nodes_sql = 'MATCH (n' + label_str + ')-[r]->(m' + label_str + ') RETURN DISTINCT n AS node, \
                          r as relation, m as node2' + limit_str
        print(find_nodes_sql)
        nodes = []
        relations = []
        for result in self.graph.cypher.execute(find_nodes_sql):
            nodes.append(result.node)
            nodes.append(result.node2)
            relations.append((result.relation, result.node, result.node2))
        return nodes, relations

    def get_all_nodes_by_name(self, _label):
        """
        get all nodes of one label type
        :param _label: str - type of label
        :return: list of nodes
        """
        find_nodes_sql = 'MATCH (n:' + _label + ') RETURN DISTINCT n AS node'
        nodes = []
        for result in self.graph.cypher.execute(find_nodes_sql):
            nodes.append(result.node)
        return nodes
