from os import getenv
from pytest_nhsd_apim.identity_service import (
    AuthorizationCodeConfig,
    AuthorizationCodeAuthenticator,
)

identifier = str(input("Enter an identifier: "))
scope = "nhs-login"
config = AuthorizationCodeConfig(
    environment=getenv("APIGEE_ENVIRONMENT"),
    identity_service_base_url=f"https://{getenv('APIGEE_ENVIRONMENT')}.api.service.nhs.uk/oauth2-mock",
    callback_url="https://oauth.pstmn.io/v1/browser-callback",
    client_id=getenv("APPLICATION_CLIENT_ID"),
    client_secret=getenv("APPLICATION_CLIENT_SECRET"),
    scope=scope,
    login_form={"username": identifier},
)

authenticator = AuthorizationCodeAuthenticator(config=config)
print(authenticator.get_token())
