import numpy as np
from numpy.dtypes import StringDType
from typing import Any
import random
from collections import Counter

# from config import Team


def optimize_position(
    matrix: np.ndarray, team_idx: list[int], n_periods: int, r_start: int, r_end: int
) -> np.ndarray:
    """
    Sets the positions of players for certain rows. The rows used (r_start, r_end) represent the
    positions for the team. The optimizer is very simple. It randomizes the players and
    selects a player for the position if that player is not a sub or keeper.
    The next iteration checks if the previous player is now a sub, and then replace. Otherwise
    it takes the player for previous iteration. A counter checks how often a player is on a position
    and the player with lowest count is selected next.

    Parameters:
    matrix (np.array): The matrix with the positions of the players.
    team_idx (list[str]): The list of team members.
    n_periods (int): The number of periods in the game.
    r_start (int): The start index of the column to optimize.
    r_end (int): The end index of the column to optimize.

    Returns:
    np.array: The optimized matrix.
    """
    random.shuffle(team_idx)

    for i in range(n_periods):
        for j in range(r_start, r_end):
            if (i + 1) % 2 == 0:
                position = matrix[j, i - 1]

                if position in matrix[:, i]:
                    loc_sub = np.where(matrix[:, i] == position)[0][0]
                    matrix[j, i] = matrix[loc_sub, i - 1]
                else:
                    matrix[j, i] = matrix[j, i - 1]
            else:
                sorted_pos = [
                    num
                    for (num, cnt) in Counter(
                        np.append(matrix[r_start:r_end, :], team_idx)
                    ).most_common()
                ]

                sorted_pos_vec: np.ndarray = np.flip(np.asarray(sorted_pos))

                val = np.array([el for el in sorted_pos_vec if el not in matrix[:, i]])

                matrix[j, i] = val[0]

    return matrix


def generate_opstelling(
    n_team: int, n_periods: int, team_idx: list[int], keeper_idx: list[int], n_subs: int
) -> np.ndarray:

    random.shuffle(team_idx)
    random.shuffle(keeper_idx)

    # Set a matrix with -1 values tht will be filled
    matrix: np.ndarray = np.full((n_team, n_periods), -1).astype(int)

    # Set the keepers
    matrix[0, np.arange(len(keeper_idx)) * 2] = keeper_idx
    matrix[0, np.arange(len(keeper_idx)) * 2 + 1] = keeper_idx

    # Set the substitutes
    sub_list: list = team_idx * (n_subs + 1)

    for i in range(n_periods):
        for j in range(1, n_subs + 1):
            # t represents the first team member id from the list
            t: int = sub_list[0]

            # Check if the team member is already in the column
            if np.isin(t, matrix[:, i]):
                # Take the next element in the list given t is Keeper
                t = sub_list[1]
                # Check if team member was sub in previous period, if yes take next
                if np.isin(t, matrix[-n_subs:, i - 1]):
                    t = sub_list.pop(2)
                else:
                    t = sub_list.pop(1)
                matrix[j * -1, i] = t
            else:
                sub_list.remove(t)
                matrix[j * -1, i] = t

    matrix = optimize_position(matrix, team_idx, n_periods, 1, 2)  # Attackers
    matrix = optimize_position(matrix, team_idx, n_periods, 2, 4)  # Midfield
    matrix = optimize_position(matrix, team_idx, n_periods, 4, 6)  # Defenders

    return matrix


def create_team_table(
    matrix: np.ndarray, team_members: list[str], positions: list[str], n_parts: int
) -> list[Any]:

    team_array = np.array(team_members)

    matrix_str: np.ndarray = team_array[matrix]

    matrix_str_condensed: np.ndarray = np.zeros(
        (matrix_str.shape[0], n_parts), dtype=StringDType()
    )

    # Condens the table to the number of parts
    for i in range(n_parts):
        for j in range(matrix.shape[0]):
            if matrix_str[j, i * 2] == matrix_str[j, i * 2 + 1]:
                matrix_str_condensed[j, i] = matrix_str[j, i * 2]
            else:
                matrix_str_condensed[j, i] = (
                    f"{matrix_str[j, i *2]} -> {matrix_str[j, i*2+1]}"
                )

    matrix_to_list: list[Any] = matrix_str_condensed.tolist()

    [row.insert(0, task) for task, row in zip(positions, matrix_to_list)]

    return matrix_to_list
