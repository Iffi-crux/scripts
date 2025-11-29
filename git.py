import requests
import sys

# Target organization/user
TARGET_USER = "hackycorp"

print(f"[*] Hunting for public repositories for user: {TARGET_USER}")
print("---------------------------------------------------------")

# GitHub API URL for user repos
url = f"https://api.github.com/users/{TARGET_USER}/repos"

try:
    response = requests.get(url)
    
    if response.status_code == 200:
        repos = response.json()
        
        if not repos:
            print("[!] No public repositories found.")
        else:
            print(f"[+] Found {len(repos)} repositories:\n")
            for repo in repos:
                print(f"Name: {repo['name']}")
                print(f"URL:  {repo['html_url']}")
                print(f"Desc: {repo['description']}")
                print("-" * 30)
                
            print("\n[*] NEXT STEPS:")
            print("1. Visit the URLs above.")
            print("2. Look for 'commits' history (the flag is often in an old commit).")
            print("3. Check for files named 'config', '.env', or 'secret'.")
            
    elif response.status_code == 404:
        print("[!] User 'hackycrop' not found on GitHub.")
    else:
        print(f"[!] Error: API returned status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"[!] Connection failed: {e}")
