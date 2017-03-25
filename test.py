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
            4143, 2094, 3637, 8249, 2106, 9787, 4155, 9785, 5693,
            8262, 4679, 7758, 8270, 2638, 5204, 2648, 7259, 3676,
            605, 1637, 5738, 8302, 4210, 3700, 9344, 3713, 5253,
            6791, 1672, 136, 8851, 3733, 4758, 6808, 8856, 667,
            6303, 6817, 2723, 4259, 5283, 8356, 3753, 8876, 6828,
            5806, 9388, 4272, 6323, 4279, 6840, 4286, 9926, 2250, 5837,
            3280, 212, 4820, 2266, 9436, 8930, 227, 3810, 2799, 4336]


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

    for item in [7681, 9223, 2570, 7183, 5136, 1021, 9748,
            7190, 6167, 543, 5151, 5152, 8740, 5673, 6699, 46,
            4143, 2094, 3637, 8249, 2106, 9787, 4155, 9785, 5693,
            8262, 4679, 7758, 8270, 2638, 5204, 2648, 7259, 3676,
            605, 1637, 5738, 8302, 4210, 3700, 9344, 3713, 5253,
            6791, 1672, 136, 8851, 3733, 4758, 6808, 8856, 667,
            6303, 6817, 2723, 4259, 5283, 8356, 3753, 8876, 6828,
            5806, 9388, 4272, 6323, 4279, 6840, 4286, 9926, 2250, 5837,
            3280, 212, 4820, 2266, 9436, 8930, 227, 3810, 2799, 4336]:
        target_key = item
        keys.remove(target_key)
        tree.remove(target_key)

        search_node = tree.find(target_key)
        if target_key in search_node.keys:
            raise Exception("cannot find a removed key")
        else:
            pass

        for exist_key in keys:
            search_node = tree.find(exist_key)
            if not (1 < len(search_node.keys) < 5):
                if tree.root != search_node:
                    raise Exception("node keys len is not correct")

            if exist_key in search_node.keys:
                pass
            else:
                raise Exception("A value({}) that should exist can not be found  !".format(exist_key))

    assert tree.root.keys == [6656]


test_cases = [
    # test_case_1,
    # test_case_2,
    # test_case_3,
    # test_case_4,
    test_case_5,
]
for item in test_cases:
    item()
