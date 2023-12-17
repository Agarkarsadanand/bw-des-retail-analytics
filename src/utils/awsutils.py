import boto3
from vaultutils import VaultCredentialsManager

# Set your Vault URL, role_id, and secret_id
vault_url = "http://127.0.0.1:8200"
role_id = "973814ff-8e7d-d52c-440c-834f746d155a"
secret_id = "00f1d936-0b93-28ef-2dd0-f257b06bcc22"
secret_path = "secret/data/aws"

# Create an instance of the VaultCredentialsManager
vault_manager = VaultCredentialsManager(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and obtain a token
token = vault_manager.authenticate_with_approle()

if token:
    print(f"Authenticated successfully. Token: {token}")

    # Retrieve secret data
    secret_data = vault_manager.get_secret_data()

    if secret_data:
        print(f"Secret data retrieved successfully: {secret_data}")

        # Access specific secrets using square bracket notation
        username = secret_data.get('aws-access-key-id', None)  # Replace with your actual key name
        password = secret_data.get('aws-secret-access-key', None)  # Replace with your actual key name

        print(f"AWS Access Key ID: {username}")
        print(f"AWS Secret Access Key: {password}")

        # Set your AWS credentials
        aws_access_key_id = username
        aws_secret_access_key = password
        aws_region = 'us-east-1'

        # Create an S3 client
        s3 = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name=aws_region)

        # Example: List all S3 buckets
        response = s3.list_buckets()

        # print("S3 Buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
    else:
        print("Failed to retrieve secret data.")
else:
    print("Failed to authenticate with AppRole.")

aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secretkey-dev']

region = 'us-east-1'  # Replace with your preferred AWS region

class AWSConnector:
    def __init__(self, aws_access_key, aws_secret_key, client='s3', region='us-east-1'):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.region = region
        self.aws_client = client
        self.session = self.create_session()
        self.aws_client_conn = self.create_aws_client()
        

    def create_session(self):
        """
        Create an AWS session using the provided credentials and region.
        """
        session = boto3.Session(
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=self.region
        )
        return session

    def create_aws_client(self):
        """
        Create an AWS client using the AWS session.
        """
        aws_client_conn = self.session.client(self.aws_client)
        return aws_client_conn

# Create an instance of the AWSConnector class
# client='s3'
# aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# # Access the S3 client through the instance
# s3_client = aws_connector.aws_client_conn

# # Now you can use s3_client to perform S3 operations
# response = s3_client.list_buckets()
# print("S3 Buckets:")
# for bucket in response['Buckets']:
#     print(f"  {bucket['Name']}")