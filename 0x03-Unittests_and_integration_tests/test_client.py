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
    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        mock_public_repos_url.return_value = "url"
        mock_get_json.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]
        repos = GithubOrgClient("name").public_repos()
        self.assertEqual(repos, [{'name': 'repo1'}, {'name': 'repo2'}])
        mock_get_json.assert_called_once_with("url")


if __name__ == '__main__':
    unittest.main()
