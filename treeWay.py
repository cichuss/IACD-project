from BST import BST
from Node import Node


def precedence(c):
    if c == '(':
        return 0
    if c == '!':
        return 3
    if c == '&' or c == '|':
        return 2
    if c == '=' or c == '>':
        return 1
    else:
        return -1


def is_operator(c):
    return c in ('!', '&', '|', '=', '>')


def handle_operator_in_stack(stack, wyj, char):
    while stack and is_operator(stack[-1]) and precedence(char) <= precedence(stack[-1]):
        wyj += stack.pop() + ' '
    stack.append(char)
    return wyj

def handle_char(stack, wyj, sb, char):
    if char.isalpha():  # Handle operands (i.e., variables)
        sb += char
    else:
        if sb:
            wyj += sb + ' '  # Add the completed operand to the output
            sb = ''
        if char == '(':
            stack.append(char)
        elif char == ')':
            while stack[-1] != '(':
                wyj += stack.pop() + ' '
            stack.pop()
        elif is_operator(char):
            wyj = handle_operator_in_stack(stack, wyj, char)
    return wyj, sb

def create_rpn(formula):
    stack = []
    sb = ''
    wyj = ''
    for char in formula:
        wyj, sb = handle_char(stack, wyj, sb, char)
    if sb:
        wyj += sb + ' '  # Add any remaining operand to the output
    while stack:
        wyj += stack.pop() + ' '
    return wyj


def create_tree(formula):
    stack = []
    for char in formula.split():
        if char in ('!', '|', '&', '=', '>'):
            n = Node(char)
            if char != '!':
                n.right = stack.pop()
            n.left = stack.pop()
            stack.append(n)
        else:
            stack.append(Node(char))
    return BST(stack.pop())


if __name__ == "__main__":
    while True:
        print("Input correct formula:")
        formula = input()
        rpn = create_rpn(formula)
        print(rpn)
        tree = create_tree(rpn)
        print(tree.inorder())
        tree.root.get_variables(tree.variables)
        tree.generate_truth_table()
