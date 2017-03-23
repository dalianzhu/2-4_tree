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

    assert tree.root.keys == [4, 12]
    assert tree.root.children[1].keys == [8, 9]


def test_case_2():
    """
    建立一个树
                  5
               /    \
            2,3    6,7,8
    删除8，不会对结构有影响
    """
    debug("test case 2 run")
    keys = [5, 2, 3, 6, 7, 8]

    tree = BTree()
    for item in keys:
        tree.add(item)

    tree.remove(8)
    assert tree.root.keys == [5]
    assert tree.root.children[0].keys == [2, 3]
    assert tree.root.children[1].keys == [6, 7]


def test_case_3():
    """
    建立一个树
                  5
               /    \
            2,3    6,7,8
    删除3
    结果需要再平衡
              6
            /   \
         2,5    7,8
    """
    debug("test case 3 run")
    keys = [5, 2, 3, 6, 7, 8]

    tree = BTree()
    for item in keys:
        tree.add(item)

    tree.remove(3)
    assert tree.root.keys == [6]
    assert tree.root.children[0].keys == [2, 5]
    assert tree.root.children[1].keys == [7, 8]


def test_case_4():
    """
    建立一个树：
                             5       10      44      55
                      |      |        |       |      |        |
                        /        /        /       /        /
                   2 3         6 7      17 22   45 50    66 68 70
    删除 3

                            10       44      55
                      |      |        |       |      |
                        /         /       /        /
                   2 5 6 7       17 22   45 50    66 68 70

    删除 44
    先替换
                            10       22      55
                      |      |        |       |      |
                        /         /       /        /
                   2 5 6 7     17 *44*   45 50    66 68 70

    再合并最胖兄弟
                             7       22      55
                      |      |        |       |      |
                        /         /       /        /
                   2 5 6      10 17    45 50    66 68 70
    """

    debug("test case 4 run")
    keys = [5, 10, 50, 2, 3, 6, 7, 17, 22, 44, 45, 55, 66, 68, 70]

    tree = BTree()
    for item in keys:
        tree.add(item)

    tree.remove(3)
    assert tree.root.keys == [10, 44, 55]
    assert tree.root.children[0].keys == [2, 5, 6, 7]
    assert tree.root.children[1].keys == [17, 22]

    tree.remove(44)
    assert [
               tree.root.keys,
               tree.root.children[0].keys,
               tree.root.children[1].keys,
               tree.root.children[2].keys,
               tree.root.children[3].keys,
           ] == [
               [7, 22, 55],
               [2, 5, 6],
               [10, 17],
               [45, 50],
               [66, 68, 70],
           ]


test_cases = [
    test_case_1,
    test_case_2,
    test_case_3,
    test_case_4,
]
for item in test_cases:
    item()
