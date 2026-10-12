
import boto3

REGION = "ap-south-1"

try:
    sts = boto3.client("sts", region_name=REGION)
    identity = sts.get_caller_identity()

    print("AWS connection successful!")
    print("AWS Account:", identity["Account"])
    print("AWS Region:", REGION)

except Exception as error:
    print("AWS connection failed.")
    print("Error:", error)
