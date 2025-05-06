from itertools import combinations
from pysat.formula import CNF

def mvts(n_teams: int, days: int, venues: int, fname=None):
    var = lambda i,j,d,v: 1 + ((((i*n_teams + j) * days) + d) * venues + v)
    cnf = CNF()
    # ULC for every unordered pair (i<j)
    for i,j in combinations(range(n_teams), 2):
        clause = [var(i,j,d,v)
                  for d in range(days)
                  for v in range(venues)]
        cnf.append(clause)              
    # at‑most‑one for each team/(day, venue)
    for t in range(n_teams):
        for d in range(days):
            lits = [var(*sorted((t,o)), d, v)
                     for o in range(n_teams) if o!=t
                     for v in range(venues)]
            for a in range(len(lits)):
                for b in range(a+1, len(lits)):
                    cnf.append([-lits[a], -lits[b]])
    # at‑most‑one for each venue/day
    for v in range(venues):
        for d in range(days):
            games = [var(i,j,d,v) for i,j in combinations(range(n_teams),2)]
            for a in range(len(games)):
                for b in range(a+1, len(games)):
                    cnf.append([-games[a], -games[b]])
    cnf.to_file(fname or f"MVRoundRobin_n{n_teams}_d{days}_v{venues}.cnf")

instances = [(12, 10, 2), (12, 10, 3), (12, 10, 4), (14, 10, 2), (14, 10, 3), (14, 10, 4), (16, 10, 2), (16, 10, 3), (20, 10, 2), (20, 10, 3)]
for n, w, k in instances:
    mvts(n, w, k)