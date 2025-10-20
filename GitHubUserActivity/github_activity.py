import argparse
import urllib.request
import json


# Function to fetch user activity from GitHub API
def fetch_user_activity(username):
    url = f"https://api.github.com/users/{username}/events/public"

    try:
        # Make a request to the GitHub API
        with urllib.request.urlopen(url) as response:
            data = response.read().decode()
            events = json.loads(data)

            if len(events) == 0:
                print(f"No recent activity found for {username}")
                return

            # Display the user activity
            for event in events:
                event_type = event["type"]
                repo_name = event["repo"]["name"]
                if event_type == "PushEvent":
                    commits = len(event["payload"]["commits"])
                    print(f"Pushed {commits} commit(s) to {repo_name}")
                elif event_type == "IssuesEvent":
                    action = event["payload"]["action"]
                    print(f"{action.capitaliz()} an issue in {repo_name}")
                elif event_type == "WatchEvent":
                    print(f"Starred {repo_name}")
                elif event_type == "ForkEvent":
                    print(f"Forked {repo_name}")
                else:
                    print(f"Performed {event_type} in {repo_name}")

    except urllib.error.HTTPError as e:
        if e.code == 404:
            print("User not found. Please check the username and try again.")
        elif e.code == 403:
            print("API rate limit exceeded. Please try again later.")
        else:
            print(f"HTTP Error: {e.code}")
    except urllib.error.URLError as e:
        print(f"Failed to connect to the GitHub API: {e.reason}")
    except json.JSONDecodeError:
        print("Failed to parse the response from the GitHub API.")


def main():
    parser = argparse.ArgumentParser(description="Fetch recent GitHub user activity.")
    parser.add_argument("username", help="GitHub username")
    args = parser.parse_args()

    fetch_user_activity(args.username)


if __name__ == "__main__":
    main()
