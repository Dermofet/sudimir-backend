from pydantic import ConfigDict, BaseModel


class ApiModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True, populate_by_name=True, from_attributes=True)
