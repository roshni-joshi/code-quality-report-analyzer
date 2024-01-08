"""
This module contains test functions for functions present in smell_analysis/analysis.py
"""
# Disabling C0116 because there is no need for docstrings in the test function
# pylint: disable=C0116

import unittest
from unittest.mock import patch
import pandas as pd

from code_quality_analyzer_analysis.smell_analysis.analysis import (
    analyze_smells, analyze_smell_files, analyze_smell_files_in_folder,
    load_and_prepare_data, retrieve_smell_files
)

class TestSmellAnalysis(unittest.TestCase):
    """
    This class contains test functions for functions present in smell_analysis/analysis.py
    """
    project_name = "Project Name"
    package_name = "Package Name"
    architecture_smell = "Architecture Smell"
    sample_folder = "/sample_folder/"
    design_smell_file_path = f"{sample_folder}DesignSmells.csv"
    testability_smell_file_path = f"{sample_folder}TestabilitySmells.csv"
    architecture_smell_file_path = f"{sample_folder}ArchitectureSmells.csv"
    implementation_smell_file_path = f"{sample_folder}ImplementationSmells.csv"
    test_smell_file_path = f"{sample_folder}TestSmells.csv"

    # Mocked return values for functions
    load_and_prepare_data_mock = pd.DataFrame({
        "Smell": ["Smell1", "Smell2", "Smell1"],
        "Concatenated_Column": ["EntityA", "EntityB", "EntityA"]
    })

    analyze_smells_mock = {
        "smell_distribution": {"Smell1": 2, "Smell2": 1},
        "top_entities": {"EntityA": 2, "EntityB": 1},
        "total_smells": 3,
    }

    pandas_dataframe_mock = pd.DataFrame({
        project_name: ["maven", "maven-core", "maven-compact"],
        package_name: ["org.apache.maven.api", "org.apache.maven.artifact",
                       "org.apache.maven.toolchain.building"],
        architecture_smell: ["Feature Concentration", "Dense Structure", "Unstable Dependency"]
    })

    retrieve_smell_files_mock = {
        "Architecture": None,
        "Design": design_smell_file_path,
        "Implementation": None,
        "Testability": testability_smell_file_path,
        "Test": None
    }

    retrieve_smell_files_empty_mock = {
        "Architecture": None,
        "Design": None,
        "Implementation": None,
        "Testability": None,
        "Test": None
    }

    analyze_smell_files_mock = {
        architecture_smell: None,
        "Design Smell": {
            "smell_distribution": {"Smell1": 2, "Smell2": 1},
            "top_entities": {"EntityA": 2, "EntityB": 1},
            "total_smells": 3,
        },
        "Implementation Smell": None,
        "Testability Smell": {
            "smell_distribution": {"Smell3": 5, "Smell4": 8},
            "top_entities": {"EntityC": 7, "EntityD": 10},
            "total_smells": 17,
        },
        "Test Smell": None,
        "total_smells": 20
    }

    analyze_smell_files_empty_mock = {
        architecture_smell: None,
        "Design Smell": None,
        "Implementation Smell": None,
        "Testability Smell": None,
        "Test Smell": None,
        "total_smells": 0
    }

    @patch("pandas.read_csv", return_value=pandas_dataframe_mock)
    def test_load_and_prepare_data_file_exists(self, _):
        result = load_and_prepare_data(
            self.architecture_smell_file_path, [self.project_name, self.package_name]
        )
        expected = self.pandas_dataframe_mock.copy()
        expected["Concatenated_Column"] = pd.Series(
            ["maven||org.apache.maven.api", "maven-core||org.apache.maven.artifact",
             "maven-compact||org.apache.maven.toolchain.building"]
        )
        pd.testing.assert_frame_equal(result, expected)

    @patch("pandas.read_csv", side_effect=FileNotFoundError("File not found"))
    def test_load_and_prepare_data_file_does_not_exist(self, _):
        result = load_and_prepare_data(
            self.architecture_smell_file_path, [self.project_name, self.package_name]
        )
        self.assertEqual(result, "File not found")

    def test_analyze_smell_some(self):
        result = analyze_smells(self.load_and_prepare_data_mock, "Smell")
        expected = {
            "smell_distribution": {
                "Smell1": 2,
                "Smell2": 1,
            },
            "top_entities": {
                "EntityA": 2,
                "EntityB": 1,
            },
            "total_smells": 3
        }
        self.assertDictEqual(result, expected)

    def test_analyze_smell_none(self):
        dataframe_no_data = pd.DataFrame(columns=["Smell", "Concatenated_Column"])
        result = analyze_smells(dataframe_no_data, "Smell")
        expected = {
            "smell_distribution": {},
            "top_entities": {},
            "total_smells": 0
        }
        self.assertDictEqual(result, expected)

    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.load_and_prepare_data",
           return_value=load_and_prepare_data_mock)
    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.analyze_smells",
           return_value=analyze_smells_mock)
    def test_analyze_smell_files_all(self, _, __):
        result = analyze_smell_files(
            self.architecture_smell_file_path, self.design_smell_file_path,
            self.implementation_smell_file_path, self.testability_smell_file_path,
            self.test_smell_file_path
        )
        self.assertEqual(result["total_smells"], 15)
        for key, value in result.items():
            if key == "total_smells":
                continue
            # pylint: disable=E1136
            self.assertEqual(value["total_smells"], 3)
            self.assertDictEqual(value["smell_distribution"], {"Smell1": 2, "Smell2": 1})
            self.assertDictEqual(value["top_entities"], {"EntityA": 2, "EntityB": 1})

    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.load_and_prepare_data",
           return_value=load_and_prepare_data_mock)
    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.analyze_smells",
           return_value=analyze_smells_mock)
    def test_analyze_smell_files_missing(self, _, __):
        result = analyze_smell_files(
            "", self.design_smell_file_path,
            self.implementation_smell_file_path,"", self.test_smell_file_path
        )
        self.assertEqual(result["total_smells"], 9)
        for key, value in result.items():
            if value:
                if key == "total_smells":
                    continue
                # pylint: disable=E1136
                self.assertEqual(value["total_smells"], 3)
                self.assertDictEqual(
                    value["smell_distribution"], {"Smell1": 2, "Smell2": 1}
                )
                self.assertDictEqual(value["top_entities"], {"EntityA": 2, "EntityB": 1})
            else:
                self.assertIsNone(value)

    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.load_and_prepare_data",
           return_value=load_and_prepare_data_mock)
    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.analyze_smells",
           return_value=analyze_smells_mock)
    def test_analyze_smell_files_none(self, _, __):
        result = analyze_smell_files("", "", "", "", "")

        self.assertEqual(result["total_smells"], 0)
        for key, value in result.items():
            if key == "total_smells":
                continue
            self.assertIsNone(value)

    @patch("os.listdir", return_value=[
        "ArchitectureSmells.csv", "DesignSmells.csv", "ImplementationSmells.csv",
        "TestabilitySmells.csv", "TestSmells.csv"])
    @patch("os.path.isfile", return_value=True)
    def test_retrieve_smell_files_all(self, _, __):
        result = retrieve_smell_files(self.sample_folder)
        self.assertEqual(result["Architecture"], self.architecture_smell_file_path)
        self.assertEqual(result["Design"], self.design_smell_file_path)
        self.assertEqual(result["Implementation"], self.implementation_smell_file_path)
        self.assertEqual(result["Testability"], self.testability_smell_file_path)
        self.assertEqual(result["Test"], self.test_smell_file_path)

    @patch("os.listdir", return_value=[
        "ArchitectureSmells.csv", "DesignSmells.csv", "TestSmells.csv"])
    @patch("os.path.isfile", return_value=True)
    def test_retrieve_smell_files_missing(self, _, __):
        result = retrieve_smell_files(self.sample_folder)
        self.assertEqual(result["Architecture"], self.architecture_smell_file_path)
        self.assertEqual(result["Design"], self.design_smell_file_path)
        self.assertIsNone(result["Implementation"])
        self.assertIsNone(result["Testability"])
        self.assertEqual(result["Test"], self.test_smell_file_path)

    @patch("os.listdir", return_value=[])
    @patch("os.path.isfile", return_value=True)
    def test_retrieve_smell_files_none(self, _, __):
        # body of test_retrieve_no_smell_files
        result = retrieve_smell_files(self.sample_folder)
        self.assertIsNone(result["Architecture"])
        self.assertIsNone(result["Design"])
        self.assertIsNone(result["Implementation"])
        self.assertIsNone(result["Testability"])
        self.assertIsNone(result["Test"])

    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.retrieve_smell_files",
           return_value=retrieve_smell_files_mock)
    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.analyze_smell_files",
           return_value=analyze_smell_files_mock)
    def test_analyze_smell_files_in_folder_some(self, _, __):
        result = analyze_smell_files_in_folder(self.sample_folder)
        self.assertEqual(result, self.analyze_smell_files_mock)

    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.retrieve_smell_files",
           return_value=retrieve_smell_files_empty_mock)
    @patch("code_quality_analyzer_analysis.smell_analysis.analysis.analyze_smell_files",
           return_value=analyze_smell_files_empty_mock)
    def test_analyze_smell_files_in_folder_empty(self, _, __):
        result = analyze_smell_files_in_folder(self.sample_folder)
        self.assertEqual(result, self.analyze_smell_files_empty_mock)
