path_suffix = flow.getVariable("proxy.pathsuffix").lower()
request_verb = flow.getVariable("request.verb").lower()

requested_endpoint = (path_suffix, request_verb)


auth_forbidden = requested_endpoint in [
    ("/fhir/r4/relatedperson", "get"),
    ("/fhir/r4/questionnaireresponse", "post"),
]

flow.setVariable("app_auth_forbidden", auth_forbidden)
