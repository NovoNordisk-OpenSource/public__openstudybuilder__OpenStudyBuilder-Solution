from clinical_mdr_api.domain_repositories._generic_repository_interface import (
    _AggregateRootType,
)
from clinical_mdr_api.domain_repositories.concepts.odms.odm_generic_repository import (
    OdmGenericRepository,
)
from clinical_mdr_api.domain_repositories.models.controlled_terminology import (
    CTTermRoot,
)
from clinical_mdr_api.domain_repositories.models.generic import (
    Library,
    VersionRelationship,
    VersionRoot,
    VersionValue,
)
from clinical_mdr_api.domain_repositories.models.odm import (
    OdmAliasRoot,
    OdmDescriptionRoot,
    OdmFormRoot,
    OdmFormValue,
    OdmStudyEventRoot,
)
from clinical_mdr_api.domains._utils import ObjectStatus
from clinical_mdr_api.domains.concepts.concept_base import ConceptARBase
from clinical_mdr_api.domains.concepts.odms.form import (
    OdmFormAR,
    OdmFormRefVO,
    OdmFormVO,
)
from clinical_mdr_api.domains.versioned_object_aggregate import (
    LibraryItemMetadataVO,
    LibraryItemStatus,
    LibraryVO,
)
from clinical_mdr_api.models.concepts.odms.odm_form import OdmForm
from common.utils import convert_to_datetime


class FormRepository(OdmGenericRepository[OdmFormAR]):
    root_class = OdmFormRoot
    value_class = OdmFormValue
    return_model = OdmForm

    def _create_aggregate_root_instance_from_version_root_relationship_and_value(
        self,
        root: VersionRoot,
        library: Library | None,
        relationship: VersionRelationship,
        value: VersionValue,
        **_kwargs,
    ) -> OdmFormAR:
        scope = root.has_scope.get_or_none()
        return OdmFormAR.from_repository_values(
            uid=root.uid,
            concept_vo=OdmFormVO.from_repository_values(
                oid=value.oid,
                name=value.name,
                sdtm_version=value.sdtm_version,
                repeating=value.repeating,
                scope_uid=scope.uid if scope else None,
                description_uids=[
                    description.uid for description in root.has_description.all()
                ],
                alias_uids=[alias.uid for alias in root.has_alias.all()],
                activity_group_uids=[
                    activity_group.uid
                    for activity_group in root.has_activity_group.all()
                ],
                item_group_uids=[
                    item_group.uid for item_group in root.item_group_ref.all()
                ],
                vendor_element_uids=[
                    vendor_element.uid
                    for vendor_element in root.has_vendor_element.all()
                ],
                vendor_attribute_uids=[
                    vendor_attribute.uid
                    for vendor_attribute in root.has_vendor_attribute.all()
                ],
                vendor_element_attribute_uids=[
                    vendor_element_attribute.uid
                    for vendor_element_attribute in root.has_vendor_element_attribute.all()
                ],
            ),
            library=LibraryVO.from_input_values_2(
                library_name=library.name,
                is_library_editable_callback=(lambda _: library.is_editable),
            ),
            item_metadata=self._library_item_metadata_vo_from_relation(relationship),
        )

    def _create_aggregate_root_instance_from_cypher_result(
        self, input_dict: dict
    ) -> _AggregateRootType:
        major, minor = input_dict.get("version").split(".")
        odm_form_ar = OdmFormAR.from_repository_values(
            uid=input_dict.get("uid"),
            concept_vo=OdmFormVO.from_repository_values(
                oid=input_dict.get("oid"),
                name=input_dict.get("name"),
                sdtm_version=input_dict.get("sdtm_version"),
                repeating=input_dict.get("repeating"),
                scope_uid=input_dict.get("scope_uid"),
                description_uids=input_dict.get("description_uids"),
                alias_uids=input_dict.get("alias_uids"),
                activity_group_uids=input_dict.get("activity_group_uids"),
                item_group_uids=input_dict.get("item_group_uids"),
                vendor_element_uids=input_dict.get("vendor_element_uids"),
                vendor_attribute_uids=input_dict.get("vendor_attribute_uids"),
                vendor_element_attribute_uids=input_dict.get(
                    "vendor_element_attribute_uids"
                ),
            ),
            library=LibraryVO.from_input_values_2(
                library_name=input_dict.get("library_name"),
                is_library_editable_callback=(
                    lambda _: input_dict.get("is_library_editable")
                ),
            ),
            item_metadata=LibraryItemMetadataVO.from_repository_values(
                change_description=input_dict.get("change_description"),
                status=LibraryItemStatus(input_dict.get("status")),
                author_id=input_dict.get("author_id"),
                author_username=input_dict.get("author_username"),
                start_date=convert_to_datetime(value=input_dict.get("start_date")),
                end_date=None,
                major_version=int(major),
                minor_version=int(minor),
            ),
        )

        return odm_form_ar

    def specific_alias_clause(
        self, only_specific_status: str = ObjectStatus.LATEST.name, **kwargs
    ) -> str:
        return f"""
WITH *,
concept_value.oid AS oid,
toString(concept_value.repeating) AS repeating,
concept_value.sdtm_version AS sdtm_version,

head([(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[:HAS_SCOPE]->(tr:CTTermRoot)-[:HAS_ATTRIBUTES_ROOT]->(:CTTermAttributesRoot)-[:LATEST]->(tav:CTTermAttributesValue) |
tr.uid]) AS scope_uid,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[:HAS_DESCRIPTION]->(dr:OdmDescriptionRoot)-[:LATEST]->(dv:OdmDescriptionValue) |
{{uid: dr.uid, name: dv.name, language: dv.language, description: dv.description, instruction: dv.instruction}}] AS descriptions,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[:HAS_ALIAS]->(ar:OdmAliasRoot)-[:LATEST]->(av:OdmAliasValue) |
{{uid: ar.uid, name: av.name, context: av.context}}] AS aliases,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[:HAS_ACTIVITY_GROUP]->(agr:ActivityGroupRoot)-[:LATEST]->(agv:ActivityGroupValue) |
{{uid: agr.uid, name: agv.name}}] AS activity_groups,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[igref:ITEM_GROUP_REF]->(igr:OdmItemGroupRoot)-[:LATEST]->(igv:OdmItemGroupValue) |
{{uid: igr.uid, name: igv.name, order: igref.order, mandatory: igref.mandatory}}] AS item_groups,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[hve:HAS_VENDOR_ELEMENT]->(ver:OdmVendorElementRoot)-[:LATEST]->(vev:OdmVendorElementValue) |
{{uid: ver.uid, name: vev.name, value: hve.value}}] AS vendor_elements,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[hva:HAS_VENDOR_ATTRIBUTE]->(var:OdmVendorAttributeRoot)-[:LATEST]->(vav:OdmVendorAttributeValue) |
{{uid: var.uid, name: vav.name, value: hva.value}}] AS vendor_attributes,

[(concept_value)<-[:{only_specific_status}]-(:OdmFormRoot)-[hvea:HAS_VENDOR_ELEMENT_ATTRIBUTE]->(var:OdmVendorAttributeRoot)-[:LATEST]->(vav:OdmVendorAttributeValue) |
{{uid: var.uid, name: vav.name, value: hvea.value}}] AS vendor_element_attributes

WITH *,
apoc.coll.toSet([description in descriptions | description.uid]) AS description_uids,
apoc.coll.toSet([alias in aliases | alias.uid]) AS alias_uids,
apoc.coll.toSet([activity_group in activity_groups | activity_group.uid]) AS activity_group_uids,
apoc.coll.toSet([item_group in item_groups | item_group.uid]) AS item_group_uids,
apoc.coll.toSet([vendor_element in vendor_elements | vendor_element.uid]) AS vendor_element_uids,
apoc.coll.toSet([vendor_attribute in vendor_attributes | vendor_attribute.uid]) AS vendor_attribute_uids,
apoc.coll.toSet([vendor_element_attribute in vendor_element_attributes | vendor_element_attribute.uid]) AS vendor_element_attribute_uids
"""

    def _get_or_create_value(
        self, root: VersionRoot, ar: ConceptARBase
    ) -> VersionValue:
        new_value = super()._get_or_create_value(root, ar)

        root.has_scope.disconnect_all()
        root.has_description.disconnect_all()
        root.has_alias.disconnect_all()

        if ar.concept_vo.scope_uid is not None:
            scope = CTTermRoot.nodes.get_or_none(uid=ar.concept_vo.scope_uid)
            root.has_scope.connect(scope)

        if ar.concept_vo.description_uids is not None:
            for description_uid in ar.concept_vo.description_uids:
                description = OdmDescriptionRoot.nodes.get_or_none(uid=description_uid)
                root.has_description.connect(description)

        if ar.concept_vo.alias_uids is not None:
            for alias_uid in ar.concept_vo.alias_uids:
                alias = OdmAliasRoot.nodes.get_or_none(uid=alias_uid)
                root.has_alias.connect(alias)

        return new_value

    def _create_new_value_node(self, ar: OdmFormAR) -> OdmFormValue:
        value_node = super()._create_new_value_node(ar=ar)

        value_node.save()

        value_node.oid = ar.concept_vo.oid
        value_node.sdtm_version = ar.concept_vo.sdtm_version
        value_node.repeating = ar.concept_vo.repeating

        return value_node

    def _has_data_changed(self, ar: OdmFormAR, value: OdmFormValue) -> bool:
        are_concept_properties_changed = super()._has_data_changed(ar=ar, value=value)

        root = OdmFormRoot.nodes.get_or_none(uid=ar.uid)

        scope_uid = scope.uid if (scope := root.has_scope.get_or_none()) else None
        description_uids = {
            description.uid for description in root.has_description.all()
        }
        alias_uids = {alias.uid for alias in root.has_alias.all()}

        are_rels_changed = (
            ar.concept_vo.scope_uid != scope_uid
            or set(ar.concept_vo.description_uids) != description_uids
            or set(ar.concept_vo.alias_uids) != alias_uids
        )

        return (
            are_concept_properties_changed
            or are_rels_changed
            or ar.concept_vo.oid != value.oid
            or ar.concept_vo.sdtm_version != value.sdtm_version
            or ar.concept_vo.repeating != value.repeating
        )

    def find_by_uid_with_study_event_relation(self, uid: str, study_event_uid: str):
        form_root = self.root_class.nodes.get_or_none(uid=uid)
        form_value = form_root.has_latest_value.get_or_none()

        study_event_root = OdmStudyEventRoot.nodes.get_or_none(uid=study_event_uid)

        rel = form_root.form_ref.relationship(study_event_root)

        return OdmFormRefVO.from_repository_values(
            uid=uid,
            name=form_value.name,
            study_event_uid=study_event_uid,
            order_number=rel.order_number,
            mandatory=rel.mandatory,
            locked=rel.locked,
            collection_exception_condition_oid=rel.collection_exception_condition_oid,
        )
