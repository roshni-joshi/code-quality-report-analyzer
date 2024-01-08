"""
This module contains functions for various trend analysis
"""

import copy

import pandas as pd

from code_quality_analyzer_analysis.smell_analysis.analysis import (analyze_smell_files_in_folder)

def get_total_lines_of_code(metrics_file_path: str, column_sum: str) -> int:
    """
    Takes the metrics csv file path as input and fetches the total Lines of Code for the commit
    eg: TypeMetrics.csv file
    :param metrics_file_path: Path of csv file containing the metrics of the repository
    :param column_sum: Name of the column in csv that contains the LOC. This column will be summed
    :return: integer representing the total Lines of Code
    """

    # Read CSV file, to extract the LOC
    df = pd.read_csv(metrics_file_path)

    # Calculate the SUM of LOC, as the file has LOC for each class/smell_type,
    # but we need total LOC of project
    total_lines_of_code = df[column_sum].sum()

    return total_lines_of_code


def get_smell_commit_changes(trend_analysis_dict: dict, commits: list, users: list) -> dict:
    """
    Calculates the difference between adjacent commits smells
    :param trend_analysis_dict: Dictionary containing all commits smells
    :param commits: List representing order of commits
    :param users: List representing order of users as per commit
    :return: dictionary containing difference between commit smells
    """
    # Disabling R0914 because there can be more than 15 variables for this function
    # pylint: disable=R0914
    trend_analysis_dict["commit_changes"] = {}

    for i in range(1, len(commits)):
        current_commit = commits[i]
        previous_commit = commits[i - 1]

        trend_analysis_dict["commit_changes"][current_commit] = {
            "Architecture Smell": {
                "smell_distribution": {},
                "total_smells": 0
            },
            "Design Smell": {
                "smell_distribution": {},
                "total_smells": 0
            },
            "Implementation Smell": {
                "smell_distribution": {},
                "total_smells": 0
            },
            "Testability Smell": {
                "smell_distribution": {},
                "total_smells": 0
            },
            "Test Smell": {
                "smell_distribution": {},
                "total_smells": 0
            },
            "total_smells": 0,
            "user": users[i],
        }

        current_commit_dict = trend_analysis_dict["full_repo"][current_commit]
        previous_commit_dict = trend_analysis_dict["full_repo"][previous_commit]

        total_smells = 0
        # Iterate over the smell types
        for smell_type in current_commit_dict:
            if isinstance(current_commit_dict[smell_type], dict):
                total_smell_type = 0
                # Iterate over the smell subtypes
                for subtype in current_commit_dict[smell_type]["smell_distribution"]:
                    # Get current commit subtype smell stats
                    current_commit_smell_value = (
                        current_commit_dict[smell_type]["smell_distribution"].get(subtype, 0)
                    )
                    # Get previous commit subtype smell stats
                    previous_commit_smell_value = 0
                    if isinstance(previous_commit_dict[smell_type], dict):
                        previous_commit_smell_value = (
                            previous_commit_dict[smell_type]["smell_distribution"].get(subtype, 0)
                        )
                    # Subtract previous from current
                    smell_sub = current_commit_smell_value - previous_commit_smell_value
                    # Only add if the difference is greater than 0
                    if smell_sub > 0:
                        commit_changes = trend_analysis_dict["commit_changes"]
                        current_commit_data = commit_changes[current_commit]
                        type_data = current_commit_data[smell_type]
                        smell_distribution = type_data["smell_distribution"]
                        smell_distribution[subtype] = smell_sub
                        total_smell_type += smell_sub

                # Calculate the total smells for the smell_type
                commit_changes = trend_analysis_dict["commit_changes"]
                current_commit_data = commit_changes[current_commit]
                type_data = current_commit_data[smell_type]
                type_data["total_smells"] = total_smell_type

                total_smells += total_smell_type

        # Calculate the overall total smells
        trend_analysis_dict["commit_changes"][current_commit]["total_smells"] = total_smells

    return trend_analysis_dict


def get_smell_density_full_repo(trend_analysis_dict, folder_path) -> dict:
    """
    Calculates the smell density for the given smell counts for full repository
    :param trend_analysis_dict: Dictionary containing all commits smells
    :param folder_path: Path containing the CSV files having smells data
    :return: dictionary containing 1 extra field "full_repo_smell_density", containing smell density
    """
    trend_analysis_dict["full_repo_smell_density"] = {}
    trend_analysis_dict["full_repo_smell_density"] = copy.deepcopy(trend_analysis_dict["full_repo"])
    full_repo_density_dict = trend_analysis_dict["full_repo_smell_density"]
    # Calculate smell densities for each commit
    for commit_id in full_repo_density_dict:
        if commit_id == "":
            continue
        total_lines_of_code = get_total_lines_of_code(
            folder_path + "/" + commit_id + "/TypeMetrics.csv", "LOC"
        )
        # Iterate over the smell types
        for smell_type in full_repo_density_dict[commit_id]:
            full_repo_smell = full_repo_density_dict[commit_id][smell_type]
            if isinstance(full_repo_smell, dict):
                # Iterate over the smell subtypes
                for subtype in full_repo_smell["smell_distribution"]:
                    full_repo_smell["smell_distribution"][subtype] = (
                        calculate_smell_density(
                            full_repo_smell["smell_distribution"][subtype],
                            total_lines_of_code
                        )
                    )
                # Calculate density for total smells of each smell_type
                full_repo_smell["total_smells"] = (
                    calculate_smell_density(
                        full_repo_smell["total_smells"],
                        total_lines_of_code
                    )
                )

        # Calculate density for total smells
        full_repo_density_dict[commit_id]["total_smells"] = (
            calculate_smell_density(
                full_repo_density_dict[commit_id]["total_smells"], total_lines_of_code
            )
        )
    return trend_analysis_dict


def calculate_smell_density(total_smells, total_lines_of_code) -> float:
    """
    Calculates smell density based on total number of smells per 1000 lines of code.
    Density is rounded till 2 decimal points.

    :param total_smells: The total number of smells in the repository
    :param total_lines_of_code: The total lines of code in the repository
    :return: float, The calculated smell density rounded to 2 decimal places
    """
    if total_lines_of_code == 0:
        return 0.0

    return round(int(total_smells) / (total_lines_of_code / 1000), 2)


def analyze_commit_folders_in_folder(
        folder_path: str, commits: list, before_oldest_commit: str,
        users: list, before_oldest_commit_user: str
) -> dict:
    """
    Analyzes all commit folders in a parent repository folder
    :param folder_path: Path to the folder containing all the commit sub-folders
    :param commits: List of commits in an ordered form. initial commit would be
    first and followed by the more recent ones
    :param users: List of users per commit in an ordered form
    :param before_oldest_commit: Commit hash of the previous commit of the oldest
    commit in oldest_to_latest_ordered_commits
    :param before_oldest_commit_user: user before the oldest commit
    :return: Dictionary containing analysis of all the commits
    """
    trend_analysis_dict = {"full_repo": {}}
    commits.insert(0, before_oldest_commit)
    users.insert(0, before_oldest_commit_user)

    for index, commit in enumerate(commits):
        path = folder_path + "/" + commit

        trend_analysis_dict["full_repo"][commit] = analyze_smell_files_in_folder(path)
        trend_analysis_dict["full_repo"][commit]["user"] = users[index]

    trend_analysis_dict = get_smell_density_full_repo(trend_analysis_dict, folder_path)
    trend_analysis_dict = get_smell_commit_changes(trend_analysis_dict, commits, users)
    trend_analysis_dict["full_repo"].pop(before_oldest_commit, None)
    trend_analysis_dict["full_repo_smell_density"].pop(before_oldest_commit, None)

    return trend_analysis_dict
