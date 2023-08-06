from typing import List

from pydantic import BaseModel


from .. import action_store
from .. bitbucket_wrapper import get_client

from ..models.kubiya_custome import (
    EditYamlFileParams,EditYamlFileResponse
)





@action_store.kubiya_action()
def edit_yaml_file(input: EditYamlFileParams)->EditYamlFileResponse:
    client = get_client(input.workspace)

    template_yaml=client._get("2.0/repositories/{}/{}/src/{}/{}".format(input.workspace,
                                                                        input.template_repository,
                                                                        input.template_commit_id,
                                                                        input.template_file_path),params=None)
    # Replace placeholders in the YAML content
    template_yaml = template_yaml.replace("KUBIYA_PARAM_1", input.kubiya_param_1)
    template_yaml = template_yaml.replace("KUBIYA_PARAM_2", input.kubiya_param_2)


    """files ex.
        files = {
            "folder123/file1": ("file1", "content"),
            "folder123/file2": ("file2", "content2"),
        }
        """

    res= client._post_files("2.0/repositories/{}/{}/src".format(input.workspace,
                                                                input.destination_repository_slug),
                            params=None,
                            data={"message": input.commit_message,"branch": input.destination_branch,},
                            files={input.destination_file_path: template_yaml},
                            )
    return res