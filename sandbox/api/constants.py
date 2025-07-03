INCLUDE_FLAG = "RelatedPerson:patient"

PATIENT_IDENTIFIERS = ["9000000017", "9000000033", "9000000042"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025", "9000000042"]

CONSENT_PERFORMER = "Consent:performer"
CONSENT_PATIENT = "Consent:patient"

# Example files

# Common examples
INTERNAL_SERVER_ERROR_EXAMPLE = "./api/examples/errors/internal-server-error.yaml"
BAD_REQUEST_INCLUDE_PARAM_INVALID = "./api/examples/errors/invalid-include-parameter.yaml"
INVALIDATED_RESOURCE = "./api/examples/errors/invalidated-resource.yaml"
MISSING_IDENTIFIER = "./api/examples/errors/missing-identifier.yaml"
INVALID_IDENTIFIER = "./api/examples/errors/invalid-identifier.yaml"

# GET Consent examples
GET_CONSENT__DIRECTORY = "./api/examples/GET_Consent/"
GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_ACTIVE = (
    f"{GET_CONSENT__DIRECTORY}filtered-relationships-status-active-include-details.yaml"
)
GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_INACTIVE = (
    f"{GET_CONSENT__DIRECTORY}filtered-relationships-status-inactive.yaml"
)
GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_PROPOSED_ACTIVE = (
    f"{GET_CONSENT__DIRECTORY}filtered-relationships-status-proposed-active.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS = f"{GET_CONSENT__DIRECTORY}multiple-relationships.yaml"
GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-include-performer-patient.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-include-patient.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-include-performer.yaml"
)
GET_CONSENT__NO_RELATIONSHIPS = f"{GET_CONSENT__DIRECTORY}no-relationships.yaml"
GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP = f"{GET_CONSENT__DIRECTORY}single-consenting-adult-relationship.yaml"
GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH = (
    f"{GET_CONSENT__DIRECTORY}single-consenting-adult-relationship-include-performer-patient.yaml"
)
GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PATIENT = (
    f"{GET_CONSENT__DIRECTORY}single-consenting-adult-relationship-include-patient.yaml"
)
GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PERFORMER = (
    f"{GET_CONSENT__DIRECTORY}single-consenting-adult-relationship-include-performer.yaml"
)
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP = f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship.yaml"
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH = (
    f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship-include-performer-patient.yaml"
)
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PATIENT = (
    f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship-include-patient.yaml"
)
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PERFORMER = (
    f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship-include-performer.yaml"
)
GET_CONSENT__STATUS_PARAM_INVALID = f"{GET_CONSENT__DIRECTORY}errors/invalid-status-parameter.yaml"
GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-single-patient.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PERFORMER = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-single-patient-include-performer.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PATIENT = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-single-patient-include-patient.yaml"
)
GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_BOTH = (
    f"{GET_CONSENT__DIRECTORY}multiple-relationships-single-patient-include-performer-patient.yaml"
)

# GET Consent by ID
GET_CONSENT_BY_ID__INVALID_ID_ERROR = f"{GET_CONSENT__DIRECTORY}ID/errors/invalid-id.yaml"

# POST Consent
POST_CONSENT__DIRECTORY = "./api/examples/POST_Consent/"
POST_CONSENT__SUCCESS = f"{POST_CONSENT__DIRECTORY}success.yaml"
POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR = f"{POST_CONSENT__DIRECTORY}errors/duplicate_relationship_error.yaml"
POST_CONSENT__PERFORMER_IDENTIFIER_ERROR = f"{POST_CONSENT__DIRECTORY}errors/invalid_performer_identifier_error.yaml"

# PATCH Consent
PATCH_CONSENT__DIRECTORY = "./api/examples/PATCH_Consent/"
PATCH_CONSENT__SUCCESS = f"{PATCH_CONSENT__DIRECTORY}success.yaml"
PATCH_CONSENT__INVALID_PATCH_FORMAT = f"{PATCH_CONSENT__DIRECTORY}errors/invalid_patch_format.yaml"
PATCH_CONSENT__INVALID_PATH = f"{PATCH_CONSENT__DIRECTORY}errors/invalid_path.yaml"
PATCH_CONSENT__INVALID_STATUS_CODE = f"{PATCH_CONSENT__DIRECTORY}errors/invalid_status_code.yaml"
PATCH_CONSENT__INVALID_STATUS_REASON = f"{PATCH_CONSENT__DIRECTORY}errors/invalid_status_reason.yaml"
PATCH_CONSENT__RESOURCE_NOT_FOUND = f"{PATCH_CONSENT__DIRECTORY}errors/resource_not_found.yaml"
PATCH_CONSENT__INVALID_STATE_TRANSITION = f"{PATCH_CONSENT__DIRECTORY}errors/invalid_state_transition.yaml"

# POST QuestionnaireResponse
POST_QUESTIONNAIRE_RESPONSE_DIRECTORY = "./api/examples/POST_QuestionnaireResponse/"
POST_QUESTIONNAIRE_RESPONSE__SUCCESS = f"{POST_QUESTIONNAIRE_RESPONSE_DIRECTORY}success.yaml"
POST_QUESTIONNAIRE_RESPONSE__DUPLICATE_RELATIONSHIP_ERROR = (
    f"{POST_QUESTIONNAIRE_RESPONSE_DIRECTORY}errors/duplicate_relationship_error.yaml"
)

# GET QuestionnaireResponse
GET_QUESTIONNAIRE_RESPONSE_DIRECTORY = "./api/examples/GET_QuestionnaireResponse/"
GET_QUESTIONNAIRE_RESPONSE__SUCCESS = f"{GET_QUESTIONNAIRE_RESPONSE_DIRECTORY}success.yaml"
GET_QUESTIONNAIRE_RESPONSE__INVALID = f"{GET_QUESTIONNAIRE_RESPONSE_DIRECTORY}errors/invalid_reference_code.yaml"
GET_QUESTIONNAIRE_RESPONSE__MISSING = f"{GET_QUESTIONNAIRE_RESPONSE_DIRECTORY}errors/missing_reference_code.yaml"
GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND = (
    f"{GET_QUESTIONNAIRE_RESPONSE_DIRECTORY}errors/questionnaire_response_not_found.yaml"
)

# GET RelatedPerson
RELATED_DIRECTORY = "./api/examples/GET_RelatedPerson/"
RELATED__ERROR_IDENTIFIER_MISSING = f"{RELATED_DIRECTORY}errors/invalid-identifier-missing.yaml"
RELATED__ERROR_IDENTIFIER_SYSTEM = f"{RELATED_DIRECTORY}errors/invalid-identifier-system.yaml"
RELATED__ERROR_IDENTIFIER = f"{RELATED_DIRECTORY}errors/invalid-identifier.yaml"
RELATED__ERROR_PATIENT_IDENTIFIER = f"{RELATED_DIRECTORY}errors/invalid-patient-identifier.yaml"
RELATED__EMPTY_RESPONSE = f"{RELATED_DIRECTORY}empty_response.yaml"
RELATED__LIST_RELATIONSHIP = f"{RELATED_DIRECTORY}list_relationship_9000000017.yaml"
RELATED__LIST_RELATIONSHIP_WITH_INCLUDE = f"{RELATED_DIRECTORY}list_relationship_9000000017_include.yaml"
RELATED__LIST_CHILD_RELATIONSHIP = f"{RELATED_DIRECTORY}list_relationship_9000000042.yaml"
RELATED__LIST_CHILD_RELATIONSHIP_WITH_INCLUDE = f"{RELATED_DIRECTORY}list_relationship_9000000042_include.yaml"
RELATED__VERIFY_RELATIONSHIP_09 = f"{RELATED_DIRECTORY}verify_relationship_9000000009.yaml"
RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE = f"{RELATED_DIRECTORY}verify_relationship_9000000009_include.yaml"
RELATED__VERIFY_RELATIONSHIP_25 = f"{RELATED_DIRECTORY}verify_relationship_9000000025.yaml"
RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE = f"{RELATED_DIRECTORY}verify_relationship_9000000025_include.yaml"
RELATED__EMPTY_RESPONSE = f"{RELATED_DIRECTORY}empty_response_9000000033.yaml"
