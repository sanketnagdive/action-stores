from pydantic import BaseModel, Field
from enum import Enum
from typing import Any, List, Optional

class JiraField(Enum):
    ASSIGNEE = "fields.assignee.displayName"
    KEY = "key"
    URL = "self"
    DESCRIPTION = "fields.description"

class JiraFieldsSelection(BaseModel):
    fields: List[JiraField] = [JiraField.ASSIGNEE, JiraField.KEY, JiraField.URL, JiraField.DESCRIPTION]

class RunJQLParams(BaseModel):
    jql_query: str
    fields_selection: Optional[JiraFieldsSelection] = JiraFieldsSelection()
    max_results: Optional[int] = 50

class RunJQLResponse(BaseModel):
    issues: Any