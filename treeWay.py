from BST import BST
from Node import Node


def precedence(c):
    if c == '(':
        return 0
    if c == '!':
        return 1
    if c == '&' or c == '|':
        return 2
    if c == '=' or c == '>':
        return 3
    else:
        return -1


def is_operator(c):
    return c in ('!', '&', '|', '=', '>')


def create_rpn(formula):
    stack = []
    sb = ''
    wyj = ''
    for char in formula:
        if char.isalpha():
            sb += char
        else:
            if sb:
                wyj += sb + ' '
                sb = ''
            if char == '(':
                stack.append(char)
            if char == ')':
                while stack[-1] != '(':
                    wyj += stack.pop() + ' '
                if stack[-1] == '(':
                    stack.pop()
            if is_operator(char):
                while stack and is_operator(stack[-1]) and precedence(char) <= precedence(stack[-1]):
                    wyj += stack.pop() + ' '
                stack.append(char)
    if sb:
        wyj += sb + ' '
    while stack:
        wyj += stack.pop() + ' '
    return wyj


def create_tree(formula):
    stos = []
    for char in formula.split():
        if char in ('!', '|', '&', '=', '>'):
            n = Node(char)
            n.right = stos.pop()
            n.left = stos.pop()
            stos.append(n)
        else:
            stos.append(Node(char))
    return BST(stos.pop())


if __name__ == "__main__":
    while True:
        print("Input correct formula:")
        formula = input()
        rpn = create_rpn(formula)
        tree = create_tree(rpn)
        tree.root.get_variables(tree.variables)
        tree.generate_truth_table()
