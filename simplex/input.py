"""
Module responsible for handling input for the Simplex problem.

Uses a Tkinter window to receive linear inequality constraints and the P function.
"""

# import tkinter as tk
from typing import Literal

Inequality = tuple[list[float], Literal["<", ">", "<=", ">="], float]


# class GUI(tk.Tk):
#     pass

def inequalities_to_tableau(*inequality: Inequality, P: list[float]) -> tuple[str, list[float]]:
    """
    Converts inequalities to a tableau, including the P function.
    """

    inequalities = list(inequality)

    n_artificials = sum(1 for i in inequalities if i[1] in [">", ">="])
    n_Pvars = len(inequalities[0])
    n_ineqs = len(inequalities)

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

    # Add P function
    p = [0] * (n_Pvars + n_ineqs + n_artificials + 1)
    p[:n_Pvars] = [-c for c in P]
    T["P"] = p

    return T