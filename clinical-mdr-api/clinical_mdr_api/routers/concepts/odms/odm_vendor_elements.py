from typing import Annotated, Any

from fastapi import APIRouter, Body, Path, Query
from pydantic.types import Json

from clinical_mdr_api.models.concepts.odms.odm_vendor_element import (
    OdmVendorElement,
    OdmVendorElementPatchInput,
    OdmVendorElementPostInput,
)
from clinical_mdr_api.models.utils import CustomPage
from clinical_mdr_api.repositories._utils import FilterOperator
from clinical_mdr_api.routers import _generic_descriptions
from clinical_mdr_api.services.concepts.odms.odm_vendor_elements import (
    OdmVendorElementService,
)
from common import config
from common.auth import rbac
from common.models.error import ErrorResponse

# Prefixed with "/concepts/odms/vendor-elements"
router = APIRouter()

# Argument definitions
OdmVendorElementUID = Path(description="The unique id of the ODM Vendor Element.")


@router.get(
    "",
    dependencies=[rbac.LIBRARY_READ],
    summary="Return every variable related to the selected status and version of the ODM Vendor Elements",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        404: _generic_descriptions.ERROR_404,
    },
)
def get_all_odm_vendor_elements(
    library_name: Annotated[str | None, Query()] = None,
    sort_by: Annotated[
        Json | None, Query(description=_generic_descriptions.SORT_BY)
    ] = None,
    page_number: Annotated[
        int | None, Query(ge=1, description=_generic_descriptions.PAGE_NUMBER)
    ] = config.DEFAULT_PAGE_NUMBER,
    page_size: Annotated[
        int | None,
        Query(
            ge=0,
            le=config.MAX_PAGE_SIZE,
            description=_generic_descriptions.PAGE_SIZE,
        ),
    ] = config.DEFAULT_PAGE_SIZE,
    filters: Annotated[
        Json | None,
        Query(
            description=_generic_descriptions.FILTERS,
            openapi_examples=_generic_descriptions.FILTERS_EXAMPLE,
        ),
    ] = None,
    operator: Annotated[
        str | None, Query(description=_generic_descriptions.FILTER_OPERATOR)
    ] = config.DEFAULT_FILTER_OPERATOR,
    total_count: Annotated[
        bool | None, Query(description=_generic_descriptions.TOTAL_COUNT)
    ] = False,
) -> CustomPage[OdmVendorElement]:
    odm_vendor_element_service = OdmVendorElementService()
    results = odm_vendor_element_service.get_all_concepts(
        library=library_name,
        sort_by=sort_by,
        page_number=page_number,
        page_size=page_size,
        total_count=total_count,
        filter_by=filters,
        filter_operator=FilterOperator.from_str(operator),
    )
    return CustomPage.create(
        items=results.items, total=results.total, page=page_number, size=page_size
    )


@router.get(
    "/headers",
    dependencies=[rbac.LIBRARY_READ],
    summary="Returns possible values from the database for a given header",
    description="""Allowed parameters include : field name for which to get possible
    values, search string to provide filtering for the field name, additional filters to apply on other fields""",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        404: {
            "model": ErrorResponse,
            "description": "Not Found - Invalid field name specified",
        },
    },
)
def get_distinct_values_for_header(
    field_name: Annotated[
        str, Query(description=_generic_descriptions.HEADER_FIELD_NAME)
    ],
    library_name: Annotated[str | None, Query()] = None,
    search_string: Annotated[
        str | None, Query(description=_generic_descriptions.HEADER_SEARCH_STRING)
    ] = "",
    filters: Annotated[
        Json | None,
        Query(
            description=_generic_descriptions.FILTERS,
            openapi_examples=_generic_descriptions.FILTERS_EXAMPLE,
        ),
    ] = None,
    operator: Annotated[
        str | None, Query(description=_generic_descriptions.FILTER_OPERATOR)
    ] = config.DEFAULT_FILTER_OPERATOR,
    page_size: Annotated[
        int | None, Query(description=_generic_descriptions.HEADER_PAGE_SIZE)
    ] = config.DEFAULT_HEADER_PAGE_SIZE,
) -> list[Any]:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.get_distinct_values_for_header(
        library=library_name,
        field_name=field_name,
        search_string=search_string,
        filter_by=filters,
        filter_operator=FilterOperator.from_str(operator),
        page_size=page_size,
    )


@router.get(
    "/{odm_vendor_element_uid}",
    dependencies=[rbac.LIBRARY_READ],
    summary="Get details on a specific ODM Vendor Element (in a specific version)",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        404: _generic_descriptions.ERROR_404,
    },
)
def get_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.get_by_uid(uid=odm_vendor_element_uid)


@router.get(
    "/{odm_vendor_element_uid}/relationships",
    dependencies=[rbac.LIBRARY_READ],
    summary="Get UIDs of a specific ODM Vendor Element's relationships",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        404: _generic_descriptions.ERROR_404,
    },
)
def get_active_relationships(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> dict:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.get_active_relationships(
        uid=odm_vendor_element_uid
    )


@router.get(
    "/{odm_vendor_element_uid}/versions",
    dependencies=[rbac.LIBRARY_READ],
    summary="List version history for ODM Vendor Element",
    description="""
State before:
 - uid must exist.

Business logic:
 - List version history for ODM Vendor Elements.
 - The returned versions are ordered by start_date descending (newest entries first).

State after:
 - No change

Possible errors:
 - Invalid uid.
    """,
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        404: {
            "model": ErrorResponse,
            "description": "Not Found - The ODM Vendor Element with the specified 'odm_vendor_element_uid' wasn't found.",
        },
    },
)
def get_odm_vendor_element_versions(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> list[OdmVendorElement]:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.get_version_history(uid=odm_vendor_element_uid)


@router.post(
    "",
    dependencies=[rbac.LIBRARY_WRITE],
    summary="Creates a new Vendor Element in 'Draft' status with version 0.1",
    status_code=201,
    responses={
        403: _generic_descriptions.ERROR_403,
        201: {
            "description": "Created - The ODM Vendor Element was successfully created."
        },
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The library doesn't exist.\n"
            "- The library doesn't allow to add new items.\n",
        },
    },
)
def create_odm_vendor_element(
    odm_vendor_element_create_input: Annotated[OdmVendorElementPostInput, Body()],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.create(
        concept_input=odm_vendor_element_create_input
    )


@router.patch(
    "/{odm_vendor_element_uid}",
    dependencies=[rbac.LIBRARY_WRITE],
    summary="Update ODM Vendor Element",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        200: {"description": "OK."},
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in draft status.\n"
            "- The ODM Vendor Element had been in 'Final' status before.\n"
            "- The library doesn't allow to edit draft versions.\n",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - The ODM Vendor Element with the specified 'odm_vendor_element_uid' wasn't found.",
        },
    },
)
def edit_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
    odm_vendor_element_edit_input: Annotated[OdmVendorElementPatchInput, Body()],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.edit_draft(
        uid=odm_vendor_element_uid, concept_edit_input=odm_vendor_element_edit_input
    )


@router.post(
    "/{odm_vendor_element_uid}/versions",
    dependencies=[rbac.LIBRARY_WRITE],
    summary=" Create a new version of ODM Vendor Element",
    description="""
State before:
 - uid must exist and the ODM Vendor Element must be in status Final.

Business logic:
- The ODM Vendor Element is changed to a draft state.

State after:
 - ODM Vendor Element changed status to Draft and assigned a new minor version number.
 - Audit trail entry must be made with action of creating a new draft version.

Possible errors:
 - Invalid uid or status not Final.
""",
    status_code=201,
    responses={
        403: _generic_descriptions.ERROR_403,
        201: {"description": "OK."},
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The library doesn't allow to create ODM Vendor Elements.\n",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in final status.\n"
            "- The ODM Vendor Element with the specified 'odm_vendor_element_uid' could not be found.",
        },
    },
)
def create_odm_vendor_element_version(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.create_new_version(uid=odm_vendor_element_uid)


@router.post(
    "/{odm_vendor_element_uid}/approvals",
    dependencies=[rbac.LIBRARY_WRITE],
    summary="Approve draft version of ODM Vendor Element",
    status_code=201,
    responses={
        403: _generic_descriptions.ERROR_403,
        201: {"description": "OK."},
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in draft status.\n"
            "- The library doesn't allow to approve ODM Vendor Element.\n",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - The ODM Vendor Element with the specified 'odm_vendor_element_uid' wasn't found.",
        },
    },
)
def approve_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.approve(uid=odm_vendor_element_uid)


@router.delete(
    "/{odm_vendor_element_uid}/activations",
    dependencies=[rbac.LIBRARY_WRITE],
    summary=" Inactivate final version of ODM Vendor Element",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        200: {"description": "OK."},
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in final status.",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - The ODM Vendor Element with the specified 'odm_vendor_element_uid' could not be found.",
        },
    },
)
def inactivate_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.inactivate_final(uid=odm_vendor_element_uid)


@router.post(
    "/{odm_vendor_element_uid}/activations",
    dependencies=[rbac.LIBRARY_WRITE],
    summary="Reactivate retired version of a ODM Vendor Element",
    status_code=200,
    responses={
        403: _generic_descriptions.ERROR_403,
        200: {"description": "OK."},
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in retired status.",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - The ODM Vendor Element with the specified 'odm_vendor_element_uid' could not be found.",
        },
    },
)
def reactivate_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
) -> OdmVendorElement:
    odm_vendor_element_service = OdmVendorElementService()
    return odm_vendor_element_service.reactivate_retired(uid=odm_vendor_element_uid)


@router.delete(
    "/{odm_vendor_element_uid}",
    dependencies=[rbac.LIBRARY_WRITE],
    summary="Delete draft version of ODM Vendor Element",
    status_code=204,
    responses={
        403: _generic_descriptions.ERROR_403,
        204: {
            "description": "No Content - The ODM Vendor Element was successfully deleted."
        },
        400: {
            "model": ErrorResponse,
            "description": "Forbidden - Reasons include e.g.: \n"
            "- The ODM Vendor Element is not in draft status.\n"
            "- The ODM Vendor Element was already in final state or is in use.\n"
            "- The library doesn't allow to delete ODM Vendor Element.",
        },
        404: {
            "model": ErrorResponse,
            "description": "Not Found - An ODM Vendor Element with the specified 'odm_vendor_element_uid' could not be found.",
        },
    },
)
def delete_odm_vendor_element(
    odm_vendor_element_uid: Annotated[str, OdmVendorElementUID],
):
    odm_vendor_element_service = OdmVendorElementService()
    odm_vendor_element_service.soft_delete(uid=odm_vendor_element_uid)
