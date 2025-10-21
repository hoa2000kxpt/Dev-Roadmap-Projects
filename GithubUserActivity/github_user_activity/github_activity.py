#!/usr/bin/env python3
"""
GitHub User Activity CLI
Fetches and displays recent activity for a GitHub user.
"""

import sys
import json
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

def fetch_user_activity(username):
    """
    Fetch recent activity for a GitHub user.
    
    Args:
        username: GitHub username
        
    Returns:
        List of activity events or None if error occurs
    """
    url = f"https://api.github.com/users/{username}/events"
    
    try:
        # Create request with a user agent (GitHub API requires one)
        headers = {"User-Agent": "GitHub-Activity-CLI"}
        req = Request(url, headers=headers)
        
        with urlopen(req, timeout=5) as response:
            data = response.read().decode("utf-8")
            return json.loads(data)
            
    except HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found on GitHub")
        else:
            print(f"Error: GitHub API returned status code {e.code}")
        return None
        
    except URLError as e:
        print(f"Error: Network error - {e.reason}")
        return None
        
    except json.JSONDecodeError:
        print("Error: Failed to parse GitHub API response")
        return None
        
    except Exception as e:
        print(f"Error: {e}")
        return None

def format_activity(event):
    """
    Format a single GitHub event for display.
    
    Args:
        event: GitHub event dictionary
        
    Returns:
        Formatted activity string
    """
    event_type = event.get("type", "Unknown")
    repo_name = event.get("repo", {}).get("name", "Unknown")
    payload = event.get("payload", {})
    
    # Format based on event type
    if event_type == "PushEvent":
        commits = payload.get("commits", [])
        count = len(commits)
        return f"- Pushed {count} commit{'s' if count != 1 else ''} to {repo_name}"
        
    elif event_type == "CreateEvent":
        ref_type = payload.get("ref_type", "repository")
        if ref_type == "branch":
            ref_name = payload.get("ref", "")
            return f"- Created branch '{ref_name}' in {repo_name}"
        elif ref_type == "tag":
            ref_name = payload.get("ref", "")
            return f"- Created tag '{ref_name}' in {repo_name}"
        else:
            return f"- Created {ref_type} in {repo_name}"
        
    elif event_type == "IssuesEvent":
        action = payload.get("action", "")
        issue_num = payload.get("issue", {}).get("number", "")
        if action == "opened":
            return f"- Opened a new issue in {repo_name}"
        else:
            return f"- {action.capitalize()}d issue #{issue_num} in {repo_name}"
        
    elif event_type == "PullRequestEvent":
        action = payload.get("action", "")
        pr_num = payload.get("pull_request", {}).get("number", "")
        if action == "opened":
            return f"- Opened a new pull request in {repo_name}"
        else:
            return f"- {action.capitalize()}d pull request #{pr_num} in {repo_name}"
        
    elif event_type == "WatchEvent":
        return f"- Starred {repo_name}"
        
    elif event_type == "ForkEvent":
        return f"- Forked {repo_name}"
        
    elif event_type == "DeleteEvent":
        ref_type = payload.get("ref_type", "")
        ref_name = payload.get("ref", "")
        return f"- Deleted {ref_type} '{ref_name}' in {repo_name}"
        
    elif event_type == "PullRequestReviewEvent":
        return f"- Reviewed a pull request in {repo_name}"
        
    elif event_type == "IssueCommentEvent":
        return f"- Commented on an issue in {repo_name}"
        
    elif event_type == "PublicEvent":
        return f"- Made {repo_name} public"
        
    else:
        return f"- {event_type} in {repo_name}"

def display_activity(events):
    """
    Display GitHub activity in terminal.
    
    Args:
        events: List of GitHub events
    """
    if not events:
        print("No recent activity found.")
        return
    
    print(f"Recent activity ({len(events)} events):\n")
    
    for event in events:
        activity_str = format_activity(event)
        if activity_str:
            print(activity_str)

def main():
    """Main entry point for the CLI."""
    if len(sys.argv) < 2:
        print("Usage: python github_activity.py <username>")
        print("Example: python github_activity.py hoa2000kxpt")
        sys.exit(1)
    
    username = sys.argv[1]
    
    # Fetch and display activity
    print(f"Fetching activity for user '{username}'...\n")
    events = fetch_user_activity(username)
    
    if events is not None:
        display_activity(events)


if __name__ == "__main__":
    main()
