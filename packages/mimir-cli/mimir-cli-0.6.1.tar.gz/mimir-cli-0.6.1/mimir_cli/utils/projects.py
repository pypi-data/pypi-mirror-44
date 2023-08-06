"""
project related utility functions
"""
import click
import json
import requests
from mimir_cli.strings import PROJECT_PROMPT
from mimir_cli.utils.io import js_ts_to_str
from mimir_cli.utils.state import debug, api_projects_url, error_out


NAME_JUSTIFY = 40


def print_projects(projects, verbose=False):
    """print a list of projects in a nice way"""
    project_strings = [
        "[{num}]{id}\t{name}\t{remaining}\t{due}".format(
            num=x,
            id="\t{}".format(p["id"]) if verbose else "",
            name=p["name"][:NAME_JUSTIFY].ljust(NAME_JUSTIFY),
            remaining=(
                "∞"
                if p["unlimitedSubmissions"]
                else "{} left".format(p["submissionsLeft"])
            ).ljust(10),
            due=js_ts_to_str(p["dueDate"]),
        )
        for x, p in enumerate(projects)
    ]
    click.echo(
        "num{}\t{}\tsubmissions\tdue date".format(
            "\tproject_id\t\t\t" if verbose else "", "project".ljust(NAME_JUSTIFY)
        )
    )
    click.echo("-" * (131 if verbose else 91))
    click.echo("\n".join(project_strings))


def get_projects_list(credentials):
    """gets the projects list for a user, sorted by due date"""
    projects_request = requests.get(
        api_projects_url(),
        cookies=credentials if "user_session_id" in credentials else {},
        headers={"Authorization": credentials["api_token"]}
        if "api_token" in credentials
        else {},
    )
    if projects_request.status_code == 401:
        error_out("project ls failed: unauthorized - please try logging back in!")
    result = json.loads(projects_request.text)
    debug(result)
    sorted_projects = sorted(result["projects"], key=lambda x: x["dueDate"])
    return sorted_projects


def prompt_for_project(projects):
    """prompts for which project"""
    print_projects(projects)
    choice = click.prompt(PROJECT_PROMPT, type=int, default=0)
    return projects[choice]
