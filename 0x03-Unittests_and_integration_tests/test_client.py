#!/usr/bin/env python3
"""
Advanced integration tests for client.py GithubOrgClient.
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

    def test_has_license(self):
        """
        Test that GithubOrgClient.has_license returns the corr boolean value.
        """
        # Test case 1: Repository has matching license
        repo_with_license = {'license': {'key': 'mit'}}
        result1 = GithubOrgClient.has_license(repo_with_license, 'mit')
        self.assertTrue(result1)

        # Test case 2: Repository has different license
        repo_different_license = {'license': {'key': 'apache-2.0'}}
        result2 = GithubOrgClient.has_license(repo_different_license, 'mit')
        self.assertFalse(result2)

        # Test case 3: Repository has no license
        repo_no_license = {'name': 'repo3'}
        result3 = GithubOrgClient.has_license(repo_no_license, 'mit')
        self.assertFalse(result3)

        # Test case 4: Repository has empty license
        repo_empty_license = {'license': {}}
        result4 = GithubOrgClient.has_license(repo_empty_license, 'mit')
        self.assertFalse(result4)

        # Test case 5: Repository has None license
        repo_none_license = {'license': None}
        result5 = GithubOrgClient.has_license(repo_none_license, 'mit')
        self.assertFalse(result5)

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
    def test_has_license_parameterized(self, repo, license_key,
                                       expected_result):
        """
        Parameterized test for has_license method.
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

    @patch('client.get_json')
    def test_org_memoization(self, mock_get_json):
        """
        Test that org property is properly memoized.
        """
        mock_payload = {'payload': True}
        mock_get_json.return_value = mock_payload

        client = GithubOrgClient('google')
        first_call = client.org
        second_call = client.org

        self.assertIs(first_call, second_call)
        mock_get_json.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_repos_payload_memoization(self, mock_public_repos_url,
                                       mock_get_json):
        """
        Test that repos_payload is properly memoized.
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
        first_call = client.repos_payload
        second_call = client.repos_payload

        self.assertIs(first_call, second_call)
        mock_get_json.assert_called_once()


# Advanced Integration Tests using Fixtures
@parameterized_class([
    # Test case with comprehensive fixture data
    (
        TEST_PAYLOAD,  # org_payload from fixtures
        [  # repos_payload from fixtures - comprehensive GitHub API structure
            {
                'id': 1,
                'name': 'repo1',
                'full_name': 'org/repo1',
                'license
