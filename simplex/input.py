"""
Module responsible for handling input for the Simplex problem.

Uses a Tkinter window to receive linear inequality constraints and the P function.
"""

# import tkinter as tk
from typing import Literal

Inequality = tuple[list[float], Literal["<", ">", "<=", ">="], float]


# class GUI(tk.Tk):
#     pass

def inequalities_to_tableau(*inequality: Inequality) -> tuple[dict[str, list[float]], list[str]]:
    """
    Converts inequalities to a tableau.

    Returns the tableau and a list of all variables.
    """

    inequalities = list(inequality)

    n_artificials = sum(1 for i in inequalities if i[1] in [">", ">="])
    n_Pvars = len(inequalities[0][0])
    n_ineqs = len(inequalities)

    # Sort to prioritise artifical variables
    inequalities.sort(key=lambda i: i[1] in [">", ">="], reverse=True)

    T = {}

    for i, ineq in enumerate(inequalities):
        coeffs, sign, value = ineq

        row = [0] * (n_Pvars + n_ineqs + n_artificials + 1)

        # Add coefficients and value
        row[:n_Pvars] = coeffs
        row[-1] = value

        # Add surplus variables
        if sign in ["<", "<="]:
            row[n_Pvars + i] = 1
            T[f"s{i + 1}"] = row
        
        # Add artificial variables
        elif sign in [">", ">="]:
            row[n_Pvars + i] = -1
            row[n_Pvars + n_ineqs + i] = 1

            T[f"a{i + 1}"] = row

        else:
            raise ValueError(f"Invalid sign: {sign}")

    # Calculate variable names
    P_vars = [chr(i) for i in range(65, 65 + n_Pvars)]
    s_vars = [f"s{i + 1}" for i in range(n_ineqs)]
    a_vars = [f"a{i + 1}" for i in range(n_artificials)]
    vars = P_vars + s_vars + a_vars + ["Value"]

    return T, vars