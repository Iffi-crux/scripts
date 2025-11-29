import requests
import sys
import time

# --- CONFIGURATION ---
# Target organization/user
TARGET_USER = "hackycorp"

# PASTE YOUR GITHUB TOKEN HERE to increase rate limits (5000 req/hr)
# Example: "ghp_xxxxxxxxxxxx"
GITHUB_TOKEN = "" 

print(f"[*] Hunting for public repositories for user: {TARGET_USER}")
print("---------------------------------------------------------")

# Headers for authentication
headers = {}
if GITHUB_TOKEN:
    headers["Authorization"] = f"token {GITHUB_TOKEN}"
else:
    print("[!] Warning: No GITHUB_TOKEN provided. You may hit rate limits (60 req/hr).")

# GitHub API URL for user repos
url = f"https://api.github.com/users/{TARGET_USER}/repos"

def get_file_content(download_url):
    """Helper to download and return text content of a file"""
    try:
        # Pass headers to ensure we don't burn rate limits on file downloads if possible
        r = requests.get(download_url, headers=headers)
        if r.status_code == 200:
            return r.text
        return f"[Error: Status {r.status_code}]"
    except Exception as e:
        return f"[Error: {e}]"

try:
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        repos = response.json()
        
        if not repos:
            print("[!] No public repositories found.")
        else:
            print(f"[+] Found {len(repos)} repositories. Starting extraction phase...\n")
            
            for repo in repos:
                repo_name = repo['name']
                print(f"\n[+] Repository: {repo_name}")
                print(f"    URL: {repo['html_url']}")
                print("-" * 30)
                
                # Build API URL for repo contents (Root Directory)
                contents_url = f"https://api.github.com/repos/{TARGET_USER}/{repo_name}/contents"
                contents_resp = requests.get(contents_url, headers=headers)
                
                if contents_resp.status_code == 200:
                    files = contents_resp.json()
                    
                    for file in files:
                        fname = file['name']
                        ftype = file['type']
                        
                        print(f"    - {fname} [{ftype}]")
                        
                        # Check for files, not directories
                        if ftype == 'file':
                            download_url = file['download_url']
                            
                            # --- AUTOMATED EXTRACTION LOGIC ---
                            # In CTFs, we look for low-hanging fruit: configs, envs, secrets, flags
                            keywords = ['flag', 'secret', 'config', 'env', 'pass', 'key', 'todo', 'admin']
                            
                            if any(k in fname.lower() for k in keywords):
                                print(f"      [!] INTERESTING FILE DETECTED. Extracting...")
                                content = get_file_content(download_url)
                                print(f"      --- CONTENT START ---")
                                print(content)
                                print(f"      --- CONTENT END ---")
                                
                elif contents_resp.status_code == 403:
                     print(f"    [!] Rate Limit Exceeded during content scan. Add a Token!")
                     break
                else:
                    print(f"    [!] Failed to list contents (Status: {contents_resp.status_code}).")
            
            print("\n[*] Reconnaissance and extraction complete.")
            
    elif response.status_code == 403:
        print("[!] FATAL: API Rate Limit Exceeded.")
        print("    Solution: Add a GITHUB_TOKEN to the script.")
    elif response.status_code == 404:
        print(f"[!] User '{TARGET_USER}' not found on GitHub.")
    else:
        print(f"[!] Error: API returned status code {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"[!] Connection failed: {e}")
