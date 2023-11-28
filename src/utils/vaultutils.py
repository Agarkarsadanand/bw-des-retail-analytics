import requests

class VaultCredentialsManager:
    def __init__(self, vault_url, role_id, secret_id, secret_path):
        self.vault_url = vault_url
        self.role_id = role_id
        self.secret_id = secret_id
        self.secret_path = secret_path
        self.token = None

    def authenticate_with_approle(self):
        # Construct the URL for authentication
        auth_url = f"{self.vault_url}/v1/auth/approle/login"

        # Set the payload with role_id and secret_id
        data = {
            "role_id": self.role_id,
            "secret_id": self.secret_id,
        }

        try:
            # Make a POST request to authenticate
            response = requests.post(auth_url, json=data)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            # Parse the JSON response
            auth_data = response.json()
            self.token = auth_data.get("auth", {}).get("client_token")

            return self.token

        except requests.exceptions.RequestException as e:
            print(f"Error authenticating with AppRole: {e}")
            return None

    def get_secret_data(self):
        # Ensure that authentication has been performed
        if not self.token:
            print("Authentication required before retrieving secret data.")
            return None

        # Construct the URL for secret retrieval
        secret_url = f"{self.vault_url}/v1/{self.secret_path}"

        try:
            # Make a GET request to retrieve secret data
            headers = {"X-Vault-Token": self.token}
            response = requests.get(secret_url, headers=headers)
            response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

            # Parse the JSON response
            secret_data = response.json().get("data", {})

            return secret_data

        except requests.exceptions.RequestException as e:
            print(f"Error retrieving secret data: {e}")
            return None

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
    else:
        print("Failed to retrieve secret data.")
else:
    print("Failed to authenticate with AppRole.")

