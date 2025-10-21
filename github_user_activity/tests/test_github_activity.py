"""
Comprehensive test suite for GitHub User Activity CLI using Pytest and Mocking
"""

import pytest
import json
from unittest.mock import patch, MagicMock, mock_open
from urllib.error import HTTPError, URLError
from io import StringIO

# Import functions from the main module
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_activity import (
    fetch_user_activity,
    format_activity,
    display_activity,
    main
)


# ============================================================================
# FIXTURES - Mock data and common test setup
# ============================================================================

@pytest.fixture
def mock_events():
    """Fixture with sample GitHub events"""
    return [
        {
            "type": "PushEvent",
            "repo": {"name": "user/repo"},
            "payload": {"commits": [{"sha": "1"}, {"sha": "2"}, {"sha": "3"}]}
        },
        {
            "type": "CreateEvent",
            "repo": {"name": "user/repo"},
            "payload": {"ref_type": "branch", "ref": "feature/test"}
        },
        {
            "type": "IssuesEvent",
            "repo": {"name": "user/repo"},
            "payload": {"action": "opened", "issue": {"number": 42}}
        },
        {
            "type": "WatchEvent",
            "repo": {"name": "user/awesome-repo"},
            "payload": {}
        }
    ]


@pytest.fixture
def empty_events():
    """Fixture with empty events list"""
    return []


@pytest.fixture
def malformed_events():
    """Fixture with incomplete event data"""
    return [
        {"type": "PushEvent"},  # Missing repo and payload
        {"repo": {"name": "user/repo"}},  # Missing type
    ]


# ============================================================================
# TESTS FOR fetch_user_activity()
# ============================================================================

class TestFetchUserActivity:
    """Test suite for fetch_user_activity function"""
    
    @patch('github_activity.urlopen')
    def test_fetch_valid_user_success(self, mock_urlopen, mock_events):
        """Test successful fetch for a valid GitHub user"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_events).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_user_activity("kamranahmedse")
        
        assert result == mock_events
        assert len(result) == 4
        mock_urlopen.assert_called_once()
    
    @patch('github_activity.urlopen')
    def test_fetch_user_not_found(self, mock_urlopen, capsys):
        """Test handling of non-existent GitHub user (404 error)"""
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/invalid-user/events",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        
        result = fetch_user_activity("invalid-user")
        
        assert result is None
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()
    
    @patch('github_activity.urlopen')
    def test_fetch_rate_limit_exceeded(self, mock_urlopen, capsys):
        """Test handling of GitHub API rate limit (403 error)"""
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/test/events",
            code=403,
            msg="Forbidden",
            hdrs={},
            fp=None
        )
        
        result = fetch_user_activity("test")
        
        assert result is None
        captured = capsys.readouterr()
        assert "403" in captured.out
    
    @patch('github_activity.urlopen')
    def test_fetch_api_server_error(self, mock_urlopen, capsys):
        """Test handling of GitHub API server errors (5xx)"""
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/test/events",
            code=500,
            msg="Internal Server Error",
            hdrs={},
            fp=None
        )
        
        result = fetch_user_activity("test")
        
        assert result is None
        captured = capsys.readouterr()
        assert "500" in captured.out
    
    @patch('github_activity.urlopen')
    def test_fetch_network_error(self, mock_urlopen, capsys):
        """Test handling of network connectivity issues"""
        mock_urlopen.side_effect = URLError("Network connection failed")
        
        result = fetch_user_activity("test")
        
        assert result is None
        captured = capsys.readouterr()
        assert "Network error" in captured.out
    
    @patch('github_activity.urlopen')
    def test_fetch_invalid_json_response(self, mock_urlopen, capsys):
        """Test handling of invalid JSON response from API"""
        mock_response = MagicMock()
        mock_response.read.return_value = b"<html>Invalid JSON</html>"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_user_activity("test")
        
        assert result is None
        captured = capsys.readouterr()
        assert "parse" in captured.out.lower()
    
    @patch('github_activity.urlopen')
    def test_fetch_timeout(self, mock_urlopen, capsys):
        """Test handling of request timeout"""
        mock_urlopen.side_effect = TimeoutError("Request timed out")
        
        result = fetch_user_activity("test")
        
        assert result is None
        captured = capsys.readouterr()
        assert "Error" in captured.out
    
    @patch('github_activity.urlopen')
    def test_fetch_empty_response(self, mock_urlopen):
        """Test handling of empty response from API"""
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps([]).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_user_activity("inactive-user")
        
        assert result == []
        assert len(result) == 0


# ============================================================================
# TESTS FOR format_activity()
# ============================================================================

class TestFormatActivity:
    """Test suite for format_activity function"""
    
    def test_format_push_event_single_commit(self):
        """Test formatting of PushEvent with single commit"""
        event = {
            "type": "PushEvent",
            "repo": {"name": "user/repo"},
            "payload": {"commits": [{"sha": "1"}]}
        }
        result = format_activity(event)
        assert "Pushed 1 commit" in result
        assert "user/repo" in result
    
    def test_format_push_event_multiple_commits(self):
        """Test formatting of PushEvent with multiple commits"""
        event = {
            "type": "PushEvent",
            "repo": {"name": "user/repo"},
            "payload": {"commits": [{"sha": "1"}, {"sha": "2"}, {"sha": "3"}]}
        }
        result = format_activity(event)
        assert "Pushed 3 commits" in result
        assert "user/repo" in result
    
    def test_format_create_branch_event(self):
        """Test formatting of CreateEvent for branch"""
        event = {
            "type": "CreateEvent",
            "repo": {"name": "user/repo"},
            "payload": {"ref_type": "branch", "ref": "feature/new"}
        }
        result = format_activity(event)
        assert "Created branch" in result
        assert "feature/new" in result
    
    def test_format_create_tag_event(self):
        """Test formatting of CreateEvent for tag"""
        event = {
            "type": "CreateEvent",
            "repo": {"name": "user/repo"},
            "payload": {"ref_type": "tag", "ref": "v1.0.0"}
        }
        result = format_activity(event)
        assert "Created tag" in result
        assert "v1.0.0" in result
    
    def test_format_create_repository_event(self):
        """Test formatting of CreateEvent for repository"""
        event = {
            "type": "CreateEvent",
            "repo": {"name": "user/new-repo"},
            "payload": {"ref_type": "repository"}
        }
        result = format_activity(event)
        assert "Created repository" in result or "Created" in result
    
    def test_format_issue_opened_event(self):
        """Test formatting of IssuesEvent with opened action"""
        event = {
            "type": "IssuesEvent",
            "repo": {"name": "user/repo"},
            "payload": {"action": "opened", "issue": {"number": 42}}
        }
        result = format_activity(event)
        assert "Opened a new issue" in result
        assert "user/repo" in result
    
    def test_format_issue_closed_event(self):
        """Test formatting of IssuesEvent with closed action"""
        event = {
            "type": "IssuesEvent",
            "repo": {"name": "user/repo"},
            "payload": {"action": "closed", "issue": {"number": 42}}
        }
        result = format_activity(event)
        assert "Closed" in result or "closed" in result
    
    def test_format_pull_request_opened(self):
        """Test formatting of PullRequestEvent with opened action"""
        event = {
            "type": "PullRequestEvent",
            "repo": {"name": "user/repo"},
            "payload": {"action": "opened", "pull_request": {"number": 10}}
        }
        result = format_activity(event)
        assert "Opened a new pull request" in result
    
    def test_format_pull_request_closed(self):
        """Test formatting of PullRequestEvent with closed action"""
        event = {
            "type": "PullRequestEvent",
            "repo": {"name": "user/repo"},
            "payload": {"action": "closed", "pull_request": {"number": 10}}
        }
        result = format_activity(event)
        assert "Closed" in result or "closed" in result
    
    def test_format_watch_event(self):
        """Test formatting of WatchEvent (star)"""
        event = {
            "type": "WatchEvent",
            "repo": {"name": "user/awesome-repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "Starred" in result
        assert "user/awesome-repo" in result
    
    def test_format_fork_event(self):
        """Test formatting of ForkEvent"""
        event = {
            "type": "ForkEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "Forked" in result
        assert "user/repo" in result
    
    def test_format_delete_event(self):
        """Test formatting of DeleteEvent"""
        event = {
            "type": "DeleteEvent",
            "repo": {"name": "user/repo"},
            "payload": {"ref_type": "branch", "ref": "old-branch"}
        }
        result = format_activity(event)
        assert "Deleted" in result
        assert "branch" in result
    
    def test_format_pull_request_review_event(self):
        """Test formatting of PullRequestReviewEvent"""
        event = {
            "type": "PullRequestReviewEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "Reviewed" in result
    
    def test_format_issue_comment_event(self):
        """Test formatting of IssueCommentEvent"""
        event = {
            "type": "IssueCommentEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "Commented" in result
    
    def test_format_public_event(self):
        """Test formatting of PublicEvent"""
        event = {
            "type": "PublicEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "public" in result.lower()
    
    def test_format_unknown_event(self):
        """Test formatting of unknown event type"""
        event = {
            "type": "UnknownEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert "UnknownEvent" in result
        assert "user/repo" in result
    
    def test_format_event_missing_repo(self):
        """Test formatting when repo data is missing"""
        event = {
            "type": "PushEvent",
            "payload": {"commits": [{"sha": "1"}]}
        }
        result = format_activity(event)
        assert result is not None
        assert "Unknown" in result or "Pushed" in result
    
    def test_format_event_missing_type(self):
        """Test formatting when event type is missing"""
        event = {
            "repo": {"name": "user/repo"},
            "payload": {}
        }
        result = format_activity(event)
        assert result is not None


# ============================================================================
# TESTS FOR display_activity()
# ============================================================================

class TestDisplayActivity:
    """Test suite for display_activity function"""
    
    def test_display_valid_events(self, mock_events, capsys):
        """Test displaying valid events"""
        display_activity(mock_events)
        captured = capsys.readouterr()
        
        assert "Recent activity" in captured.out
        assert "4 events" in captured.out
        assert "Pushed" in captured.out
        assert "Created branch" in captured.out
        assert "Opened a new issue" in captured.out
        assert "Starred" in captured.out
    
    def test_display_empty_events(self, empty_events, capsys):
        """Test displaying when no events exist"""
        display_activity(empty_events)
        captured = capsys.readouterr()
        
        assert "No recent activity" in captured.out
    
    def test_display_single_event(self, capsys):
        """Test displaying a single event"""
        events = [{
            "type": "WatchEvent",
            "repo": {"name": "user/repo"},
            "payload": {}
        }]
        display_activity(events)
        captured = capsys.readouterr()
        
        assert "1 event" in captured.out
        assert "Starred" in captured.out
    
    def test_display_malformed_events(self, malformed_events, capsys):
        """Test displaying events with missing data"""
        display_activity(malformed_events)
        captured = capsys.readouterr()
        
        # Should handle gracefully without crashing
        assert captured.out is not None
    
    def test_display_none_input(self, capsys):
        """Test handling of None input"""
        display_activity(None)
        captured = capsys.readouterr()
        
        assert "No recent activity" in captured.out or captured.out == ""


# ============================================================================
# TESTS FOR main() - CLI entry point
# ============================================================================

class TestMain:
    """Test suite for main CLI function"""
    
    def test_main_missing_username_argument(self, capsys):
        """Test main function without username argument"""
        with patch.object(sys, 'argv', ['github-activity.py']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            
            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "Usage" in captured.out
    
    @patch('github_activity.fetch_user_activity')
    def test_main_with_valid_username(self, mock_fetch, capsys, mock_events):
        """Test main function with valid username"""
        mock_fetch.return_value = mock_events
        
        with patch.object(sys, 'argv', ['github-activity.py', 'testuser']):
            main()
        
        captured = capsys.readouterr()
        assert "Fetching activity" in captured.out
        assert "testuser" in captured.out
        mock_fetch.assert_called_once_with('testuser')
    
    @patch('github_activity.fetch_user_activity')
    def test_main_with_invalid_user(self, mock_fetch, capsys):
        """Test main function with non-existent user"""
        mock_fetch.return_value = None
        
        with patch.object(sys, 'argv', ['github-activity.py', 'invalid-user']):
            main()
        
        captured = capsys.readouterr()
        assert "Fetching activity" in captured.out
    
    @patch('github_activity.fetch_user_activity')
    def test_main_with_empty_activity(self, mock_fetch, capsys, empty_events):
        """Test main function with user having no activity"""
        mock_fetch.return_value = empty_events
        
        with patch.object(sys, 'argv', ['github-activity.py', 'inactive-user']):
            main()
        
        captured = capsys.readouterr()
        assert "No recent activity" in captured.out
    
    @patch('github_activity.fetch_user_activity')
    def test_main_with_special_characters_in_username(self, mock_fetch, mock_events):
        """Test main function with special characters in username"""
        mock_fetch.return_value = mock_events
        
        with patch.object(sys, 'argv', ['github-activity.py', 'user-name_123']):
            main()
        
        mock_fetch.assert_called_once_with('user-name_123')


# ============================================================================
# INTEGRATION TESTS
# ============================================================================

class TestIntegration:
    """Integration tests for the complete workflow"""
    
    @patch('github_activity.urlopen')
    def test_full_workflow_success(self, mock_urlopen, capsys):
        """Test complete workflow from CLI to display"""
        mock_events = [
            {
                "type": "PushEvent",
                "repo": {"name": "user/repo"},
                "payload": {"commits": [{"sha": "1"}, {"sha": "2"}]}
            }
        ]
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_events).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        with patch.object(sys, 'argv', ['github-activity.py', 'testuser']):
            main()
        
        captured = capsys.readouterr()
        assert "Fetching activity" in captured.out
        assert "Pushed 2 commits" in captured.out
        assert "user/repo" in captured.out
    
    @patch('github_activity.urlopen')
    def test_full_workflow_user_not_found(self, mock_urlopen, capsys):
        """Test complete workflow with non-existent user"""
        mock_urlopen.side_effect = HTTPError(
            url="https://api.github.com/users/nonexistent/events",
            code=404,
            msg="Not Found",
            hdrs={},
            fp=None
        )
        
        with patch.object(sys, 'argv', ['github-activity.py', 'nonexistent']):
            main()
        
        captured = capsys.readouterr()
        assert "not found" in captured.out.lower()


# ============================================================================
# EDGE CASE TESTS
# ============================================================================

class TestEdgeCases:
    """Test edge cases and boundary conditions"""
    
    def test_format_event_with_empty_commits(self):
        """Test PushEvent with no commits"""
        event = {
            "type": "PushEvent",
            "repo": {"name": "user/repo"},
            "payload": {"commits": []}
        }
        result = format_activity(event)
        assert "Pushed 0 commits" in result
    
    def test_format_event_with_very_long_repo_name(self):
        """Test event with extremely long repository name"""
        long_name = "user/" + "a" * 200
        event = {
            "type": "WatchEvent",
            "repo": {"name": long_name},
            "payload": {}
        }
        result = format_activity(event)
        assert long_name in result
    
    def test_display_large_number_of_events(self, capsys):
        """Test displaying a large number of events"""
        events = [
            {
                "type": "WatchEvent",
                "repo": {"name": f"user/repo-{i}"},
                "payload": {}
            }
            for i in range(100)
        ]
        display_activity(events)
        captured = capsys.readouterr()
        
        assert "100 events" in captured.out
        assert "Starred" in captured.out
    
    @patch('github_activity.urlopen')
    def test_fetch_with_unicode_in_response(self, mock_urlopen):
        """Test handling of unicode characters in API response"""
        mock_events = [
            {
                "type": "IssueCommentEvent",
                "repo": {"name": "user/repo-日本語"},
                "payload": {}
            }
        ]
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(mock_events).encode('utf-8')
        mock_urlopen.return_value.__enter__.return_value = mock_response
        
        result = fetch_user_activity("test")
        assert result == mock_events
        assert "日本語" in result[0]["repo"]["name"]


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])