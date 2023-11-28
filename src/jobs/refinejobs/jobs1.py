import boto3
from utils.vaultutils import authenticate_with_approle

test = authenticate_with_approle()
print(test)