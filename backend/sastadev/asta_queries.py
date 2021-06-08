from sastadev import SDLOGGER
from sastadev.dedup import getposition, mlux2
from sastadev.macros import expandmacros
from sastadev.treebankfunctions import (asta_recognised_nounnode, clausecats,
                                        getattval, showtns)

noun_xpath = './/node[%asta_noun%]'
expanded_noun_xpath = expandmacros(noun_xpath)


def asta_noun(stree):
    mluxnodes, dupinfo = mlux2(stree)
    noun_nodes = stree.xpath(expanded_noun_xpath)
    # print(showtns(noun_nodes))

    clean_noun_nodes = noun_nodes

    # remove words not recognised as nouns
    clean_noun_nodes = [node for node in clean_noun_nodes if asta_recognised_nounnode(node)]
    # print(showtns(clean_noun_nodes))

    toremovenodes = [node for node in mluxnodes if node not in dupinfo.icsws]
    clean_noun_nodes = [node for node in clean_noun_nodes if node not in toremovenodes]
    # print(showtns(clean_noun_nodes))
    clean_noun_nodes = [node for node in clean_noun_nodes if getposition(node) not in dupinfo.shortdups]
    # print(showtns(clean_noun_nodes))
    clean_noun_nodes = [node for node in clean_noun_nodes if getposition(node) not in dupinfo.longdups]
    # print(showtns(clean_noun_nodes))
    additional_nodes = getmluxnodes(mluxnodes, clean_noun_nodes, dupinfo)
    result = clean_noun_nodes + additional_nodes
    # print(showtns(result))
    return result


def getmluxnodes(mluxnodes, posnodes, dupinfo):
    resultnodes = []
    for node in mluxnodes:
        nodeposition = getposition(node)
        origpos = get_origpos(nodeposition, dupinfo)
        targetnode = find_node(origpos, posnodes)
        if targetnode is not None:
            resultnodes.append(node)
    return resultnodes


def get_origpos(nodeposition, dupinfo):
    newposition = nodeposition
    if newposition not in dupinfo.longdups:
        result = None
    else:
        while newposition in dupinfo.longdups:
            newposition = dupinfo.longdups[newposition]
        result = newposition
    return result


def find_node(position, nodes):
    results = [node for node in nodes if getposition(node) == position]
    lresults = len(results)
    if lresults == 0:
        result = None
    elif lresults == 1:
        result = results[0]
    else:
        SDLOGGER.warning('Multiple nodes found for position {}: {}, in {}'.format(position, showtns(results), showtns(nodes)))
        result = results[0]
    return result


bijzin_xpath = './/node[%ASTA_Bijzin%]'
expanded_bijzin_xpath = expandmacros(bijzin_xpath)


def asta_bijzin(stree):
    candnodes = stree.xpath(expanded_bijzin_xpath)
    tops = stree.xpath('.//node[@cat="top"]')
    top = tops[0]
    done, resultingnodes = removehoofdzin(top, candnodes)
    return resultingnodes


def removehoofdzin(stree, clausenodes):
    resultingnodes = clausenodes
    done = False
    for child in stree:
        chatt = getattval(child, 'cat')
        if chatt in clausecats:
            if child in clausenodes:
                resultingnodes.remove(child)
                done = True
                return done, resultingnodes
            else:
                done = True
        if not done:
            done, resultingnodes = removehoofdzin(child, clausenodes)
    return done, resultingnodes
