CONST_MAX_KEY = 4
CONST_MIN_KEY = 2

isdebug = True
def debug(str):
    if isdebug:
        print(str)


class BTree(object):
    """
    参考资料：
    http://www.cnblogs.com/chobits/p/4813368.html
    https://github.com/julycoding/The-Art-Of-Programming-By-July/blob/master/ebook/zh/03.02.md

    B树的每个节点包含的KEYS 数量都在2-4之间。
    添加节点从叶子节点开始。如果叶子节点的数量大于4,将会发生分裂。
    """
    def __init__(self):
        self.root = None

    def add(self, key):
        """
        增加一个key到B树中
        :param 增加的值:
        :return:

        增加值到B树中有两种情况：
        1. 找到一个叶子节点，增加一个KEY，此时该叶子节点KEYS <= 4，此时直接添加即可
        2. 找到一个叶子节点，增加一个KEY，此时该叶子节点KEYS > 4，此时把这个节点“分裂”
        """
        if not self.root:
            self.root = BTreeNode()
            self.root.add_key(key)
        else:
            node = self.find(key)
            if key in node.keys:
                pass
            else:
                node.add_key(key)
                if len(node.keys) > CONST_MAX_KEY:
                    self.split(node)

    def remove(self,key):
        pass

    def find(self, key):
        return self._find(self.root, key)

    def _find(self, node, key):
        if key in node.keys:
            return node
        else:
            if node.has_children():
                position = node.find_sub_position(key)
                sub_node = node.children[position]
                return self._find(sub_node, key)
            else:
                # 如果节点没有孩子，Key也没在节点中。
                # 仍然返回这个节点
                return node

    def split(self, node):
        # 分裂开始，首先生成新的左右子树节点
        left = BTreeNode()
        right = BTreeNode()

        # 找到分裂的位置，如果keys == 5，则中间的分裂点为 3
        mid_position = len(node.keys) // 2
        # 求分裂的中心值，这个中心值将被加到父节点中去
        mid_key = node.keys[mid_position]

        # 处理左子树
        left.keys = [v for k, v in enumerate(node.keys) if k < mid_position]
        left.children = [v for k, v in enumerate(node.children) if k <= mid_position]

        # 处理右子树
        right.keys = [v for k, v in enumerate(node.keys) if k > mid_position]
        right.children = [v for k, v in enumerate(node.children) if k > mid_position]

        # 把中间值加到父节点中
        parent = node.parent
        if parent:
            # add_key方法会处理因为增加key该节点新增加的child。
            # 默认会在正确的位置填一个None，不用担心，在处理子树绑定的时候（如果有的话），
            # 这个none值就会被赋值
            mid_key_pos_in_parent = parent.add_key(mid_key)

            # 把左右子树绑定到parent上
            parent.children[mid_key_pos_in_parent] = left
            parent.children[mid_key_pos_in_parent + 1] = right

            left.parent = parent
            right.parent = parent

            # 检查一下parent，如果parent在添加了Keys之后，keys长度大于4,则递归分裂
            if len(parent.keys) > CONST_MAX_KEY:
                self.split(parent)
        else:
            # 如果父节点为None，说明这个节点是根
            # 构造一个新根，然后分裂，把左右子树加到新根上去
            self.root = BTreeNode()
            self.root.add_key(mid_key)

            self.root.children[0] = left
            self.root.children[1] = right

            left.parent = self.root
            right.parent = self.root



class BTreeNode(object):
    def __init__(self):
        self.keys = []
        self.children = [None] # children len == len(key) + 1
        self.parent = None

    def add_key(self, key):
        pos = self.find_sub_position(key)  # oh，神奇。在这里也可以用这个函数来求得插入的位置
        self.keys.insert(pos, key)
        self.children.insert(pos + 1, None)  # 插入了一个key，children当然也要相应变化
        return pos

    def find_sub_position(self, key):
        """
        根据Key查找子树的位置，如
        arr = [3,5,   9,12]
                    ^
                    |
                 key = 6
        则6应该在 2 子树上
        """
        if not self.keys:
            return 0

        position = 0
        for k, v in enumerate(self.keys):
            if key > v:
                position += 1
            else:
                break
        return position

    def has_children(self):
        for item in self.children:
            if item is not None:
                return True
        return False





