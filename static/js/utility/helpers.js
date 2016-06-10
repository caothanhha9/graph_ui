class ColorHelper {
    getRandomColor() {
        var letters = '0123456789ABCDEF'.split('');
        var color = '#';
        for (var i = 0; i < 6; i++ ) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
}

class KeyGen {
    gen_key(num_size)
    {
        var text = "";
        var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

        for( var i=0; i < num_size; i++ )
            text += possible.charAt(Math.floor(Math.random() * possible.length));

        return text;
    }
    hash_key(s){
        return Math.abs(s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0));
    }

    gen_id(num_size, s) {
        var root_id = this.hash_key(s).toString();
        var max_root_length = num_size - (num_size / 2);
        if (root_id.length > max_root_length) {
            root_id = root_id.substring(0, max_root_length);
        }
        var sub_id = this.gen_key(num_size - root_id.length);
        return root_id + sub_id;
    }
}

class TemplateHelper {
    build_suggestions(suggestion_data) {
        var html = '<ul id="search-results" class="search results" >';
        var i;
        for (i=0; i<suggestion_data.length; i++) {
            var new_node = suggestion_data[i];
            var data_id = new_node["id"];
            var data_name = new_node["name"];
            var data_label = new_node["label"];
            html += '<li>';
            html += '<p class="node-name" data-id="' + data_id + '"';
            html += ' data-name="' + data_name + '"';
            html += ' data-label="' + data_label + '"';
            html += ' >';
            html += data_name;
            html += '</p>';
            html += '</li>';
        }
        html += '</ul>';
        return html;
    }

    build_edge_properties(edge_properties_data) {
        var html = '';
        for (var i=0; i < edge_properties_name.length; i++) {
            var name_property = edge_properties_name[i];
            var s = "";
            if (edge_properties_data[name_property] == null) {
                s += '<input type="text" value="" placeholder="Value..." class="form-control edge-value"> </div> </li>';
            }
            else {
                var discrete = edge_properties_data[name_property];
                s += ' <select class="form-control edge-value" > ';
                discrete.forEach(function(e) {
                    s += ' <option value="' + e + '">'+ e +'</option> ';
                })
                s += '</select> </li>';
            }
            html += '<li role="presentation"> <div class="form-inline">'
            html += '<button id="btn'+ i +'" type="button" class="btn btn-default select-btn" aria-label="Left Align"'
            html += ' onclick="check(' + i + ',\''+ name_property +'\')">'
            html += '<span class="glyphicon glyphicon-unchecked" aria-hidden="true"></span> '
            html += '<label class="prop-name">' + name_property + '</label>'
            html += '</button>'
            html += s;
        }
        return html;
    }
}

class DataConverter {
    convert_node_data(node_data) {
        var n_node_data = new Array();
        var i;
        for (i=0; i<node_data.length; i++) {
            var node = node_data[i];
            var id_ = node["id"];
            var label_ = node["name"];
            var group_ = node["label"][0];
            n_node_data.push({id: id_, label: label_, group: group_});
        }
        return n_node_data;
    }

    convert_relation(relation) {
//        var relation_color_dict = {"ACCOMPANY": "#01DF3A", "REPLACE": "#2E64FE", "ATTACK": "#FF0040", "HAS_ATTRIBUTE": "#F7D358"}
        var from_ = relation["from"];
        var to_ = relation["to"];
        var label_ = relation["type"];
        var dict_ = JSON.stringify(relation["dict"]);
        if (relation_color_dict[label_] == null) {
            relation_color_dict[label_] = colorHelper.getRandomColor();
        }
        var arrows_ = to_ + ";" + from_
        var color_ = relation_color_dict[label_]
        return {from: from_, to: to_, label: label_, color: color_, title: dict_}
    }
    convert_relation_data(relation_data) {
        var n_relation_data = new Array();
        var i;
        for (i=0; i<relation_data.length; i++) {
            var relation = relation_data[i];
            n_relation_data.push(this.convert_relation(relation));
        }
        return n_relation_data;
    }
}


/*
function getRandomColor() {
    var letters = '0123456789ABCDEF'.split('');
    var color = '#';
    for (var i = 0; i < 6; i++ ) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}
function gen_key(num_size)
{
    var text = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for( var i=0; i < num_size; i++ )
        text += possible.charAt(Math.floor(Math.random() * possible.length));

    return text;
}
function hash_key(s){
  return Math.abs(s.split("").reduce(function(a,b){a=((a<<5)-a)+b.charCodeAt(0);return a&a},0));
}

function gen_id(num_size, s) {
  var root_id = hash_key(s).toString();
  var max_root_length = num_size - (num_size / 2);
  if (root_id.length > max_root_length) {
    root_id = root_id.substring(0, max_root_length);
  }
  var sub_id = gen_key(num_size - root_id.length);
  return root_id + sub_id;
}

function build_suggestions(suggestion_data) {
    var html = '<ul id="search-results" class="search results" >';
    for (i=0; i<suggestion_data.length; i++) {
        var new_node = suggestion_data[i];
        var data_id = new_node["id"];
        var data_name = new_node["name"];
        var data_label = new_node["label"];
        html += '<li>';
        html += '<p class="node-name" data-id="' + data_id + '"';
        html += ' data-name="' + data_name + '"';
        html += ' data-label="' + data_label + '"';
        html += ' >';
        html += data_name;
        html += '</p>';
        html += '</li>';
    }
    html += '</ul>';
    return html;
}
*/


/*
function convert_node_data(node_data) {
    var n_node_data = new Array();
    for (i=0; i<node_data.length; i++) {
        var node = node_data[i];
        var id_ = node["id"];
        var label_ = node["name"];
        var group_ = node["label"][0];
        n_node_data.push({id: id_, label: label_, group: group_});
    }
    return n_node_data;
}

function convert_relation(relation) {
    var from_ = relation["from"];
    var to_ = relation["to"];
    var label_ = relation["type"];
    var dict_ = JSON.stringify(relation["dict"]);
    if (relation_color_dict[label_] == null) {
        relation_color_dict[label_] = colorHelper.getRandomColor();
    }
    var arrows_ = to_ + ";" + from_
    var color_ = relation_color_dict[label_]
    return {from: from_, to: to_, label: label_, color: color_, title: dict_}
}
function convert_relation_data(relation_data) {
    var n_relation_data = new Array();
    for (i=0; i<relation_data.length; i++) {
        var relation = relation_data[i];
        n_relation_data.push(convert_relation(relation));
    }
    return n_relation_data;
}
*/