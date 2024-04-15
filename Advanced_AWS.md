# Index

1. [Creating AMI](#creating-ami)
2. [Monitoring Instances](#monitoring-instances)
3. [Creating an Autoscaling Group](#creating-an-autoscaling-group)
4. [Create Database AMI](#create-database-ami)
5. [Creating a VPC](#creating-a-vpc)

# Creating AMI

## 1. Create a Running Instance

Launch a running instance to create an AMI from.
![alt text](image-10.png)

## 2. Create Image from Instance

From the instance page, follow these steps:
   1. Click **Actions**.
   2. Select **Image and templates**.
   3. Choose **Create Image**.

![alt text](image-11.png)
   
Fill in the name, description, and tags for the AMI. Adjust the EBS storage as needed, then click **Create Image**.
![alt text](image-12.png)

## 3. Launch Instance from AMI

  1. Here we can see our ami is created and available.
   ![alt text](image-13.png)
  2. Because user-data does not rerun upon reboot, launch a new instance from the AMI to ensure the application runs upon boot. 
      - Include user-data for our use-case, such as:
```bash
#!/bin/bash
# Move to app repo
cd tech257_sparta_app/repo/app/

# Stop any running processes
pm2 stop all

# Run the application using pm2
pm2 start app.js
```
  1. Fill in as needed and ensure to include user-data for our use-case
   ![alt text](image-14.png)

## 4. Verify Application

Ensure the application is running as intended on the new instance.
![alt text](image-15.png)

## 5. Clean Up

   - Delete the AMI:
     1. Click on your AMI and select **Deregister AMI**.
      ![alt text](image-16.png)
     2. Here we can see that we should delete the associated snapshot, copy the id and then proceed to delete the ami, after deleting the ami delete the snapshot.<br>
      ![alt text](image-17.png)
      ![alt text](image-18.png)
     3. Delete the associated snapshot by copying the snapshot ID, then clicking on it, selecting **Actions**, and choosing **Delete Snapshot**. Confirm the deletion.
     ![alt text](image-19.png)
     4. (Note: Deleting the snapshot must be after deregistration of the AMI otherwise you will get the following error)
      ![alt text](image-20.png)

# Monitoring Instances

To monitor instances, navigate to the instance and scroll down. Click on "Monitoring".
![alt text](image-25.png)

- Enable Detailed Monitoring:
  - Click on "Manage detailed monitoring" to enable detailed monitoring for the instance.
  ![alt text](image-26.png)
- Add to Dashboard:
  - You can also add the instance to a centralized dashboard by selecting "Add to dashboard".
  - Choose "Create new dashboard" and then add the instance to the dashboard.
  ![alt text](image-27.png)

# Creating an Autoscaling Group

![alt text](image-46.png)

## Start with Launch Template
![alt text](image-28.png)

- Select the configuration for the app instance.
![alt text](image-29.png)
- Create a launch template.
![alt text](image-30.png)
- Launch an instance using this template to test its functionality.
![alt text](image-31.png)
![alt text](image-32.png)
- Check application is working
![alt text](image-33.png)

## Create Autoscaling Group
![alt text](image-34.png)
1. **Select Launch Template**:
   - Choose the launch template you created.
   
2. **Select VPC and Subnets**:
   - Specify the VPC and subnets for the autoscaling group.
   ![alt text](image-35.png)

3. **Attach Load Balancer**:
   - Choose `Attach a new load balancer` and select `Application Load Balancer`.
   - Configure it as `internet-facing`, ensure port 80 is open, and create or select a target group.
   - Enable `Elastic Load Balancing health checks`.
  ![alt text](image-36.png)

4. **Configure Autoscaling**:
   - Set minimum, desired, and maximum capacity.
   - Select a target tracking policy (e.g., 50% CPU utilization).
   - Choose "launch before terminating" as the policy behavior.
   ![alt text](image-37.png)

5. **Leave Default Configuration**:
   - Leave other settings as default.

6. **Add Tags**:
   - Associate tags with any created instances.
  ![alt text](image-38.png)

7. **Review and Create**:
   - Review the configuration and create the autoscaling group.
  ![alt text](image-39.png)

## Check Instances and Load Balancer

- Verify that instances are created from the autoscaling group.
  ![alt text](image-40.png)
- Check the load balancer URL to ensure it connects to the application instances.
 ![alt text](image-41.png)

## Testing Autoscaling Group

To test the Autoscaling Group (ASG), terminate an instance and observe its behavior.

- Terminate an Instance:
  - Terminate one of the instances within the ASG.
  ![alt text](image-42.png)

- Verify Load Balancer Behavior:
  - The load balancer should continue sending traffic to the terminated instance until it realises that the instance fails the health check.
  ![alt text](image-43.png)

- New Instance Creation:
  - Once the terminated instance fails the health check, a new instance should be created by the ASG.
  ![alt text](image-44.png)
  - This confirms our autoscaling group maintaining the minimum set instances

## Cleaning Up

To clean up resources, follow these steps:

1. Delete Load Balancers:
  - Navigate to Load Balancers and delete the relevant load balancers.
  ![alt text](image-47.png)

2. Delete Target Groups:
  - Go to Target Groups and delete any associated target groups.
  ![alt text](image-48.png)

3. Delete Autoscaling Groups:
  - Remove the autoscaling groups from the AWS Management Console.<br>
 ![alt text](image-49.png)

# Create Database AMI

We should have a database image so that we can deploy a mongo database in a private subnet without any configurations:

1. **Create Database AMI**:
   - Launch an EC2 instance and install the database using the installation script.
   - SSH into the instance and confirm that the MongoDB service is running.
    ![alt text](image-50.png)
   - Create an image (AMI) from this instance.
    ![alt text](image-51.png)

2. **Test AMI**:
   - Launch a new instance from the AMI to ensure it works properly.
   - Try to connect to the application and check `/posts` to verify connectivity.
    ![alt text](image-52.png)

3. **Remove Running Instances**:
   - Once the AMI is confirmed to be working, remove any running instances as they are no longer needed.

4. **Update App User Data**:
   - Modify the user data of the application VM to export the database IP address.
   - Use the following script:
```bash
#!/bin/bash

# Connect to the database from application vm
export DB_HOST=mongodb://<private-ip-of-db>:27017/posts
# Move to app repo
cd tech257_sparta_app/repo/app/
# Install npm in the environment
npm -E install
# Stop any running processes
pm2 stop all
# Run the application using pm2
pm2 start app.js
 ```
        

# Creating a VPC

We will create our own Virtual Private Cloud (VPC) to isolate our resources and increase security for our two-tier deployment. Using a VPC allows us to have control over our network environment, enabling us to define our own IP address range, create subnets, and configure route tables and gateways, enhancing security by ensuring that our resources are only accessible within the defined network boundaries.

![alt text](image-53.png)

1. **Create VPC**:
   - Navigate to the VPC section and create a new VPC.
   - Set up the VPC with a `10.0.0.0/16` CIDR range and click "Create".
     ![alt text](image-54.png)

2. **Create Subnets**:
   - Click on the newly created VPC and create subnets.
   - Add a public subnet.
    ![alt text](image-55.png)
   - Add a private subnet. 
    ![alt text](image-56.png)
   - Ensure that both subnets are created successfully.
     ![alt text](image-57.png)

3. **Set Up Internet Gateway**:
   - Create an internet gateway (IG) and attach it to the VPC.
  ![alt text](image-58.png)
   - Select the VPC and attach the internet gateway.
   ![alt text](image-59.png)
   ![alt text](image-60.png)

4. **Create Public Route Table**:
   - Create a public route table.
     ![alt text](image-61.png)
   - Edit the route table subnet associations and add the public subnet.
     ![alt text](image-62.png)
   - Associate the route table with the internet gateway.
   - Add the internet gateway as a target with `0.0.0.0/0` as the destination.
     ![alt text](image-63.png)

5. **Confirm Configuration**:
   - Verify that the resource map for the VPC looks as intended.
   ![alt text](image-64.png)

6. **Launch Database VM**:
   - Launch a database VM from the AMI with the correct network settings.
    ![alt text](image-65.png)
   - Click "Launch" and ensure it is running.

7. **Launch Application VM**:
   - Launch an application VM from the AMI with the correct network settings.
    ![alt text](image-66.png)
   - Configure the user data to export the database host (`db_host`).
    ![alt text](image-67.png)
   - Click "Create" and verify that the application and `/posts` page work as expected.
     ![alt text](image-68.png)

8. **Clean Up**:
   - Remove instances.
   - Remove security groups.
   - Remove the VPC (this will also delete route tables and subnets).

# Simple Storage Service (S3)

## Advantages:
- **Limitless/Scalable**: S3 offers virtually unlimited storage capacity, allowing you to scale your storage needs as your data grows.
- **Secure**: By default, S3 buckets are private and access to objects can be controlled through permissions, making it highly secure.
- **Accessible**: S3 can be accessed from anywhere with an internet connection, providing URLs and endpoints for easy access.
- **Redundancy and Durability**: S3 is designed with built-in redundancy, ensuring high durability and reliability with a high Service Level Agreement (SLA).

## Getting Started:
1. **Launch EC2 Instance**:
   - Launch an EC2 instance with Ubuntu 22.04 and port 22 open.
   ![alt text](image-69.png)

2. **SSH into Instance and Update**:
   - SSH into the instance and perform an update and upgrade:
     ```
     sudo apt update -y
     sudo apt upgrade -y
     ```

3. **Install AWS CLI**:
   - Install Python pip and then install AWS CLI:
     ```
     sudo apt install python3-pip -y
     sudo pip install awscli
     ```

4. **Configure AWS CLI**:
   - Run `aws configure` to log in to your AWS account.
    ![alt text](image-70.png)

5. **Create S3 Bucket**:
   - Create an S3 bucket using the AWS CLI:
     ```
     aws s3 mb s3://<s3_name>
     ```
     ![alt text](image-71.png)

6. **Upload and Manage Objects**:
   - Upload a file to the S3 bucket:
     ```
     aws s3 cp <file> <bucket_destination>
     ```
   - List the contents of the bucket to confirm the upload:
     ```
     aws s3 ls <bucket>
     ```
     ![alt text](image-72.png)
     ![alt text](image-73.png)
   - Download the contents of the bucket locally:
     ```
     aws s3 sync <bucket_path> <directory_destination>
     ```
     ![alt text](image-74.png)
   - Upload files from a local directory to the bucket:
     ```
     aws s3 sync <directory_path> <bucket_destination>
     ```

7. **Remove Objects and Buckets**:
   - :warning: Remove a specific file from the bucket:
     ```
     aws s3 rm <bucket_file_path>
     ```
   - :warning: Remove all files in a bucket:
     ```
     aws s3 rm --recursive <bucket>
     ```
     ![alt text](image-75.png)
   - :warning: Delete a bucket along with its files:
     ```
     aws s3 rb --force <bucket_name>
     ```
     ![alt text](image-76.png)
