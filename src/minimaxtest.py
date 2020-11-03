# Minimax test

class Node:
    def __init__(self, score, children):
        self.score = score
        self.children = children or []


root = Node(0, [
    Node('A', [
        Node('a', [
            Node(1, []),
            Node(3, []),
            ]),
        Node('b', [
            Node(1, []),
            Node(4, []),
            ]),
        ]),
    Node('B', [
        Node('c', [
            Node(1, []),
            Node(5, []),
            ]),
        Node('d', [
            Node(6, []),
            Node(5, []),
        ]),
    ]),
])


def select_next_best_move(root: Node):

    def get_best_score(node: Node, _min: bool):
        if not node.children:
            return None

        _min = not _min

        for child in node.children:
            get_best_score(child, _min)

        scores = (child.score for child in node.children)
        node.score = max(scores) if _min else min(scores)

        return node.score

    print(get_best_score(root, True))


select_next_best_move(root)
