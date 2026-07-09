#!/usr/bin/env python3
# tool/str/business-analyst/acceptance-criteria.py — Parse requirement → GWT criteria
import argparse, re, sys

TEMPLATES = {
    "login": [
        "Given a registered user with valid credentials",
        "When they submit the login form with correct email and password",
        "Then they are authenticated and redirected to the dashboard",
        "",
        "Given a registered user with invalid credentials",
        "When they submit the login form with incorrect password",
        "Then they see an error message and are not authenticated",
    ],
    "crud": [
        "Given an authenticated user",
        "When they create a new {entity} with valid data",
        "Then the {entity} is saved and they see a success confirmation",
        "",
        "Given an authenticated user with an existing {entity}",
        "When they update the {entity} with new valid data",
        "Then the {entity} changes are persisted",
        "",
        "Given an authenticated user with an existing {entity}",
        "When they delete the {entity}",
        "Then the {entity} is removed from the system",
    ],
    "search": [
        "Given a set of {items} in the system",
        "When the user searches for '{query}'",
        "Then results matching '{query}' are displayed",
        "",
        "Given no {items} match the search query",
        "When the user searches for '{query}'",
        "Then they see an empty state with a helpful message",
    ],
    "auth": [
        "Given an unauthenticated user",
        "When they access a protected resource",
        "Then they are redirected to the login page",
        "",
        "Given an authenticated user without required role",
        "When they access a role-protected resource",
        "Then they see a 403 Forbidden response",
    ],
}


def generate(requirement, entity=None, query=None, items=None):
    req_lower = requirement.lower()
    for keyword, template in TEMPLATES.items():
        if keyword in req_lower:
            lines = []
            for line in template:
                if entity and "{entity}" in line:
                    line = line.replace("{entity}", entity)
                if query and "{query}" in line:
                    line = line.replace("{query}", query)
                if items and "{items}" in line:
                    line = line.replace("{items}", items)
                lines.append(line)
            return "\n".join(lines)
    return f"# No template matched for: {requirement}\n# Define GWT criteria manually."


def main():
    ap = argparse.ArgumentParser(description="Generate GWT acceptance criteria from requirement")
    ap.add_argument("requirement", nargs="?", help="Requirement description")
    ap.add_argument("--entity", help="Entity name for CRUD templates")
    ap.add_argument("--query", help="Search query for search templates")
    ap.add_argument("--items", help="Item type for search templates")
    args = ap.parse_args()

    if args.requirement:
        print(generate(args.requirement, args.entity, args.query, args.items))
    else:
        print("Available templates: login, crud, search, auth")
        print("Usage: acceptance-criteria.py <requirement> [--entity X] [--query Y]")


if __name__ == "__main__":
    main()
