from b_tree import BTree, debug
import random

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

def test_case_5():
    debug("test case 5 run")
    keys = [6656, 7681, 9223, 2570, 7183, 5136, 1021, 9748,
            7190, 6167, 543, 5151, 5152, 8740, 5673, 6699, 46,
            4143,  ]

    tree = BTree()
    for item in keys:
        tree.add(item)

    for item in keys:
        target_key = item
        search_node = tree.find(target_key)
        if target_key in search_node.keys:
            pass
        else:
            raise Exception("not find!")

    for item in [9223, 2570, 7183, 5136, 1021, 9748,
                 7190, 6167, 543, 5151, 5152, 8740, 5673, 6699, 46,
                 4143]:
        target_key = item
        debug(target_key)
        keys.remove(target_key)
        tree.remove(target_key)

        search_node = tree.find(target_key)
        if target_key in search_node.keys:
            raise Exception("cannot find a removed key")
        else:
            pass

        for exist_key in keys:
            search_node = tree.find(exist_key)
            if exist_key in search_node.keys:
                pass
            else:
                raise Exception("A value({}) that should exist can not be found  !".format(exist_key))




test_cases = [
    # test_case_1,
    # test_case_2,
    # test_case_3,
    # test_case_4,
    test_case_5,
]
for item in test_cases:
    item()
