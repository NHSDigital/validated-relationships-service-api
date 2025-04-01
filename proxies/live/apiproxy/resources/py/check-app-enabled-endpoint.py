path_suffix = flow.getVariable("proxy.pathsuffix")
request_verb = flow.getVariable("request.verb")

requested_endpoint = (path_suffix, request_verb)


auth_permitted = requested_endpoint in [("/FHIR/R4/Consent", "GET")]

flow.setVariable("app_auth_permitted", auth_permitted)
