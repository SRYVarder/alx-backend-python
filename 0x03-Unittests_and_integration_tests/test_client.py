#!/usr/bin/env python3
"""
Comprehensive test suite for client.py GithubOrgClient.
"""
import unittest
from unittest.mock import Mock, PropertyMock, patch
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient individual methods.
    """

    @parameterized.expand([
        ('google', {'payload': True}),
        ('abc', {'payload': True}),
    ])
    @patch('client.get_json')
    def test_org(self, test_input, expected_result, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = expected_result

        with self.subTest(org=test_input):
            client = GithubOrgClient(test_input)
            result = client.org
            self.assertEqual(result, expected_result)
            mock_get_json.assert_called_once_with(
                f'https://api.github.com/orgs/{test_input}'
            )

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url(self, mock_org):
        """
        Test that _public_repos_url returns the correct URL.
        """
        mock_org.return_value = {'repos_url': 'http://mocked_url.com'}
        client = GithubOrgClient('test_org')
        self.assertEqual(client._public_repos_url, 'http://mocked_url.com')

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test that public_repos returns the correct list of repositories.
        """
        repos_payload = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}}
        ]
        mock_get
