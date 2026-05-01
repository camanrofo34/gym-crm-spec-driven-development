from pydantic import BaseModel, ConfigDict


class AssignmentCreateRequest(BaseModel):
    trainee_id: int
    trainer_id: int


class AssignmentRead(BaseModel):
    id: int
    trainee_id: int
    trainer_id: int

    model_config = ConfigDict(from_attributes=True)

