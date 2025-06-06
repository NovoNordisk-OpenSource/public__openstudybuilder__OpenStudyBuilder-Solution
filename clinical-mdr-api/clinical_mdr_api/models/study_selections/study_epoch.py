from typing import Annotated

from pydantic import Field

from clinical_mdr_api.models.controlled_terminologies.ct_term import (
    SimpleCTTermNameWithConflictFlag,
)
from clinical_mdr_api.models.utils import BaseModel, PatchInputModel, PostInputModel
from common import config


class StudyEpochCreateInput(PostInputModel):
    study_uid: Annotated[str, Field()]
    start_rule: Annotated[
        str | None,
        Field(
            description="Study Epoch Start description",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    end_rule: Annotated[
        str | None,
        Field(
            description="Study Epoch end description",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    epoch: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = None
    epoch_subtype: Annotated[str, Field()]
    duration_unit: Annotated[
        str | None,
        Field(
            description="Study Epoch duration preferred unit",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    order: Annotated[
        int | None,
        Field(
            description="The ordering of the selection",
            json_schema_extra={"nullable": True},
            gt=0,
            lt=config.MAX_INT_NEO4J,
        ),
    ] = None
    description: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = (
        None
    )
    duration: Annotated[
        int | None,
        Field(
            description="Calculated epoch duration",
            json_schema_extra={"nullable": True},
            lt=config.MAX_INT_NEO4J,
        ),
    ] = None
    color_hash: Annotated[
        str | None,
        Field(
            description="Epoch Color for display", json_schema_extra={"nullable": True}
        ),
    ] = "#FFFFFF"


class StudyEpochEditInput(PatchInputModel):
    study_uid: Annotated[str, Field()]
    start_rule: Annotated[
        str | None, Field(description="Study Epoch Start description")
    ] = None
    end_rule: Annotated[
        str | None, Field(description="Study Epoch end description")
    ] = None
    epoch: Annotated[str | None, Field()] = None
    duration_unit: Annotated[
        str | None, Field(description="Study Epoch duration preferred unit")
    ] = None
    order: Annotated[
        int | None,
        Field(
            description="The ordering of the selection", gt=0, lt=config.MAX_INT_NEO4J
        ),
    ] = None
    description: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = (
        None
    )
    duration: Annotated[
        int | None,
        Field(description="Calculated epoch duration", lt=config.MAX_INT_NEO4J),
    ] = None
    color_hash: Annotated[str | None, Field(description="Epoch Color for display")] = (
        "#FFFFFF"
    )
    # Override epoch from Create Input to make it Optional
    epoch_subtype: Annotated[str | None, Field()] = None
    change_description: Annotated[str, Field()]


class StudyEpoch(BaseModel):
    study_uid: Annotated[str, Field()]
    start_rule: Annotated[
        str | None,
        Field(
            description="Study Epoch Start description",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    end_rule: Annotated[
        str | None,
        Field(
            description="Study Epoch end description",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    epoch: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = None
    duration_unit: Annotated[
        str | None,
        Field(
            description="Study Epoch duration preferred unit",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    order: Annotated[
        int | None,
        Field(
            description="The ordering of the selection",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    description: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = (
        None
    )
    duration: Annotated[
        int | None,
        Field(
            description="Calculated epoch duration",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    color_hash: Annotated[
        str | None,
        Field(
            description="Epoch Color for display", json_schema_extra={"nullable": True}
        ),
    ] = "#FFFFFF"

    epoch_name: Annotated[str, Field(description="Name of the epoch based on CT term")]
    epoch_subtype_name: Annotated[
        str | None,
        Field(
            description="Name of the epoch sub type based on CT term",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    epoch_type_name: Annotated[str, Field()]
    epoch_subtype: Annotated[
        str | None, Field(json_schema_extra={"nullable": True})
    ] = None
    uid: Annotated[str, Field()]
    study_version: Annotated[
        str | None,
        Field(
            title="study version or date information",
            description="Study version number, if specified, otherwise None.",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    epoch_ctterm: Annotated[
        SimpleCTTermNameWithConflictFlag, Field(title="Study epoch Term")
    ]
    epoch_subtype_ctterm: Annotated[
        SimpleCTTermNameWithConflictFlag, Field(title="Study Epoch subtype Term")
    ]
    epoch_type_ctterm: Annotated[
        SimpleCTTermNameWithConflictFlag, Field(title="Study Epoch type CTTermName")
    ]
    start_day: Annotated[
        int | None,
        Field(title="Study Epoch start day", json_schema_extra={"nullable": True}),
    ] = None
    end_day: Annotated[
        int | None,
        Field(title="Study Epoch end day", json_schema_extra={"nullable": True}),
    ] = None
    start_week: Annotated[
        int | None,
        Field(title="Study Epoch start week", json_schema_extra={"nullable": True}),
    ] = None
    end_week: Annotated[
        int | None,
        Field(title="Study Epoch end week", json_schema_extra={"nullable": True}),
    ] = None
    start_date: Annotated[
        str, Field(description="Study Epoch initial modification date")
    ]
    end_date: Annotated[
        str | None,
        Field(
            description="Study Epoch last modification date",
            json_schema_extra={"nullable": True},
        ),
    ] = None
    status: Annotated[str, Field(description="Study Epoch status")]
    author_username: Annotated[
        str | None, Field(json_schema_extra={"nullable": True})
    ] = None
    possible_actions: Annotated[
        list[str],
        Field(description="List of actions to perform on item"),
    ]
    change_description: Annotated[
        str | None,
        Field(
            description="Description of change reasons",
            json_schema_extra={"nullable": True},
        ),
    ] = ""
    study_visit_count: Annotated[
        int, Field(description="Count of Study Visits assigned to Study Epoch")
    ]
    change_type: Annotated[str | None, Field(json_schema_extra={"nullable": True})] = (
        None
    )


class StudyEpochVersion(StudyEpoch):
    changes: Annotated[list[str], Field()]


class StudyEpochTypes(BaseModel):
    type: Annotated[str, Field(description="Study Epoch type")]
    type_name: Annotated[str, Field()]
    subtype: Annotated[str, Field(description="Study Epoch subtype")]
    subtype_name: Annotated[str, Field()]
