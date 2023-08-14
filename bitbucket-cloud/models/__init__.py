from typing import Literal

DEFAULT_BB_WORKSPACE ="kubiya-se"

BitBucketPlayGroundWorkspace= Literal[DEFAULT_BB_WORKSPACE]


TEST_REPOS=["test-repo","dummy-repo"]

BitBucketPlayGroundRepos= Literal[*TEST_REPOS]

DEFAULT_BRANCH="master"