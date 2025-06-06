from datetime import datetime
from typing import Annotated, Self

from pydantic import Field

from clinical_mdr_api.models.controlled_terminologies.ct_package import (
    CodelistChangeItem,
    TermChangeItem,
)
from clinical_mdr_api.models.utils import BaseModel


class CTCatalogue(BaseModel):
    name: Annotated[str, Field()]

    library_name: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = (
        None
    )


class CTCatalogueChanges(BaseModel):
    start_datetime: Annotated[datetime, Field()]
    end_datetime: Annotated[datetime, Field()]
    new_codelists: Annotated[list[CodelistChangeItem], Field()]
    deleted_codelists: Annotated[list[CodelistChangeItem], Field()]
    updated_codelists: Annotated[list[CodelistChangeItem], Field()]
    new_terms: Annotated[list[TermChangeItem], Field()]
    deleted_terms: Annotated[list[TermChangeItem], Field()]
    updated_terms: Annotated[list[TermChangeItem], Field()]

    @classmethod
    def from_repository_output(
        cls, start_datetime: datetime, end_datetime: datetime, query_output
    ) -> Self:
        return cls(
            start_datetime=start_datetime,
            end_datetime=end_datetime,
            new_codelists=[
                CodelistChangeItem.from_repository_output(item)
                for item in query_output["new_codelists"]
            ],
            updated_codelists=[
                CodelistChangeItem.from_repository_output(item)
                for item in query_output["updated_codelists"]
            ],
            deleted_codelists=[
                CodelistChangeItem.from_repository_output(item)
                for item in query_output["deleted_codelists"]
            ],
            new_terms=[
                TermChangeItem.from_repository_output(item)
                for item in query_output["new_terms"]
            ],
            updated_terms=[
                TermChangeItem.from_repository_output(item)
                for item in query_output["updated_terms"]
            ],
            deleted_terms=[
                TermChangeItem.from_repository_output(item)
                for item in query_output["deleted_terms"]
            ],
        )
