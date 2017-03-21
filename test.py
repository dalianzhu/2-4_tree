from b_tree import BTree, debug


def test_case_1():
    debug("test case 1 run")
    tree = BTree()
    tree.add(1)
    tree.add(3)
    tree.add(9)
    tree.add(12)
    tree.add(4)
    tree.add(8)
    tree.add(14)
    tree.add(17)
    debug("tree root key {}".format(tree.root.keys))
    assert tree.root.keys == [4, 12]
    assert tree.root.children[1].keys == [8, 9]


test_cases = [
    test_case_1,
]
for item in test_cases:
    item()
