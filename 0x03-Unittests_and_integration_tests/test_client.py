#!/usr/bin/env python3
"""
Test file for client.py
"""
import unittest
from unittest.mock import patch, Mock, PropertyMock
from parameterized import parameterized, parameterized_class
from client import GithubOrgClient
from fixtures import TEST_PAYLOAD


class TestGithubOrgClient(unittest.TestCase):
    """
    TestGithubOrgClient class to test the GithubOrgClient.
    """
    @parameterized.expand([
        ('google',),
        ('abc',),
    ])
    @patch('client.get_json')
    def test_org(self, org_name, mock_get_json):
        """
        Test that GithubOrgClient.org returns the correct value.
        """
        mock_get_json.return_value = {"payload": True}
        client = GithubOrgClient(org_name)
        result = client.org()
        self.assertEqual(result, {"payload": True})
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}")

    def test_public_repos_url(self):
        """
        Test that _public_repos_url returns the correct URL.
        """
        with patch('client.GithubOrgClient.org',
                   new_callable=PropertyMock) as mock_org:
            mock_org.return_value = {"repos_url": "http://mocked_url.com"}
            client = GithubOrgClient("test_org")
            self.assertEqual(client._public_repos_url,
                             "http://mocked_url.com")

    @patch('client.get_json')
    def test_public_repos(self, mock_get_json):
        """
        Test that public_repos returns the correct list of repositories.
        """
        test_payload = [{"name": "repo1"}, {"name": "repo2"}]
        mock_get_json.return_value = test_payload

        with patch('client.GithubOrgClient._public_repos_url',
                   new_callable=PropertyMock) as mock_public_repos_url:
            mock_public_repos_url.return_value = "http://mocked_repos_url.com"
            client = GithubOrgClient("test_org")

            result = client.public_repos()

            self.assertEqual(result, ["repo1", "repo2"])
            mock_public_repos_url.assert_called_once()
            mock_get_json.assert_called_once()

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected_result):
        """
        Test that GithubOrgClient.has_license returns the correct boolean value.
        """
        self.assertEqual(GithubOrgClient.has_license(repo, license_key),
                         expected_result)


@parameterized_class([
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos")
])

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
            if url == "http://repos_url.com":
                return Mock(**{'json.return_value': cls.repos_payload})
            return Mock(**{'json.return_value': cls.org_payload})

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
        client = GithubOrgClient("google")
        self.assertEqual(client.public_repos(), self.expected_repos)
        self.assertEqual(client.public_repos("apache-2.0"), self.apache2_repos)
