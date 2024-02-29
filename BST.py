def operation(a, b, s):
    if s == "!":
        return not a
    elif s == "|":
        return a or b
    elif s == "&":
        return a and b
    elif s == "=":
        return a == b
    elif s == ">":
        return not a or b
    return 0


class BST:
    def __init__(self, root):
        self.root = root
        self.variables = set()

    def evaluate(self, elem, truth_assignment):
        if elem is None:
            return 0
        if elem.left is None and elem.right is None:
            # If the element is a variable, return its truth value from the truth assignment
            return truth_assignment[elem.value]
        elem.value
        a = self.evaluate(elem.left, truth_assignment)
        elem.value
        b = self.evaluate(elem.right, truth_assignment)

        return operation(a, b, elem.value)

    def generate_truth_table(self):
        # Get the list of unique variables
        variables = list(self.variables)
        variables.sort()
        num_variables = len(variables)

        # Print table header
        header = " | ".join(variables) + " | Result"
        print(header)
        print("-" * len(header))

        # Generate all possible truth assignments and evaluate the expression for each
        for i in range(2 ** num_variables):
            truth_assignment = {}
            binary_str = bin(i)[2:].zfill(num_variables)  # Convert the index to binary and pad with zeros
            for j, var in enumerate(variables):
                truth_assignment[var] = bool(int(binary_str[j]))  # Assign truth values based on binary representation

            result = self.evaluate(self.root, truth_assignment)
            # Print truth values and result
            values = [str(truth_assignment[var])[0] for var in variables]  # Convert boolean to 0 or 1
            print(" | ".join(values) + " | " + str(result))

    def nodes(self, elem):
        count = 0
        if elem:
            count += 1
            if elem.left:
                count += self.nodes(elem.left)
            if elem.right:
                count += self.nodes(elem.right)
        return count

    def inorder(self, elem=None):
        if elem is None:
            elem = self.root
        if elem.left:
            self.inorder(elem.left)
        print(elem.value, end=' ')
        if elem.right:
            self.inorder(elem.right)
