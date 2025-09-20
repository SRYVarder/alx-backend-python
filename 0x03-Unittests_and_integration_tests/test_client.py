#!/usr/bin/env python3
"""
Unit and integration tests for client.py.
"""

import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos


class TestGithubOrgClient(unittest.TestCase):
    """
    Test class for the GithubOrgClient.
    """

    @parameterized.expand([
        ("google",),
        ("abc",)
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Tests that GithubOrgClient.org returns the correct value.
        """
        test_payload = {"org_name": org_name}
        mock_get_json.return_value = test_payload
        client = GithubOrgClient(org_name)
        self.assertEqual(client.org(), test_payload)
        mock_get_json.assert_called_once_with(f"[https://api.github.com/orgs/](https://api.github.com/orgs/){org_name}")

    def test_public_repos_url(self):
        """
        Tests that _public_repos_url returns the correct URL.
        """
        with patch('client.GithubOrgClient.org', new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "[http://example.com/repos](http://example.com/repos)"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url(), "[http://example.com/repos](http://example.com/repos)")

    @patch('client.get_json', return_value=repos_payload)
    def test_public_repos(self, mock_get_json):
        """
        Tests that public_repos returns the list of repos.
        """
        with patch('client.GithubOrgClient._public_repos_url', new_callable=PropertyMock) as mock_repos_url:
            mock_repos_url.return_value = "[http://example.com/repos](http://example.com/repos)"
            client = GithubOrgClient("test_org")
            self.assertEqual(client.public_repos(), expected_repos)
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Tests the has_license method.
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key), expected_result)


@parameterized_class([
    {"org_payload": org_payload, "repos_payload": repos_payload, "expected_repos": expected_repos, "apache2_repos": apache2_repos}
])
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration test class for GithubOrgClient.
    """

    @classmethod
    def setUpClass(cls):
        """
        Mocks requests.get to return a series of payloads.
        """
        cls.get_patcher = patch('requests.get', side_effect=[
            Mock(json=lambda: cls.org_payload),
            Mock(json=lambda: cls.repos_payload)
        ])
        cls.mock_get = cls.get_patcher.start()

    @classmethod
    def tearDownClass(cls):
        """
        Stops the patcher.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Tests public_repos with a mocked get.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.mock_get.assert_called()

    def test_public_repos_with_license(self):
        """
        Tests public_repos with a mocked get and a license.
        """
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(license="apache-2.0"), self.apache2_repos)
        self.mock_get.assert_called()
