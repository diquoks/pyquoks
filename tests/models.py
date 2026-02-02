import pydantic


class TestModel(pydantic.BaseModel):
    test: str


class TestDataModel(pydantic.BaseModel):
    id: int
    test_data: str
