path_suffix = flow.getVariable("proxy.pathsuffix").lower()
request_verb = flow.getVariable("request.verb").lower()

auth_forbidden = False
if request_verb == "patch":
    # Check blocked endpoint is within path suffix i.e. ignore path parameters
    blocked_resources = ["/fhir/r4/consent"]
    for blocked_resource in blocked_resources:
        if blocked_resource in path_suffix:
            auth_forbidden = True
else:
    # Check blocked endpoint is equal to path suffix
    requested_resource = (path_suffix, request_verb)
    blocked_resources = [
        ("/fhir/r4/relatedperson", "get"),
        ("/fhir/r4/questionnaire", "get"),
        ("/fhir/r4/questionnaireresponse", "post"),
        ("/fhir/r4/questionnaireresponse", "get"),
        ("/fhir/r4/consent", "post"),
    ]
    auth_forbidden = requested_resource in blocked_resources

flow.setVariable("app_auth_forbidden", auth_forbidden)
