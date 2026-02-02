path_suffix = flow.getVariable("proxy.pathsuffix").lower()
request_verb = flow.getVariable("request.verb").lower()

auth_forbidden = False

# Check blocked endpoint is equal to path suffix
requested_resource = (path_suffix, request_verb)
blocked_resources = [
    ("/fhir/r4/relatedperson", "get"),
    ("/fhir/r4/questionnaire", "get"),
    ("/fhir/r4/questionnaireresponse", "post"),
]
auth_forbidden = requested_resource in blocked_resources

flow.setVariable("app_auth_forbidden", auth_forbidden)
