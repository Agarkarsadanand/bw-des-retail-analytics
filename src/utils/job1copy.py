import boto3
from vaultutils import VaultCredentialsManager
from awsutils import AWSConnector 
from snowutil import SnowflakeConnector


# Set your Vault URL, role_id, and secret_id
vault_url = "http://127.0.0.1:8200"
role_id = "7674ac31-c26e-04b4-560a-51c3f2f84b56"
secret_id = "b82db2ac-9dda-a38c-fe38-d7389666f78b"
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

        print("S3 Buckets:")
        for bucket in response['Buckets']:
            print(f"- {bucket['Name']}")
    else:
        print("Failed to retrieve secret data.")
else:
    print("Failed to authenticate with AppRole.")

aws_access_key = secret_data['data']['bw-aws-accesskey-dev']
aws_secret_key = secret_data['data']['bw-aws-secret-dev']

region = 'us-east-1'  # Replace with your preferred AWS region

# Create an instance of the AWSConnector class
client='iam'
aws_connector = AWSConnector(aws_access_key, aws_secret_key, client, region)

# # Access the S3 client through the instance
iam_client = aws_connector.aws_client_conn

# # Now you can use s3_client to perform S3 operations
response = iam_client.list_groups()
print("iam groups {response}:")



# Replace these with your Snowflake account details
secret_path = "secret/data/snow"

# Create an instance of the VaultCredentialsManager
vault_manager = VaultCredentialsManager(vault_url, role_id, secret_id, secret_path)

# Authenticate with AppRole and obtain a token
token = vault_manager.authenticate_with_approle()

if token:
    # Retrieve secret data
    secret_data = vault_manager.get_secret_data()

    if secret_data:
        print(f"Secret data retrieved successfully: {secret_data}")

    else:
        print("Failed to retrieve secret data.")
else:
    print("Failed to authenticate with AppRole.")

aws_access_key = secret_data['data']['bw-snow-serviceusername-dev']
aws_secret_key = secret_data['data']['bw-snow-serviceuserpassword-dev']
# user = "Sadanand"
# password = "Sada@1234"
account = "ZPQVWVF-XVB45506"
warehouse = "COMPUTE_WH"
database = "SNOWFLAKE_SAMPLE_DATA"
schema = "TPCDS_SF10TCL"

# Create an instance of SnowflakeConnector
snowflake_conn = SnowflakeConnector(account, user, password, warehouse, database, schema)

# Connect to Snowflake
snowflake_conn.connect()

# Execute a query
query_result = snowflake_conn.execute_query("SELECT * FROM SNOWFLAKE_SAMPLE_DATA.TPCDS_SF10TCL.CALL_CENTER;")
print(query_result)
# Print the result
print("Current Date in Snowflake:", query_result[0][0])

# Close the connection
snowflake_conn.close_connection()