// TODO: display and handle editing nodes and edges


//------------------------------------------------------------------
// TODO: Define global variables
//------------------------------------------------------------------
var service_address = "http://192.168.30.155:8080"
//------------------------------------------------------------------

var colorHelper = new ColorHelper();
var keyGen = new KeyGen();
var templateHelper = new TemplateHelper();
var dataConverter = new DataConverter();
// Build nodes and edges
var id_size = 32;
// create an array with nodes
var relation_color_dict = {"ACCOMPANY": "#01DF3A", "REPLACE": "#2E64FE", "ATTACK": "#FF0040", "HAS_ATTRIBUTE": "#F7D358"}
var node_data, edge_data;
var data;
var network;
var current_node_id = null;
var current_edge_id = null;
//var current_object = null;
var current_nodes = null;
var current_edges = null;
var edge_show = true;
var virtual_node_id = "_virtual";
var virtual_edge_id = "_virtual";
var new_relation_name = "UNDEFINED";
var hidden_node_ids = new Array();
var hidden_edge_ids = new Array();
var last_hover_node_id = null;

var edge_properties_name = new Array(); //["Diameter of gun", "Color", "Rating", "Shape", "Size", "Weight", "Mate", "Taste", "Dead Or Alive"];
var edge_properties_data = new Array(); //['continuous', 'continuous', 'discrete', 'continuous', 'continuous', 'continuous', 'continuous', 'continuous', 'continuous', 'continuous'];
//var discrete = [1,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5,2,3,4,5]
var node_label_list = new Array();
var edge_name_list = new Array();

//------------------------------------------------------------------
// TODO: load and display data at the beginning
//------------------------------------------------------------------
function load_default_data() {
    // TODO: fetch nodes and relations data from server. Display network and setup event when callback
    var url = service_address + '/get_all_nodes'
    var label = 'Product'
    var limit = 1
//    url += '?label=' + label + '&limit=' + limit
    url += '?limit=' + limit
    $.ajax({
			url: url,
			type: 'GET',
			success: function(response){
				var jsonResponseData = JSON.parse(response);
				node_data = dataConverter.convert_node_data(jsonResponseData["nodes"]);
				edge_data = dataConverter.convert_relation_data(jsonResponseData["relations"]);
				render_graph();
				setup_event();
			},
			error: function(error){
				console.log(error);
			}
    });

    $.ajax({
            url: '/getNodeLabels',
            type: 'GET',
            success: function(response){
                node_label_list = JSON.parse(response);
                $("#node-label").autocomplete({
                      source: node_label_list
                });

            },
            error: function(error) {
                console.log(error);
            }
    });

    $.ajax({
            url: '/getEdgeNames',
            type: 'GET',
            success: function(response){
                edge_name_list = JSON.parse(response);
                for (i=0; i < edge_name_list.length; i++) {
                        var name_edge = edge_name_list[i];
                        $("#lb-properties").append('<li role="presentation" id="name' + i + '" onclick="choose('+ i + ')">'+ name_edge +'</li>')
                }
            },
            error: function(error){
                console.log(error);
            }
    });

    $.ajax({
            url: '/getEdgeProperties',
            type: 'GET',
            success: function(response){
                var jsonResponseData = JSON.parse(response);
                edge_properties_name = jsonResponseData["edge name"];
                if (jsonResponseData["edge data"] != null) {
                    edge_properties_data = jsonResponseData["edge data"];
                }
                var html = templateHelper.build_edge_properties(edge_properties_data);
                $("#dd-properties").html(html);
//                for (i=0; i < edge_properties_name.length; i++) {
//                    var name_property = edge_properties_name[i];
//                    var s = "";
//                    if (edge_properties_data[name_property] == null) {
//                        s += '<input type="text" value="" placeholder="Value..." class="form-control"> </div> </li>';
//                    }
//                    else {
//                        var discrete = edge_properties_data[name_property];
//                        s += ' <select class="form-control" style="width:200px;"> ';
//                        discrete.forEach(function(e) {
//                            s += ' <option>'+ e +'</option> ';
//                        })
//                        s += '</select> </li>';
//                    }
//                    $("#dd-properties").append('<li role="presentation"> <div class="form-inline"> <button id="btn'+ i +'" type="button" class="btn btn-default" aria-label="Left Align" style="width: 150px" onclick="check('+i+',\''+ name_property +'\')"> <span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> '+ name_property + '</button>' + s);
//                }
            },
            error: function(error){
                console.log(error);
            }
    });
}

function check(i, name_) {
    var check = $('#btn'+ i + ' span').hasClass('glyphicon-check');
    if (check == true) {
//        $('#btn'+ i).html('<span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> ' + name_);
        $('#btn' + i).find('.glyphicon').removeClass('glyphicon-check').addClass('glyphicon-unchecked');
    }
    else {
        $('#btn' + i).find('.glyphicon').removeClass('glyphicon-unchecked').addClass('glyphicon-check');
//        $('#btn'+ i).html('<span class="glyphicon glyphicon-check" aria-hidden="true"></span> ' + name_);
    }
}

function choose(i) {
    var choose = $('#name' + i).text();
    $('#edge-name').html(choose);
    $('#edge-name').dropdown('toggle');
}

//------------------------------------------------------------------
// TODO: editor and network interconnected handlers
//------------------------------------------------------------------
function update_node_editor(current_node_data) {
    // TODO: update data for node editor table (when a node is selected)
    $("#node-id").html(current_node_data["id"]);
    $("#node-name").val(current_node_data["label"])
    $("#node-label").val(current_node_data["group"])
}
function update_edge_editor(current_edge_data, from_node, to_node) {
    // TODO: update data for edge editor table (when a edge is selected)
    $("#edge-id").html(current_edge_data["id"]);
    $("#edge-id").attr("data-id", current_edge_data["id"]);
    $("#edge-from").html(from_node["label"]);
    $("#edge-from").attr("data-from", current_edge_data["from"]);
    $("#edge-to").html(to_node["label"]);
    $("#edge-to").attr("data-to", current_edge_data["to"]);
    $("#edge-name").html(current_edge_data["label"]);
//    $("#edge-dict").val(current_edge_data["title"]);
    var props_dict = JSON.parse(current_edge_data["title"]);
    $("#edge-dict").find("li").each(function(id, el) {
            var key = $(el).find(".prop-name").html();
            var value = props_dict[key];
            if (value != null) {
                $(el).find(".glyphicon").removeClass("glyphicon-unchecked").addClass("glyphicon-check");
                $(el).find(".edge-value").val(value);
//                var is_select = $(el).find(".edge-value").is("select");
//                if (is_select) {
//                    value = $(el).find(".edge-value").val(value);
//                }
//                else {
//                    value = $(el).find(".edge-value").val(value);
//                }
            }
            else {
                $(el).find(".glyphicon").removeClass("glyphicon-check").addClass("glyphicon-unchecked");
            }
    });
    var title_ = JSON.stringify(props_dict);
}

function add_new_edges(edge_data) {
    // TODO: add new edges to network if not exist
    for (i=0; i < edge_data.length; i++) {
        var new_edge_data = edge_data[i]
        var exist = false;
        data.edges.forEach(function (t, e) {
            if (((new_edge_data["from"]) == t["from"]) & (new_edge_data["to"] == t["to"]) &
                new_edge_data["type"] == t["label"]) {
                t["hidden"] = false;
                data.edges.update(t);
                exist = true;
            }
        });
        if (!exist) {
            data.edges.add(dataConverter.convert_relation(new_edge_data));
        }
        else {
            network.redraw();
        }
    }
}

function find_all_edges_of_node(node_id) {
    // TODO: add new edges to network if not exist
    var current_node_edges = new Array();
    data.edges.forEach(function (t, e) {
        if ((node_id == t["from"]) | (node_id == t["to"])) {
            current_node_edges.push(t);
        }
    });
    return current_node_edges;
}

function add_new_nodes(node_data) {
    // TODO: add new nodes to network if not exist
    model_nodes = dataConverter.convert_node_data(node_data);
    for (i=0; i < model_nodes.length; i++) {
        if (data.nodes.get(model_nodes[i]["id"]) == null) {
            data.nodes.add(model_nodes[i]);
        }
        else {
            var exist_node = data.nodes.get(model_nodes[i]["id"]);
            exist_node.hidden = false;
            data.nodes.update(exist_node);
//            network.redraw();
            // do nothing
        }
    }
}
//------------------------------------------------------------------
// TODO: keypress event handlers
//------------------------------------------------------------------
function key_delete_handler(event) {
    // TODO: call server for deleting a node or edge. When server notice success remove it from network
    if (confirm('Are you sure you want to delete?')) {
            // Save it!
           if (current_node_id != null) {
                if (current_node_id != virtual_node_id) {
                    var group_ = data.nodes.get(current_node_id)["group"]
                    $.ajax({
                        url: service_address + '/deleteNode',
                        data: {"id": current_node_id, "label": group_},
                        type: 'POST',
                        success: function(response){
                            if (JSON.parse(response)) {
                                data.nodes.remove(current_node_id);
                            } else {
                                alert("Failed to delete node");
                            }
                        },
                        error: function(error){
                            console.log(error);
                        }
                    });
                }
                else {
                    data.nodes.remove(current_node_id);
                }
           } else {
                if (current_edge_id != null) {
                    var current_edge_obj = data.edges.get(current_edge_id);
                    var type_ = current_edge_obj["label"];
                    var from_id_ = current_edge_obj["from"];
                    var to_id_ = current_edge_obj["to"];
                    var from_label_ = data.nodes.get(from_id_)["group"];
                    var to_label_ = data.nodes.get(to_id_)["group"];
                    $.ajax({
                        url: service_address + '/deleteRelation',
                        data: {"from_id": from_id_, "to_id": to_id_, "type": type_, "from_label": from_label_,
                               "to_label": to_label_},
                        type: 'POST',
                        success: function(response){
                            if (JSON.parse(response)) {
                                data.edges.remove(current_edge_id);
                            } else {
                                alert("Failed to delete edge");
                            }
                        },
                        error: function(error){
                            console.log(error);
                        }
                    });
                }
           }
        } else {
            // Do nothing!
        }
}

function key_r_handler(event) {
    // TODO: call server to get all relations from selected node. Receive relation data and call display edges function
    if (current_node_id != null) {
        if (current_node_id != virtual_node_id) {
            var group_ = data.nodes.get(current_node_id)["group"]
            var url = service_address + '/getNodeRelations' + '?node_id=' + current_node_id + '&label=' + group_;
            $.ajax({
                url: url,
                type: 'GET',
                success: function(response){
                    // Display edge
                    var responseJSON = JSON.parse(response);
//                    add_new_nodes(responseJSON["nodes"]);
                    add_new_edges(responseJSON["relations"]);
//                    add_new_edges(JSON.parse(response));
                },
                error: function(error){
                    console.log(error);
                }
            });
        }
    }
}

function key_shift_r_handler(event) {
    // TODO: call server to get all relations from selected node. Receive relation data and call display edges function
    if (current_node_id != null) {
        if (current_node_id != virtual_node_id) {
            var group_ = data.nodes.get(current_node_id)["group"]
            var url = service_address + '/getNodeRelations' + '?node_id=' + current_node_id + '&label=' + group_;
            $.ajax({
                url: url,
                type: 'GET',
                success: function(response){
                    // Display edge
                    var responseJSON = JSON.parse(response);
                    add_new_nodes(responseJSON["nodes"]);
                    add_new_edges(responseJSON["relations"]);
//                    add_new_edges(JSON.parse(response));
                },
                error: function(error){
                    console.log(error);
                }
            });
        }
    }
}

function key_h_handler(event) {
    // TODO: hide a node or an edge
    if (current_node_id != null) {
        if (current_node_id != virtual_node_id) {
            var current_node = data.nodes.get(current_node_id);
            if (current_node != null) {
                current_node.hidden = true;
                data.nodes.update(current_node);
                hidden_node_ids.push(current_node_id);
            }
        }
    }
    else if (current_edge_id != null) {
        if (current_edge_id != virtual_edge_id) {
            var current_edge = data.edges.get(current_edge_id);
            if (current_edge != null) {
                current_edge.hidden = true;
                data.edges.update(current_edge);
                hidden_edge_ids.push(current_edge_id);
            }
        }
    }
}

function key_shift_h_handler(event) {
    // TODO: remove a node from network
    if (current_node_id != null) {
        if (current_node_id != virtual_node_id) {
            data.nodes.remove(current_node_id);
        }
    }
}

function key_e_handler(event) {
    // TODO: hide/show all edges of a node
    edge_show = !edge_show;
    if (current_node_id != null) {
        if (current_node_id != virtual_node_id) {
            var current_node = data.nodes.get(current_node_id);
            if (current_node != null) {
//                current_node.hidden = true;
//                data.nodes.update(current_node);
//                hidden_node_ids.push(current_node_id);
                var current_node_edges = find_all_edges_of_node(current_node_id);
                for (i=0; i<current_node_edges.length; i++) {
                    var edge_ = current_node_edges[i];
                    edge_.hidden = edge_show;
                    data.edges.update(edge_);
                    hidden_edge_ids.push(edge_["id"]);
                }

            }
        }
    }
}

function key_f_handler(event) {
    network.redraw();
}

function key_s_handler(event) {
    // TODO: show all hidden nodes
    for (i=0; i<hidden_node_ids.length; i++) {
        var node_id = hidden_node_ids[i];
        var node_ = data.nodes.get(node_id);
        if (node_ != null) {
            node_.hidden = false;
            data.nodes.update(node_);
        }
    }
    hidden_node_ids = new Array();
}

function key_shift_s_handler(event) {
    // TODO: show all hidden relations
    key_s_handler(event);
    for (i=0; i<hidden_edge_ids.length; i++) {
        var edge_id = hidden_edge_ids[i];
        var edge_ = data.edges.get(edge_id);
        if (edge_ != null) {
            edge_.hidden = false;
            data.edges.update(edge_);
        }
    }
    hidden_edge_ids = new Array();
}

function keypress_handler(event) {
    // TODO handle keypress event
//    var code = event.keyCode || event.which;
//    var code = event.keyCode || event.charCode;
    var code = event.which || event.keyCode || event.charCode;
    console.log(code);
    if (code == 68 & event.shiftKey) {
        key_delete_handler(event);
    }
    else if (code == 114) {
        key_r_handler(event);
    }
    else if (code == 104) {
        key_h_handler(event);
    }
    else if (code == 115) {
        key_s_handler(event);
    }
    else if (code == 83 & event.shiftKey) {
        key_shift_s_handler(event);
    }
    else if (code == 72 & event.shiftKey) {
        key_shift_h_handler(event);
    }
    else if (code == 82 & event.shiftKey) {
        key_shift_r_handler(event);
    }
    else if (code == 101) {
        key_e_handler(event);
    }
    else if (code == 102) {
        key_f_handler(event);
    }

}
function keydown_handler(event) {
//    console.log(event.keyCode);
}
//------------------------------------------------------------------
// TODO: node and edge editing handler
//------------------------------------------------------------------
function searchNode() {
    // TODO: call server to get a list of related nodes. Build html and display the result
    var search_key = document.getElementById('search').value;
    var url = service_address + '/searchNode' + '?keyword=' + search_key;
    $.ajax({
			url: url,
			type: 'GET',
			success: function(response){
				var fetch_nodes = JSON.parse(response);
				var html = templateHelper.build_suggestions(fetch_nodes);
                document.getElementById('search-suggestions').innerHTML = html;
                showSuggestions();
			},
			error: function(error){
				console.log(error);
			}
    });

}

function showSuggestions() {
    // TODO: show the searched result list
    document.getElementById('search-suggestions').removeAttribute("hidden");
}

function hideSuggestions() {
    // TODO: hide the searched result list
    document.getElementById('search-suggestions').setAttribute("hidden", "hidden");
}
function addNode() {
    // TODO: send request to server for adding a node to db. Display new node to network
    try {
        if (confirm('Are you sure you want to add new node?')) {
            var node_name = document.getElementById('node-name').value;
            if (node_name.length > 0) {
                var node_id_ = keyGen.gen_id(id_size, node_name);
                var label_ = document.getElementById('node-name').value;
                var group_ = document.getElementById('node-label').value;

                $.ajax({
                    url: service_address + '/addNewNode',
                    data: {"id": node_id_, "name": label_, "label": group_},
                    type: 'POST',
                    success: function(response){
                        console.log(response);
                        if (JSON.parse(response)) {
                            data.nodes.add({
                                id: node_id_,
                                label: label_,
                                group: group_
                            });
                        } else {
                            alert("Failed to add node");
                        }

                    },
                    error: function(error){
                        console.log(error);
                    }
                });
            }

        } else {
            // Do nothing;
        }
    }
    catch (err) {
        alert(err);
    }
}

function updateNode() {
    // TODO: send request to server for updating a node to db. Update node to network
    try {
        if (document.getElementById('node-id').innerHTML.length > 0){
            var node_id_ = document.getElementById('node-id').innerHTML;
            var label_ = document.getElementById('node-name').value;
            var group_ = document.getElementById('node-label').value;
            $.ajax({
                url: service_address + '/updateNode',
                data: {"id": node_id_, "name": label_, "label": group_},
                type: 'POST',
                success: function(response){
                    if (JSON.parse(response)) {
                        data.nodes.update({
                            id: node_id_,
                            label: label_,
                            group: group_
                        });
                    } else {
                        alert("Failed to update node");
                    }
                },
                error: function(error){
                    console.log(error);
                }
            });

        }
    }
    catch (err) {
        alert(err);
    }
}

function updateEdge() {
    // TODO: send request to server for updating an edge to db. Update edge to network
    try {
        var edge_id_ = document.getElementById('edge-id').innerHTML;
        var origin_rel_type_ = data.edges.get(edge_id_)["label"];
        var from_id_ = document.getElementById('edge-from').getAttribute("data-from");
        var to_id_ = document.getElementById('edge-to').getAttribute("data-to");
        var label_ = document.getElementById('edge-name').innerHTML;
//        var title_ = document.getElementById('edge-dict').value;
        var from_label = data.nodes.get(from_id_)["group"];
        var to_label = data.nodes.get(to_id_)["group"];
        var props_dict = {};
        var new_type_ = "";
        $("#edge-dict").find("li").each(function(id, el) {
            var is_check = $(el).find(".glyphicon").hasClass("glyphicon-check");
            if (is_check) {
                var key = $(el).find(".prop-name").html();
                var is_select = $(el).find(".edge-value").is("select");
                var value;
                if (is_select) {
                    value = $(el).find(".edge-value option:selected").text();
                }
                else {
                    value = $(el).find(".edge-value").val();
                }
                props_dict[key] = value;
            }
        });
        var title_ = JSON.stringify(props_dict);

        if (label_ != origin_rel_type_) {
            new_type_ = label_
        }
        if (relation_color_dict[label_] == null) {
            relation_color_dict[label_] = colorHelper.getRandomColor();
        }
        var color_ = relation_color_dict[label_]
        $.ajax({
            url: service_address + '/updateRelation',
            data: {"from_id": from_id_, "to_id": to_id_, "type": origin_rel_type_,
                   "props": title_, "from_label": from_label, "to_label": to_label, "new_type": new_type_},
            type: 'POST',
            success: function(response){
                if (JSON.parse(response)) {
                    data.edges.update({
                        id: edge_id_,
                        from: from_id_,
                        to: to_id_,
                        label: label_,
                        title: title_,
                        color: color_
                    });
                } else {
                    alert("Failed to create relation");
                }
            },
            error: function(error){
                console.log(error);
            }
        });
    }
    catch (err) {
        alert(err);
    }
}
//------------------------------------------------------------------
// TODO: network render
//------------------------------------------------------------------
function render_graph() {
    // TODO: create nodes and edges from nodes data and edges data. Define options and create network.
    var nodes = new vis.DataSet(node_data)
    var edges = new vis.DataSet(edge_data)
    current_nodes = nodes;
    current_edges = edges;

    // create a network
    var container = document.getElementById('mynetwork');

    // provide the data in the vis format
    data = {
        nodes: nodes,
        edges: edges
    };
    var options = {
        nodes: {
            shape: 'dot',
            size: 30,
            font: {
                size: 32,
                color: '#ffffff'
            },
            borderWidth: 2,
        },
        edges: {
            width: 1,
            length:500,
            arrows: {
              to:     {enabled: false, scaleFactor:1},
              middle: {enabled: true, scaleFactor:1},
              from:   {enabled: false, scaleFactor:1}
            }
        }
    };

    // initialize your network!
    network = new vis.Network(container, data, options);

}
//------------------------------------------------------------------
// TODO: mouse event handlers for network
//------------------------------------------------------------------
function setup_event() {
    // TODO: setup event handler for network
    network.on("click", function (params) {
//        console.log(params);
//        params.event = "[original event]";
    });
    network.on("dragStart", function (params) {
//        params.event = "[original event]";
//        console.log(params);
    });
    network.on("select", function (params) {
//        console.log('select Event:', params);
        if (params.nodes.length > 0) {
            current_node_id = params.nodes[0];
//            current_object = {id: current_node_id, type: "node"};
        }
        else {
            current_node_id = null;
        }
        if ((params.edges.length > 0) & (params.nodes.length == 0)) {
            current_edge_id = params.edges[0]
//            current_object = {id: current_edge_id, type: "edge"};
        }
        else {
            current_edge_id = null;
        }
        var canvasPos = network.DOMtoCanvas({x: params.pointer.DOM.x, y: params.pointer.DOM.y});
        if (current_node_id != null) {
            update_node_editor(data.nodes.get(current_node_id));
            var virtual_node_data = {id: virtual_node_id, group: "virtual", size: 15,
                color: "rgba(0,255,0,0.1)",
                physics: false,
                x: canvasPos.x + 50,
                y: canvasPos.y + 50
            }
            var virtual_edge_data = {id: virtual_edge_id, from: current_node_id, to: virtual_node_id,
                                     color: "rgba(255,0,0,0.3)", width: 5}
            if (data.nodes.get(virtual_node_id) == null) {
                data.nodes.add(virtual_node_data);
            }
            else {
                data.nodes.remove(virtual_node_id);
                data.nodes.add(virtual_node_data);
            }
            if (data.edges.get(virtual_edge_id) == null) {
                data.edges.add(virtual_edge_data);
            }
            else {
                data.edges.remove(virtual_edge_id);
                data.edges.add(virtual_edge_data);
            }
        }
        if (current_edge_id != null) {
            var current_edge_data = data.edges.get(current_edge_id);
            var from_node = data.nodes.get(current_edge_data["from"]);
            var to_node = data.nodes.get(current_edge_data["to"]);
            update_edge_editor(current_edge_data, from_node, to_node);
        }


    });
    network.on("selectNode", function (params) {
//        console.log('selectNode Event:', params);
    });
    network.on("selectEdge", function (params) {
//        console.log('selectEdge Event:', params);
    });
    network.on("deselectNode", function (params) {
//        console.log('deselectNode Event:', params);
        current_node_id = null;
    });
    network.on("deselectEdge", function (params) {
//        console.log('deselectEdge Event:', params);
        current_edge_id = null;
    });
    network.on("dragEnd", function (params) {
        if (params.nodes.length > 0) {
            if (params.nodes[0] == virtual_node_id) {
                data.nodes.remove(virtual_node_id);
                data.edges.remove(virtual_edge_id);
                var here_node = network.getNodeAt({x: params.pointer.DOM.x, y: params.pointer.DOM.y});
                if (here_node != null) {
                    var new_edge_data = {from: current_node_id, to: here_node, label: new_relation_name};
                    var from_label = data.nodes.get(current_node_id)["group"];
                    var to_label = data.nodes.get(here_node)["group"];
                    $.ajax({
                        url: service_address + '/createRelation',
                        data: {"from_id": current_node_id, "to_id": here_node, "type": new_relation_name,
                               "props": "", "from_label": from_label, "to_label": to_label},
                        type: 'POST',
                        success: function(response){
                            if (JSON.parse(response)) {
                                data.edges.add(new_edge_data);
                            } else {
                                alert("Failed to create relation");
                            }
                        },
                        error: function(error){
                            console.log(error);
                        }
                    });
                }
                current_node = null;
            }
        }
    });
    network.on("hoverNode", function (params) {
        console.log('hover node:', params);
        last_hover_node_id = params.nodes[0];
    });
}
//------------------------------------------------------------------
// TODO: mouse event handlers for editor
//------------------------------------------------------------------
$(function(){
    // TODO: setup mouse event for html tags
    $("#search-box").mouseover(function() {
        showSuggestions();
    });
    $("#search-box").mouseout(function() {
        hideSuggestions();
    });
    $("#search-suggestions").delegate('ul li', 'click', function(){
        var that_node = $(this).children(".node-name");
        var node_id_ = that_node.attr("data-id");
        if (data.nodes.get(node_id_) == null) {
            var label_ = that_node.attr("data-name");
            var group_ = that_node.attr("data-label");
            data.nodes.add({
                id: node_id_,
                label: label_,
                group: group_
            });
        }
    });

    $('#mynetwork').on("click", clickAction);
});

function clickAction() {
    var $this = $(this);
    $this.on('keypress', keypress_handler);
    $this.focus();
}
//------------------------------------------------------------------
