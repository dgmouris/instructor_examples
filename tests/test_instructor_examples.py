# Additional test for copy_repo_contents with mocks
from unittest.mock import MagicMock, patch

import pytest

from instructor_examples.utils import InstructorExamplesCopier


# mocks to the github package.
def make_github_api_response():
    return [
        {
            "type": "file",
            "name": "file1.txt",
            "download_url": "http://example.com/file1.txt",
        },
        {"type": "dir", "name": "subdir", "path": "subdir"},
    ]


def make_subdir_api_response():
    return [
        {
            "type": "file",
            "name": "file2.txt",
            "download_url": "http://example.com/file2.txt",
        },
    ]


@pytest.mark.parametrize(
    "input_str,expected_output",
    [
        ("1-intro-blog-example-start", "1-intro-blog-example-start"),
        ("\x961-intro-blog-example-start", "1-intro-blog-example-start"),
        ("abc\x96def", "abcdef"),
        ("normalstring", "normalstring"),
        ("\x96\x96\x96", ""),
    ],
)
def test_clean_remote_repo_folder(input_str, expected_output):
    copier = InstructorExamplesCopier(remote_repo_folder=input_str, out_folder=None, repo=None, console=None)
    assert copier.remote_repo_folder == expected_output


@pytest.mark.parametrize(
    "repo_url,expected_owner,expected_repo",
    [
        ("https://github.com/owner/repo", "owner", "repo"),
        ("https://github.com/anotheruser/anotherrepo", "anotheruser", "anotherrepo"),
        ("https://github.com/testuser/testrepo/", "testuser", "testrepo"),
    ],
)
def test_parse_repo_url(repo_url, expected_owner, expected_repo):
    copier = InstructorExamplesCopier(remote_repo_folder="", out_folder=None, repo=repo_url, console=None)
    assert copier.repo_owner == expected_owner
    assert copier.repo_name == expected_repo


@patch("os.makedirs")
@patch("requests.get")
@patch("builtins.open", new_callable=MagicMock)
def test_copy_repo_contents_end(mock_open, mock_requests_get, mock_makedirs):
    # Mock top-level API response
    mock_response_top = MagicMock()
    mock_response_top.json.return_value = make_github_api_response()
    mock_response_top.raise_for_status.return_value = None

    # Mock subdir API response
    mock_response_subdir = MagicMock()
    mock_response_subdir.json.return_value = make_subdir_api_response()
    mock_response_subdir.raise_for_status.return_value = None

    # Mock file download responses
    mock_file1 = MagicMock()
    mock_file1.content = b"file1 contents"
    mock_file2 = MagicMock()
    mock_file2.content = b"file2 contents"

    # requests.get side effects
    mock_requests_get.side_effect = [
        mock_response_top,  # top-level API
        mock_file1,  # file1.txt download
        mock_response_subdir,  # subdir API
        mock_file2,  # file2.txt download
    ]

    copier = InstructorExamplesCopier(
        remote_repo_folder="",
        out_folder="testfolder",
        repo="https://github.com/owner/repo",
        console=None,
    )
    copier.copy_repo_contents()

    # Check that makedirs was called for the main and subdir
    assert mock_makedirs.call_count >= 1
    # Check that requests.get was called for API and file downloads
    assert mock_requests_get.call_count == 4


def test_find_settings_file(tmp_path):
    # Create a nested directory structure
    root = tmp_path / "root"
    root.mkdir()
    subdir = root / "subdir"
    subdir.mkdir()
    # No settings file initially
    copier = InstructorExamplesCopier(remote_repo_folder="", out_folder=str(subdir), repo=None, console=None)
    assert copier.find_settings_file(str(subdir)) is None

    # Add settings file in root
    settings_path = root / "instructor_examples_settings.json"
    settings_path.write_text('{"repo": "https://github.com/owner/repo"}')
    assert copier.find_settings_file(str(subdir)) == str(settings_path)


def test_parse_settings(tmp_path):
    # Create a valid settings file
    settings_path = tmp_path / "instructor_examples_settings.json"
    settings_path.write_text('{"repo": "https://github.com/owner/repo", "extra": 123}')
    copier = InstructorExamplesCopier(remote_repo_folder="", out_folder=None, repo=None, console=None)
    copier.settings_file = str(settings_path)
    parsed = copier.parse_settings()
    assert parsed["repo"] == "https://github.com/owner/repo"
    assert parsed["extra"] == 123

    # Create an invalid settings file
    bad_settings_path = tmp_path / "bad_settings.json"
    bad_settings_path.write_text("not a json")
    copier.settings_file = str(bad_settings_path)
    parsed = copier.parse_settings()
    assert parsed == {}
