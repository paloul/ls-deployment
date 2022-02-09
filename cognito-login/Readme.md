# Cognito Login
As of this writing, January 19th 2022, both *ISTIO* and *oauth2-proxy* are configured to 
put priority on user sessions. They work in tandem with AWS Cognito to log users of the 
application via a browser based login UI either via the configured SSO interface 
(Microsoft's in our case) or the AWS hosted login page. 

When dealing with machine-to-machine API usage, we need to remove the browser-based UI from 
authentication flow. Another mechanism that is more suitable for authenticating programmatic
access is required. 

There are client libraries for various platforms offered by AWS, i.e. Javascript, Android, 
iOS, Python. In Python there are third parties that offer the libraries with similar client
functionality, i.e. BOTO3. They all interface over REST-based calls with Cognito services. 
We can recreate these calls via manual HTTP post calls. 

To be clear, we do not want to use the Client Credentials option. This method requires the use 
of the ClientId and ClientSecret directly by the client. We also would need to create and provide
individual ClientId/ClientSecret pairs for each client. This can be difficult to maintain and track
as record of each ClientId/ClientSecret pair assigned to client must be kept. 

In order to authenticate programmatically and receive and the set of ID, Referesh and Access Tokens,
you will need the following:

0. A properly configured AWS Cognito User Pool backed with an IdP and custom Domain. 
    1. Refer to instructions on main Readme.md to see how to integrate with Cognito
1. App Client registered under a User Pool in Cognito
    1. Client Id
    2. Client Secret
2. Username in the User Pool
3. Password for the User

A successful authentication will result in a set of Id, Refresh and Access tokens. These are true for
both machine-to-machine and user interaction via a browser. 

## Browser-based User Login
User login is straight forward. There are two flows setup as we have an IdP for Corporate (BL) users 
and external users via Cognito's basic User Pool. 

Upon visiting https://dashboard.hawkeye.beyond.ai via a browser, if a session already exists, the user 
is automatically logged in. If a session does not exist in the context of the browser, then the user 
will see a login page. Two options are presented, one to the left is for BL Corporate employees via
SSO, and the other to the right is the option to input basic user/password combination for users 
added directly on the Cognito User Pool.

AWS Cognito generates a hosted UI for Cognito interaction. The hosted UI provides an OAuth 2.0 authorization server with built-in webpages that can be used to sign in users using the domain 
created. Pay attention to the URL Parameters in the link, as they play a part in the authentication
process. 

The following is a direct link to the 
Cognito hosted login page:
[Cognito hosted Hawkeye Login](https://auth.hawkeye.beyond.ai/login?client_id=28chfb9s239131j9mrc1blagag&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+profile&redirect_uri=https://dashboard.hawkeye.beyond.ai/oauth2/callback)

## Programmatic Login for machine-to-machine interaction 
When there is only machine-to-machine interaction for Perfecta APIs, the browser-based user login is
inconvenient. We need a way to stay secure but still generate an ID Token to be used with the cluster. 
The set of ID, Refresh and Access Tokens generated via the login process are JWT tokens. Once generated
and in possession of an ID Token, HTTP requests can embed them within an Authorization header. The
cluster, with the help of ISTIO, will authorize the incoming ID Token as a Bearer access token. 

An Authorization header example:
`Authorization: Bearer 18f034b5c1ad23`

The benefit here is that even though it is a machine-to-machine interaction, the cluster is able to
identify the certain user identity via the ID Token. This allows us to differentiate between multiple
entities from the same tenant/company/client/etc. In example, both Bob and Bill from CompanyX can 
communicate with the cluster using their own user accounts and we can differentiate between the two.
This is in direct comparison to a different flow known as `Client Credentials` where often times is 
connected to only one external tenant/company/client/etc via specific Client Id and Secret pair.

### Generating Tokens programmatically
Cognito provides a RESTful interface to generate and retrieve tokens. The only extra step required
before submitting the RESTful API request is to generate a unique SECRET HASH from the combination of
three data fields: Client Id, Client Secret and Username. 

The POST API call expects the following data in the request body:
```
{
    "AuthParameters": {
        "USERNAME": "user@company.com",
        "PASSWORD": "userpa$$word",
        "SECRET_HASH": "0nsiY6WMsNSFzQTftIWz9rcSISW3sRVViTZefH7xfDs="
    },
    "AuthFlow": "USER_PASSWORD_AUTH",
    "ClientId": "28chfb9s239131j9mrc1blagag"
}
```
In the above data structure, only the SECRET_HASH field is generated. It is generated with the 
following Python snippet of code. 
```
>>> import hmac
>>> import base64
>>> import hashlib

>>> username = b"user@company.com"
>>> appClientId = b"123zsf123basdlfkj"
>>> appClientSecret = b"asdf0asdf2jd4asdasdfasdfasdf123asdf123"

>>> signed = hmac.new(appClientSecret, username+appClientId, digestmod=hashlib.sha256)
>>> secret_hash = base64.b64encode(signed.digest())
>>> secret_hash

b'0nsiY6WMsNSFzQTftIWz9rcSISW3sRVViTZefH7xfDs='
```
The generated SECRET_HASH is unique for each User requesting ID tokens. The User's password is not used
in generating the SECRET_HASH. The SECRET_HASH should be provided to the customer and can be used by 
the User indefinitely. The use of the SECRET_HASH removes the need to share the ClientSecret with the
tenant/customer/client/etc. The ClientSecret remains in Beyond Limits' possession and should remain 
confidential. Beyond Limits will generate the SECRET_HASH for each unique user requesting access to 
the application, after which the users can proceed to call the following Cognito POST API endpoint
with the data and generate tokens. 

The RESTful API endpoint is: `https://cognito-idp.us-west-2.amazonaws.com`. The region in the URL needs
to match the Region of the Cognito UserPool deployed for the application. Hawkeye's Cognito service is
currently deployed in Oregon (us-west-2). If the application's Cognito service is deployed in another
region, update the URL appropriately. 

Two specific headers need to be defined for the request to function correctly:  
```X-Amz-Target AWSCognitoIdentityProviderService.InitiateAuth```   
```Content-Type application/x-amz-json-1.1```

Fill in the correct parameters in the JSON structure above and submit the request. The request needs 
to be a POST.

## Authentication Result Response
The response to the above request will be a JSON structure containing an Authentication Result property 
with Access Token, Id Token and Refresh Token.
```
{
    "AuthenticationResult": {
        "AccessToken": "eyJraWQiOi...yxaVXbWLi7e6T439A",
        "ExpiresIn": 3600,
        "IdToken": "eyJraWQiOiJZlJ...XD4D98c1i-iZm0A",
        "RefreshToken": "eyJjdHiLC...1QXKAKtnmu72dA",
        "TokenType": "Bearer"
    },
    "ChallengeParameters": {}
}
```

## Authenticated API Requests
Once you have the Authentication Result JSON response, you can make authenticated Hawkeye API requests.
Extract the IdToken from the Authentication Result JSON response and use it in all subsequent Hawkeye
API requests. The Id Token should be added as a Bearer type token as an Authorization header.
```
Key: Authorization 
Value: Bearer eyJraWQiOiJZlJ...XD4D98c1i-iZm0A
```

## Using the Refresh Token
The option to refresh tokens is possible as well. Once you have Tokens generated from
the main Initiate Auth call, you can use the Refresh Token and generate new Id Tokens without
using your username/password combination.  
The Request Body needs to be updated to reflect the request for Refresh Tokens.  
**The Endpoint and any headers remain the same as above.**
```
# Example Refresh Token POST Body
{
    "AuthParameters": {
        "REFRESH_TOKEN": "eyJjdHiLC...1QXKAKtnmu72dA",
        "SECRET_HASH": "c932...vdd3"
    },
    "AuthFlow": "REFRESH_TOKEN_AUTH",
    "ClientId": "68u17si0t3apv22e4o06h1i41t"
}
```
Changes to POST Body:  
1. Set the "AuthFlow" property value to "REFRESH_TOKEN_AUTH"
2. Remove the "USERNAME" and "PASSWORD" properties from "AuthParameters"
3. Add a "REFRESH_TOKEN" property to "AuthParameters" and set its value to the refresh token
4. Set the "SECRET_HASH" value to the actual Client Secret provided to you without modification  

You will receive a similar JSON Authentication Result response as above, minus a Refresh Token.
```
{
    "AuthenticationResult": {
        "AccessToken": "eyJraWQiOi...vPVhtQ",
        "ExpiresIn": 3600,
        "IdToken": "eyJraWQiO...KfX_daLNqpA",
        "TokenType": "Bearer"
    },
    "ChallengeParameters": {}
}
```


## References 
[Stackoverflow - What is the REST (or CLI) API for logging in to Amazon Cognito user pools](https://stackoverflow.com/questions/37941780/what-is-the-rest-or-cli-api-for-logging-in-to-amazon-cognito-user-pools/53343689#53343689)

[StackOverflow - Unable to verify secret hash for client at REFRESH_TOKEN_AUTH](https://stackoverflow.com/questions/54430978/unable-to-verify-secret-hash-for-client-at-refresh-token-auth)

[StackOverflow - Example code for AWS Cognito User Pool InitiateAuth with Username and Password via HTTPS call?](https://stackoverflow.com/questions/62249845/example-code-for-aws-cognito-user-pool-initiateauth-with-username-and-password-v)