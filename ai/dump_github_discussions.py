import json
import os
from typing import Any, Dict, List

import requests

GRAPHQL_API_ENDPOINT = "https://api.github.com/graphql"

TOKEN = os.environ["GITHUB_PERSONAL_ACCESS_TOKEN"]

# Repository details
OWNER = "google"
REPO = "mesop"


def get_discussions(owner: str, repo: str, token: str) -> List[Dict[str, Any]]:
  headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json",
  }

  query = """
    query($owner: String!, $repo: String!, $cursor: String) {
      repository(owner: $owner, name: $repo) {
        discussions(first: 100, after: $cursor) {
          pageInfo {
            hasNextPage
            endCursor
          }
          nodes {
            id
            title
            url
            createdAt
            category {
              name
            }
            author {
              login
            }
            body
            answer {
              author {
                login
              }
              body
              createdAt
              isAnswer
            }
          }
        }
      }
    }
    """

  discussions: List[Any] = []
  has_next_page = True
  cursor = None

  while has_next_page:
    variables = {"owner": owner, "repo": repo, "cursor": cursor}

    response = requests.post(
      GRAPHQL_API_ENDPOINT,
      headers=headers,
      json={"query": query, "variables": variables},
    )

    if response.status_code == 200:
      data = response.json()
      if "errors" in data:
        print(f"GraphQL Errors: {json.dumps(data['errors'], indent=2)}")
        break
      discussion_data = data["data"]["repository"]["discussions"]
      discussions.extend(discussion_data["nodes"])
      has_next_page = discussion_data["pageInfo"]["hasNextPage"]
      cursor = discussion_data["pageInfo"]["endCursor"]
    else:
      print(f"Error fetching discussions: {response.status_code}")
      print(f"Response content: {response.text}")
      break

  return discussions


def write_discussions_to_file(
  discussions: List[Dict[str, Any]], filename: str
) -> None:
  with open(filename, "w", encoding="utf-8") as f:
    for discussion in discussions:
      f.write(f"Discussion: {discussion['title']}\n")
      f.write(f"URL: {discussion['url']}\n")
      f.write(f"Category: {discussion['category']['name']}\n")
      f.write(f"Author: {discussion['author']['login']}\n")
      f.write(f"Created at: {discussion['createdAt']}\n")
      f.write(f"Body:\n{discussion['body']}\n")

      # Add recommended answer if available
      if discussion["answer"]:
        recommended_answer = discussion["answer"]
        f.write("\nRecommended answer:\n")
        f.write(f"Author: {recommended_answer['author']['login']}\n")
        f.write(f"Created at: {recommended_answer['createdAt']}\n")
        f.write(f"Body:\n{recommended_answer['body']}\n")
      else:
        f.write("\nNo recommended answer yet.\n")

      f.write("-" * 50 + "\n\n")


if __name__ == "__main__":
  discussions = get_discussions(OWNER, REPO, TOKEN)
  if discussions:
    filename = "gen/prompt_context/discussions.txt"
    write_discussions_to_file(discussions, filename)
    print(f"Discussions extracted to {filename}")
  else:
    print("No discussions found or error occurred")
