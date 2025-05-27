translated_header_names = ["X-Request-ID", "X-Correlation-ID"]
for translated_header_name in translated_header_names:
    # Access original request headers dictionary
    original_request_header = flow.getVariable("original_request_header." + translated_header_name)
    if original_request_header:
        original_request_header = original_request_header.split("=")
        # Remove original response header
        flow.removeVariable("response.header." + translated_header_name)
        # Mirror original request header
        flow.setVariable("response.header." + original_request_header[0], original_request_header[1])
