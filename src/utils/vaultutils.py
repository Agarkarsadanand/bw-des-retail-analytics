import requests

vault_url = "http://127.0.0.1:8200"
role_id = "7674ac31-c26e-04b4-560a-51c3f2f84b56"
secret_id = "b82db2ac-9dda-a38c-fe38-d7389666f78b"
secret_path = "secret/data/snow"


def authenticate_with_approle(vault_url=vault_url, role_id=role_id, secret_id=secret_id):
    # Construct the URL for authentication
    auth_url = f"{vault_url}/v1/auth/approle/login"

    # Set the payload with role_id and secret_id
    data = {
        "role_id": role_id,
        "secret_id": secret_id,
    }

    try:
        # Make a POST request to authenticate
        response = requests.post(auth_url, json=data)
        response.raise_for_status()  # Raise an exception for 4xx and 5xx status codes

        # Parse the JSON response
        auth_data = response.json()
        client_token = auth_data.get("auth", {}).get("client_token")

        return client_token

    except requests.exceptions.RequestException as e:
        print(f"Error authenticating with AppRole: {e}")
        return None


def get_secret_data(token, secret_path):
    # Construct the URL for secret retrieval
    secret_url = f"{vault_url}/v1/{secret_path}"

    try:
        # Make a GET request to retrieve secret data
        headers = {"X-Vault-Token": token}
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

# Authenticate with AppRole and obtain a token
token = authenticate_with_approle(vault_url, role_id, secret_id)

if token:
    print(f"Authenticated successfully. Token: {token}")

    # Retrieve secret data
    secret_data = get_secret_data(token, secret_path)

    if secret_data:
        print(f"Secret data retrieved successfully: {secret_data}")
    else:
        print("Failed to retrieve secret data.")
else:
    print("Failed to authenticate with AppRole.")
