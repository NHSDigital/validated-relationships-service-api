auth_level = flow.getVariable("accesstoken.auth_level").lower()
path_suffix = flow.getVariable("proxy.pathsuffix").lower()
request_verb = flow.getVariable("request.verb").lower()

requested_resource = (path_suffix, request_verb)

if auth_level == "p9":
    blocked_resources = [("/fhir/r4/consent", "post"), ("/fhir/r4/consent", "patch")]
elif auth_level == "all3":
    blocked_resources = [("/fhir/r4/questionnaireresponse", "post")]
else:
    blocked_resources = []

auth_forbidden = requested_resource in blocked_resources

flow.setVariable("user_auth_forbidden", auth_forbidden)
