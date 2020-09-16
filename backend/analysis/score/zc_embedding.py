
from typing import Dict

CLAUSALS = ['smain', 'rel', 'whrel', 'whsub', 'whq', 'sv1']


def is_token(node):
    return any(x in ['pt', 'pos'] for x in node.keys())


def has_cat(node):
    return 'cat' in node.keys()


def is_clausal(node):
    return is_direct_clausal(node) or is_child_clausal(node)


def is_direct_clausal(node):
    return node.attrib['cat'] in CLAUSALS


def is_child_clausal(node):
    return node.attrib['cat'] in ['cp'] and \
        any(n.attrib['cat'] in ['ssub', 'ti'] for n in list(node))


def solve(node, embed, results):
    if is_token(node):
        results[node.attrib['begin']] = embed
    if has_cat(node) and is_clausal(node):
        embed += 1
    for child in node.getchildren():
        solve(child, embed, results)
    return results


def get_zc_embeddings(syntree) -> Dict[str, int]:
    try:
        root = syntree.getroot()
    except:
        root = syntree
    top_node = root.find('node')
    results = solve(top_node, 0, {})
    return results
