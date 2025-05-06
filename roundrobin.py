from itertools import combinations
from pysat.formula import CNF

# Round-robin schedule generator
instances = [(15, 13), (16, 14), (16, 13), (17, 15), (17, 14), (17, 13), (18, 16), (18, 15), (18, 14), (18, 13)]  # (n, r) pairs
for (n, r) in instances:
    cnf = CNF()
    # Create variables x(i,j,k) for 1 <= i < j <= n, 1 <= k <= r
    vpool = {}  # mapping (i,j,k) -> variable ID
    var_id = 1
    for i in range(1, n):
        for j in range(i+1, n+1):
            for k in range(1, r+1):
                vpool[(i,j,k)] = var_id
                var_id += 1
    # Constraint: each pair (i,j) plays in exactly one round
    for i, j in combinations(range(1, n+1), 2):
        # At-least-one: clause with all round vars for pair (i,j)
        cnf.append([vpool[(i,j,k)] for k in range(1, r+1)])
        # At-most-one: pairwise negatives for every two rounds
        for k1 in range(1, r):
            for k2 in range(k1+1, r+1):
                cnf.append([-vpool[(i,j,k1)], -vpool[(i,j,k2)]])
    # Constraint: no player has two games in the same round
    for p in range(1, n+1):
        for k in range(1, r+1):
            # gather all games in round k involving player p
            games = []
            for opp in range(1, n+1):
                if opp != p:
                    i, j = (p, opp) if p < opp else (opp, p)
                    games.append(vpool[(i,j,k)])
            # pairwise negatives for any two games of player p in round k
            for a in range(len(games)):
                for b in range(a+1, len(games)):
                    cnf.append([-games[a], -games[b]])
    cnf.to_file(f"RoundRobin_n{n}_d{r}.cnf")
