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
        Test that GithubOrgClient.has_license returns the correct boolean value.
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
    # Test case 3: Empty repos list
    (
        TEST_PAYLOAD,
        [],
        [],
        [],
    ),
], params=[
    ('org_payload', 'repos_payload', 'expected_repos', 'apache2_repos'),
],
class_name_func=lambda cls, _, idx: f'TestIntegrationGithubOrgClient_{idx}')
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for the complete GithubOrgClient workflow.
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
            return {}

        cls.get_patcher = patch('requests.get', side_effect=get_side_effect)
        cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Tear down the class-level fixtures.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Test the public_repos method with a known payload.
        """
        client = GithubOrgClient('google')
        result = client.public_repos()
        self.assertEqual(result, self.expected_repos)

    def test_public_repos_with_license(self):
        """
        Test the public_repos method with license filtering.
        """
        client = GithubOrgClient('google')
        apache2_result = client.public_repos('apache-2.0')
        self.assertEqual(apache2_result, self.apache2_repos)

    def test_org_payload_access(self):
        """
        Test that org payload is accessible and correct.
        """
        client = GithubOrgClient('google')
        org_data = client.org
        self.assertEqual(org_data, self.org_payload)
        self.assertEqual(org_data.get('login'), 'google')

    def test_repos_payload_memoization(self):
        """
        Test that repos_payload is properly memoized.
        """
        client = GithubOrgClient('google')
        first_call = client.repos_payload
        second_call = client.repos_payload
        self.assertIs(first_call, second_call)
        self.assertEqual(first_call, self.repos_payload)

    def test_public_repos_url_integration(self):
        """
        Test that _public_repos_url works correctly in integration.
        """
        client = GithubOrgClient('google')
        repos_url = client._public_repos_url
        self.assertIn('repos', repos_url)
        self.assertEqual(repos_url, self.org_payload['repos_url'])

    def test_complete_workflow(self):
        """
        Test the complete integration workflow from org to filtered repos.
        """
        client = GithubOrgClient('google')

        # Step 1: Get organization data
        org_data = client.org
        self.assertIn('repos_url', org_data)

        # Step 2: Get all public repositories
        all_repos = client.public_repos()
        self.assertEqual(len(all_repos), len(self.expected_repos))

        # Step 3: Get filtered repositories
        filtered_repos = client.public_repos('apache-2.0')
        self.assertEqual(filtered_repos, self.apache2_repos)

        # Step 4: Verify memoization
        repos1 = client.repos_payload
        repos2 = client.repos_payload
        self.assertIs(repos1, repos2)


class TestGithubOrgClientEdgeCases(unittest.TestCase):
    """
    Edge case tests for GithubOrgClient error conditions.
    """

    @patch('client.get_json')
    def test_org_empty_response(self, mock_get_json):
        """
        Test org property with empty response.
        """
        mock_get_json.return_value = {}
        client = GithubOrgClient('empty_org')
        result = client.org
        self.assertIsInstance(result, dict)
        self.assertEqual(result, {})
        mock_get_json.assert_called_once()

    @patch('client.GithubOrgClient.org', new_callable=PropertyMock)
    def test_public_repos_url_missing_repos_url(self, mock_org):
        """
        Test _public_repos_url when repos_url is missing from org data.
        """
        mock_org.return_value = {'other_field': 'value'}
        client = GithubOrgClient('test_org')

        with self.assertRaises(KeyError):
            _ = client._public_repos_url

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_empty_list(self, mock_public_repos_url,
                                     mock_get_json):
        """
        Test public_repos with empty repository list.
        """
        mock_get_json.return_value = []
        mock_public_repos_url.return_value = (
            'https://api.github.com/orgs/test/repos'
        )

        client = GithubOrgClient('test_org')
        result = client.public_repos()

        self.assertEqual(result, [])
        mock_get_json.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_no_license_info(self, mock_public_repos_url,
                                          mock_get_json):
        """
        Test public_repos with repos missing license information.
        """
        repos_payload = [
            {'name': 'repo1'},  # No license
            {'name': 'repo2', 'license': {'key': 'mit'}},
            {'name': 'repo3'},  # No license
        ]
        mock_get_json.return_value = repos_payload
        mock_public_repos_url.return_value = (
            'https://api.github.com/orgs/test/repos'
        )

        client = GithubOrgClient('test_org')
        result = client.public_repos('apache-2.0')

        self.assertEqual(result, ['repo1', 'repo2', 'repo3'])

    @parameterized.expand([
        (
            {
                'license': {
                    'key': 'apache-2.0',
                    'name': 'Apache License 2.0'
                }
            },
            'apache-2.0',
            True
        ),
        (
            {'license': {'key': 'mit', 'name': 'MIT License'}},
            'MIT License',
            False
        ),
        (
            {'license': {'key': 'apache-2.0'}},
            'Apache-2.0',
            False
        ),
    ])
    def test_has_license_complex_cases(self, repo, license_key,
                                       expected_result):
        """
        Test has_license with more complex repository license structures.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (
            {'license': {'key': 'mit'}},
            'mi',
            False
        ),
        (
            {'license': {'key': 'apache-2.0'}},
            'apache',
            False
        ),
        (
            {'license': None},
            'none',
            False
        ),
    ])
    def test_has_license_partial_matches(self, repo, license_key,
                                         expected_result):
        """
        Test has_license with partial string matches.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @parameterized.expand([
        (
            {'license': {'key': 'mit', 'url': 'http://example.com'}},
            'mit',
            True
        ),
        (
            {'license': {'key': None, 'name': 'Unknown'}},
            'mit',
            False
        ),
        (
            {'license': {'key': 'proprietary', 'spdx_id': 'PROPRIETARY'}},
            'proprietary',
            True
        ),
    ])
    def test_has_license_advanced_structures(self, repo, license_key,
                                             expected_result):
        """
        Test has_license with advanced GitHub license structures.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

    @patch('client.get_json')
    def test_org_api_error_response(self, mock_get_json):
        """
        Test org property with API error response.
        """
        error_response = {'message': 'Not found', 'documentation_url': 'url'}
        mock_get_json.return_value = error_response

        client = GithubOrgClient('nonexistent_org')
        result = client.org
        self.assertIn('message', result)
        self.assertEqual(result['message'], 'Not found')
        mock_get_json.assert_called_once()

    @patch('client.get_json')
    @patch('client.GithubOrgClient._public_repos_url',
           new_callable=PropertyMock)
    def test_public_repos_api_error(self, mock_public_repos_url,
                                    mock_get_json):
        """
        Test public_repos with API error response.
        """
        error_response = {'message': 'Not found'}
        mock_get_json.return_value = error_response
        mock_public_repos_url.return_value = (
            'https://api.github.com/orgs/test/repos'
        )

        client = GithubOrgClient('test_org')
        result = client.public_repos()

        self.assertEqual(result, [])
        mock_get_json.assert_called_once()


if __name__ == '__main__':
    unittest.main()
