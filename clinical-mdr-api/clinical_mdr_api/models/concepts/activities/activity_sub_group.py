from datetime import datetime
from typing import Annotated, Callable, Self

from pydantic import Field

from clinical_mdr_api.descriptions.general import CHANGES_FIELD_DESC
from clinical_mdr_api.domain_repositories.models._utils import convert_to_datetime
from clinical_mdr_api.domains.concepts.activities.activity_sub_group import (
    ActivitySubGroupAR,
)
from clinical_mdr_api.domains.controlled_terminologies.ct_term_name import CTTermNameAR
from clinical_mdr_api.models.concepts.activities.activity import (
    ActivityBase,
    ActivityHierarchySimpleModel,
    SimpleActivity,
)
from clinical_mdr_api.models.concepts.concept import ExtendedConceptPostInput
from clinical_mdr_api.models.libraries.library import Library
from clinical_mdr_api.models.utils import BaseModel, EditInputModel


class ActivitySubGroup(ActivityBase):
    @classmethod
    def from_activity_ar(
        cls,
        activity_subgroup_ar: ActivitySubGroupAR,
        find_activity_by_uid: Callable[[str], CTTermNameAR | None],
    ) -> Self:
        return cls(
            uid=activity_subgroup_ar.uid,
            name=activity_subgroup_ar.name,
            name_sentence_case=activity_subgroup_ar.concept_vo.name_sentence_case,
            definition=activity_subgroup_ar.concept_vo.definition,
            abbreviation=activity_subgroup_ar.concept_vo.abbreviation,
            activity_groups=[
                ActivityHierarchySimpleModel.from_activity_uid(
                    uid=activity_group.activity_group_uid,
                    version=activity_group.activity_group_version,
                    find_activity_by_uid=find_activity_by_uid,
                )
                for activity_group in activity_subgroup_ar.concept_vo.activity_groups
            ],
            library_name=Library.from_library_vo(activity_subgroup_ar.library).name,
            start_date=activity_subgroup_ar.item_metadata.start_date,
            end_date=activity_subgroup_ar.item_metadata.end_date,
            status=activity_subgroup_ar.item_metadata.status.value,
            version=activity_subgroup_ar.item_metadata.version,
            change_description=activity_subgroup_ar.item_metadata.change_description,
            author_username=activity_subgroup_ar.item_metadata.author_username,
            possible_actions=sorted(
                [_.value for _ in activity_subgroup_ar.get_possible_actions()]
            ),
        )

    activity_groups: Annotated[list[ActivityHierarchySimpleModel], Field()]


class ActivitySubGroupCreateInput(ExtendedConceptPostInput):
    name: Annotated[
        str,
        Field(
            description="The name or the actual value. E.g. 'Systolic Blood Pressure', 'Body Temperature', 'Metformin', ...",
            min_length=1,
        ),
    ]
    name_sentence_case: Annotated[str, Field(min_length=1)]
    activity_groups: Annotated[list[str] | None, Field()] = None
    library_name: Annotated[str, Field(min_length=1)]


class ActivitySubGroupEditInput(ActivitySubGroupCreateInput, EditInputModel):
    pass


class ActivitySubGroupVersion(ActivitySubGroup):
    """
    Class for storing ActivitySubGroup and calculation of differences
    """

    changes: list[str] = Field(description=CHANGES_FIELD_DESC, default_factory=list)


class ActivityGroup(BaseModel):
    uid: Annotated[str, Field()]
    name: Annotated[str, Field()]
    version: Annotated[str | None, Field()] = None
    status: Annotated[str | None, Field()] = None


class ActivitySubGroupDetail(BaseModel):
    name: Annotated[str | None, Field()] = None
    name_sentence_case: Annotated[str | None, Field()] = None
    library_name: Annotated[str | None, Field()] = None
    definition: Annotated[str | None, Field()] = None
    start_date: Annotated[datetime | None, Field()] = None
    end_date: Annotated[datetime | None, Field()] = None
    status: Annotated[str | None, Field()] = None
    version: Annotated[str | None, Field()] = None
    possible_actions: Annotated[list[str] | None, Field()] = None
    change_description: Annotated[str | None, Field()] = None
    author_username: Annotated[str | None, Field()] = None
    activity_groups: Annotated[list[ActivityGroup], Field()]


class ActivitySubGroupOverview(BaseModel):
    activity_subgroup: Annotated[ActivitySubGroupDetail, Field()]
    activities: Annotated[list[SimpleActivity], Field()]
    all_versions: Annotated[list[str], Field()]

    @classmethod
    def from_repository_input(cls, overview: dict):
        # Extract subgroup data from correct nested structure
        subgroup_value = overview.get("subgroup_value", {})
        latest_version = overview.get("has_version", {})
        library_info = overview.get("library", {})

        # Get version data from correct structure
        version_data = latest_version.get("has_version", {}) if latest_version else {}

        return cls(
            activity_subgroup=ActivitySubGroupDetail(
                # Map basic fields from subgroup_value
                name=subgroup_value.get("name"),
                name_sentence_case=subgroup_value.get("name_sentence_case"),
                definition=subgroup_value.get("definition"),
                abbreviation=subgroup_value.get("abbreviation"),
                # Get library name from library node
                library_name=library_info.get("name"),
                # Get version metadata from version node
                start_date=convert_to_datetime(version_data.get("start_date")),
                end_date=convert_to_datetime(version_data.get("end_date")),
                status=version_data.get("status"),
                version=version_data.get("version"),
                possible_actions=version_data.get("possible_actions"),
                change_description=version_data.get("change_description"),
            ),
            activities=[
                SimpleActivity(
                    nci_concept_id=activity.get("nci_concept_id"),
                    nci_concept_name=activity.get("nci_concept_name"),
                    name=activity.get("name"),
                    name_sentence_case=activity.get("name_sentence_case"),
                    synonyms=activity.get("synonyms", []),
                    definition=activity.get("definition"),
                    abbreviation=activity.get("abbreviation"),
                    is_data_collected=activity.get("is_data_collected", False),
                    is_multiple_selection_allowed=activity.get(
                        "is_multiple_selection_allowed", True
                    ),
                    library_name=activity.get("library_name"),
                    version=activity.get("version"),
                    status=activity.get("status"),
                    start_date=convert_to_datetime(activity.get("start_date")),
                    end_date=convert_to_datetime(activity.get("end_date")),
                )
                for activity in overview.get("activities", [])
            ],
            all_versions=overview.get("all_versions", []),
        )
