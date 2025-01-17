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
INVALIDATED_RESOURCE = "./api/examples/errors/invalidated-resource.yaml"
MISSING_IDENTIFIER = "./api/examples/errors/missing-identifier.yaml"
INVALID_IDENTIFIER = "./api/examples/errors/invalid-identifier.yaml"

# Consent examples
CONSENT__DIRECTORY = "./api/examples/GET_Consent/"
CONSENT__FILTERED_RELATIONSHIPS_STATUS_ACTIVE = (
    f"{CONSENT__DIRECTORY}filtered-relationships-status-active.yaml"
)
CONSENT__FILTERED_RELATIONSHIPS_STATUS_INACTIVE = (
    f"{CONSENT__DIRECTORY}filtered-relationships-status-inactive.yaml"
)
CONSENT__FILTERED_RELATIONSHIPS_STATUS_PROPOSED_ACTIVE = (
    f"{CONSENT__DIRECTORY}filtered-relationships-status-proposed-active.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS = f"{CONSENT__DIRECTORY}multiple-relationships.yaml"
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH = (
    f"{CONSENT__DIRECTORY}multiple-relationships-include-performer-patient.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT = (
    f"{CONSENT__DIRECTORY}multiple-relationships-include-patient.yaml"
)
CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER = (
    f"{CONSENT__DIRECTORY}multiple-relationships-include-performer.yaml"
)
CONSENT__NO_RELATIONSHIPS = f"{CONSENT__DIRECTORY}no-relationships.yaml"
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP = (
    f"{CONSENT__DIRECTORY}single-consenting-adult-relationship.yaml"
)
CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH = (
    f"{CONSENT__DIRECTORY}single-consenting-adult-relationship-include-performer-patient.yaml"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP = (
    f"{CONSENT__DIRECTORY}single-mother-child-relationship.yaml"
)
CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH = (
    f"{CONSENT__DIRECTORY}single-mother-child-relationship-include-performer-patient.yaml"
)
CONSENT__STATUS_PARAM_INVALID = f"{CONSENT__DIRECTORY}errors/invalid-status-parameter.yaml"
