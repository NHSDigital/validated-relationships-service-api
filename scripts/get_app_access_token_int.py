from os import getenv
from pytest_nhsd_apim.identity_service import (
    ClientCredentialsConfig,
    ClientCredentialsAuthenticator,
)

client_id = getenv("APPLICATION_CLIENT_ID")
kid = getenv("APPLICATION_CLIENT_KID")
private_key = getenv("APPLICATION_CLIENT_PRIVATE_KEY").replace("\\n", "\n")
config = ClientCredentialsConfig(
    environment=getenv("APIGEE_ENVIRONMENT"),
    identity_service_base_url=f"https://{getenv('APIGEE_ENVIRONMENT')}.api.service.nhs.uk/oauth2-mock",
    client_id=client_id,
    jwt_private_key=private_key,
    jwt_kid=kid,
)

authenticator = ClientCredentialsAuthenticator(config=config)
print(authenticator.get_token())
