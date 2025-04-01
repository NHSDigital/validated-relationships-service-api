path_suffix = flow.getVariable("proxy.pathsuffix")
request_verb = flow.getVariable("request.verb")

requested_endpoint = (path_suffix, request_verb)


auth_forbidden = requested_endpoint in [
    ("/FHIR/R4/RelatedPerson", "GET"),
    ("/FHIR/R4/QuestionnaireResponse", "POST"),
]

flow.setVariable("app_auth_forbidden", auth_forbidden)
