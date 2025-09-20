#!/usr/bin/env python3
"""
Test file for client.py
"""
import unittest
from unittest.mock import patch, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test the GithubOrgClient.
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
        mock_get_json.return_value = repos_payload
        mock_public_repos_url.return_value = (
            'https://api.github.com/orgs/test/repos'
        )

        client = GithubOrgClient('test_org')
        result = client.public_repos()

        self.assertEqual(result, ['repo1', 'repo2'])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            'https://api.github.com/orgs/test/repos'
        )

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_with_license(self, mock_public_repos_url,
                                       mock_get_json):
        """
        Test public_repos with license filtering.
        """
        repos_payload = [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}}
        ]
        mock_get_json.return_value = repos_payload
        mock_public_repos_url.return_value = (
            'https://api.github.com/orgs/test/repos'
        )

        client = GithubOrgClient('test_org')
        result = client.public_repos('apache-2.0')

        self.assertEqual(result, ['repo2'])
        mock_get_json.assert_called_once()

    @parameterized.expand([
        (
            {'license': {'key': 'my_license'}},
            'my_license',
            True
        ),
        (
            {'license': {'key': 'other_license'}},
            'my_license',
            False
        ),
        (
            {'license': None},
            'my_license',
            False
        ),
        (
            {'license': {}},
            'my_license',
            False
        ),
        (
            {'license': {'key': ''}},
            'my_license',
            False
        ),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that GithubOrgClient.has_license returns the correct boolean value.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (None, TypeError, 'license_key cannot be None'),
    ])
    def test_has_license_none_key(self, license_key, expected_exception,
                                  expected_msg):
        """
        Test has_license with None license_key raises AssertionError.
        """
        with self.assertRaises(expected_exception) as cm:
            GithubOrgClient.has_license({}, license_key)

        self.assertIn(expected_msg, str(cm.exception))


@parameterized_class([
    # Test case 1: Standard mixed licenses
    (
        TEST_PAYLOAD,
        [
            {'name': 'repo1', 'license': {'key': 'mit'}},
            {'name': 'repo2', 'license': {'key': 'apache-2.0'}},
            {'name': 'repo3', 'license': {'key': 'mit'}},
            {'name': 'repo4', 'license': {'key': 'apache-2.0'}},
        ],
        ['repo1', 'repo2', 'repo3', 'repo4'],
        ['repo2', 'repo4'],
    ),
    # Test case 2: No apache licenses
    (
        TEST_PAYLOAD,
        [
            {'name': 'repo5'},  # No license
            {'name': 'repo6', 'license': {'key': 'mit'}},
            {'name': 'repo7', 'license': {'key': 'mit'}},
        ],
        ['repo5', 'repo6', 'repo7'],
        [],  # No apache-2.0 repos
    ),
], names=('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
   class_name_func=lambda cls, _, idx: f'TestIntegrationGithubOrgClient_{idx}')
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test for the GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up the class-level fixtures for the integration test.
        """
        def get_side_effect(url):
            if 'orgs' in url:
                return cls.org_payload
            if 'repos' in url:
                return cls.repos_payload
            return
