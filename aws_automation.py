
import os
import boto3
from botocore.exceptions import ClientError

REGION = "ap-south-1"
BUCKET_NAME = "riya-aws-resource-automation-2026"
TARGET_INSTANCE_ID = "i-08e42195f94d0f3cb"

s3 = boto3.client("s3", region_name=REGION)
ec2 = boto3.client("ec2", region_name=REGION)


def list_s3_buckets():
    try:
        response = s3.list_buckets()
        print("\n--- S3 Buckets ---")
        for bucket in response["Buckets"]:
            print(bucket["Name"])
        if not response["Buckets"]:
            print("No S3 buckets found.")
    except ClientError as error:
        print("Error:", error)


def list_ec2_instances():
    try:
        response = ec2.describe_instances()
        print("\n--- EC2 Instances ---")
        for reservation in response["Reservations"]:
            for instance in reservation["Instances"]:
                name = "Unnamed"
                for tag in instance.get("Tags", []):
                    if tag["Key"] == "Name":
                        name = tag["Value"]
                        break
                print(
                    f"Name: {name} | "
                    f"ID: {instance['InstanceId']} | "
                    f"State: {instance['State']['Name']} | "
                    f"Type: {instance['InstanceType']}"
                )
    except ClientError as error:
        print("Error:", error)


def upload_file_to_s3():
    file_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "sample.txt"
    )

    if not os.path.isfile(file_path):
        print("Error: sample.txt was not found.")
        return

    try:
        s3.upload_file(file_path, BUCKET_NAME, "sample.txt")
        print("File uploaded successfully!")
        print("Bucket:", BUCKET_NAME)
        print("File: sample.txt")
    except ClientError as error:
        print("Upload failed:", error)


def manage_ec2(action):
    try:
        response = ec2.describe_instances(
            InstanceIds=[TARGET_INSTANCE_ID]
        )
        instance = response["Reservations"][0]["Instances"][0]
        state = instance["State"]["Name"]

        print("\nTarget instance:", TARGET_INSTANCE_ID)
        print("Current state:", state)

        if action == "start":
            if state == "running":
                print("Instance is already running.")
            elif state in ["stopped"]:
                confirm = input(
                    "Start this instance? It may incur charges (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    ec2.start_instances(
                        InstanceIds=[TARGET_INSTANCE_ID]
                    )
                    print("Start request sent successfully.")
                else:
                    print("Start cancelled.")

            else:
                print("Cannot start while instance is in state:", state)

        elif action == "stop":
            if state == "stopped":
                print("Instance is already stopped.")
            elif state == "running":
                confirm = input(
                    "Stop this instance? (yes/no): "
                ).strip().lower()

                if confirm == "yes":
                    ec2.stop_instances(
                        InstanceIds=[TARGET_INSTANCE_ID]
                    )
                    print("Stop request sent successfully.")
                else:
                    print("Stop cancelled.")
            else:
                print("Cannot stop while instance is in state:", state)

    except ClientError as error:
        print("EC2 operation failed:", error)


def main():
    while True:
        print("\n===== AWS Resource Provisioning Automation =====")
        print("1. List S3 Buckets")
        print("2. List EC2 Instances")
        print("3. Upload sample.txt to S3")
        print("4. Start riya01 EC2 Instance")
        print("5. Stop riya01 EC2 Instance")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            list_s3_buckets()
        elif choice == "2":
            list_ec2_instances()
        elif choice == "3":
            upload_file_to_s3()
        elif choice == "4":
            manage_ec2("start")
        elif choice == "5":
            manage_ec2("stop")
        elif choice == "6":
            print("Exiting AWS Automation Program.")
            break
        else:
            print("Invalid choice. Enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
