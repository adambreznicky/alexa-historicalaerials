# Alexa TNRIS Lookup Application
Amazon Alexa Skill for utilizing the TNRIS API's to retrieve information on what data and archive is available from TNRIS.
Currently, only implements basic Historical Aerials functionality.

### Setup
* Requires Python 2.7
* Lambda Functionality is contained to the lambda-code folder. All external packages utilized in the lambda function must be installed into the 'alexa-historicalaerials/lambda-code' folder so that all packages are localized

### Deploying
* Create a zipfile of the contents of the 'lambda-code' folder and upload to the Lambda Function in AWS

#### Future
* Expand Historical Aerials for more detailed information and interactions
* Add Data Download API and data inventory
* Add Data Catalog details