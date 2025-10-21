# GitHub User Activity CLI 🖥️
The [GitHub User Activity](https://roadmap.sh/projects/github-user-activity) challenge from [roadmap.sh](https://roadmap.sh/).

A command-line tool that fetches and displays the recent activity of a specified GitHub user. This project uses the GitHub API to show various events like pushes, issues, stars, and more, allowing users to monitor the activities of any GitHub profile directly from the terminal.

## **Features**
- Fetches recent activities of a GitHub user.
- Displays events such as push, star, fork, and issue creation.
- Handles errors gracefully, including invalid usernames, network issues, and API rate limits.

## **Installation**

1. **Clone the Repository:**
   ```bash
   https://github.com/hoa2000kxpt/python_dev_roadmap_GitHubUserActivity.git
   ```
   
2. **Ensure Python is Installed:** 
Make sure you have Python 3.6 or higher installed on your machine. You can check this by running:
   ```bash
   python --version
   ```
   
## **Usage**
To fetch the recent activity of a GitHub user, run the CLI tool from the terminal:
```bash
   python github_activity.py <username>
```
Replace <username> with the actual GitHub username you want to check.

### **Example**
To fetch the activity for user `hoa2000kxpt`:

```bash
   python github_activity.py hoa2000kxpt
```
### **Sample Output**
```bash
Performed CreateEvent in hoa2000kxpt/python_dev_roadmap_GitHubUserActivity
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_GitHubUserActivity
Performed CreateEvent in hoa2000kxpt/python_dev_roadmap_GitHubUserActivity
Performed CreateEvent in hoa2000kxpt/python_dev_roadmap_GitHubUserActivity
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 5 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Performed CreateEvent in hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Performed CreateEvent in hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Pushed 1 commit(s) to hoa2000kxpt/python_dev_roadmap_TaskTrackerCLI
Starred sontn/ragwithllamaindex
```