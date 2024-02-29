class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

    def get_variables(self, variables):
        if not self:
            return
        if self.value.isalpha():
            variables.add(self.value)
        if self.left:
            self.left.get_variables(variables)
        if self.right:
            self.right.get_variables(variables)
