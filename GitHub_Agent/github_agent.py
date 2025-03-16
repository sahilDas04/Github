from github import Github
from git import Repo
import os
import shutil

GITHUB_TOKEN = input("Enter your GitHub Personal Access Token: ").strip()
GITHUB_USER = input("Enter your GitHub Username: ").strip()

g = Github(GITHUB_TOKEN)
user = g.get_user()

def create_repo(repo_name, description="", private=True):
    repo = user.create_repo(
        name=repo_name,
        description=description,
        private=private,
        auto_init=True 
    )
    print(f"Repository '{repo_name}' created successfully.")
    return repo

def delete_repo(repo_name):
    try:
        repo = g.get_repo(f"{GITHUB_USER}/{repo_name}")
        repo.delete()
        print(f"Repository '{repo_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting repository: {e}")

def fork_repo(owner, repo_name):
    repo_to_fork = g.get_repo(f"{owner}/{repo_name}")
    forked_repo = repo_to_fork.create_fork()
    print(f"Repository '{repo_name}' forked successfully to your account.")
    return forked_repo

def create_branch(repo_name, new_branch_name, source_branch='main'):
    repo = g.get_repo(f"{GITHUB_USER}/{repo_name}")
    source_ref = repo.get_git_ref(f"heads/{source_branch}")
    repo.create_git_ref(ref=f"refs/heads/{new_branch_name}", sha=source_ref.object.sha)
    print(f"Branch '{new_branch_name}' created from '{source_branch}'.")

def commit_and_push(repo_url, repo_name, file_name, file_content, commit_message, branch='main'):
    local_dir = f"./{repo_name}"
    
    if os.path.exists(local_dir):
        shutil.rmtree(local_dir)  
    
    print(f"Cloning repository {repo_url}...")
    Repo.clone_from(repo_url, local_dir, branch=branch)
    
    file_path = os.path.join(local_dir, file_name)
    with open(file_path, 'w') as f:
        f.write(file_content)
    
    repo = Repo(local_dir)
    repo.git.add(file_name)
    repo.index.commit(commit_message)
    
    origin = repo.remote(name='origin')
    origin.push()
    
    print(f"Committed and pushed '{file_name}' to '{branch}'.")

def create_issue(repo_name, title, body=""):
    repo = g.get_repo(f"{GITHUB_USER}/{repo_name}")
    issue = repo.create_issue(title=title, body=body)
    print(f"Issue '{title}' created.")
    return issue

def create_pull_request(repo_name, head_branch, base_branch='main', title='Pull Request', body=''):
    repo = g.get_repo(f"{GITHUB_USER}/{repo_name}")
    pr = repo.create_pull(title=title, body=body, head=head_branch, base=base_branch)
    print(f"Pull request created: {pr.html_url}")
    return pr

def clone_repo(repo_url, clone_path):
    try:
        if not clone_path:
            repo_name = repo_url.rstrip('/').split('/')[-1]
            if repo_name.endswith('.git'):
                repo_name = repo_name[:-4]
            clone_path = os.path.join(os.getcwd(), repo_name)
        if os.path.exists(clone_path):
            print(f"Directory '{clone_path}' already exists. Deleting it for a clean clone...")
            shutil.rmtree(clone_path)
        
        print(f"Cloning repository from {repo_url} into '{clone_path}'...")
        Repo.clone_from(repo_url, clone_path)
        print(f"Repository cloned successfully into '{clone_path}'.")
    
    except Exception as e:
        print(f"Error cloning repository: {e}")


if __name__ == "__main__":
    while True:
        print("\nGitHub AI Agent - Choose an action:")
        print("1. Create Repo")
        print("2. Delete Repo")
        print("3. Fork Repo")
        print("4. Create Branch")
        print("5. Commit & Push File")
        print("6. Create Issue")
        print("7. Create Pull Request")
        print("8. Clone Repo")
        print("9. Exit")
        
        choice = input("Enter choice (1-8): ").strip()
        
        if choice == '1':
            repo_name = input("Enter new repo name: ").strip()
            desc = input("Enter repo description: ").strip()
            private = input("Private repo? (y/n): ").strip().lower() == 'y'
            create_repo(repo_name, desc, private)
            
        elif choice == '2':
            repo_name = input("Enter repo name to delete: ").strip()
            delete_repo(repo_name)
            
        elif choice == '3':
            owner = input("Enter owner of the repo to fork: ").strip()
            repo_name = input("Enter repo name to fork: ").strip()
            fork_repo(owner, repo_name)
            
        elif choice == '4':
            repo_name = input("Enter repo name: ").strip()
            branch_name = input("Enter new branch name: ").strip()
            source_branch = input("Enter source branch (default 'main'): ").strip() or 'main'
            create_branch(repo_name, branch_name, source_branch)
            
        elif choice == '5':
            repo_name = input("Enter repo name: ").strip()
            branch = input("Enter branch (default 'main'): ").strip() or 'main'
            repo_url = f"https://{GITHUB_TOKEN}@github.com/{GITHUB_USER}/{repo_name}.git"
            file_name = input("Enter file name: ").strip()
            file_content = input("Enter file content: ").strip()
            commit_message = input("Enter commit message: ").strip()
            commit_and_push(repo_url, repo_name, file_name, file_content, commit_message, branch)
            
        elif choice == '6':
            repo_name = input("Enter repo name: ").strip()
            issue_title = input("Enter issue title: ").strip()
            issue_body = input("Enter issue body: ").strip()
            create_issue(repo_name, issue_title, issue_body)
            
        elif choice == '7':
            repo_name = input("Enter repo name: ").strip()
            head_branch = input("Enter head branch: ").strip()
            base_branch = input("Enter base branch (default 'main'): ").strip() or 'main'
            pr_title = input("Enter pull request title: ").strip()
            pr_body = input("Enter pull request body: ").strip()
            create_pull_request(repo_name, head_branch, base_branch, pr_title, pr_body)
            
        elif choice == '8':
            repo_url = input("Enter the repository URL to clone: ").strip()
            
            clone_path = input("Enter the full directory path to clone into (leave blank to clone in current dir with repo name): ").strip()
            
            clone_repo(repo_url, clone_path)

        
        elif choice == '9':
            print("Exiting GitHub AI Agent.")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
