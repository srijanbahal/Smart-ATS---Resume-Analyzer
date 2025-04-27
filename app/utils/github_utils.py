import requests
import json
import base64
import streamlit as st
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv
from utils.logging_utils import default_logger as logger

# Load environment variables
load_dotenv()
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

class GithubRepoFetcher:
    def __init__(self, username: str):
        """Initialize the GitHub repository fetcher.
        
        Args:
            username (str): GitHub username to fetch data for
        """
        self.username = username
        self.headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}
        self.base_url = f"https://api.github.com/repos/{username}"

    def fetch_languages(self, repo_name: str) -> Dict[str, float]:
        """Fetch languages used in a repository."""
        try:
            logger.debug(f"Fetching languages for repo: {repo_name}")
            response = requests.get(f"{self.base_url}/{repo_name}/languages", headers=self.headers)
            response.raise_for_status()
            
            languages = response.json()
            total = sum(languages.values())
            if total > 0:
                languages = {k: round((v / total) * 100, 2) for k, v in languages.items()}
            return languages
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch languages for {repo_name}: {str(e)}")
            return {}

    def fetch_readme(self, repo_name: str) -> str:
        """Fetch README content for a repository."""
        try:
            logger.debug(f"Fetching README for repo: {repo_name}")
            response = requests.get(
                f"{self.base_url}/{repo_name}/readme",
                headers={**self.headers, "Accept": "application/vnd.github.v3.raw"}
            )
            response.raise_for_status()
            return response.text
            
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to fetch README for {repo_name}: {str(e)}")
            return "No README available"

    def fetch_repo_info(self) -> Optional[Dict[str, Any]]:
        """
        Fetches repository information for the user
        
        Returns:
            Optional[Dict[str, Any]]: Dictionary containing GitHub data or None if failed
        """
        logger.info(f"Fetching GitHub data for username: {self.username}")
        
        try:
            # Fetch user data
            user_url = f"https://api.github.com/users/{self.username}"
            logger.debug(f"Making request to: {user_url}")
            user_response = requests.get(user_url, headers=self.headers)
            user_response.raise_for_status()
            user_data = user_response.json()
            
            # Fetch repositories
            repos_url = f"https://api.github.com/users/{self.username}/repos"
            logger.debug(f"Making request to: {repos_url}")
            repos_response = requests.get(repos_url, headers=self.headers)
            repos_response.raise_for_status()
            repos_data = repos_response.json()
            
            if not repos_data:
                logger.warning(f"No repositories found for user {self.username}")
                return None
                
            # Process repository data
            processed_repos = []
            for repo in repos_data:
                if not repo['fork']:  # Only include non-forked repositories
                    repo_info = {
                        'name': repo['name'],
                        'description': repo['description'] or "No description available",
                        'stars': repo['stargazers_count'],
                        'forks': repo['forks_count'],
                        'language': repo['language'],
                        'url': repo['html_url'],
                        'languages': self.fetch_languages(repo['name']),
                        'topics': repo.get('topics', []),
                        'readme': self.fetch_readme(repo['name'])
                    }
                    processed_repos.append(repo_info)
            
            github_data = {
                'username': self.username,
                'name': user_data.get('name'),
                'bio': user_data.get('bio'),
                'followers': user_data.get('followers'),
                'following': user_data.get('following'),
                'public_repos': user_data.get('public_repos'),
                'repositories': processed_repos
            }
            
            logger.info(f"Successfully fetched GitHub data for {self.username}")
            logger.debug(f"Processed GitHub data: {github_data}")
            return github_data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching GitHub data: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error while processing GitHub data: {str(e)}")
            return None

@st.cache_data(ttl=3600)
def fetch_github_data(username: str) -> Optional[Dict[str, Any]]:
    """
    Cached wrapper for fetching GitHub data
    
    Args:
        username (str): GitHub username
        
    Returns:
        Optional[Dict[str, Any]]: Dictionary containing GitHub data or None if failed
    """
    if not username:
        logger.warning("No username provided for GitHub data fetch")
        return None
    fetcher = GithubRepoFetcher(username)
    return fetcher.fetch_repo_info() 