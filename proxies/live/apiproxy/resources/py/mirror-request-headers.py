# Access original request headers dictionary
request_headers = JSON.parse(flow.getVariable("original.headers"))

# Loop through request headers and set them as response headers
for key, value in request_headers.items():
    flow.setVariable("response.header.{0}".format(key), value)
