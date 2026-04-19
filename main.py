from simplex.tableau import Tableau
from simplex.input import inequalities_to_tableau

if __name__ == "__main__":

    ineqs = (
        ([2, 3, 1], ">", 20),
        ([1, 1, 2], "<", 30),
        ([3, 2, 4], "<", 50),
        )
    P = [5, 3, 4]

    t = Tableau(*inequalities_to_tableau(*ineqs), P)
    t.add_I()
    print(t)

    t.solve()

"theyre everwhere"
"""
:O fr twin
"""