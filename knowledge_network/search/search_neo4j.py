# -*- coding: utf-8 -*-
import unidecode as unidecode
import string
import re
from py2neo import authenticate, Graph, Path
import unicodedata
from knowledge_network.search.non_ascii import non_ascii
from knowledge_network.search.Similarity import levenshtein
from knowledge_network.utility.dao.neo4j_db import NeoFJ
from knowledge_network.config.config import DBAddress


class Search(object):

    def __init__(self):
        self.address = DBAddress.neo4j_address

    def search_product_name(self,_name):
        new_neofj = NeoFJ(address=self.address)
        names = _name.split(" ")
        list =[]
        dictionary = {}
        node_pn = new_neofj.get_all_nodes_by_name('Product')
        for node in node_pn:
            for name in names:
                if non_ascii(non_ascii(_name.lower())) == _name.lower():
                    s1 = non_ascii(name.lower())
                    # s2 = non_ascii(unicodedata.normalize('NFKD', node.lower()).encode('ascii','ignore'))
                    s2 = non_ascii(node["name"].lower().encode('utf-8'))
                    if s1 in s2:
                        if node not in list:
                            list.append(node)

                else:
                    if name.decode('utf-8').lower() in node["name"].lower():
                        if node not in list:
                            list.append(node)
        for _el in list:
            if non_ascii(non_ascii(_name.lower())) == _name.lower():
                # print _el.encode('utf-8')
                # s3 = unicodedata.normalize('NFKD', _el.lower()).encode('ascii','ignore')
                simi1 = levenshtein(_name.decode('utf-8').lower().encode('utf-8'),non_ascii(_el["name"].lower().encode('utf-8')))
                if names[0].lower()!= _el["name"].split(" ")[0].lower().encode('utf-8'):
                    d = dict({_el:simi1+0.5})
                else:
                    d = dict({_el:simi1})
                dictionary.update(d)
            else:
                simi2 = levenshtein(_name.decode('utf-8').lower().encode('utf-8'), _el["name"].lower().encode('utf-8'))
                if names[0].lower() != _el["name"].split(" ")[0].lower().encode('utf-8'):
                    d = dict({_el: simi2 + 0.5})
                else:
                    d = dict({_el: simi2})
                dictionary.update(d)


        sort =  sorted(dictionary, key=dictionary.__getitem__)
        return sort



def main():
    search = Search()
    # print levenshtein('Bóng đá', 'Bóng đá')
    # test =  non_ascii('Viên nang buồng Trứng')
    # print test
    node = search.search_product_name('bóng')
    for el_ in node:
        print(el_)


if __name__ == '__main__':
    main()