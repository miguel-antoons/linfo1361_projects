from clause import *

"""
For the tapestry problem, the only code you have to do is in this file.

You should replace

# your code here

by a code generating a list of clauses modeling the queen problem
for the input file.

You should build clauses using the Clause class defined in clause.py

Read the comment on top of clause.py to see how this works.
"""


def get_expression(size, fixed_cells=None):
    expression = []
    # your code here

    for cell in fixed_cells:
        row = cell[0]
        column = cell[1]
        shape = cell[2]
        color = cell[3]


        new_clause = Clause(size)
        new_clause.add_positive(cell[0], cell[1], cell[2], cell[3])
        expression.append(new_clause)

    for i in range(n_rows):
        for a in range(n_shapes):
            for b in range(n_colors):
                clause = [Cijab(i, j, a, b) for j in range(n_columns)]
                exactly_one(clause)

        for b in range(n_colors):
            for a in range(n_shapes):
                clause = [Cijab(i, j, a, b) for j in range(n_columns)]
                exactly_one(clause)

    print(expression)

    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)
