from knowledge_network.utility.dao.neo4j_db import NeoFJ


class NeoNode(object):
    def __init__(self, id_=None, name=None, label=None):
        """
        :param id_: node id
        :param name: node name
        :param label: node label
        """
        self.id_ = id_
        self.name = name
        self.label = label

    def get_name(self):
        """
        get node name
        :return: node name
        """
        return self.name

    def get_label(self):
        """
        get node label
        :return: label
        """
        return self.label

    def to_dict(self):
        data = {'id': self.id_, 'name': self.name, 'label': self.label}
        return data

    def fetch_node(self, address):
        """
        fetch node from neo4j db
        :param address: neo4j db address
        """
        if self.id_ is not None:
            new_neofj = NeoFJ(address=address)
            fetch_node = new_neofj.get_node(alias=self.id_, label=self.label)
            self.name = fetch_node.properties['name']
            self.label = []
            while len(fetch_node.labels) > 0:
                self.label.append(fetch_node.labels.pop())


class NeoRelation(object):
    def __init__(self, rel_type=None, from_id=None, to_id=None, rel_dict=None):
        """
        :param rel_type: (str) relation type
        :param from_id: (str) from node id
        :param to_id: (str) to node id
        :param rel_dict: (dict) relation data
        """
        self.rel_type = rel_type
        self.from_id = from_id
        self.to_id = to_id
        self.rel_dict = rel_dict

    def fetch_relation(self, address):
        """
        fetch data of relation from neo4j db
        :param address: neo4j db address
        """
        if (self.from_id is not None) and (self.to_id is not None):
            new_neofj = NeoFJ(address=address)
            relations = new_neofj.get_two_node_relations(_id1=self.from_id, _id2=self.to_id, _f_relation=self.rel_type)
            relation = relations[0]
            self.rel_type = relation.type
            self.rel_dict = relation.properties

    def to_dict(self):
        data = {'type': self.rel_type, 'from': self.from_id, 'to': self.to_id, 'dict': self.rel_dict}
        return data
