#!/usr/bin/env python3
"""
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
    @patch('client.GithubOrgClient.get_json')
    def test_org(self, org_name, mock_get_json):
        """Test the org method of GithubOrgClient."""
        mock_get_json.return_value = {"name": org_name}
        self.assertEqual(GithubOrgClient(org_name).org(), {"name": org_name})
        url = f'https://api.github.com/orgs/{org_name}'
        mock_get_json.assert_called_once_with(url)
