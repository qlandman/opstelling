from tabulate import tabulate
from typing import List
import numpy as np
import random

num_periods: int = 8

team_members: List[str] = [
    "Benjamin",
    "Vik",
    "Vigo",
    "Can",
    "Njabulo",
    "Lars",
    "Sebas",
    "Kees",
    "Hamza",
]

tasks = [
    "Keeper",
    "Aanvaller",
    "Middenvelder 1",
    "Middenvelder 2",
    "Verdediger 1",
    "Verdediger 2",
]

excl_team: List[str] = ["Lars", "Kees"]

keepers: List[str] = ["Hamza", "Vik", "Vigo", "Can"]

play_team: List[str] = [i for i in team_members if i not in excl_team]

n_team: int = len(play_team)
n_tasks: int = len(tasks)
matrix: np.array = np.zeros((n_team, num_periods))
# matrix = [[0 for _ in range(num_periods)] for _ in range(n_tasks)]
print(matrix)
# Create headers
headers = [i + 1 for i in range(num_periods)]


# Set the keepers
keeper_indexes = [team_members.index(keeper) for keeper in keepers]
random.shuffle(keeper_indexes)
matrix[0, np.arange(len(keeper_indexes)) * 2] = keeper_indexes
matrix[0, np.arange(len(keeper_indexes)) * 2 + 1] = keeper_indexes

# matrix[0][i * 2] = keeper
# matrix[0][i * 2 + 1] = keeper
print(matrix)

# Add tasks row
# for i, row in enumerate(matrix):
#     row.insert(0, tasks[i])


print(tabulate(matrix, headers=headers, tablefmt="grid"))


print(keeper_indexes)
