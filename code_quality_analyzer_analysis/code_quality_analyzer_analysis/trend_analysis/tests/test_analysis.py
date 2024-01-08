"""
This module contains test functions for functions present in trend_analysis/analysis.py
"""
import copy
import unittest
from unittest.mock import patch

import pandas as pd
from code_quality_analyzer_analysis.trend_analysis.analysis import (
    analyze_commit_folders_in_folder, get_smell_commit_changes,
    get_total_lines_of_code, get_smell_density_full_repo, calculate_smell_density
)

# Disabling C0116 because there is no need for docstrings in the test function
# pylint: disable=C0116


class TestTrendAnalysis(unittest.TestCase):
    """
    This class contains test functions for functions present in trend_analysis/analysis.py
    """
    architecture_smell = "Architecture Smell"
    design_smell = "Design Smell"
    implementation_smell = "Implementation Smell"
    testability_smell = "Testability Smell"
    test_smell = "Test Smell"
    sample_folder = "/sample_folder/"
    # Mocked return values for functions
    analyze_smell_files_mock = {
        architecture_smell: None,
        design_smell: {
            "smell_distribution": {"Smell1": 2, "Smell2": 1},
            "top_entities": {"EntityA": 2, "EntityB": 1},
            "total_smells": 3,
        },
        implementation_smell: None,
        testability_smell: {
            "smell_distribution": {"Smell3": 5, "Smell4": 8},
            "top_entities": {"EntityC": 7, "EntityD": 10},
            "total_smells": 13,
        },
        test_smell: None,
        "total_smells": 16,
        "user": "user1"
    }

    analyze_smell_files_empty_mock = {
        architecture_smell: None,
        design_smell: None,
        implementation_smell: None,
        testability_smell: None,
        test_smell: None,
        "total_smells": 0,
        "user": "user1"
    }

    full_repo_mock = {
        "full_repo": {
            "c0": analyze_smell_files_empty_mock,
            "c1": analyze_smell_files_mock,
            "c2": analyze_smell_files_empty_mock,
            "c3": analyze_smell_files_mock,
        }
    }

    full_repo_smell_density_mock = {
        "full_repo_smell_density": {
                "c0": {
                    architecture_smell: None,
                    design_smell: None,
                    implementation_smell: None,
                    testability_smell: None,
                    test_smell: None,
                    "total_smells": 0.0,
                    "user": "user1"
                },
                "c1": {
                    architecture_smell: None,
                    design_smell: {
                        "smell_distribution": {
                            "Smell1": 0.2,
                            "Smell2": 0.1
                        },
                        "top_entities": {"EntityA": 2, "EntityB": 1},
                        "total_smells": 0.3
                    },
                    implementation_smell: None,
                    testability_smell: {
                        "smell_distribution": {
                            "Smell3": 0.5,
                            "Smell4": 0.8
                        },"top_entities": {"EntityC": 7, "EntityD": 10},
                        "total_smells": 1.3
                    },
                    test_smell: None,
                    "total_smells": 1.6,
                    "user": "user1"
                },
                "c2": {
                    architecture_smell: None,
                    design_smell: None,
                    implementation_smell: None,
                    testability_smell: None,
                    test_smell: None,
                    "total_smells": 0.0,
                    "user": "user1"
                },
                "c3": {
                    architecture_smell: None,
                    design_smell: {
                        "smell_distribution": {
                            "Smell1": 0.2,
                            "Smell2": 0.1
                        },"top_entities": {"EntityA": 2, "EntityB": 1},
                        "total_smells": 0.3
                    },
                    implementation_smell: None,
                    testability_smell: {
                        "smell_distribution": {
                            "Smell3": 0.5,
                            "Smell4": 0.8
                        },"top_entities": {"EntityC": 7, "EntityD": 10},
                        "total_smells": 1.3
                    },
                    test_smell: None,
                    "total_smells": 1.6,
                    "user": "user1"
                }
            }
    }

    commit_changes_mock = {
        "commit_changes": {
                "c1": {
                    architecture_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    design_smell: {
                        "smell_distribution": {
                            "Smell1": 2,
                            "Smell2": 1
                        },
                        "total_smells": 3
                    },
                    implementation_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    testability_smell: {
                        "smell_distribution": {
                            "Smell3": 5,
                            "Smell4": 8
                        },
                        "total_smells": 13
                    },
                    test_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    "total_smells": 16,
                    "user": "user1"
                },
                "c2": {
                    architecture_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    design_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    implementation_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    testability_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    test_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    "total_smells": 0,
                    "user": "user1"
                },
                "c3": {
                    architecture_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    design_smell: {
                        "smell_distribution": {
                            "Smell1": 2,
                            "Smell2": 1
                        },
                        "total_smells": 3
                    },
                    implementation_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    testability_smell: {
                        "smell_distribution": {
                            "Smell3": 5,
                            "Smell4": 8
                        },
                        "total_smells": 13
                    },
                    test_smell: {
                        "smell_distribution": {

                        },
                        "total_smells": 0
                    },
                    "total_smells": 16,
                    "user": "user1"
                }
            }
    }

    pandas_dataframe_mock = pd.DataFrame({
        "Project Name": ["maven", "maven-core", "maven-compact"],
        "Package Name": [
            "org.apache.maven.api", "org.apache.maven.artifact",
            "org.apache.maven.toolchain.building"
        ],
        "LOC": [20, 40, 10]
    })

    pandas_dataframe_empty_mock = pd.DataFrame({
        "Project Name": [],
        "Package Name": [],
        "LOC": []
    })


    @patch("code_quality_analyzer_analysis.trend_analysis.analysis.analyze_smell_files_in_folder",
           side_effect=[analyze_smell_files_empty_mock,
                        analyze_smell_files_mock,
                        analyze_smell_files_empty_mock,
                        analyze_smell_files_mock,
                        ]
           )
    @patch("code_quality_analyzer_analysis.trend_analysis.analysis.get_smell_density_full_repo",
           return_value={**full_repo_mock, **copy.deepcopy(full_repo_smell_density_mock)})
    @patch("code_quality_analyzer_analysis.trend_analysis.analysis.get_smell_commit_changes",
           return_value={
               **full_repo_mock, **copy.deepcopy(full_repo_smell_density_mock),
               **commit_changes_mock
           })
    def test_analyze_commit_folders_in_folder(self, _, __, ___):
        result = analyze_commit_folders_in_folder(
            "/sample_folder/", ["c1", "c2", "c3"], "c0",
            ["user1", "user1", "user1"], "user2"
        )
        expected = {
            "full_repo": {
                "c1": self.analyze_smell_files_mock,
                "c2": self.analyze_smell_files_empty_mock,
                "c3": self.analyze_smell_files_mock
            },
            "full_repo_smell_density": {
                "c1": self.full_repo_smell_density_mock["full_repo_smell_density"]["c1"],
                "c2": self.full_repo_smell_density_mock["full_repo_smell_density"]["c2"],
                "c3": self.full_repo_smell_density_mock["full_repo_smell_density"]["c3"]
            },
            "commit_changes": {
                "c1": self.commit_changes_mock["commit_changes"]["c1"],
                "c2": self.commit_changes_mock["commit_changes"]["c2"],
                "c3": self.commit_changes_mock["commit_changes"]["c3"]
            }
        }
        self.assertEqual(result, expected)

    def test_get_smell_commit_changes(self):
        commits = ["c0", "c1", "c2", "c3"]
        users = ["user2", "user1", "user1", "user1"]
        full_repo_mock = {
            "full_repo": {
                "c0": self.analyze_smell_files_empty_mock,
                "c1": self.analyze_smell_files_mock,
                "c2": self.analyze_smell_files_empty_mock,
                "c3": self.analyze_smell_files_mock,
            }
        }
        result = get_smell_commit_changes(full_repo_mock, commits, users)
        expected = {
            "full_repo": full_repo_mock["full_repo"],
            "commit_changes": self.commit_changes_mock["commit_changes"]
        }
        print(result)
        self.assertEqual(result, expected)

    @patch("pandas.read_csv", return_value=pandas_dataframe_mock)
    def test_get_total_lines_of_code(self, _):

        metrics_file_path = "test.csv"
        column_sum = "LOC"
        expected_lines_of_code = 70

        total_lines_of_code = get_total_lines_of_code(metrics_file_path, column_sum)

        self.assertEqual(total_lines_of_code, expected_lines_of_code)

    @patch("pandas.read_csv", return_value=pandas_dataframe_empty_mock)
    def test_get_total_lines_of_code_empty_case(self, _):

        metrics_file_path = "test.csv"
        column_sum = "LOC"
        expected_lines_of_code = 0

        total_lines_of_code = get_total_lines_of_code(metrics_file_path, column_sum)

        self.assertEqual(total_lines_of_code, expected_lines_of_code)

    @patch("code_quality_analyzer_analysis.trend_analysis.analysis.get_total_lines_of_code",
           return_value=10000)
    def test_get_smell_density_full_repo(self, _):
        full_repo_mock = {
            "full_repo": {
                "c0": copy.deepcopy(self.analyze_smell_files_empty_mock),
                "c1": copy.deepcopy(self.analyze_smell_files_mock),
                "c2": copy.deepcopy(self.analyze_smell_files_empty_mock),
                "c3": copy.deepcopy(self.analyze_smell_files_mock)
            }
        }
        expected = {
            "full_repo": full_repo_mock["full_repo"],
            "full_repo_smell_density": self.full_repo_smell_density_mock["full_repo_smell_density"]
        }

        result = get_smell_density_full_repo(full_repo_mock, "test_folder")
        self.assertDictEqual(result, expected)

    def test_calculate_smell_density(self):
        total_smells = 1
        total_lines_of_code = 1000
        expected = 1.0
        result = calculate_smell_density(total_smells, total_lines_of_code)

        self.assertEqual(result,expected)

    def test_calculate_smell_density_zero_lines(self):
        total_smells = 0
        total_lines_of_code = 0
        expected = 0.0
        result = calculate_smell_density(total_smells, total_lines_of_code)

        self.assertEqual(result,expected)
