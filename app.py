from flask import Flask, render_template, request
import requests 

app = Flask(__name__)

@app.route("/")
def hello_world():
    return render_template("index.html")

@app.route("/github")
def github_form():
    return render_template("githubusername.html")


@app.route("/submit", methods=["POST"])
def submit():
    input_name = request.form.get("name")
    input_age = request.form.get("age")

@app.route("/GHsubmit", methods=["POST"])
def GHsubmit():
    input_GithubUsername = request.form.get("username")

    github_url = "https://api.github.com/users/" + input_GithubUsername + "/repos"
    print("Trying to request: " + github_url)

    response = requests.get(github_url)
    print("Response Status Code:", response.status_code) 

    if response.status_code == 200:
        repos = response.json()
        print("Repositories Fetched:", repos)  # Debug: Print the repos list to confirm data
        
        if not repos:
            print("No repositories found.") 
        for repo in repos:
            print(repo["full_name"])

            # Check if the repository is public or private
            repo['is_private'] = "Private" if repo['private'] else "Public"
            print(f"{repo['full_name']} visibility: {repo['is_private']}") 

            commits_url = f"https://api.github.com/repos/{input_GithubUsername}/{repo['name']}/commits"
            commits_response = requests.get(commits_url)
            
            if commits_response.status_code == 200:
                commits = commits_response.json()
                if commits:
                    latest_commit = commits[0]  # Get the latest commit
                    # Add latest commit info to the repo dictionary
                    repo['commit_hash'] = latest_commit['sha']
                    repo['commit_author'] = latest_commit['commit']['author']['name']
                    repo['commit_date'] = latest_commit['commit']['author']['date']
                    repo['commit_message'] = latest_commit['commit']['message']
                else:
                    # If no commits are found
                    repo['commit_hash'] = "N/A"
                    repo['commit_author'] = "N/A"
                    repo['commit_date'] = "N/A"
                    repo['commit_message'] = "No commits"
            else:
                # Handle error if unable to fetch commits
                repo['commit_hash'] = "Error"
                repo['commit_author'] = "Error"
                repo['commit_date'] = "Error"
                repo['commit_message'] = "Error fetching commits"

    else:
        repos = []

    return render_template("github_results.html", repos=repos, username=input_GithubUsername)


@app.route("/query", methods=["GET"])
def process_query_route():
    query = request.args.get("q")
    return process_query(query)


def process_query(query):
    if query == "dinosaurs":
        return "Dinosaurs ruled the Earth 200 million years ago"
    elif query == "asteroids":
        return "Unknown"
    else:
        return "Unknown"
