import typing
import requests

from .base import BaseClient


class Client(BaseClient):
    def __init__(self, user, password, owner=None):
        """Initial session with user/password, and setup repository owner

        Args:
            params:

        Returns:

        """
        super().__init__(user, password, owner)

        # for shared repo, set baseURL to owner
        if owner is None:
            user_data = self.get_user()
            owner = user_data.get("username")
        self.workspace = owner

    def get_user(self, params=None):
        """Returns the currently logged in user.

        Args:
            params:

        Returns:

        """
        return self._get("2.0/user", params=params)

    def _get_objs(
                self,
                repository_slug: str,
                objs: typing.List[typing.Dict[str, typing.Any]],
                params=None,
        ) -> typing.List[dict[str, typing.Any]]:
        files = []
        for obj in objs:
            if obj.get("type") == "commit_directory":
                link = obj.get("links", {}).get("self", {}).get("href")
                print(f"link: {link}")
                if link is None:
                    continue
                folder_objs = self._get(link, params=params)
                files = files + self._get_objs(
                    repository_slug, list(folder_objs), params=params
                )
            elif obj.get("type") == "commit_file":
                files.append(
                    {
                        "path": obj["path"],
                        "commit_hash": obj["commit"]["hash"],
                    }
                )
        return files

    def _get(self, endpoint: str, params=None):
        print(f"GET {endpoint}")

        all_results = []  # List to store all paginated results

        while endpoint:
            response = requests.get(
                endpoint if endpoint.startswith("http") else self.BASE_URL + endpoint,
                params=params,
                auth=(self.user, self.password),
            )

            data = self.parse(response)
            if isinstance(data, dict) and "values" in data:
                # Paginated response
                all_results.extend(data["values"])

                # Check if there are more pages to fetch
                next_page = data.get("next")
                if next_page:
                    endpoint = next_page
                else:
                    endpoint = None
            else:
                # Non-paginated response
                all_results = data
                endpoint = None

        return all_results


    def _post_files(self, endpoint, params=None, data=None, files=None):
        print(f"MY POST {endpoint}")
        response = requests.post(
            self.BASE_URL + endpoint,
            params=params,
            data=data,
            files=files,
            auth=(self.user, self.password),
        )
        return self.parse(response)

    def _post(self, endpoint, params=None, data=None):
        print(f"POST {endpoint}")
        response = requests.post(
            self.BASE_URL + endpoint,
            params=params,
            json=data,
            auth=(self.user, self.password),
        )
        return self.parse(response)

    def _put(self, endpoint, params=None, data=None):
        print(f"PUT {endpoint}")
        response = requests.put(
            self.BASE_URL + endpoint,
            params=params,
            json=data,
            auth=(self.user, self.password),
        )
        return self.parse(response)

    def _delete(self, endpoint, params=None):
        print(f"DELETE {endpoint}")
        response = requests.delete(
            self.BASE_URL + endpoint, params=params, auth=(self.user, self.password)
        )
        return self.parse(response)