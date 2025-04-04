path_suffix = flow.getVariable("proxy.pathsuffix").lower()
request_verb = flow.getVariable("request.verb").lower()

blocked_resources = [
    ("/fhir/r4/relatedperson", "get"),
    ("/fhir/r4/questionnaireresponse", "post"),
]

for blocked_resources in blocked_resources:
    if blocked_resources[0] in path_suffix and blocked_resources[1] == request_verb:
        auth_forbidden = True

flow.setVariable("app_auth_forbidden", auth_forbidden)
