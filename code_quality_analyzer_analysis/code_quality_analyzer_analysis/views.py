"""
This module contains views for various types of analysis.

It includes:
- SmellAnalysisView: Provides a view for one commit analysis data
- TrendAnalysisView: Provides a view for trend analysis data.
- HotspotAnalysisView: Provides a view for hotspot analysis data.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from code_quality_analyzer_analysis.smell_analysis.analysis import analyze_smell_files_in_folder

from code_quality_analyzer_analysis.trend_analysis.analysis import analyze_commit_folders_in_folder

from code_quality_analyzer_analysis.hotspot_analysis.analysis import get_hotspot_analysis


ERROR_MESSAGE = "No path provided"

class SmellAnalysisView(APIView):
    """
    SmellAnalysisView provides an interface for handling requests related to one commit analysis.
    """

    def post(self, request):
        """
        Handles the POST request to analyze smell files.

        This method retrieves the 'reportPath' from the request data, validates it,
        and then performs the smell analysis using the 'analyze_smell_files_in_folder' function.
        If the 'reportPath' is not provided, it returns a 400 Bad Request response.
        On successful analysis, it returns the analysis results with a 200 OK status.

        Parameters:
        - request: The request object containing the data sent by the client.

        Returns:
        - Response: A Django REST framework Response object with either the analysis results
                    and a 200 OK status, or an error message and a 400 Bad Request status.
        """
        path = request.data.get('reportPath', None)

        if not path:
            return Response({"error": ERROR_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        results = analyze_smell_files_in_folder(path)
        return Response(results, status=status.HTTP_200_OK)


class TrendAnalysisView(APIView):
    """
    TrendAnalysisView provides an interface for handling requests related to trend analysis.
    """

    def post(self, request):
        """
        Handles the POST request to analyze smell files.

        This method retrieves the 'reportPath', 'commitsData', 'previousCommit' from the request
        data, validates them, and then performs the smell analysis using the
        'analyze_commit_folders_in_folder' function. If the 'reportPath' or 'commitsData' is not
        provided, it returns a 400 Bad Request response. On successful analysis, it returns the
        analysis results with a 200 OK status.

        Parameters:
        - request: The request object containing the data sent by the client.

        Returns:
        - Response: A Django REST framework Response object with either the analysis results
                    and a 200 OK status, or an error message and a 400 Bad Request status.
        """
        report_path = request.data.get('reportPath', None)
        commits_data = request.data.get('commitsData', None)
        previous_commit = request.data.get('previousCommit', None)

        if not report_path:
            return Response({"error": ERROR_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)
        if not commits_data:
            return Response(
                {"error": "No commitsData provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        commits = list(commits_data.keys())
        users = list(commits_data.values())
        before_oldest_commit = ""
        before_oldest_commit_user = ""
        if previous_commit:
            before_oldest_commit = list(previous_commit.keys())[0]
            before_oldest_commit_user = list(previous_commit.values())[0]

        results = analyze_commit_folders_in_folder(
            report_path, commits[::-1], before_oldest_commit, users[::-1], before_oldest_commit_user
        )
        return Response(results, status=status.HTTP_200_OK)


class HotspotAnalysisView(APIView):
    """
    HotspotAnalysisView provides an interface for handling requests related to hotspot analysis.
    """

    def post(self, request):
        """
        Handles the POST request to analyze smell files.

        This method retrieves the 'reportPath' from the request data, validates it,
        and then performs the smell analysis using the 'get_hotspot_analysis' function.
        If the 'reportPath' is not provided, it returns a 400 Bad Request response.
        On successful analysis, it returns the analysis results with a 200 OK status.

        Parameters:
        - request: The request object containing the data sent by the client.

        Returns:
        - Response: A Django REST framework Response object with either the analysis results
                    and a 200 OK status, or an error message and a 400 Bad Request status.
        """
        path = request.data.get('reportPath', None)

        if not path:
            return Response({"error": ERROR_MESSAGE}, status=status.HTTP_400_BAD_REQUEST)

        results = get_hotspot_analysis(path)
        return Response(results, status=status.HTTP_200_OK)
