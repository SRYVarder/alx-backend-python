#!/usr/bin/env python3
"""
Unit tests for the GithubOrgClient
class defined in client.py
"""
import unittest
from unittest.mock import patch, PropertyMock, Mock
from parameterized import parameterized_class, parameterized
from client import GithubOrgClient
from fixtures import org_payload, repos_payload, expected_repos, apache2_repos

@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    [
        (org_payload, repos_payload, expected_repos, apache2_repos),
    ]
)
class TestIntegrationGithubOrgClient(unittest.TestCase):
    """
    Integration tests for GithubOrgClient.public_repos
    using fixture payloads.
    """

    @classmethod
    def setUpClass(cls) -> None:
        """
        Set up class mock for requests.get so that
        external calls are able to
        return controlled fixture payloads.
        """
        cls.get_patcher = patch("requests.get")
        mock_get = cls.get_patcher.start()

        def side_effect(url, *args, **kwargs):
            mock_response = Mock()
            if url == f"https://api.github.com/orgs/{cls.org_payload['login']}":
                mock_response.json.return_value = cls.org_payload
            elif url == cls.org_payload["repos_url"]:
                mock_response.json.return_value = cls.repos_payload
            else:
                mock_response.json.return_value = {}
            return mock_response

        mock_get.side_effect = side_effect

    @classmethod
    def tearDownClass(cls) -> None:
        """
        Halts the requests.get patcher restore
        the original requests.get behavior.
        """
        cls.get_patcher.stop()

    def test_public_repos(self):
        """
        Check that test_public_repos function
        returns the expected repos list.
        """
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(),
            self.expected_repos
        )

    def test_public_repos_with_license(self):
        """
        Test helps by filtering repos using license key.
        """
        client = GithubOrgClient(self.org_payload["login"])
        self.assertEqual(
            client.public_repos(license="apache-2.0"),
            self.apache2_repos,
        )


class TestGithubOrgClient(unittest.TestCase):
    """
    Unit tests for GithubOrgClient to ensure correct API calls
    and returned values when retrieving details.
    """

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name: str, mock_get_json) -> None:
        """
        Test that GithubOrgClient.org returns the expected value and
        that get_json is called once with the correct URL.
        """
        test_payload = {"login": org_name}
        mock_get_json.return_value = test_payload

        client = GithubOrgClient(org_name)
        result = client.org
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )
        self.assertEqual(result, test_payload)

    def test_public_repos_url(self) -> None:
        """
        Test that the function test_public_repos_url
        returns expected URL.
        """
        test_payload = {
            "repos_url": "https://api.github.com/orgs/google/repos"
        }

        with patch.object(
            GithubOrgClient,
            "org",
            new_callable=PropertyMock,
            return_value=test_payload
        ):
            client = GithubOrgClient("google")
            result = client._public_repos_url

        self.assertEqual(result, test_payload["repos_url"])

    @patch("client.get_json")
    def test_public_repos(self, mock_get_json) -> None:
        """
        Test that the function public_repos returns expected
        list of repos and calls helpers once.
        """
        test_payload = [
            {"name": "repo0"},
            {"name": "repo1"},
            {"name": "repo2"},
        ]
        mock_get_json.return_value = test_payload

        with patch.object(
            GithubOrgClient,
            "_public_repos_url",
            new_callable=PropertyMock,
            return_value="https://api.github.com/orgs/google/repos"
        ) as mock_url:
            client = GithubOrgClient("google")
            result = client.public_repos()

        self.assertEqual(result, ["repo0", "repo1", "repo2"])

        mock_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/google/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo: dict, license_key: str, expected: bool) -> None:
        """
        Test that the function test_has_license
        correctly checks if the repo has
        the specified license key.
        """
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
