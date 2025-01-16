EMPTY_RESPONSE = "./api/responses/GET_RelatedPerson/empty_response_9000000033.json"
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

PATIENT_IDENTIFIERS = ["9000000017", "9000000033"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025"]

CONSENT_PERFORMER = "Consent:performer"
CONSENT_PATIENT = "Consent:patient"

# Example files

# Common examples
INTERNAL_SERVER_ERROR_EXAMPLE = "./api/examples/errors/internal-server-error.yaml"
BAD_REQUEST_INCLUDE_PARAM_INVALID = (
    "./api/examples/errors/invalid-include-parameter.yaml"
)
NOT_FOUND = "./api/examples/errors/not-found.yaml"
MISSING_IDENTIFIER = "./api/examples/errors/missing-identifier.yaml"
INVALID_IDENTIFIER = "./api/examples/errors/invalid-identifier.yaml"

# Consent examples
consent_dir = "./api/examples/GET_Consent/"
CONSENT__FILTERED_RELATIONSHIPS_STATUS_ACTIVE = (
    consent_dir + "filtered-relationships-status-active.yaml"
)
CONSENT__FILTERED_RELATIONSHIPS_STATUS_INACTIVE = (
    consent_dir + "filtered-relationships-status-inactive.yaml"
)
CONSENT__FILTERED_RELATIONSHIPS_STATUS_PROPOSED_ACTIVE = (
    consent_dir + "filtered-relationships-status-proposed-active.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS = consent_dir + "multiple-relationships.yaml"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH = (
    consent_dir + "multiple-relationships-include-performer-patient.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT = (
    consent_dir + "multiple-relationships-include-patient.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER = (
    consent_dir + "multiple-relationships-include-performer.yaml"
)
CONSENT__NO_RELATIONSHIPS = consent_dir + "no-relationships.yaml"
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP = (
    consent_dir + "single-consenting-adult-relationship.yaml"
)
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH = (
    consent_dir + "single-consenting-adult-relationship-include-performer-patient.yaml"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP = (
    consent_dir + "single-mother-child-relationship.yaml"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH = (
    consent_dir + "single-mother-child-relationship-include-performer-patient.yaml"
)
CONSENT__STATUS_PARAM_INVALID = consent_dir + "errors/invalid-status-parameter.yaml"
