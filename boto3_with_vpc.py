import boto3 as bt3

ec2 = bt3.client('ec2')
ec2_resource = bt3.resource('ec2')
vpc_name = {'Key': 'Name', 'Value': 'boto3Vpc'}
subnet1_tag = {'Key': 'Name', 'Value': 'boto3Subnet1'}
subnet2_tag = {'Key': 'Name', 'Value': 'boto3Subnet2'}
route_table_tag = {'Key': 'Name', 'Value': 'boto3RouteTable'}
vpc = ec2.create_vpc(CidrBlock='10.0.0.0/16')

vpc_id = vpc['Vpc']['VpcId']
ec2.create_tags(Resources=[vpc_id], Tags=[vpc_name])


subnet1 = ec2.create_subnet(AvailabilityZone='us-east-1a', CidrBlock='10.0.1.0/24', VpcId=vpc_id, TagSpecifications=[
    {
        'ResourceType': 'subnet',
        'Tags': [
            subnet1_tag,
        ]
    },])
subnet2 = ec2.create_subnet(AvailabilityZone='us-east-1b', CidrBlock='10.0.0.0/24', VpcId=vpc_id, TagSpecifications=[
    {
        'ResourceType': 'subnet',
        'Tags': [
            subnet2_tag,
        ]
    },])

subnet1_id = subnet1['Subnet']['SubnetId']
subnet2_id = subnet2['Subnet']['SubnetId']


# creating the internet gateway
internet_gateway = ec2.create_internet_gateway(TagSpecifications=[
    {
        'ResourceType': 'internet-gateway',
        'Tags': [
            {
                'Key': 'Name',
                'Value': 'boto3internetgateway'
            },
        ]
    },])

# getting the internetgatway id
internet_gateway_id = internet_gateway['InternetGateway']['InternetGatewayId']

response = ec2.attach_internet_gateway(
    InternetGatewayId=internet_gateway_id, VpcId=vpc_id)
# create routing table
routetable = ec2.create_route_table(VpcId=vpc_id)
routetable_id = routetable['RouteTable']['RouteTableId']
ec2.create_tags(Resources=[routetable_id], Tags=[route_table_tag])
# associate routing table to internet gateway and subnet
# associate = ec2.associate_route_table(RouteTableId=routetable_id,GatewayId=internet_gateway_id)
associate = ec2.associate_route_table(
    RouteTableId=routetable_id, SubnetId=subnet2_id)
ec2.create_route(
    DestinationCidrBlock='0.0.0.0/0',
    RouteTableId=routetable_id,
    GatewayId=internet_gateway_id
)

security_group = ec2.describe_security_groups(
    Filters=[{'Name': 'vpc-id', 'Values': [vpc_id]}, {'Name': 'group-name', 'Values': ['default']}])
default_security_group_id = security_group['SecurityGroups'][0]['GroupId']

# Define the inbound rules to enable SSH, HTTP, and HTTPS
inbound_rules = [
    {
        'IpProtocol': 'tcp',
        'FromPort': 22,
        'ToPort': 22,
        # Allow SSH from anywhere (0.0.0.0/0)
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 80,
        'ToPort': 80,
        # Allow HTTP from anywhere (0.0.0.0/0)
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    },
    {
        'IpProtocol': 'tcp',
        'FromPort': 443,
        'ToPort': 443,
        # Allow HTTPS from anywhere (0.0.0.0/0)
        'IpRanges': [{'CidrIp': '0.0.0.0/0'}]
    }
]

# Authorize the inbound rules on the default security group
ec2.authorize_security_group_ingress(
    GroupId=default_security_group_id, IpPermissions=inbound_rules)


# Enable "Auto-assign Public IP" on the subnet (if not already enabled)

ec2.modify_subnet_attribute(
    MapPublicIpOnLaunch={'Value': True}, SubnetId=subnet2_id,)

# Use the create_instances method without specifying SecurityGroupIds
instances = ec2_resource.create_instances(
    ImageId='ami-03a6eaae9938c858c',
    InstanceType='t2.micro',
    SubnetId=subnet2_id,
    MinCount=1,
    MaxCount=1,
    TagSpecifications=[
        {
            'ResourceType': 'instance',
            'Tags': [
                {'Key': 'Name', 'Value': 'boto3Instance'}
            ]
        }
    ]
)

# Wait for the instance to be in a 'running' state
instance = instances[0]
instance.wait_until_running()

print(
    f"EC2 instance {instance.id} created successfully with the default security group.")
