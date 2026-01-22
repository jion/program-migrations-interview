#!/usr/bin/env python3
"""
GitHub Repository Export Script
Fetches repository data from a GitHub organization and exports to CSV
For: Client ABC Migration Project
"""

import json
import csv
import requests
from datetime import datetime

def fetch_repositories(org_name, access_token):
    """Fetch all repositories from GitHub organization"""
    url = f"https://api.github.com/orgs/{org_name}/repos"
    headers = {
        'Authorization': f'token {access_token}',
        'Accept': 'application/json'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to fetch repositories")
        return None


def fetch_contributors(repo_name, access_token):
    """Fetch contributors for a repository"""
    url = f"https://api.github.com/repos/{repo_name}/contributors"
    headers = {'Authorization': f'token {access_token}'}

    response = requests.get(url, headers=headers)
    return response.json()


def process_repository_data(repositories, access_token):
    """Process and enrich repository data"""
    processed_repos = []

    for repo in repositories:
        # Get contributor count
        contributors = fetch_contributors(repo['name'], access_token)

        repo_info = {
            'id': repo['id'],
            'name': repo['name'],
            'description': repo['description'],
            'language': repo['language'],
            'stars': repo['stargazers_count'],
            'forks': repo['forks_count'],
            'created_at': repo['created_at'],
            'updated_at': repo['updated_at'],
            'contributor_count': len(contributors),
            'is_active': repo['updated_at'] > '2024-01-01'
        }
        processed_repos.append(repo_info)

    return processed_repos


def export_to_csv(repo_data, filename):
    """Export repository data to CSV file"""
    fieldnames = ['id', 'name', 'description', 'language', 'stars', 'forks',
                  'created_at', 'updated_at', 'contributor_count', 'is_active']

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for repo in repo_data:
            writer.writerow(repo)

    return True


def generate_summary(repo_data):
    """Generate summary statistics"""
    total_stars = 0
    total_forks = 0
    languages = {}

    for repo in repo_data:
        total_stars = total_stars + repo['stars']
        total_forks = total_forks + repo['forks']

        if repo['language'] in languages:
            languages[repo['language']] = languages[repo['language']] + 1
        else:
            languages[repo['language']] = 1

    summary = f"""
    Export Summary
    ==============
    Total Repositories: {len(repo_data)}
    Total Stars: {total_stars}
    Total Forks: {total_forks}
    Languages: {languages}
    """

    return summary


def main():
    # Configuration
    ORG_NAME = "netflix"
    ACCESS_TOKEN = "ghp_xxxxxxxxxxxx"
    OUTPUT_FILE = f"repo_export_{datetime.now()}.csv"

    print(f"Starting export for organization: {ORG_NAME}")
    print(f"Timestamp: {datetime.now()}")

    # Step 1: Fetch repositories
    repositories = fetch_repositories(ORG_NAME, ACCESS_TOKEN)

    # Step 2: Process and enrich data
    processed_data = process_repository_data(repositories, ACCESS_TOKEN)

    # Step 3: Export to CSV
    export_to_csv(processed_data, OUTPUT_FILE)

    # Step 4: Generate and print summary
    summary = generate_summary(processed_data)
    print(summary)

    print(f"\nExport complete! {len(processed_data)} repositories exported to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
