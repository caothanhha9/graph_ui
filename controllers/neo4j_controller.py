from knowledge_network.config.config import DBAddress
from knowledge_network.search.search_neo4j import Search
from knowledge_network.utility.dao.neo4j_db import NeoFJ
from knowledge_network.webserver.models.neo4j_data import NeoNode, NeoRelation
from knowledge_network.webserver.controllers import stable_neo4j_property


class Neo4JConnector(object):
    def __init__(self):
        self.address = DBAddress.neo4j_address

    def convert_node(self, data_node):
        """
        Convert node from Node type to data model type
        :param data_node: object of node
        :return: NeoNode model
        """
        id_ = data_node.properties['alias']
        name = data_node.properties['name']
        label_set = data_node.labels
        labels = []
        while len(label_set) > 0:
            labels.append(label_set.pop())
        model_node = NeoNode(id_=id_, name=name, label=labels)
        return model_node

    def convert_relation(self, data_relation):
        """
        Convert relation_arr (relation, node, node2) to NeoRelation type
        :param data_relation: tuple of (relation, node, node2)
        :return: instance of NeoRelation
        """
        relation = data_relation[0]
        node = data_relation[1]
        node2 = data_relation[2]
        type_ = relation.type
        from_id = node.properties['alias']
        to_id = node2.properties['alias']
        model_relation = NeoRelation(rel_type=type_, from_id=from_id, to_id=to_id, rel_dict=relation.properties)
        return model_relation

    def convert_node_relation(self, current_node, node_relation):
        from_id = current_node
        to_id = node_relation[0]
        rel_type = node_relation[1].type
        rel_dict = node_relation[1].properties
        model_relation = NeoRelation(rel_type=rel_type, from_id=from_id, to_id=to_id, rel_dict=rel_dict)
        return model_relation

    def get_all_nodes_and_relations(self, label=None, limit=None):
        """
        :param label: label of nodes
        :param limit: limit number of nodes
        :return:
        """
        new_neofj = NeoFJ(address=self.address)
        nodes, relations = new_neofj.get_all_nodes_and_relations(_label=label, _limit=limit)
        nodes = list(set(nodes))
        node_data = [self.convert_node(node) for node in nodes]
        relation_data = [self.convert_relation(data_relation) for data_relation in relations]
        node_data = [node.to_dict() for node in node_data]
        relation_data = [relation.to_dict() for relation in relation_data]
        return node_data, relation_data

    def search_node(self, _keyword, _label=None):
        """
        search a node by its name (and label)
        :param _keyword: search key
        :param _label: label of node
        :return:
        """
        new_neofj = NeoFJ(address=self.address)
        nodes = new_neofj.search_node(_keyword=_keyword, label=_label)
        # new_neofj = Search()
        # nodes = new_neofj.search_product_name(_name= _keyword.encode('utf-8'))
        # order nodes .... TOBE
        model_nodes = [self.convert_node(node_) for node_ in nodes]
        model_nodes = [node.to_dict() for node in model_nodes]
        return model_nodes

    def add_new_node(self, _id, _name, _label):
        """
        add new node to db
        :param _id: (str) node id
        :param _name: (str) node name
        :param _label: (str) node label
        :return: True or False
        """
        is_valid = stable_neo4j_property.label_validate(_label)
        if is_valid:
            new_neofj = NeoFJ(address=self.address)
            result = new_neofj.create_node(name=_name, alias=_id, label=_label)
            return result
        else:
            return False

    def update_node(self, _id, _name, _label):
        """
        update a node
        :param _id: node id
        :param _name:  node name
        :param _label: node label
        :return: True or False
        """
        is_valid = stable_neo4j_property.label_validate(_label)
        if is_valid:
            new_neofj = NeoFJ(address=self.address)
            result = new_neofj.update_node(name=_name, alias=_id, label=_label)
            return result
        else:
            return False

    def delete_node(self, _id, _label=None):
        """
        update a node
        :param _id: node id
        :param _label: label of node
        :return: True or False
        """
        new_neofj = NeoFJ(address=self.address)
        result = new_neofj.delete_node(alias=_id, label=_label)
        return result

    def create_relation(self, _from_id, _to_id, _rel_type, _rel_props, _from_label=None, _to_label=None):
        """
        create a new relation
        :param _from_id: (str) from node id
        :param _to_id: (str) to node id
        :param _rel_type: (str) relation type
        :param _rel_props:(dict) relation properties
        :param _from_label: (str) label of from node
        :param _to_label: (str) label of to node
        :return: True or False
        """
        new_neofj = NeoFJ(address=self.address)
        return new_neofj.create_relation(_id1=_from_id, _id2=_to_id, _rel_type=_rel_type,
                                         _rel_props=_rel_props, _label1=_from_label, _label2=_to_label)

    def update_relation(self, _from_id, _to_id, _rel_type, _rel_props, _from_label=None,
                        _to_label=None, _new_type=None):
        """
        update a new relation
        :param _from_id: (str) from node id
        :param _to_id: (str) to node id
        :param _rel_type: (str) relation type
        :param _rel_props:(dict) relation properties
        :param _from_label: (str) label of from node
        :param _to_label: (str) label of to node
        :param _new_type: (str) new type of relation
        :return: True or False
        """
        new_neofj = NeoFJ(address=self.address)
        return new_neofj.update_relation(_id1=_from_id, _id2=_to_id, _rel_type=_rel_type,
                                         _rel_props=_rel_props, _label1=_from_label, _label2=_to_label,
                                         _new_type=_new_type)

    def delete_relation(self, _from_id, _to_id, _rel_type, _from_label=None, _to_label=None):
        """
        delete a new relation
        :param _from_id: (str) from node id
        :param _to_id: (str) to node id
        :param _rel_type: (str) relation type
        :param _from_label: (str) label of from node
        :param _to_label: (str) label of to node
        :return: True or False
        """
        new_neofj = NeoFJ(address=self.address)
        return new_neofj.delete_relation(_id1=_from_id, _id2=_to_id, _rel_type=_rel_type,
                                         _label1=_from_label, _label2=_to_label)

    def get_node_relations(self, _node_id, _label=None):
        """
        get all relations of a node
        :param _node_id: node id
        :param _label: label of node (for filtering)
        :return: direct related nodes and relations
        """
        new_neofj = NeoFJ(address=self.address)
        node_relations, nodes = new_neofj.get_all_relations_of_one_node(_id=_node_id, _label=_label)
        model_relations = [self.convert_node_relation(_node_id, node_relation_) for node_relation_ in node_relations]
        model_relations = [relation.to_dict() for relation in model_relations]
        model_nodes = [self.convert_node(node_) for node_ in nodes]
        model_nodes = [node_.to_dict() for node_ in model_nodes]
        return model_relations, model_nodes


def main():
    search = Neo4JConnector()
    node = search.search_node(_keyword='iphone', _label='Product')
    for el_ in node:
        print(el_)


if __name__ == '__main__':
    main()

