# How to run Scripts

## First Steps

### Install packages

The tooling we use to manage our packages in poetry so this needs to be installed on your local machine in order to run
the scripts.

Then run the following command in the scripts directory

```
poetry install
```

## Script Specific

### Get CIS2 Access Token for Int Environment

#### Set Environment Variables

You will require the following environment variables in order to run the script:

```
export APIGEE_ENVIRONMENT=int
export APPLICATION_CLIENT_ID={application_client_id}
export APPLICATION_CLIENT_SECRET={application_client_secret}
```

The values for `APPLICATION_CLIENT_ID` and `APPLICATION_CLIENT_SECRET` can be found on the NHS Developer Account
portal 'NHS - Proxy Core Services...' environment resource in the Active API keys section.

#### Select an identifier

There are a different levels of authenticator assurance levels eg. AAL3.
For VRS CIS2 users are only accessible to access selected APIs.
Please find a list of test users detailed in this page:
https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/testing-apis-with-our-mock-authorisation-service#test-users-for-cis2-authentication
This can be used to select your identifier for the next step.
i.e. 656005750108 to test with a CIS2 user with AAL3 authenticator assurance level.

#### Run the script

Then run the following command in the scripts directory

```
poetry run python3 get_cis2_access_token_int.py
```

You will be prompted to "Enter an identifier: "

Enter the identifier selected in previous step eg. 656005750108

In your terminal you should see a response that includes an access token

e.g.

```
{'access_token': 'EFFs3EeT0SZbF2J14LvM93vVDTaA', 'expires_in': '599', 'refresh_token': 'BDEcXjJI36DJA8Dlw8wS0jCuYJJqC8tK', 'refresh_token_expires_in': '43199', 'refresh_count': '0', 'token_type': 'Bearer'}
```

### Get NHS Login Access Token for Int Environment

#### Set Environment Variables

You will require the following environment variables in order to run the script:

```
export APIGEE_ENVIRONMENT=int
export APPLICATION_CLIENT_ID={application_client_id}
export APPLICATION_CLIENT_SECRET={application_client_secret}
```

The values for `APPLICATION_CLIENT_ID` and `APPLICATION_CLIENT_SECRET` can be found on the NHS Developer Account
portal 'NHS - Proxy Core Services...' environment resource in the Active API keys section.

#### Select an identifier

There are a different identity proofing levels eg. p9.
For VRS p9 users are only accessible to access selected APIs.
Please find a list of test users detailed in this page:
https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation/testing-apis-with-our-mock-authorisation-service#test-users-for-nhs-login
This can be used to select your identifier for the next step.
i.e. 9912003071 to test with a p9 user.

#### Run the script

Then run the following command in the scripts directory

```
poetry run python3 get_nhs_login_access_token_int.py
```

You will be prompted to "Enter an identifier: "

Enter the identifier selected in previous step eg. 9912003071

In your terminal you should see a response that includes an access token

e.g.

```
{'access_token': 'EFFs3EeT0SZbF2J14LvM93vVDTaA', 'expires_in': '599', 'refresh_token': 'BDEcXjJI36DJA8Dlw8wS0jCuYJJqC8tK', 'refresh_token_expires_in': '43199', 'refresh_count': '0', 'token_type': 'Bearer'}
```

### Get App Restricted Access Token for Int Environment

Application restricted authentication is when a system is trying to access an API rather than a person. For example the
Validated Relationship Service (VRS) will need an app restricted access token in order to call the Personal Demographic
Service (PDS) API.
https://digital.nhs.uk/developer/guides-and-documentation/security-and-authorisation#application-restricted-apis

#### Set Environment Variables

You will require the following environment variables in order to run the script:

```
export APIGEE_ENVIRONMENT=int
export APPLICATION_CLIENT_ID={vrs_application_client_id}
export APPLICATION_CLIENT_KID={vrs_application_client_secret}
export APPLICATION_CLIENT_PRIVATE_KEY={vrs_application_client_private_key}
```

Note with VRS_CLIENT_PRIVATE_KEY it needs to be wrapped in double quotation marks otherwise there can be formatting
errors

The values for `APPLICATION_CLIENT_ID` and `APPLICATION_CLIENT_KID` can be found on the NHS Developer Account portal '
NHS - Proxy Core Services...' environment resource in the Active API keys section.

The `APPLICATION_CLIENT_PRIVATE_KEY` is stored in AWS Secrets Manager. Please contact the VRS team if you don't have AWS
access to obtain this.

#### Run the script

Then run the following command in the scripts directory

```
poetry run python3 get_app_access_token_int.py
```

In your terminal you should see a response that includes an access token

e.g.

```
{'access_token': 'EFFs3EeT0SZbF2J14LvM93vVDTaA', 'expires_in': '599', 'refresh_token': 'BDEcXjJI36DJA8Dlw8wS0jCuYJJqC8tK', 'refresh_token_expires_in': '43199', 'refresh_count': '0', 'token_type': 'Bearer'}
```

### Trouble Shooting

If you have issues with the script, a good place to start is to ensure the environment variables are accessible to
poetry. This can be achieved by installing the poetry dotenv plugin

Run this command

```
poetry plugin add poetry-dotenv-plugin
```
