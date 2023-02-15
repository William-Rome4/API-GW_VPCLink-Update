# API-GW_VPCLink-Update
Python script that uses the boto3 library to update AWS API Gateways that use VPC Proxy / VPC Link as Integration Request

## :one: Certify that AWS CLI is installed
You have to configure AWS CLI on your environment, so you can use boto3 library correctly to manage your AWS account. 
> <a href="https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html">Get more information here</a>

## :two: Clone the repository 
Clone this repository into your Command Prompt environment, with the following git command: <br>
```shell
git clone https://github.com/William-Rome4/API-GW_VPCLink-Update.git api-gw-update-vpc
```

## :three: Run the visualization Script
To see all your API GWs configurations', you can use the command below:
```shell
python3 visualize_api_gws.py > ApiGWs.txt
```
<br><br>
Doing so, you'll generate a .txt file with all data on your API GWs that use VPC Link/Proxy

## :four: Update your RestApis
After viewing all the API Gateways that need changes or updates by analyzing the ApiGWs.txt file, you can run the Update Script with the following code:
```shell
python3 update_api_gw_vpc.py
```
<br><br>

# All set! You're ready to go!
> Thanks for reading! :wink:
