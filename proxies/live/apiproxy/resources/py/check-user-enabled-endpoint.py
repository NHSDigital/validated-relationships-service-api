auth_level = flow.getVariable("accesstoken.auth_level")
path_suffix = flow.getVariable("proxy.pathsuffix")
request_verb = flow.getVariable("request.verb")

requested_resource = (path_suffix, request_verb)

if auth_level == "p9":
    blocked_resources = [("/FHIR/R4/Consent", "POST"), ("/FHIR/R4/Consent", "PATCH")]
elif auth_level == "all3":
    blocked_resources = [("/FHIR/R4/QuestionnaireResponse", "POST")]
else:
    blocked_resources = []

auth_forbidden = requested_resource in blocked_resources

flow.setVariable("user_auth_forbidden", auth_forbidden)
