# Differences between Azure and AWS

## Instance IP Addresses

#### Azure:
- Static: Assigned IP addresses are static and remain constant.

#### AWS:
- Dynamic: Assigned IP addresses are dynamic and may change upon instance restart.
  - Use elastic IP if you want a static IP.

## Resource Groups (RG)

#### Azure:
- Resources must go in a Resource Group: A logical container that holds related resources for an Azure solution.

#### AWS:
- Not necessary, but you can use a RG to help organize resources: AWS does not enforce the use of resource groups, but they can be used for organization and management purposes.

## Virtual Network

#### Azure:
- Create your own virtual network from the beginning and configure subnets: Azure requires you to create and configure your own virtual network, including subnets, for your resources.

#### AWS:
- Default VPC: AWS automatically provides a default Virtual Private Cloud (VPC) for your resources, simplifying the setup process. And subnets are linked to availability zones

## Monitoring
#### Azure:
- Monitoring interval is 1 minute by default

#### AWS:
- By default the monitoring of VMS is interval of 5mins
- Detailed monitoring must be enabled to get 1 minute interval
  
## Autoscaling

#### Azure:


#### AWS:
- Uses a launch template- has the other instance configurations, such as security groups, key pair etc.
- Subnets are associated with an Availability zone so instances in different azs are in different subnets.

## AMI Creation

In Azure, you will have to run the waagent deprovision user command in the virtual machine and then deallocate and generalize the VM from the terminal. However, in AWS, It's much more straighforward - it reboots the virtual machine however so note that user data will not re-run.

#### Azure:
- Get an instance that you'd like to make an image up and running.
- Run `sudo waagent -deprovision+user` in the virtual machine.
  ![alt text](img/image-21.png)
- Using Azure CLI, Deallocate and generalize the VM from the terminal.
  `az vm deallocate --resource-group <resource-group-name> --name <vm-name>`<br>![alt text](img/image-22.png)<br>
  `az vm generalize --resource-group <resource-group-name> --name <vm-name>`<br>![alt text](img/image-23.png)<br>
- On the Azure portal, navigate to the VM page and click on "Capture" to capture the VM image.
- Create an image from the instance, providing name, description, storage and tags.

#### AWS:
- Get an instance that you'd like to make an image up and running.
![alt text](img/image-24.png)
- Create an image from the instance, providing name, description, storage and tags.

### Clean Up for Images

#### Azure:
- Using Azure CLI, Deallocate and generalize the VM.
- Delete the image.

#### AWS:
- Delete the AMI:
  - Deregister the AMI.
  - Delete the associated snapshot.
