import inspect
from typing import Any

from pydantic import ConfigDict, BaseModel
from pydantic.fields import FieldInfo


class ApiModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, from_attributes=True)
