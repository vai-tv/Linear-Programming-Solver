"""
Module for solving the linear programming problem.

Holds a class that receives a dictionary with the key as the basic variable and the value as a list of coefficients.
"""

TableauDict = dict[str, list[float]]
Pivot = tuple[str, int]

class Tableau:

    def __init__(self, tableau: TableauDict, variables: list[str] = None, P_vars: list[str] = None):
        self.T = tableau
        self.variables = variables
        self.P_vars = P_vars # Always assume P variables are first

    def __str__(self):
        max_len = 0
        for k, v in self.T.items():
            for c in v:
                max_len = max(max_len, len(str(round(c, 2))))
        
        fmt = "{{:^{}}}".format(max_len)
        # Variables header
        s = " | ".join([fmt.format(v) for v in ["b.v."] + self.variables]) + "\n"

        for k, v in self.T.items():
            s += fmt.format(k) + " | "
            s += " | ".join(
                [
                    fmt.format(int(i))
                    if i.is_integer() else fmt.format(str(round(i, 2)))
                    for i in v
                ]
            ) + "\n"
        return s
    
    def add_I(self) -> None:
        """
        Adds the I (negative sum of all artificial variables) row to the tableau.
        """

        # Get all artificals
        a = {k: [0 if self.variables[i].startswith("a") else c for i, c in enumerate(v)] 
             for k, v in self.T.items() if k.startswith("a")}

        self.T["I"] = [-sum(i) for i in zip(*a.values())]
    
    def get_pivot(self) -> Pivot:
        """Returns the key of the row and index of the column to pivot on."""
        
        # 1. Identify the lowest coefficient in P or I
        
        X = self.T.get("I")
        if not X: X = self.T.get("P")

        # min_col = X.index(min(X[:len(self.P_vars)]))
        min_col = X.index(min(X[:-1]))

        # Calculate all theta values and choose the minimum positive
        min_row = None
        min_theta = float("inf")

        for bv, c in self.T.items():
            # Ignore P and I
            if bv in ["P", "I"]: continue
            # Do not pivot where the b.v. is a P-variable
            if bv in self.P_vars: continue
            # Avoid DB0
            if c[min_col] == 0: continue

            theta = c[-1] / c[min_col]
            if theta > 0 and theta < min_theta:
                min_theta = theta
                min_row = bv

        return min_row, min_col
    
    def apply_pivot(self, pivot: Pivot) -> None:
        """Applies the pivot to the tableau."""

        row, col = pivot
        pivot_val = self.T[row][col]

        # 1. Divide all values in the pivot row by the pivot value
        self.T[row] = [i / pivot_val for i in self.T[row]]

        # 2. Subtract the pivot row from all other rows
        for k, v in self.T.items():
            if k == row: continue
            self.T[k] = [v[i] - self.T[row][i] * v[col] for i in range(len(v))]

        # 3. Change the basic variable name (without changing order)
        new_name = self.variables[col]
        self.T = {k if k != row else new_name: v for k, v in self.T.items()}
    
    def is_stage_1_complete(self) -> bool:
        """
        Returns True if the value of I is 0.
        """
        return self.T["I"][-1] == 0
    
    def isoptimal(self) -> bool:
        """
        Returns True if all P variables are non-negative.
        """

        return all(i >= 0 for i in self.T["P"][:len(self.P_vars)])

    def change_to_stage_2(self) -> None:
        """
        Changes the tableau to stage 2 by removing the I row and all artificial variables.
        """

        del self.T["I"]
        self.T = {k: [c for i, c in enumerate(v) if not self.variables[i].startswith("a")] for k, v in self.T.items() if not k.startswith("a")}
        self.variables = [v for v in self.variables if not v.startswith("a")]