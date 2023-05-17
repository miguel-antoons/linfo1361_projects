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
    for row in range(size):
        for col in range(size):
            for shape in range(size):
                for color in range(size):
                    # each row must contain only one color
                    for col2 in range(size):
                        if col2 != col:
                            for shape2 in range(size):
                                if shape2 != shape:
                                    clause = Clause(size)
                                    clause.add_negative(row, col, shape, color)
                                    clause.add_negative(row, col2, shape2, color)
                                    expression.append(clause)

                    # each row must contain only one shape
                    for col2 in range(size):
                        if col2 != col:
                            for color2 in range(size):
                                if color2 != color:
                                    clause = Clause(size)
                                    clause.add_negative(row, col, shape, color)
                                    clause.add_negative(row, col2, shape, color2)
                                    expression.append(clause)

                    # each column must contain only one color
                    for row2 in range(size):
                        if row2 != row:
                            for shape2 in range(size):
                                if shape2 != shape:
                                    clause = Clause(size)
                                    clause.add_negative(row, col, shape, color)
                                    clause.add_negative(row2, col, shape2, color)
                                    expression.append(clause)

                    # each column must contain only one shape
                    for row2 in range(size):
                        if row2 != row:
                            for color2 in range(size):
                                if color2 != color:
                                    clause = Clause(size)
                                    clause.add_negative(row, col, shape, color)
                                    clause.add_negative(row2, col, shape, color2)
                                    expression.append(clause)

                    # each color and shape combination ust be unique
                    for row2 in range(size):
                        if row2 != row:
                            for col2 in range(size):
                                if col2 != col:
                                    clause = Clause(size)
                                    clause.add_negative(row, col, shape, color)
                                    clause.add_negative(row2, col2, shape, color)
                                    expression.append(clause)

    # Fixed cells clauses
    for row, col, shape, color in fixed_cells:
        clause = Clause(size)
        clause.add_positive(row, col, shape, color)
        expression.append(clause)

    return expression


if __name__ == '__main__':
    expression = get_expression(3)
    for clause in expression:
        print(clause)