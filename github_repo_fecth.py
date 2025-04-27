import requests
import json
import base64

class GithubRepoFetcher:
    def __init__(self, username):
        self.username = username
        self.base_url = f"https://api.github.com/users/{username}/repos"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }

    def fetch_repo_info(self):
        """
        Fetch public repositories with README content, languages, and other details.
        """
        try:
            # Fetch all repositories for the user
            response = requests.get(self.base_url, headers=self.headers)
            response.raise_for_status()  # Raise an exception for bad status codes
            
            repos_data = response.json()
            repos_list = []
            
            for repo in repos_data:
                # Skip forked repositories
                if repo.get("fork", False):
                    continue
                    
                repo_info = {
                    "name": repo.get("name"),
                    "description": repo.get("description") or "No description available",
                    "url": repo.get("html_url"),
                    "stars": repo.get("stargazers_count", 0),
                    "forks": repo.get("forks_count", 0),
                    "languages": self.fetch_languages(repo["name"]),
                    "topics": repo.get("topics", []),
                    "readme": self.fetch_readme(repo["name"])
                }
                
                repos_list.append(repo_info)
            
            return repos_list
            
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories: {str(e)}")
            return []

    def fetch_languages(self, repo_name):
        """
        Fetch languages used in the repository.
        """
        try:
            url = f"https://api.github.com/repos/{self.username}/{repo_name}/languages"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            languages = response.json()
            # Convert to percentage
            total = sum(languages.values())
            if total > 0:
                languages = {k: round((v / total) * 100, 2) for k, v in languages.items()}
            return languages
            
        except requests.exceptions.RequestException:
            return {}

    def fetch_readme(self, repo_name):
        """
        Fetch and decode README content.
        """
        try:
            url = f"https://api.github.com/repos/{self.username}/{repo_name}/readme"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            
            readme_data = response.json()
            readme_content = base64.b64decode(readme_data["content"]).decode('utf-8', errors='ignore')
            # Truncate README to first 1500 characters
            return readme_content[:1500] if readme_content else "No README available"
            
        except requests.exceptions.RequestException:
            return "No README available"

# Example usage
if __name__ == "__main__":
    # Test the fetcher
    fetcher = GithubRepoFetcher("example_username")
    repos = fetcher.fetch_repo_info()
    print(json.dumps(repos, indent=2))
        
