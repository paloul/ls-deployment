# Hawkeye MEIT

## Authentication

User accounts will be provided to you via AWS Cognito platform. Upon receiving your email login, 
you will be given a temporary password, please proceed to set a new password. This will be a 
required step on first login attempt via AWS Cognito. 

You can try to login at the Cognito hosted login page for Hawkeye MEIT:
[Cognito hosted Hawkeye MEIT Login](https://auth.hawkeye-meit.beyond.ai/login?client_id=68u17si0t3apv22e4o06h1i41t&response_type=code&scope=aws.cognito.signin.user.admin+email+openid+profile&redirect_uri=https://perfecta.hawkeye-meit.beyond.ai)

Hawkeye MEIT **does not** have any associated UI or dashboard. It is setup to offer only APIs for 
machine-to-machine interaction.

### <u>Programmatic Login for machine-to-machine interaction</u>
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
 - ```X-Amz-Target AWSCognitoIdentityProviderService.InitiateAuth```   
 - ```Content-Type application/x-amz-json-1.1```  

Finally, fill in the correct parameters for the POST body and submit the request. 

### <u>Authentication Result Response</u>
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

### <u>Authenticated API Requests</u>
Once you have the Authentication Result JSON response, you can make authenticated Hawkeye API requests.
Extract the IdToken from the Authentication Result JSON response and use it in all subsequent Hawkeye
API requests. The Id Token should be added as a Bearer type token to the Authorization header property.
```
Key: Authorization 
Value: Bearer eyJraWQiOiJZlJ...XD4D98c1i-iZm0A
```

## <u>Hawkeye Reasoner APIs</u>
#### <u>Is Alive</u>
  - https://perfecta.hawkeye-meit.beyond.ai/api/v1/is_alive
  - GET 
  - Requires Authentication Header
  - Successful Response: 200 OK
  - Failure Response: Any HTTP Error Code
  - Response Body: None 

#### <u>Versions</u>
  - https://perfecta.hawkeye-meit.beyond.ai/api/v1/versions
  - GET 
  - Requires Authentication Header
  - Successful Response: 200 OK
  - Failure Response: Any HTTP Error Code
  - Response Body: JSON
```
# Versions - Sample Response Body
{
"code": 200,
"reasoner": "00.10.03"
}
```

#### <u>Reset Patient State</u>
  - https://perfecta.hawkeye-meit.beyond.ai/api/v1/reset_patient
  - POST 
  - Requires Authentication Header
  - Successful Response: 200 OK
  - Failure Response: Any HTTP Error Code
  - Request Body: JSON
  - Response Body: None
```
# Reset Patient - Sample Request Body
{
    "patientId": "GeorgePaloulian"
}
```

#### <u>Feature Frame Reason</u>
  - https://perfecta.hawkeye-meit.beyond.ai/api/v1/feature_frame
  - POST 
  - Requires Authentication Header
  - Successful Response: 200 OK
  - Failure Response: Any HTTP Error Code
  - Response: JSON
```
# Feature Frame - Sample Request Body
{
    "age": 450,
    "bioSensorId": "GeorgePaloulian123",
    "heartRate": 90,
    "respRate": 20,
    "skinTempChest": 12.4,
    "gender": 1,
    "height": 35,
    "patientId": "GeorgePaloulian",
    "physActivity": 0,
    "posture": 1,
    "healthStatus": 1,
    "seqNo": 234234234,
    "time": 1233312554,
    "weight": 341.12
}

# Feature Frame - Sample Response Body
{
    "code": 200,
    "message": {
        "Audit_Trail": "Conclusion 1:..... has the certain value of '341.12'.",
        "Body_Visual_Status_Age": 37.5,
        "Body_Visual_Status_Blood_Pressure": [
            "White",
            "--"
        ],
        "Body_Visual_Status_Heart_Rate": [
            "Good",
            "90.00"
        ],
        "Body_Visual_Status_Height": "1.15'(35.00 cm)",
        "Body_Visual_Status_Motion": [
            "White",
            "Quiet"
        ],
        "Body_Visual_Status_Posture": [
            "White",
            "Resting"
        ],
        "Body_Visual_Status_Respiration": [
            "Good",
            "20.00"
        ],
        "Body_Visual_Status_SPO2": [
            "White",
            "--"
        ],
        "Body_Visual_Status_Sex": "--",
        "Body_Visual_Status_Temp": [
            "Good",
            "95.20F (35.11C)"
        ],
        "Body_Visual_Status_Weight": "752.04 lbs (341.12 kg)",
        "D_Heart_Rate": 0,
        "D_Holistic_View": 0,
        "D_Respiration": 0,
        "D_Temperature": [
            95.20,
            35.11,
            0.95,
            0
        ],
        "English_Bad_Measurements": "they have an abnormal BMI...they are obese.",
        "English_Critical_Alerts": "",
        "English_Diagnoses": "",
        "English_Good_Measurements": "Temp is 95.20F (35.11C) with...amount of time.",
        "English_Inputs": "Age_In_Months = 450...Weight_Kg = 341.12",
        "English_Interpretations": "Their overall vitals are good...limited amount of time.",
        "English_Medical_KBs_Used": "The general medical knowledge...Weight Analysis.",
        "English_Patient_Context": "This is adult unknown sex...BMI score of 2784.65.",
        "English_Recommendations": "",
        "English_Summary": "Their overall vitals are good.",
        "English_Wellness_Rating": [
            "Green",
            "75%"
        ],
        "Plot_Heart_Rate": [
            "90.00",
            "Good"
        ],
        "Plot_Respiration": [
            "20.00",
            "Good"
        ],
        "Plot_Temp_C": [
            "35.11",
            "Good"
        ],
        "Plot_Temp_F": [
            "95.20",
            "Good"
        ],
        "Time": 1233312444
    },
    "patientId": "GeorgePaloulian",
    "seqNo": 234234234,
    "status": "success",
    "time": 1233312444
}
```