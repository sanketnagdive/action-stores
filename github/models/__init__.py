from typing import Literal

DEFAULT_GH_ORG ="kubiya-se"

GitHubPlayGroundOrg= Literal[DEFAULT_GH_ORG]


TEST_REPOS=[
    "sample-repo1",
    "sample-repo2"
]

GitHubPlayGroundRepos= Literal[*TEST_REPOS]

DEFAULT_BRANCH="main"