################ IMPORTS ################
# Internal Python Modules
import subprocess
import argparse
from time import time, sleep
import logging 


################ Configs ################
# Set the logging level with timestamp
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Arguments Parser
parser = argparse.ArgumentParser(description="Deploy the stack to the specified AWS region")
parser.add_argument('--update', action='store_true', help='Update the stack if it exists')
args = parser.parse_args()

# Unique Stack Name
unique_id = int(time())
stack_name = f"SimpleStack-{unique_id}"

# Regions
regions_to_deploy = ["us-east-1"]


################ FUNCTIONS ################
def deploy_stack_to_region(region:str) -> None:
    '''Deploy the stack to the specified region
    Args:
        region (str): The AWS region where the stack will be deployed
    '''
    # Define the AWS CLI command to deploy the stack in the specified region
    aws_command = [
        "aws", "cloudformation", "create-stack" if not args.update else "update-stack",
        "--stack-name", stack_name,
        "--template-body", "file://infrastructure/create-resources.yaml",
        "--region", region
    ]

    # Execute the AWS CLI command
    subprocess.run(aws_command, check=True)

    # Wait for the stack to be created
    if not args.update:
        logging.info(f"Waiting for the stack to be created in {region}... This usually takes around 5 minutes to 7 minutes.")
        wait_command = [
            "aws", "cloudformation", "wait", "stack-create-complete" if not args.update else "stack-update-complete",
            "--stack-name", stack_name,
            "--region", region
        ]   
        subprocess.run(wait_command, check=True)
        logging.info(f"Stack created in {region}.")



def get_cloudfront_distribution_url(region:str) -> str:
    '''Retrieve the CloudFront Distribution Domain Name
    Args:
        region (str): The AWS region where the CloudFront distribution is located
    Returns:
        str: The CloudFront Distribution Domain Name'''
    
    # Retrieve the CloudFront Distribution Domain Name
    describe_command = [
        "aws", "cloudformation", "describe-stacks",
        "--stack-name", stack_name,
        "--region", region,
        "--query", "Stacks[0].Outputs[?OutputKey=='CloudFrontDistributionDomainName'].OutputValue",
        "--output", "text"
    ]
    result = subprocess.run(describe_command, check=True, capture_output=True, text=True)
    return result.stdout.strip()



def get_s3_bucket_name(region:str) -> str:
    '''Retrieve the name of the S3 bucket created by the CloudFormation stack
    Args:
        region (str): The AWS region where the S3 bucket is located
    Returns:
        str: The name of the S3 bucket'''
    
    # Retrieve the S3 Bucket Name
    describe_command = [
        "aws", "cloudformation", "describe-stacks",
        "--stack-name", stack_name,
        "--region", region,
        "--query", "Stacks[0].Outputs[?OutputKey=='WebsiteURL'].OutputValue",
        "--output", "text"
    ]
    result = subprocess.run(describe_command, check=True, capture_output=True, text=True).stdout.strip()
    stripped_url = result.split("//")[1].split(".")[0]

    logging.debug(f"S3 result: {stripped_url}")
    return stripped_url



def upload_files_to_s3(region:str, s3_bucket_name:str) -> None:
    '''Upload the files to the S3 bucket in the specified region
    Args:
        region (str): The AWS region where the S3 bucket is located
        s3_bucket_name (str): The name of the S3 bucket'''
    
    path = "infrastructure"
    files_to_upload = ["index.html", "error.html"]
    for file_name in files_to_upload:
        upload_command = [
            "aws", "s3", "cp", path+"/"+file_name,
            f"s3://{s3_bucket_name}/{file_name}",
            "--region", region
        ]
        subprocess.run(upload_command, check=True)
        logging.info(f"Uploaded {file_name} to S3 bucket: {s3_bucket_name}")\
        

################ MAIN ################
if __name__ == "__main__":
    # Deploy the stack to each region
    for region in regions_to_deploy:
        logging.info(f"Deploying stack to {region}...")
        deploy_stack_to_region(region)

        cloudfront_url = get_cloudfront_distribution_url(region)
        logging.info(f"CloudFront URL for region {region}: {cloudfront_url}")

        s3_bucket_name = get_s3_bucket_name(region)
        logging.info(f"S3 Bucket Name for region {region}: {s3_bucket_name}")

        logging.info(f"Uploading files to S3 bucket in region {region}...")
        upload_files_to_s3(region, s3_bucket_name)
        logging.info(f"Files uploaded to S3 bucket in region {region}.")

    logging.info("Stack deployment to all regions completed.")

    logging.info("\n Running Tests with Go!")
    subprocess.run(["go", "test", "-v", "./infrastructure/site_test.go", f"-domain={cloudfront_url}"], check=True)
    logging.info("\n Tests completed successfully!")

    print(f"\nSuccess! Please go to CloudFront URL to see the website: {cloudfront_url}")

    