from nltk.tree import Tree
import logging

def isterminal(t):
    """

    :param t: Subtree
    :return: Is this a terminal subtree
    """
    return not isinstance(t, Tree)


def ispreterminal(t):
    """

    :param t: Subtree
    :return: Is this a preterminal subtree
    """
    if not isterminal(t):
        return all(isterminal(st) for st in t)
    else:
        return False


def filterLexical(t):
    """

    :param t: Tree to be freed from lexical nodes
    """
    if ispreterminal(t):
        logging.debug( "Delete tree ", t, len(t))
        del t[:]
        t.append('')
    else:
        for i in range(len(t)):
            filterLexical(t[i])


def testTreeFilter(tree=None):
    """

    :param tree: Sample tree string in bracket notation.
    """
    if tree:
        t = Tree(tree)
    else:
        t = Tree(
            '((S(NP-SBJ (PRP They))(ADVP-TMP (RB never))(VP (VBD considered)(S (NP-SBJ (PRP themselves) (VP (TO to) (VP (VB be) (NP-PRD (NN anything) (RB else)))))))))')
    t2 = t.copy(deep=True)
    filterLexical(t2)

    from nltk.draw.tree import draw_trees

    draw_trees(t, t2)

if __name__ == "__main__":
    testTreeFilter()