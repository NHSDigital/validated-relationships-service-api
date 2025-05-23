def get_request_headers():
    request_header_names = flow.getVariable("request.headers.names")
    request_headers = {}
    for name in request_header_names:
        request_headers[name] = flow.getVariable("request.header." + name)

    return request_headers


# Access request headers dictionary
request_headers = get_request_headers()

# Store copy of original request headers
flow.setVariable("original.headers", str(request_headers))

# Map of lowercase header name to desired parcel case header name
request_header_translation = {"x-request-id": "X-Request-ID", "x-correlation-id": "X-Correlation-ID"}

# Loop through request headers
for key, value in request_headers.items():
    desired_name = request_header_translation.get(key.lower())
    if desired_name:
        # Remove original header
        flow.removeVariable("request.header." + key)
        # Set header with correct casing
        flow.setVariable("request.header." + desired_name, value)
