
import boto3

REGION = "ap-south-1"

def list_ec2_instances():
    try:
        ec2 = boto3.client("ec2", region_name=REGION)
        response = ec2.describe_instances()

        print("\n===== YOUR EC2 INSTANCES =====")

        found = False

        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                found = True

                name = "No Name"
                for tag in instance.get("Tags", []):
                    if tag["Key"] == "Name":
                        name = tag["Value"]
                        break

                print("Name:", name)
                print("Instance ID:", instance["InstanceId"])
                print("State:", instance["State"]["Name"])
                print("Instance Type:", instance["InstanceType"])
                print("-" * 35)

        if not found:
            print("No EC2 instances found in", REGION)

        print("EC2 listing completed.")

    except Exception as error:
        print("Unable to list EC2 instances.")
        print("Error:", error)

if __name__ == "__main__":
    list_ec2_instances()
