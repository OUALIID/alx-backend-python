#!/usr/bin/env python3
"""
This script contains test cases for the GithubOrgClient class.
"""
import unittest
from parameterized import parameterized
from client import GithubOrgClient
from unittest.mock import patch


class TestGithubOrgClient(unittest.TestCase):
    """Test cases for the GithubOrgClient class."""

    @parameterized.expand([
            ("google"),
            ("abc"),
        ])
    def test_org(self, org_name):
        """Test the org method of GithubOrgClient."""
        with patch("client.get_json", return_value={"payload": True}) as mock_get:
            github_org_client = GithubOrgClient(org_name)
            expected_result = {"payload": True}
            self.assertEqual(github_org_client.org, expected_result)
            url = f"https://api.github.com/orgs/{org_name}"
            mock_get.assert_called_once_with(url)

    def test_public_repos_url(self):
        """Test the _public_repos_url method of GithubOrgClient."""
        with patch.object(GithubOrgClient, "org") as mock_org:
            result = GithubOrgClient("google")._public_repos_url()
            expected_result = "https://api.github.com/orgs/google/repos"
            self.assertEqual(result, expected_result)
        


if __name__ == '__main__':
    unittest.main()
