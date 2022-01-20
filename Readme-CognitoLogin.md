## Cognito API Login
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

### References 
[Stackoverflow - What is the REST (or CLI) API for logging in to Amazon Cognito user pools](https://stackoverflow.com/questions/37941780/what-is-the-rest-or-cli-api-for-logging-in-to-amazon-cognito-user-pools/53343689#53343689)

[StackOverflow - Unable to verify secret hash for client at REFRESH_TOKEN_AUTH](https://stackoverflow.com/questions/54430978/unable-to-verify-secret-hash-for-client-at-refresh-token-auth)

[StackOverflow - Example code for AWS Cognito User Pool InitiateAuth with Username and Password via HTTPS call?](https://stackoverflow.com/questions/62249845/example-code-for-aws-cognito-user-pool-initiateauth-with-username-and-password-v)