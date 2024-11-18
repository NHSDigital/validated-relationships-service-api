NOT_FOUND = "./api/responses/not_found.json"
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

# Example files

# Common examples
INTERNAL_SERVER_ERROR_EXAMPLE = "./api/examples/errors/internal-server-error.yaml"
# Consent examples
CONSENT__ADULT_CONSENTING_EXAMPLE = "./api/examples/GET_Consent/adults-consenting.yaml"
CONSENT__MIXED_EXAMPLE = "./api/examples/GET_Consent/mixed.yaml"
CONSENT__MOTHER_CHILD_EXAMPLE = "./api/examples/GET_Consent/mother-child.yaml"
