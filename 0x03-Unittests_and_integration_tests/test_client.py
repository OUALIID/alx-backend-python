#!/usr/bin/env python3
"""
This script contains test cases for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch, PropertyMock


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
            ("google"),
            ("abc"),
        ])
    def test_org(self, org_name):
        """Test the org method of GithubOrgClient."""
        with patch("client.get_json",
                   return_value={"payload": True}) as mock_get:
            github_org_client = GithubOrgClient(org_name)
            expected_result = {"payload": True}
            self.assertEqual(github_org_client.org, expected_result)
            url = f"https://api.github.com/orgs/{org_name}"
            mock_get.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test the _public_repos_url method of GithubOrgClient."""
        with patch.object(GithubOrgClient, "org"):
            result = GithubOrgClient("google")._public_repos_url()
            expected_result = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected_result)

    @patch("client.get_json")
    def test_public_repos(self, mock_get):
        """Test the public_repos method of the GithubOrgClient class."""
        with patch("client.GithubOrgClient._public_repos_url",
                   new_callable=PropertyMock, return_value = "url"):
            mock_get.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
            list_repos = GithubOrgClient("name").public_repos()
            self.assertEqual(list_repos, ["repo1", "repo2"])
            mock_get.assert_called_once_with("url")


    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo_info, license_key, expected_result):
        """Test the has_license method of GithubOrgClient."""
        result = GithubOrgClient("org_name").has_license(repo_info, license_key)
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()
