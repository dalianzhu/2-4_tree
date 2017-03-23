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

    def remove(self, key):
        """
        :param key: 要删除的值
        :return:
        """
        # 首先 定位到这个值可以出现的节点
        target_node = self.find(key)
        self._remove(target_node, key)

    def _remove(self, delnode, key):
        """
        从delnode中，删除key
        :param delnode:当前要被删除的Node
        :param key:当前要被删除的值，即从 node中删除该值
        """
        if key not in delnode.keys:
            return

        if not delnode.has_children():
            # 说明这是一个叶子
            delnode.keys.remove(key)
            delnode.children.remove(None)  # 叶子节点的children都是none,删谁都一样

            if len(delnode.keys) < CONST_MIN_KEY:
                # keys数量合规，这种情况不需要再平衡
                self._rebalance(delnode)
        else:
            # 说明在中间节点删除
            # 需要将最近子树的节点上移
            # 然后改为删除子树的这个节点
            current_key_pos = delnode.find_key_position(key)
            left_node = delnode.children[current_key_pos]
            delnode.keys[current_key_pos], left_node.keys[len(left_node.keys) - 1] = \
                left_node.keys[len(left_node.keys) - 1], delnode.keys[current_key_pos]

            delnode = left_node
            self._remove(delnode, key)

    def _rebalance(self, delnode):
        if self.root == delnode:
            # merge根节点
            if len(delnode.keys) == 0:
                self.root = self.root.children[0]
            return

        # 说明删除的是叶子 or 树干节点，进行合并操作
        # 首先把delnode和父节点与合适的兄弟合并成一个节点
        new_node, old_parent_key = self._new_node_with_parent_fat_brother(delnode)
        parent = delnode.parent
        old_parent_key_pos = parent.find_key_position(old_parent_key)

        # 判断，new_node的Keys 如果 > CONST_MAX_KEY，说明需要马上分裂
        # 此情况下不会影响父以上的结构，因为不需要从父借节点，而是把子节点中的某个key替换给父
        # 分裂后，生成新的节点，和左右子树
        if len(new_node.keys) > CONST_MAX_KEY:
            mid_key, left, right = new_node.split()
            # 把新的mid key对父节点的目标key赋值
            # 绑定左右子树
            parent.keys[old_parent_key_pos] = mid_key

            parent.children[old_parent_key_pos] = left
            left.parent = parent
            parent.children[old_parent_key_pos + 1] = right
            right.parent = parent

        # 如果构造的新节点，刚好等于 CONST_MAX_KEY
        # 在此情况下，不能分裂，所以从父节点借来的key，不能归还
        if len(new_node.keys) == CONST_MAX_KEY:
            # 父节点对应的keys删除，返回被删除的位置
            del_pos = parent.del_key(old_parent_key)

            # 被删除的位置恰好是父节点对应子树的位置
            parent.children[del_pos] = new_node
            new_node.parent = parent

        # 父节点可能发生了变化，如果被借了节点，且借后节点小于2个递归处理
        if len(parent.keys) < CONST_MIN_KEY:
            self._rebalance(parent)

    def _new_node_with_parent_fat_brother(self, input_node):
        """
        传入一个节点，让它和父亲的合适KEY及最胖的兄弟构成一个新节点
        :param input_node:传入的节点
        :return:新节点，原来父节点的合适key
        """
        parent = input_node.parent
        this_pos = parent.find_child_position(input_node)  # 首先找到delnode的位置

        left_brother_pos = this_pos - 1
        right_brother_pos = this_pos + 1
        # 得到两个兄弟（不一定两个都存在，但必有一个），我们选择一个比较胖的兄弟作为待合并兄弟
        fatter_brother_pos = self._choose_fat_child(parent, left_brother_pos, right_brother_pos)

        if fatter_brother_pos == left_brother_pos:
            #        parent
            #        /   \
            #      left   input_node
            #   会生成新节点：
            #   left_parent_inputnode

            new_node = BTreeNode()
            left_node_keys = parent.children[left_brother_pos].keys
            parent_key_val = parent.keys[this_pos - 1]
            input_node_keys = input_node.keys
            new_node.keys = left_node_keys + [parent_key_val] + input_node_keys
            new_node.children = parent.children[left_brother_pos].children + input_node.children
        else:
            # 说明
            #        parent
            #        /       \
            #      input_node   right
            #   会生成新节点：
            #   inputnode_parent_right

            new_node = BTreeNode()

            input_node_keys = input_node.keys
            parent_key_val = parent.keys[this_pos]
            right_node_keys = parent.children[right_brother_pos].keys

            new_node.keys = input_node_keys + [parent_key_val] + right_node_keys
            new_node.children = parent.children[left_brother_pos].children + input_node.children

        return new_node, parent_key_val

    def _choose_fat_child(self, current_node, child1_pos, child2_pos):
        positions = [child1_pos, child2_pos]
        positions = [x for x in positions if x in range(0, len(current_node.children))]

        if not positions:
            return None

        positions.sort(key=lambda x: len(current_node.children[x].keys))

        return positions[len(positions) - 1]

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
        # 首先，分裂一个节点
        mid_key, left, right = node.split()
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
        self.children = [None]  # children len == len(key) + 1
        self.parent = None

    def add_key(self, key):
        pos = self.find_sub_position(key)  # oh，神奇。在这里也可以用这个函数来求得插入的位置
        self.keys.insert(pos, key)
        self.children.insert(pos + 1, None)  # 插入了一个key，children当然也要相应变化
        return pos

    def del_key(self, key):
        pos = self.find_key_position(key)
        if pos == -1:
            return pos

        self.keys.pop(pos)
        self.children.pop(pos)
        return pos

    def find_sub_position(self, subkey):
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
            if subkey > v:
                position += 1
            else:
                break
        return position

    def find_key_position(self, key):
        for k, v in enumerate(self.keys):
            if key == v:
                return k
        return -1

    def find_child_position(self, child_node):
        for k, v in enumerate(self.children):
            if v == child_node:
                return k
        return -1

    def has_children(self):
        for item in self.children:
            if item is not None:
                return True
        return False

    def split(self):
        # 分裂开始，首先生成新的左右子树节点
        left = BTreeNode()
        right = BTreeNode()

        # 找到分裂的位置，如果keys == 5，则中间的分裂点为 3
        mid_position = len(self.keys) // 2
        # 求分裂的中心值，这个中心值将被加到父节点中去
        mid_key = self.keys[mid_position]

        # 处理左子树
        left.keys = [v for k, v in enumerate(self.keys) if k < mid_position]
        left.children = [v for k, v in enumerate(self.children) if k <= mid_position]

        # 处理右子树
        right.keys = [v for k, v in enumerate(self.keys) if k > mid_position]
        right.children = [v for k, v in enumerate(self.children) if k > mid_position]

        return mid_key, left, right
