import os
import sys
import datetime
from flask import Flask, render_template, request, json, send_from_directory
from knowledge_network.utility.service.gen_daemon import MyDaemon
from knowledge_network.webserver.controllers.user_controller import Login
from knowledge_network.webserver.controllers.neo4j_controller import Neo4JConnector
from knowledge_network.webserver.controllers import stable_neo4j_property as neo4jppt
import ast
import logging


app = Flask(__name__)


def start_server():
    """
    Start server at port 8080 with max processes 5
    """
    app.run(host='0.0.0.0', port='8080', processes=5)


def get_optional_param(param_key, request_):
    """
    Get optional param from get request
    :param param_key: key
    :param request_: current request
    :return: value
    """
    try:
        param_value = request_.args.get(param_key)
    except Exception as inst:
        logging.error(inst)
        param_value = None
    return param_value


def get_optional_form_data(param_key, request_):
    """
    Get optional data from POST form
    :param param_key: key
    :param request_: current request
    :return: value
    """
    try:
        param_value = request_.form[param_key]
    except Exception as inst:
        logging.error(inst)
        param_value = None
    return param_value


@app.route('/signUp')
def sign_up():
    """
    handler at route /signUp
    :return: html page for signUp
    """
    return render_template('/user/signUp.html')


@app.route('/signUpUser', methods=['POST'])
def sign_up_user():
    """
    handler for sign a user to db
    :return: status, user, pass
    """
    user = request.form['username']
    password = request.form['password']
    return json.dumps({'status': 'OK', 'user': user, 'pass': password})


@app.route('/login')
def login_handler():
    """
    handler at route /login
    :return: html page for login
    """
    return render_template('/user/login.html')


@app.route('/logInUser', methods=['POST'])
def log_in_user():
    """
    handler for checking user login
    :return: status, token
    """
    user = request.form['username']
    password = request.form['password']
    login = Login()
    login.validate(user, password)
    if login.status and (login.token is not None):
        return json.dumps({'status': True, 'token': login.default_token})
    else:
        return json.dumps({'status': False, 'token': ''})


@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    """
    handler for checking user login
    :return: status, token
    """
    user = request.form['username']
    password = request.form['token']
    login = Login()
    check = login.security_check(user, password)
    return check


@app.route('/graphEdit', methods=['GET'])
def graph_edit():
    """
    render graph edit page
    :return: graph editor page
    """
    return render_template('/graph/graph_editor.html')


@app.route('/get_all_nodes', methods=['GET'])
def get_all_nodes():
    """
    get all nodes
    :return: nodes and relations
    """
    label = get_optional_param('label', request)
    if label is not None:
        if len(label) == 0:
            label = None
    limit = get_optional_param('limit', request)
    if limit is not None:
        if len(limit) == 0:
            limit = None
    new_neo4j_connector = Neo4JConnector()
    nodes, relations = new_neo4j_connector.get_all_nodes_and_relations(label=label, limit=limit)
    output = {'nodes': nodes, 'relations': relations}
    return json.dumps(output)


@app.route('/searchNode', methods=['GET'])
def search_node():
    """
    search a node by key
    :return: list of nodes
    """
    keyword = request.args.get("keyword")
    node_label = get_optional_param("label", request)
    if node_label is not None:
        if len(node_label) == 0:
            node_label = None
    new_neo4j_connector = Neo4JConnector()
    nodes = new_neo4j_connector.search_node(keyword, _label=node_label)
    return json.dumps(nodes)


@app.route('/addNewNode', methods=['POST'])
def add_new_node():
    """
    add new node to db
    :return: True or False
    """
    node_id = request.form["id"]
    node_name = request.form["name"]
    node_label = request.form["label"]
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.add_new_node(_id=node_id, _name=node_name, _label=node_label)
    return json.dumps(output)


@app.route('/updateNode', methods=['POST'])
def update_node():
    """
    Update a node to db
    :return: True or False
    """
    node_id = request.form["id"]
    node_name = request.form["name"]
    node_label = request.form["label"]
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.update_node(_id=node_id, _name=node_name, _label=node_label)
    return json.dumps(output)


@app.route('/deleteNode', methods=['POST'])
def delete_node():
    """
    Remove a node from db
    :return: True or False
    """
    node_id = request.form["id"]
    node_label = get_optional_form_data("label", request)
    if node_label is not None:
        if len(node_label) == 0:
            node_label = None
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.delete_node(_id=node_id, _label=node_label)
    return json.dumps(output)


@app.route('/createRelation', methods=['POST'])
def create_relation():
    """
    Create a new relation for two nodes
    :return: True or False
    """
    from_id = request.form["from_id"]
    to_id = request.form["to_id"]
    rel_type = request.form["type"]
    rel_props = request.form["props"]
    from_label = get_optional_form_data("from_label", request)
    to_label = get_optional_form_data("to_label", request)
    if from_label is not None:
        if len(from_label) == 0:
            from_label = None
    if to_label is not None:
        if len(to_label) == 0:
            to_label = None
    if len(rel_props) == 0:
        rel_props = dict()
    else:
        rel_props = ast.literal_eval(rel_props)
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.create_relation(_from_id=from_id, _to_id=to_id, _rel_type=rel_type,
                                                 _rel_props=rel_props, _from_label=from_label, _to_label=to_label)
    return json.dumps(output)


@app.route('/updateRelation', methods=['POST'])
def update_relation():
    """
    Update relation between two nodes
    :return: True or False
    """
    from_id = request.form["from_id"]
    to_id = request.form["to_id"]
    rel_type = request.form["type"]
    rel_props = request.form["props"]
    from_label = get_optional_form_data("from_label", request)
    to_label = get_optional_form_data("to_label", request)
    new_type = get_optional_form_data("new_type", request)
    if from_label is not None:
        if len(from_label) == 0:
            from_label = None
    if to_label is not None:
        if len(to_label) == 0:
            to_label = None
    if new_type is not None:
        if len(new_type) == 0:
            new_type = None
    if len(rel_props) == 0:
        rel_props = dict()
    else:
        rel_props = ast.literal_eval(rel_props)
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.update_relation(_from_id=from_id, _to_id=to_id, _rel_type=rel_type,
                                                 _rel_props=rel_props, _from_label=from_label,
                                                 _to_label=to_label, _new_type=new_type)
    return json.dumps(output)


@app.route('/deleteRelation', methods=['POST'])
def delete_relation():
    """
    Delete a relation between two nodes
    :return: True or False
    """
    from_id = request.form["from_id"]
    to_id = request.form["to_id"]
    rel_type = request.form["type"]
    from_label = get_optional_form_data("from_label", request)
    to_label = get_optional_form_data("to_label", request)
    if from_label is not None:
        if len(from_label) == 0:
            from_label = None
    if to_label is not None:
        if len(to_label) == 0:
            to_label = None
    new_neo4j_connector = Neo4JConnector()
    output = new_neo4j_connector.delete_relation(_from_id=from_id, _to_id=to_id, _rel_type=rel_type,
                                                 _from_label=from_label, _to_label=to_label)
    return json.dumps(output)


@app.route('/getNodeRelations', methods=['GET'])
def get_node_relations():
    """
    Get all relations of a node
    :return: relations
    """
    node_id = request.args.get('node_id')
    node_label = get_optional_param("label", request)
    if node_label is not None:
        if len(node_label) == 0:
            node_label = None
    new_neo4j_connector = Neo4JConnector()
    relations, nodes = new_neo4j_connector.get_node_relations(_node_id=node_id, _label=node_label)
    output = {"nodes": nodes, "relations": relations}
    return json.dumps(output)


@app.route('/getNodeLabels', methods=['GET'])
def get_node_labels():
    output = neo4jppt.get_node_labels()
    return json.dumps(output)


@app.route('/getEdgeNames', methods=['GET'])
def get_edge_names():
    output = neo4jppt.get_edge_names()
    return json.dumps(output)


@app.route('/getEdgeProperties', methods=['GET'])
def get_edge_properties():
    edge_name, edge_data = neo4jppt.get_edge_properties()
    output = {"edge name": edge_name, "edge data": edge_data}
    return json.dumps(output)


if __name__ == "__main__":
    daemon = MyDaemon('/home/hact/daemon-knowledge-network-webservice.pid', start_server, None)
    if len(sys.argv) == 2:
        if 'start' == sys.argv[1]:
            daemon.start()
        elif 'stop' == sys.argv[1]:
            daemon.stop()
        elif 'restart' == sys.argv[1]:
            daemon.restart()
        elif 'start_one' == sys.argv[1]:
            start_server()
        else:
            print("Unknown command")
            sys.exit(2)
        sys.exit(0)
    else:
        start_server()
        print("usage: %s start|stop|restart|start_one" % sys.argv[0])
        # sys.exit(2)
