"""
This module contains test functions for views present in views.py
"""
import json
from unittest.mock import patch
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

# Disabling C0116 because there is no need for docstrings in the test function
# pylint: disable=C0116

ALL_COMMITS_ANALYSIS_PATH = "test_files"
SINGLE_COMMIT_ANALYSIS_PATH = f"{ALL_COMMITS_ANALYSIS_PATH}/commit1"


def load_json_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


class SmellAnalysisViewTests(APITestCase):
    """
    This class contains test functions for one commit analysis view
    """

    def setUp(self) -> None:
        self.url = reverse("smell_analysis")
        self.path = "some/valid/path"

    @patch("code_quality_analyzer_analysis.views.analyze_smell_files_in_folder")
    def test_post_with_no_path(self, mock_analyze):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_analyze.assert_not_called()

    @patch("code_quality_analyzer_analysis.views.analyze_smell_files_in_folder")
    def test_post_with_valid_path(self, mock_analyze):
        mock_analyze.return_value = {"result": "some_result"}
        data = {"reportPath": self.path}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analyze.assert_called_once_with(self.path)

    def test_post_full_functionality(self):
        one_commit_response_path = "code_quality_analyzer_analysis/tests/one_commit.json"
        one_commit_analysis_response = load_json_data(one_commit_response_path)
        data = {"reportPath": SINGLE_COMMIT_ANALYSIS_PATH}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data, one_commit_analysis_response)


class TrendAnalysisViewTests(APITestCase):
    """
    This class contains test functions for trend analysis view
    """

    def setUp(self) -> None:
        self.url = reverse("trend_analysis")
        self.path = "some/path"

    @patch("code_quality_analyzer_analysis.views.analyze_commit_folders_in_folder")
    def test_post_with_no_path(self, mock_analyze):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_analyze.assert_not_called()

    @patch("code_quality_analyzer_analysis.views.analyze_commit_folders_in_folder")
    def test_post_with_no_commits_data(self, mock_analyze):
        data = {"reportPath": self.path}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_analyze.assert_not_called()

    @patch("code_quality_analyzer_analysis.views.analyze_commit_folders_in_folder")
    def test_post_with_no_previous_commit(self, mock_analyze):
        mock_analyze.return_value = {"result": "some_result"}
        data = {
            "reportPath": self.path,
            "commitsData": {
                "commit1": "user1",
                "commit2": "user2",
            }
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analyze.assert_called_once_with(
            self.path, ["commit2", "commit1"], "", ["user2", "user1"], ""
        )

    @patch("code_quality_analyzer_analysis.views.analyze_commit_folders_in_folder")
    def test_post_with_complete_data(self, mock_analyze):
        mock_analyze.return_value = {"result": "some_result"}
        data = {
            "reportPath": self.path,
            "commitsData": {
                "commit1": "user1",
                "commit2": "user2",
            },
            "previousCommit": {
                "commit0": "user0"
            }
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analyze.assert_called_once_with(
            self.path, ["commit2", "commit1"], "commit0", ["user2", "user1"], "user0"
        )

    def test_post_full_functionality(self):
        trend_response_path = "code_quality_analyzer_analysis/tests/trend.json"
        trend_analysis_response = load_json_data(trend_response_path)

        data = {
            "reportPath": f"{ALL_COMMITS_ANALYSIS_PATH}",
            "commitsData": {
                "commit5": "user5",
                "commit4": "user4",
                "commit3": "user3",
                "commit2": "user2",
            },
            "previousCommit": {
                "commit1": "user1"
            }
        }
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data, trend_analysis_response)


class HotspotAnalysisViewTests(APITestCase):
    """
    This class contains test functions for hotspot analysis
    """

    def setUp(self) -> None:
        self.url = reverse("hotspot_analysis")
        self.path = "some/valid/path"

    @patch("code_quality_analyzer_analysis.views.get_hotspot_analysis")
    def test_post_with_no_path(self, mock_analyze):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        mock_analyze.assert_not_called()

    @patch("code_quality_analyzer_analysis.views.get_hotspot_analysis")
    def test_post_with_valid_path(self, mock_analyze):
        mock_analyze.return_value = {"result": "some_result"}
        data = {"reportPath": self.path}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        mock_analyze.assert_called_once_with(self.path)

    def test_post_full_functionality(self):
        hotspot_response_path = "code_quality_analyzer_analysis/tests/hotspot.json"
        hotspot_analysis_response = load_json_data(hotspot_response_path)
        data = {"reportPath": SINGLE_COMMIT_ANALYSIS_PATH}
        response = self.client.post(self.url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response_data = response.json()
        self.assertEqual(response_data, hotspot_analysis_response)
