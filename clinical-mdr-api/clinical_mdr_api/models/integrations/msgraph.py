from typing import Annotated

from pydantic import BaseModel, Field


class GraphGroup(BaseModel):
    id: Annotated[str, Field(title="Unique identifier for the group")]
    display_name: str = Field(alias="displayName", title="Display name for the group")
    description: Annotated[
        str | None,
        Field(
            title="An optional description for the group",
            json_schema_extra={"nullable": True},
        ),
    ]


class GraphUser(BaseModel):
    id: Annotated[str, Field(title="Unique identifier for the user")]
    display_name: str | None = Field(
        None,
        alias="displayName",
        title="Name displayed in the address book for the user",
        json_schema_extra={"nullable": True},
    )
    given_name: str | None = Field(
        None,
        alias="givenName",
        title="First name of the user",
        json_schema_extra={"nullable": True},
    )
    email: str | None = Field(
        None,
        alias="mail",
        title="User's email address",
        json_schema_extra={"nullable": True},
    )
    surname: Annotated[
        str | None,
        Field(title="Last name of the user", json_schema_extra={"nullable": True}),
    ] = None
