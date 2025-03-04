INCLUDE_FLAG = "RelatedPerson:patient"

PATIENT_IDENTIFIERS = ["9000000017", "9000000033"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025"]

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
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP = f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship.yaml"
GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH = (
    f"{GET_CONSENT__DIRECTORY}single-mother-child-relationship-include-performer-patient.yaml"
)
GET_CONSENT__STATUS_PARAM_INVALID = f"{GET_CONSENT__DIRECTORY}errors/invalid-status-parameter.yaml"

# POST Consent
POST_CONSENT__DIRECTORY = "./api/examples/POST_Consent/"
POST_CONSENT__SUCCESS = f"{POST_CONSENT__DIRECTORY}success.yaml"
POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR = f"{POST_CONSENT__DIRECTORY}errors/duplicate_relationship_error.yaml"
POST_CONSENT__INVALID_ACCESS_LEVEL_ERROR = f"{POST_CONSENT__DIRECTORY}errors/invalid_access_level_error.yaml"
POST_CONSENT__INVALID_EVIDENCE_ERROR = f"{POST_CONSENT__DIRECTORY}errors/invalid_evidence_error.yaml"
POST_CONSENT__INVALID_PATIENT_AGE_ERROR = f"{POST_CONSENT__DIRECTORY}errors/invalid_patient_age_error.yaml"
POST_CONSENT__PERFORMER_IDENTIFIER_ERROR = f"{POST_CONSENT__DIRECTORY}errors/invalid_performer_identifier_error.yaml"

QR_DIRECTORY = "./api/examples/POST_QuestionnaireResponse/"
QUESTIONNAIRE_RESPONSE__SUCCESS = f"{QR_DIRECTORY}success.yaml"

RELATED_DIRECTORY = "./api/examples/GET_RelatedPerson/"
RELATED__ERROR_IDENTIFIER_MISSING = f"{RELATED_DIRECTORY}errors/invalid-identifier-missing.yaml"
RELATED__ERROR_IDENTIFIER_SYSTEM = f"{RELATED_DIRECTORY}errors/invalid-identifier-system.yaml"
RELATED__ERROR_IDENTIFIER = f"{RELATED_DIRECTORY}errors/invalid-identifier.yaml"
RELATED__EMPTY_RESPONSE = f"{RELATED_DIRECTORY}empty_response.yaml"
RELATED__LIST_RELATIONSHIP = f"{RELATED_DIRECTORY}list_relationship_9000000017.yaml"
RELATED__LIST_RELATIONSHIP_WITH_INCLUDE = f"{RELATED_DIRECTORY}list_relationship_9000000017_include.yaml"
RELATED__VERIFY_RELATIONSHIP_09 = f"{RELATED_DIRECTORY}verify_relationship_9000000009.yaml"
RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE = f"{RELATED_DIRECTORY}verify_relationship_9000000009_include.yaml"
RELATED__VERIFY_RELATIONSHIP_25 = f"{RELATED_DIRECTORY}verify_relationship_9000000025.yaml"
RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE = f"{RELATED_DIRECTORY}verify_relationship_9000000025_include.yaml"
RELATED__EMPTY_RESPONSE = f"{RELATED_DIRECTORY}empty_response_9000000033.yaml"
