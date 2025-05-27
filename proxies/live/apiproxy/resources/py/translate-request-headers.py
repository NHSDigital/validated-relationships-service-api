def get_request_headers():
    request_header_names = flow.getVariable("request.headers.names")
    request_headers = {}
    for name in request_header_names:
        request_headers[name] = flow.getVariable("request.header." + name)

    return request_headers


# Access request headers dictionary
request_headers = get_request_headers()

# Map of lowercase header name to desired parcel case header name
request_header_translation = {"x-request-id": "X-Request-ID", "x-correlation-id": "X-Correlation-ID"}

# Loop through request headers
for original_header_name, header_value in request_headers.items():
    desired_header_name = request_header_translation.get(original_header_name.lower())
    if desired_header_name:
        # Store original header against the desired name for mirroring in response
        flow.setVariable(
            "original_request_header." + desired_header_name, "%s=%s" % (original_header_name, header_value)
        )
        # Remove original request header
        flow.removeVariable("request.header." + original_header_name)
        # Set header with correct casing
        flow.setVariable("request.header." + desired_header_name, header_value)
