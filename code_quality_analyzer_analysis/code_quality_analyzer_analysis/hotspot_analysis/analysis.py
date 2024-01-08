"""
This module contains functions for hotspot analysis
"""

import pandas as pd

from code_quality_analyzer_analysis.smell_analysis.analysis import (
    retrieve_smell_files, load_and_prepare_data
)

# Disabling R0801 because it is showing duplication in variable with the test file
# which is intended.
# pylint: disable=R0801


def get_top_entities(
        df: pd.DataFrame, smell_type: str, smell_subtypes: list,
        concat_column: str = 'Concatenated_Column', top: int = 10
) -> list:
    """
    Analyzes a DataFrame containing information about specific smell and returns a
    list of top entities with smell distribution based on total smell count.

    :param df: DataFrame containing the smell information.
    :param smell_type: The main smell type to be considered
    (e.g., 'Design Smell', 'Implementation Smell').
    :param smell_subtypes: List defining subtypes of the specified smell_type.
    This will be considered for smell_distribution.
    :param concat_column: The name of the column in the DataFrame that contains concatenated
    project, package, type name (and method name).
    :param top: The number of top entities to return. Default is 10.
    :return: A list of dictionaries, where each dictionary represents an entity and includes:
             - The entity's concatenated column value,
             - A dictionary of smell distribution for each subtype,
             - The total number of smells associated with the entity.
            The list will be in descending order based on the total smell count of each entity.
    """
    # Create an empty list to store the results
    result_list = []

    # Iterate over unique values in Concatenated_Column
    for column_value in df[concat_column].unique():

        # Filter the dataframe for the current Concatenated_Column value
        subset_df = df[df[concat_column] == column_value]

        # Creating smell distribution dict, to store count of each sub-type of smell
        smell_distribution = {}
        for smell_subtype in smell_subtypes:
            smell_distribution[smell_subtype] = (
                subset_df[smell_type].str.lower().str.contains(smell_subtype.lower())
            ).sum()

        # Calculate the total number of smells
        total_smells = sum(smell_distribution.values())

        entities = {}
        # Create the final dictionary for the current Concatenated_Column value
        entities[column_value] = {
            'smell_distribution': smell_distribution,
            'total_smells': total_smells
        }

        # Add the entity details to the list of top_entities.
        result_list.append(entities)

    # Sort the list based on total_smells in descending order
    sorted_list = sorted(result_list, key=lambda x: x[next(iter(x))]["total_smells"], reverse=True)

    # Only return top few
    top_entities = sorted_list[:top]

    return top_entities


def get_hotspot_analysis(path: str) -> dict:
    """
    Returns a hotspot analysis based on design and implementation smells by using CSV files.
    top 10 classes with most design smells and top 10 methods with most implementation smells
    will be returned in descending order.

    :param path: The path containing CSV files of design and implementation smells.
    :return: A dictionary containing the results of the hotspot analysis, including
    top classes and methods.
             The dictionary structure is as follows:
             {
                "top_classes_list": List of dictionaries representing top classes,
                "top_methods_list": List of dictionaries representing top methods
             }
    """
    # Get the paths of csv files to process Design and Implementation smells later on.
    path_dict = retrieve_smell_files(path)

    # Load the Design Smells CSV and replace Feature Envy with Abstraction,
    # for easy comparision with sub-types during smell distribution.
    design_df = load_and_prepare_data(
        path_dict["Design"], ["Project Name", "Package Name", "Type Name"]
    )

    design_df['Design Smell'] = design_df['Design Smell'].replace("Feature Envy", "Abstraction")

    # Load the Implementation Smells CSV
    impl_df = load_and_prepare_data(
        path_dict["Implementation"], ["Project Name", "Package Name", "Type Name", "Method Name"]
    )

    # Defining subtypes of implementation smells.
    # This will be used for smell_distribution counting for each sub-type.
    impl_smell_subtypes = [
        "Long Method",
        "Complex Method",
        "Long Parameter List",
        "Long Identifier",
        "Long Statement",
        "Complex Conditional",
        "Virtual Method Call from Constructor",
        "Empty Catch Clause",
        "Magic Number",
        "Duplicate Code",
        "Missing Default"]

    # Defining subtypes of design smells.
    # This will be used for smell_distribution counting for each sub-type.
    design_smell_subtypes = [
        "Abstraction",
        "Encapsulation",
        "Modularization",
        "Hierarchy"]

    # Fetch the top classes and methods along with their smell_distribution as per subtypes.
    class_list = get_top_entities(design_df, "Design Smell", design_smell_subtypes)
    method_list = get_top_entities(impl_df, "Implementation Smell", impl_smell_subtypes)

    # Merge both lists into a dictionary.
    result = {
        "top_classes_list": class_list,
        "top_methods_list": method_list
    }

    return result
