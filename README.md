# Comcast Interview

## 1. Infrastructure Assignment

### Steps to Run 
1. Attach Policy to IAM User being used within cli, so that the user may deploy the appropriate resources.
2. navigate to the root folder of this repository and run python infrastructure/deploy.py or python3 infrastructure/deploy.py
3. Wait for cloudformation stack and then check cloudfront url for success.

### File Explanations
* **create-resources.yaml**: Cloud Formation Template which deploys a WebACL, CloudFront & S3
* **deploy.py**: Python File which deploys the cloudformation template, uploads the files to s3, runs go tests and returns cloudfront url. 
* **site_tests.go**: Go File checking http --> https routing and checks for https success status. 
* **index.html**: The displayed file
* **error.html**: The error file that is displayed if there is an issue. 
* **policy.json**: This is the policy that should be attached to the IAM User. 

# 2. Coding Assignment
In the coding folder I have the file which completes the hackerrank task.

