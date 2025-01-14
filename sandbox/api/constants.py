NOT_FOUND = "./api/responses/not_found.json"
EMPTY_RESPONSE = "./api/responses/GET_RelatedPerson/no_relationships.json"
LIST_RELATIONSHIP = (
    "./api/responses/GET_RelatedPerson/list_relationship_9000000017.json"
)
LIST_RELATIONSHIP_INCLUDE = (
    "./api/responses/GET_RelatedPerson/list_relationship_include_9000000017.json"
)
VALIDATE_RELATIONSHIP_009 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_9000000009.json"
)
VALIDATE_RELATIONSHIP_INCLUDE_009 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000009.json"
)
VALIDATE_RELATIONSHIP_025 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_9000000025.json"
)
VALIDATE_RELATIONSHIP_INCLUDE_025 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000025.json"
)
INTERNAL_ERROR_RESPONSE = "./api/responses/internal_server_error.json"
INCLUDE_FLAG = "RelatedPerson:patient"

QUESTIONNAIRE_RESPONSE_SUCCESS = (
    "./api/responses/POST_QuestionnaireResponse/questionnaire_response_success.json"
)

BAD_REQUEST_INCLUDE_PARAM_INVALID = "./api/responses/bad_request_include_param_invalid.json"

consent_dir = "./api/responses/GET_Consent/"
CONSENT__MULTIPLE_RELATIONSHIPS = consent_dir + "multiple_relationships.json"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH = consent_dir + "multiple_relationships_include_both.json"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT = consent_dir + "multiple_relationships_include_patient.json"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER = consent_dir + "multiple_relationships_include_performer.json"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER = consent_dir + "multiple_relationships_include_performer.json"
CONSENT__MULTIPLE_RELATIONSHIPS_STATUS_ACTIVE = consent_dir + "multiple_relationships_status_active.json"
CONSENT__MULTIPLE_RELATIONSHIPS_STATUS_ACTIVE_INCLUDE_BOTH = (
    consent_dir + "multiple_relationships_status_active_include_both.json"
)
CONSENT__MULTIPLE_RELATIONSHIPS_STATUS_ACTIVE_INCLUDE_PATIENT = (
    consent_dir + "multiple_relationships_status_active_include_patient.json"
)
CONSENT__MULTIPLE_RELATIONSHIPS_STATUS_ACTIVE_INCLUDE_PERFORMER = (
    consent_dir + "multiple_relationships_status_active_include_performer.json"
)
CONSENT__NO_RELATIONSHIPS = consent_dir + "no_relationships.json"
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP = consent_dir + "single_consenting_adult_relationship.json"
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH = (
    consent_dir + "single_consenting_adult_relationship_include_both.json"
)
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PATIENT = (
    consent_dir + "single_consenting_adult_relationship_include_patient.json"
)
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PERFORMER = (
    consent_dir + "single_consenting_adult_relationship_include_performer.json"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP = consent_dir + "single_mother_child_relationship.json"
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH = (
    consent_dir + "single_mother_child_relationship_include_both.json"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PATIENT = (
    consent_dir + "single_mother_child_relationship_include_patient.json"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PERFORMER = (
    consent_dir + "single_mother_child_relationship_include_performer.json"
)
CONSENT__STATUS_PARAM_INVALID = consent_dir + "bad_request_status_param_invalid.json"

PATIENT_IDENTIFIERS = ["9000000017", "9000000033"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025"]

CONSENT_PERFORMER = "Consent:performer"
CONSENT_PATIENT = "Consent:patient"

# Example files

# Common examples
INTERNAL_SERVER_ERROR_EXAMPLE = "./api/examples/shared/internal-server-error.yaml"
# Consent examples
CONSENT__ADULT_CONSENTING_EXAMPLE = "./api/examples/GET_Consent/adults-consenting.yaml"
CONSENT__MIXED_EXAMPLE = "./api/examples/GET_Consent/mixed.yaml"
CONSENT__MOTHER_CHILD_EXAMPLE = "./api/examples/GET_Consent/mother-child.yaml"
