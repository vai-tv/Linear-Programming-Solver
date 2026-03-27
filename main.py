from simplex.tableau import Tableau
from simplex.input import inequalities_to_tableau

if __name__ == "__main__":

    ineqs = (([1, 1, 1], ">", 20),
             ([2, -1, 2], ">", 25),
             ([2, 3, 4], "<", 80))
    P = [2, 4, 3]

    t = inequalities_to_tableau(*ineqs, P=P)
    print(t)

    # These should be calculated from the input
    vars = ["x", "y", "z", "s1", "s2", "s3", "a1", "a2"]
    P_vars = ["x", "y", "z"]

    t = Tableau(t, vars + ["Value"], P_vars)
    t.add_I()
    print(t)

    while not t.is_stage_1_complete():
        p = t.get_pivot()
        
        if not p[0]: # If no pivot is found, the problem has no solution
            print("No feasible solution.")
            break

        t.apply_pivot(p)
        print(t)

    t.change_to_stage_2()

    while not t.isoptimal():
        p = t.get_pivot()

        t.apply_pivot(p)
        print(t)

"theyre everwhere"
"""
:O fr twin
"""