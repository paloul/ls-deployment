# Authentication - Hawkeye MEIT

User accounts will be provided to you via AWS Cognito platform. Upon receiving your email login, 
you will be given a temporary password, please proceed to set a new password. This will be a 
required step on first login attempt via AWS Cognito. 

You can try to login at the Cognito hosted login page for Hawkeye MEIT:
[Cognito hosted Hawkeye MEIT Login](https://auth.hawkeye-meit.beyond.ai/login?client_id=68u17si0t3apv22e4o06h1i41t&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+profile&redirect_uri=https://perfecta.hawkeye-meit.beyond.ai)

Hawkeye MEIT **does not** have any associated UI or dashboard. It is setup to offer only APIs for 
machine-to-machine interaction.

## <u>Programmatic Login for machine-to-machine interaction</u>
We need to generate an ID Token to be used with the cluster and authenticate the API requests. 
AWS Cognito provides the means to generate a set of ID, Refresh and Access Tokens as JWT tokens. 
Once generated and in possession of an ID Token, HTTP requests can embed them within an Authorization 
header. The cluster will authorize the incoming ID Token as a Bearer access token via the Authorization header. 

An Authorization header example:
`Authorization: Bearer 18f034b....5c1ad23`

### <u>Generating Tokens programmatically</u>
Cognito provides a RESTful interface to generate and retrieve tokens. The fields required to make the request 
to generate tokens will be provided to you. These are:  
1. Username
2. Secret Hash

The POST API call expects the following data in the request body:
```
{
    "AuthParameters": {
        "USERNAME": "user@company.com",
        "PASSWORD": "userpa$$word",
        "SECRET_HASH": "0nsiY6WMsN......ViTZefH7xfDs="
    },
    "AuthFlow": "USER_PASSWORD_AUTH",
    "ClientId": "28chf........blagag"
}
```
You will use the password you created for the account. Beyond Limits **does not** know your password.  

The RESTful POST API endpoint is: `https://cognito-idp.ap-southeast-1.amazonaws.com`. Take note of the region. 
It is Asia Pacific Southeast-1 which corresponds to Singapore.

Two specific headers need to be defined for the request to Cognito be successful. Add the following as headers
to the POST request. 
```X-Amz-Target AWSCognitoIdentityProviderService.InitiateAuth```   
```Content-Type application/x-amz-json-1.1```  

Finally, fill in the correct parameters for the POST body and submit the request. 

## <u>Authentication Result Response</u>
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

## <u>Authenticated API Requests</u>
Once you have the Authentication Result JSON response, you can make authenticated Hawkeye API requests.
Extract the IdToken from the Authentication Result JSON response and use it in all subsequent Hawkeye
API requests. The Id Token should be added as a Bearer type token to the Authorization header property.
```
Key: Authorization 
Value: Bearer eyJraWQiOiJZlJ...XD4D98c1i-iZm0A
```

## <u>Hawkeye Reasoner APIs</u>

**FILL IN**


## <u>References</u>
[Stackoverflow - What is the REST (or CLI) API for logging in to Amazon Cognito user pools](https://stackoverflow.com/questions/37941780/what-is-the-rest-or-cli-api-for-logging-in-to-amazon-cognito-user-pools/53343689#53343689)

[StackOverflow - Unable to verify secret hash for client at REFRESH_TOKEN_AUTH](https://stackoverflow.com/questions/54430978/unable-to-verify-secret-hash-for-client-at-refresh-token-auth)

[StackOverflow - Example code for AWS Cognito User Pool InitiateAuth with Username and Password via HTTPS call?](https://stackoverflow.com/questions/62249845/example-code-for-aws-cognito-user-pool-initiateauth-with-username-and-password-v)