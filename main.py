from simplex.tableau import Tableau
from simplex.input import inequalities_to_tableau

if __name__ == "__main__":

    ineqs = (
        ([1, 1], "<", 1000),
        ([2, 1], "<", 1500),
        ([3, 2], "<", 2400),
        ([1, 1], ">", 800),
        )
    P = [1, 0.8]

    t = Tableau(*inequalities_to_tableau(*ineqs, P=P))
    t.add_I()
    print(t)

    t.solve()

"theyre everwhere"
"""
:O fr twin
"""