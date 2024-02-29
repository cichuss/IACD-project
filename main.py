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
    skip_next = False
    stack = []
    for index, char in enumerate(formula):
        if skip_next:
            skip_next = False
        elif char == '!':
            stack.append(not prop_dict[formula[index + 1]])
            skip_next = True
        elif char.isalpha():
            stack.append(prop_dict[char])
        elif char == '&':
            stack.append(stack.pop() and prop_dict[formula[index + 1]])
            skip_next = True
        elif char == '|':
            stack.append(stack.pop() or prop_dict[formula[index + 1]])
            skip_next = True
        elif char == '>':
            a, b = stack.pop(), prop_dict[formula[index + 1]]
            stack.append(not a or b)
            skip_next = True
        elif char == '=':
            a, b = stack.pop(), prop_dict[formula[index + 1]]
            stack.append(a == b)
            skip_next = True
    return stack[0]


def evaluate(formula, prop_dict):
    """
    Evaluates the formula considering parentheses.
    """
    stack = []
    prop_dict['T'] = True
    prop_dict['F'] = False
    for char in formula:
        if char == ')':
            sub_formula = ''
            while stack[-1] != '(':
                sub_formula = str(stack.pop()) + sub_formula
            stack.pop()  # Pop '('
            if evaluate_basic(sub_formula, prop_dict):
                stack.append('T')
            else:
                stack.append('F')
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


def add_parentheses(formula):
    formula2 = ""
    skip_next = False
    skip_next2 = False
    for i, char in enumerate(formula):
        if skip_next:
            skip_next = False
        elif skip_next2:
            skip_next2 = False
        elif char == "!":
            formula2 = formula2 + "(" + char + formula[i + 1] + ")"
            skip_next = True
        elif ((char == "|") or (char == "&")) and (formula2[-1] != ")") and (formula[i+1] != "!"):
            formula2 = formula2[:-1]
            formula2 = formula2 + "(" + formula[i - 1] + char + formula[i + 1] + ")"
            skip_next = True
        elif ((char == "|") or (char == "&")) and (formula2[-1] != ")"):
            formula2 = formula2[:-1]
            formula2 = formula2 + "(" + formula[i - 1] + char + "(" + formula[i + 1] + formula[i + 2] + "))"
            skip_next = True
            skip_next2 = True
        else:
            formula2 += char
    return formula2


def main():
    formula = input("Enter a well-formed formula in propositional logic: ").replace(" ", "")
    prop_dict = {}
    formula = add_parentheses(formula)
    print(formula)
    for char in formula:
        if not is_atomic(char, prop_dict) and char not in ['!', '&', '|', '>', '=', '(', ')']:
            print("ERROR: Invalid character detected.")
            return
    print(prop_dict)
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
    while True:
        main()
