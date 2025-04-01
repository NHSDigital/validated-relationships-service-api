auth_level = flow.getVariable("accesstoken.auth_level")
path_suffix = flow.getVariable("proxy.pathsuffix")
request_verb = flow.getVariable("request.verb")

requested_endpoint = (path_suffix, request_verb)

if auth_level == "p9":
    auth_permitted = requested_endpoint in [
        ("/FHIR/R4/RelatedPerson", "GET"),
        ("/FHIR/R4/QuestionnaireResponse", "POST"),
        ("/FHIR/R4/QuestionnaireResponse", "GET"),
        ("/FHIR/R4/Consent", "GET"),
        ("/FHIR/R4/Consent", "PATCH"),
    ]
elif auth_level == "all3":
    auth_permitted = requested_endpoint in [
        ("/FHIR/R4/RelatedPerson", "GET"),
        ("/FHIR/R4/Questionnaire", "GET"),
        ("/FHIR/R4/QuestionnaireResponse", "GET"),
        ("/FHIR/R4/Consent", "GET"),
        ("/FHIR/R4/Consent", "POST"),
        ("/FHIR/R4/Consent", "PATCH"),
    ]
else:
    auth_permitted = False

flow.setVariable("user_auth_permitted", auth_permitted)
