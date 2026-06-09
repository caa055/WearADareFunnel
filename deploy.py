import subprocess

def push_updates():
    print("Pushing updated catalog to live server...")
    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Automated product sync"])
    subprocess.run(["git", "push", "origin", "main"])
    print("Done! GitHub Actions will update your live site within 30 seconds.")

if __name__ == "__main__":
    push_updates()