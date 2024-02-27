def is_atomic(formula, prop_dict):
    """
    Checks if the formula is an atomic proposition.
    If it is, adds it to the proposition dictionary.
    """
    if formula.islower() and formula.isalpha():
        prop_dict[formula] = None
        return True
    return False


def evaluate_basic(formula, prop_dict):
    """
    Evaluates the formula without considering parentheses.
    """
    stack = []
    for char in formula:
        if char.isalpha():
            stack.append(prop_dict[char])
        elif char == '-':
            stack.append(not stack.pop())
        elif char == '&':
            stack.append(stack.pop() and stack.pop())
        elif char == '|':
            stack.append(stack.pop() or stack.pop())
        elif char == '>':
            a, b = stack.pop(), stack.pop()
            stack.append(not a or b)
        elif char == '=':
            a, b = stack.pop(), stack.pop()
            stack.append(a == b)
    return stack[0]


def evaluate(formula, prop_dict):
    """
    Evaluates the formula considering parentheses.
    """
    stack = []
    for char in formula:
        if char == '(':
            stack.append(char)
        elif char == ')':
            sub_formula = ''
            while stack[-1] != '(':
                sub_formula = stack.pop() + sub_formula
            stack.pop()  # Pop '('
            stack.append(str(evaluate_basic(sub_formula, prop_dict)))
        else:
            stack.append(char)
    return evaluate_basic(''.join(stack), prop_dict)


def generate_truth_table(prop_dict):
    """
    Generates the truth table for the given propositions.
    """
    propositions = list(prop_dict.keys())
    num_props = len(propositions)
    table = []
    for i in range(2 ** num_props):
        row = {}
        for j in range(num_props):
            row[propositions[j]] = bool((i >> (num_props - 1 - j)) & 1)
        table.append(row)
    return table


def determine_type(table, prop_dict):
    """
    Determines if the formula is a tautology, contradiction, or contingency.
    """
    values = list(prop_dict.values())
    for row in table:
        if all(row.values()):
            return "Tautology"
        if not any(row.values()):
            return "Contradiction"
    return "Contingency"


def main():
    formula = input("Enter a well-formed formula in propositional logic: ").replace(" ", "")

    prop_dict = {}
    for char in formula:
        if not is_atomic(char, prop_dict) and char not in ['-', '&', '|', '>', '=', '(', ')']:
            print("ERROR: Invalid character detected.")
            return

    truth_table = generate_truth_table(prop_dict)

    print("\nTruth Table:")
    print("-" * (len(prop_dict) * 4 + len(prop_dict) - 1))
    for prop in prop_dict:
        print(prop, end=" ")
    print("| Result")
    print("-" * (len(prop_dict) * 4 + len(prop_dict) - 1))
    for row in truth_table:
        for prop in prop_dict:
            print(int(row[prop]), end=" " * (len(prop) - 1))
        print("|", int(evaluate(formula, row)))
    print("-" * (len(prop_dict) * 4 + len(prop_dict) - 1))

    formula_type = determine_type(truth_table, prop_dict)
    print("\nFormula type:", formula_type)


if __name__ == "__main__":
    main()
