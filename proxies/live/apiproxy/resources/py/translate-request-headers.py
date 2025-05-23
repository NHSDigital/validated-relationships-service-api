# Access request headers dictionary
request_headers = request.headers

# Map of lowercase header name to desired parcel case header name
request_header_translation = {"x-request-id": "X-Request-ID", "x-correlation-id": "X-Correlation-ID"}

# Loop through request headers
for key, value in request_headers.items():
    key = key.lower()
    desired_name = request_header_translation.get(key)
    if desired_name:
        flow.setVariable(f"request.header.{desired_name}", value)
