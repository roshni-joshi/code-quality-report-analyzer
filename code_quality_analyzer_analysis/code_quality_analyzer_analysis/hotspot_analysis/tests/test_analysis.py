"""
This module contains test functions for functions present in hotspot_analysis/analysis.py
"""
import unittest
from unittest.mock import patch

import pandas as pd
from code_quality_analyzer_analysis.hotspot_analysis.analysis import (
    get_top_entities, get_hotspot_analysis
)

# Disabling C0116 because there is no need for docstrings in the test function
# pylint: disable=C0116

class TestHotspotAnalysis(unittest.TestCase):
    """
    This class contains test functions for functions present in hotspot_analysis/analysis.py
    """
    design_smell = "Design Smell"
    implementation_smell = "Implementation Smell"
    sample_folder = "/sample_folder/"
    design_smell_subtypes = [
        "Abstraction",
        "Encapsulation",
        "Modularization",
        "Hierarchy"]
    maven_wrapper_downloader = \
        "Retail-Product-Management-System||(default package)||MavenWrapperDownloader"
    unutilized_abstraction = "Unutilized Abstraction"
    unnecessary_abstraction = "Unnecessary Abstraction"
    m2_package = "Retail-Product-Management-System||(default package)||MavenWrapperDownloader||m2"
    m3_package = "Retail-Product-Management-System||(default package)||MavenWrapperDownloader||m3"
    long_method = "Long Method"
    magic_number = "Magic Number"
    long_statement = "Long Statement"
    empty_catch_clause = "Empty Catch Clause"
    long_parameter_list = "Long Parameter List"
    complex_method = "Complex Method"
    missing_default = "Missing Default"
    duplicate_code = "Duplicate Code"
    long_identifier = "Long Identifier"
    virtual_method_call = "Virtual Method Call from Constructor"
    complex_conditional = "Complex Conditional"

    design_df = pd.DataFrame({
        "Concatenated_Column": [maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                maven_wrapper_downloader,
                                "Retail-Product-Management-System||com.product.microservices.api"
                                "gatewayauth||ApiGatewayAuthApplication",
                                "Retail-Product-Management-System||com.product.microservices."
                                "apigatewayauth.filters||JwtRequestFilter",
                                "Retail-Product-Management-System||com.product.microservices."
                                "apigatewayauth.model||User"],
        "Design Smell": ["Abstraction",
                        unutilized_abstraction,
                        unutilized_abstraction,
                        unnecessary_abstraction,
                        unutilized_abstraction,
                        unnecessary_abstraction,
                        unutilized_abstraction,
                        unutilized_abstraction,
                        unutilized_abstraction,
                        unnecessary_abstraction]
    })

    impl_df = pd.DataFrame({
        "Concatenated_Column": ["Retail-Product-Management-System||(default package)||"
                                "MavenWrapperDownloader||m1",
                                m2_package,
                                m2_package,
                                m2_package,
                                m2_package,
                                m3_package,
                                m3_package,
                                "Retail-Product-Management-System||com.product.microservices."
                                "apigatewayauth||ApiGatewayAuthApplication||m1",
                                "Retail-Product-Management-System||com.product.microservices."
                                "apigatewayauth.filters||JwtRequestFilter||m1",
                                "Retail-Product-Management-System||com.product.microservices."
                                "apigatewayauth.model||User||m1"],
        "Implementation Smell": [long_method,
                         magic_number,
                         long_method,
                         long_statement,
                         magic_number,
                         long_statement,
                         long_method,
                         magic_number,
                         magic_number,
                         long_method]
    })

    impl_smell_subtypes = [
        long_method,
        complex_method,
        "Long Parameter List",
        long_identifier,
        long_statement,
        complex_conditional,
        virtual_method_call,
        "Empty Catch Clause",
        magic_number,
        duplicate_code,
        missing_default]

    top_classes_list = [
        {"Retail-Product-Management-System||(default package)||MavenWrapperDownloader":
                {"smell_distribution": {"Abstraction": 7, "Encapsulation": 0,
                                        "Modularization": 0, "Hierarchy": 0}, "total_smells": 7}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth||"
         "ApiGatewayAuthApplication":
             {"smell_distribution": {"Abstraction": 1, "Encapsulation": 0, "Modularization": 0,
                                     "Hierarchy": 0}, "total_smells": 1}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth.filters||"
         "JwtRequestFilter":
             {"smell_distribution": {"Abstraction": 1, "Encapsulation": 0, "Modularization": 0,
                                     "Hierarchy": 0}, "total_smells": 1}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth.model||User":
             {"smell_distribution": {"Abstraction": 1, "Encapsulation": 0, "Modularization": 0,
                                     "Hierarchy": 0}, "total_smells": 1}}
        ]
    top_method_list = [
        {"Retail-Product-Management-System||(default package)||MavenWrapperDownloader||m2":
             {"smell_distribution": {long_method: 1, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 1, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 2, duplicate_code: 0, missing_default: 0},
              "total_smells": 4}},
        {m3_package:
             {"smell_distribution": {long_method: 1, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 1, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 0, duplicate_code: 0, missing_default: 0},
              "total_smells": 2}},
        {"Retail-Product-Management-System||(default package)||MavenWrapperDownloader||m1":
             {"smell_distribution": {long_method: 1, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 0, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 0, duplicate_code: 0, missing_default: 0},
              "total_smells": 1}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth||"
         "ApiGatewayAuthApplication||m1":
             {"smell_distribution": {long_method: 0, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 0, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 1, duplicate_code: 0, missing_default: 0},
              "total_smells": 1}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth.filters"
         "||JwtRequestFilter||m1":
             {"smell_distribution": {long_method: 0, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 0, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 1, duplicate_code: 0, missing_default: 0},
              "total_smells": 1}},
        {"Retail-Product-Management-System||com.product.microservices.apigatewayauth.model||"
         "User||m1":
             {"smell_distribution": {long_method: 1, complex_method: 0, long_parameter_list: 0,
                                     long_identifier: 0, long_statement: 0, complex_conditional: 0,
                                     virtual_method_call: 0, empty_catch_clause: 0,
                                     magic_number: 0, duplicate_code: 0, missing_default: 0},
              "total_smells": 1}}]

    retrieve_smell_files_mock = {
        "Architecture": None,
        "Design": f"{sample_folder}DesignSmells.csv",
        "Implementation": f"{sample_folder}ImplementationSmells.csv",
        "Testability": None,
        "Test": None
    }

    def test_get_top_entities(self):

        result = get_top_entities(self.design_df, self.design_smell, self.design_smell_subtypes)
        self.assertEqual(result, self.top_classes_list)

    @patch("code_quality_analyzer_analysis.hotspot_analysis.analysis.retrieve_smell_files",
           return_value=retrieve_smell_files_mock)
    @patch("code_quality_analyzer_analysis.hotspot_analysis.analysis.load_and_prepare_data",
           side_effect=[design_df, impl_df])
    @patch("code_quality_analyzer_analysis.hotspot_analysis.analysis.get_top_entities",
           side_effect=[top_classes_list, top_method_list])
    def test_get_hotspot_analysis(self, _, __, ___):
        expected = {
        "top_classes_list": self.top_classes_list,
        "top_methods_list": self.top_method_list
        }

        result = get_hotspot_analysis(self.sample_folder)

        self.assertEqual(result, expected)
