class DBAddress(object):
    neo4j_address_local = 'http://neo4j:iloveyou@localhost:7474/db/data/'
    neo4j_address_dev = 'http://neo4j:iloveyou@192.168.23.34:7348/db/data/'
    neo4j_address_cloud = 'http://productnetwork:zQ7T1dF9BUjrdB3npP18@productnetwork.sb05.stations.graphenedb.com:24789/db/data/'
    neo4j_address = neo4j_address_cloud


class GlobalFilePath(object):
    data_root_path = '/home/hact/workspace/python/knowledge_network/data'
    model_root_path = '/home/hact/workspace/python/knowledge_network/models'


class Neo4JFilePath(object):
    node_label = GlobalFilePath.data_root_path + "/db/neo4j/NodeLabelList"
    edge_name = GlobalFilePath.data_root_path + "/db/neo4j/EdgeNameList"


class ProRecFilePath(object):
    module_path = '/parsers/product_recognize'
    train_sim_address = GlobalFilePath.data_root_path + module_path + '/train/train_data_sim'
    train_anti_address = GlobalFilePath.data_root_path + module_path + '/train/train_data_anti'
    train_root_address = {'sim': train_sim_address, 'anti': train_anti_address}
    vocabulary_root_path = GlobalFilePath.model_root_path + module_path + '/vocabulary/vocabulary'
    checkpoint_root_path = GlobalFilePath.model_root_path + module_path + '/runs'
