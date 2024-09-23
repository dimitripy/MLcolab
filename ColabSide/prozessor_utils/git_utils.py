# git_utils.py
import os
import git
import shutil

def check_project_version(project_path, branch):
    if not os.path.exists(project_path):
        print(f"Projektpfad {project_path} existiert nicht.")
        return False
    
    try:
        repo = git.Repo(project_path)
        remote_branches = [ref.name for ref in repo.remotes.origin.refs]
        if f'origin/{branch}' in remote_branches:
            print(f"Branch '{branch}' ist bereits lokal vorhanden.")
            return True
        else:
            print(f"Branch '{branch}' ist nicht lokal vorhanden.")
            return False
    except git.exc.InvalidGitRepositoryError:
        print(f"{project_path} ist kein gültiges Git-Repository.")
        return False
    except Exception as e:
        print(f"Fehler bei der Überprüfung des Branches: {str(e)}")
        return False

def clone_project_from_github(project_name, branch, project_path):
    github_url = f"https://github.com/dimitripy/{project_name}.git"
    branch = branch if branch else 'main'
    try:
        if os.path.exists(project_path):
            print(f"Projektpfad {project_path} existiert bereits. Aktualisiere Repository.")
            repo = git.Repo(project_path)
            repo.git.checkout(branch)
            repo.remotes.origin.pull(branch)
        else:
            shutil.rmtree(project_path, ignore_errors=True)
            print(f"Klonen des Branches '{branch}' von {github_url}")
            git.Repo.clone_from(github_url, project_path, branch=branch)
        return True, f"Branch '{branch}' erfolgreich geklont oder aktualisiert."
    except Exception as e:
        return False, str(e)
    