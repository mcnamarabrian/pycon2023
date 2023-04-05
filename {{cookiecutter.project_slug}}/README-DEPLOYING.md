# Deploying the Serverless Application

You built and interacted with our serverless application locally in our [previous step](./README-INTERACTING-LOCALLY.md). You're at the point where you can deploy your API to the [Amazon Web Services (AWS)](https://aws.amazon.com) cloud.

## Building the API

In order to run the application, you will need to first `build` it. The [Makefile](./Makefile) has a target that allows for a clean building of artifacts.

```bash
make all
```

In this step, the AWS SAM CLI will processes your AWS SAM template file, application code, and any applicable language-specific files and dependencies.

## Deploying the API

The AWS SAM CLI has a `deploy` subcommand. It's been wrapped in a `make` task. Use the following command to deploy your serverless application the first time. The AWS SAM CLI will prompt you for the necessary inputs.

```bash
make deploy.guided
```

<details>
<summary>Sample Output from make deploy.guided</summary>

The following output is representative output of deploying your Python API.

```bash
% make deploy.guided
sam deploy --guided --region us-east-1 --profile brian-admin

Configuring SAM deploy
======================

        Looking for config file [samconfig.toml] :  Not found

        Setting default arguments for 'sam deploy'
        =========================================
        Stack Name [sam-app]: pycon-us-2023
        AWS Region [us-east-1]: 
        #Shows you resources changes to be deployed and require a 'Y' to initiate deploy
        Confirm changes before deploy [y/N]: 
        #SAM needs permission to be able to create roles to connect to the resources in your template
        Allow SAM CLI IAM role creation [Y/n]: 
        #Preserves the state of previously provisioned resources when an operation fails
        Disable rollback [y/N]: 
        GetBalanceFunction may not have authorization defined, Is this okay? [y/N]: y
        PostPaymentFunction may not have authorization defined, Is this okay? [y/N]: y
        Save arguments to configuration file [Y/n]: 
        SAM configuration file [samconfig.toml]: 
        SAM configuration environment [default]: 

        Looking for resources needed for deployment:

        Managed S3 bucket: aws-sam-cli-managed-default-samclisourcebucket-1n87uhj5iy5vy
        A different default S3 bucket can be set in samconfig.toml

        Saved arguments to config file
        Running 'sam deploy' for future deployments will use the parameters saved above.
        The above parameters can be changed by modifying samconfig.toml
        Learn more about samconfig.toml syntax at 
        https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-config.html

        Uploading to pycon-us-2023/c34f8217a8b08737c0c0cbafcd6426c4  934 / 934  (100.00%)
        Uploading to pycon-us-2023/917744d7f239fb1e48855d01930d4810  1451 / 1451  (100.00%)

        Deploying with following values
        ===============================
        Stack name                   : pycon-us-2023
        Region                       : us-east-1
        Confirm changeset            : False
        Disable rollback             : False
        Deployment s3 bucket         : aws-sam-cli-managed-default-samclisourcebucket-1n87uhj5iy5vy
        Capabilities                 : ["CAPABILITY_IAM"]
        Parameter overrides          : {}
        Signing Profiles             : {}

Initiating deployment
=====================

        Uploading to pycon-us-2023/162bd43c56881d9ea4226d301ec2546d.template  6219 / 6219  (100.00%)


Waiting for changeset to be created..

CloudFormation stack changeset
---------------------------------------------------------------------------------------------------------------------------------------------------------
Operation                              LogicalResourceId                      ResourceType                           Replacement                          
---------------------------------------------------------------------------------------------------------------------------------------------------------
+ Add                                  Account                                AWS::ApiGateway::Account               N/A                                  
+ Add                                  ApiCloudWatchRole                      AWS::IAM::Role                         N/A                                  
+ Add                                  CardApiDeployment753f91cdd6            AWS::ApiGateway::Deployment            N/A                                  
+ Add                                  CardApiLogGroup                        AWS::Logs::LogGroup                    N/A                                  
+ Add                                  CardApiv1Stage                         AWS::ApiGateway::Stage                 N/A                                  
+ Add                                  CardApi                                AWS::ApiGateway::RestApi               N/A                                  
+ Add                                  GetBalanceFunctionGetBalancePermissi   AWS::Lambda::Permission                N/A                                  
                                       onv1                                                                                                               
+ Add                                  GetBalanceFunctionLogGroup             AWS::Logs::LogGroup                    N/A                                  
+ Add                                  GetBalanceFunctionRole                 AWS::IAM::Role                         N/A                                  
+ Add                                  GetBalanceFunction                     AWS::Lambda::Function                  N/A                                  
+ Add                                  PostPaymentFunctionGetBalancePermiss   AWS::Lambda::Permission                N/A                                  
                                       ionv1                                                                                                              
+ Add                                  PostPaymentFunctionLogGroup            AWS::Logs::LogGroup                    N/A                                  
+ Add                                  PostPaymentFunctionRole                AWS::IAM::Role                         N/A                                  
+ Add                                  PostPaymentFunction                    AWS::Lambda::Function                  N/A                                  
---------------------------------------------------------------------------------------------------------------------------------------------------------


Changeset created successfully. arn:aws:cloudformation:us-east-1:408023262302:changeSet/samcli-deploy1680440406/a4bbf0ac-c282-4d7e-ba16-a153fba839b6


2023-04-02 09:00:18 - Waiting for stack create/update to complete

CloudFormation events from stack operations (refresh every 0.5 seconds)
---------------------------------------------------------------------------------------------------------------------------------------------------------
ResourceStatus                         ResourceType                           LogicalResourceId                      ResourceStatusReason                 
---------------------------------------------------------------------------------------------------------------------------------------------------------
CREATE_IN_PROGRESS                     AWS::IAM::Role                         PostPaymentFunctionRole                -                                    
CREATE_IN_PROGRESS                     AWS::IAM::Role                         ApiCloudWatchRole                      -                                    
CREATE_IN_PROGRESS                     AWS::IAM::Role                         GetBalanceFunctionRole                 -                                    
CREATE_IN_PROGRESS                     AWS::IAM::Role                         ApiCloudWatchRole                      Resource creation Initiated          
CREATE_IN_PROGRESS                     AWS::IAM::Role                         GetBalanceFunctionRole                 Resource creation Initiated          
CREATE_IN_PROGRESS                     AWS::IAM::Role                         PostPaymentFunctionRole                Resource creation Initiated          
CREATE_COMPLETE                        AWS::IAM::Role                         ApiCloudWatchRole                      -                                    
CREATE_COMPLETE                        AWS::IAM::Role                         GetBalanceFunctionRole                 -                                    
CREATE_COMPLETE                        AWS::IAM::Role                         PostPaymentFunctionRole                -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::Account               Account                                -                                    
CREATE_IN_PROGRESS                     AWS::Lambda::Function                  GetBalanceFunction                     -                                    
CREATE_IN_PROGRESS                     AWS::Lambda::Function                  PostPaymentFunction                    -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::Account               Account                                Resource creation Initiated          
CREATE_COMPLETE                        AWS::ApiGateway::Account               Account                                -                                    
CREATE_IN_PROGRESS                     AWS::Lambda::Function                  GetBalanceFunction                     Resource creation Initiated          
CREATE_IN_PROGRESS                     AWS::Lambda::Function                  PostPaymentFunction                    Resource creation Initiated          
CREATE_COMPLETE                        AWS::Lambda::Function                  GetBalanceFunction                     -                                    
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    GetBalanceFunctionLogGroup             -                                    
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    GetBalanceFunctionLogGroup             Resource creation Initiated          
CREATE_COMPLETE                        AWS::Logs::LogGroup                    GetBalanceFunctionLogGroup             -                                    
CREATE_COMPLETE                        AWS::Lambda::Function                  PostPaymentFunction                    -                                    
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    PostPaymentFunctionLogGroup            -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::RestApi               CardApi                                -                                    
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    PostPaymentFunctionLogGroup            Resource creation Initiated          
CREATE_COMPLETE                        AWS::Logs::LogGroup                    PostPaymentFunctionLogGroup            -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::RestApi               CardApi                                Resource creation Initiated          
CREATE_COMPLETE                        AWS::ApiGateway::RestApi               CardApi                                -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::Deployment            CardApiDeployment753f91cdd6            -                                    
CREATE_IN_PROGRESS                     AWS::Lambda::Permission                GetBalanceFunctionGetBalancePermissi   -                                    
                                                                              onv1                                                                        
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    CardApiLogGroup                        -                                    
CREATE_IN_PROGRESS                     AWS::Lambda::Permission                PostPaymentFunctionGetBalancePermiss   -                                    
                                                                              ionv1                                                                       
CREATE_IN_PROGRESS                     AWS::Lambda::Permission                GetBalanceFunctionGetBalancePermissi   Resource creation Initiated          
                                                                              onv1                                                                        
CREATE_IN_PROGRESS                     AWS::Lambda::Permission                PostPaymentFunctionGetBalancePermiss   Resource creation Initiated          
                                                                              ionv1                                                                       
CREATE_IN_PROGRESS                     AWS::Logs::LogGroup                    CardApiLogGroup                        Resource creation Initiated          
CREATE_IN_PROGRESS                     AWS::ApiGateway::Deployment            CardApiDeployment753f91cdd6            Resource creation Initiated          
CREATE_COMPLETE                        AWS::Logs::LogGroup                    CardApiLogGroup                        -                                    
CREATE_COMPLETE                        AWS::ApiGateway::Deployment            CardApiDeployment753f91cdd6            -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::Stage                 CardApiv1Stage                         -                                    
CREATE_IN_PROGRESS                     AWS::ApiGateway::Stage                 CardApiv1Stage                         Resource creation Initiated          
CREATE_COMPLETE                        AWS::ApiGateway::Stage                 CardApiv1Stage                         -                                    
CREATE_COMPLETE                        AWS::Lambda::Permission                GetBalanceFunctionGetBalancePermissi   -                                    
                                                                              onv1                                                                        
CREATE_COMPLETE                        AWS::Lambda::Permission                PostPaymentFunctionGetBalancePermiss   -                                    
                                                                              ionv1                                                                       
CREATE_COMPLETE                        AWS::CloudFormation::Stack             pycon-us-2023                          -                                    
---------------------------------------------------------------------------------------------------------------------------------------------------------

CloudFormation outputs from deployed stack
---------------------------------------------------------------------------------------------------------------------------------------------------------
Outputs                                                                                                                                                 
---------------------------------------------------------------------------------------------------------------------------------------------------------
Key                 GetBalanceUrl                                                                                                                       
Description         API Gateway endpoint URL for GetBalanceFunction                                                                                     
Value               https://idio2a0qyb.execute-api.us-east-1.amazonaws.com/v1/balance/{user-id}                                                         

Key                 PostPaymentUrl                                                                                                                      
Description         API Gateway endpoint URL for PostPaymentFunction                                                                                    
Value               https://idio2a0qyb.execute-api.us-east-1.amazonaws.com/v1/payment                                                                   
---------------------------------------------------------------------------------------------------------------------------------------------------------


Successfully created/updated stack - pycon-us-2023 in us-east-1
```

</details>

Subsequent deployments can be done using the following simplified command:

```bash
make deploy
```

The values you specified earlier will be used; they've been stored in the `samconfig.toml` file.

The output of the `make deploy` task includes two URLs - one that is wired to the `GetBalanceFunction` Lambda function and one that is wired to the `PostPaymentFunction`. These URLs are real and live.

## Making Use of the API

Congratulations! You now have a functioning - if simple - Python-based API deployed to the AWS cloud!

![Congrats!](https://media.giphy.com/media/10bHcDcPM925ry/giphy.gif)

At this point, you can issue `GET` requests to your **GetBalanceUrl** and `POST`requests to your **PostPaymentURL**.

### Get Balance

You can use any HTTP client to make your requests. The example below uses `curl`.

```bash
curl -XGET https://idio2a0qyb.execute-api.us-east-1.amazonaws.com/v1/balance/user123
```

**NOTE:** Make use of your **GetBalanceUrl** returned from `make deploy.guided` when issuing the HTTP request.

### Post Payment

```bash
curl -XPOST https://idio2a0qyb.execute-api.us-east-1.amazonaws.com/v1/payment \
-H 'Content-Type: application/json' \
-d '{"user_id": "user123", "payment_date": "2100-05-01", "amount": 100}'
```

**NOTE:** Make use of your **PostPaymentUrl** returned from `make deploy.guided` when issuing the HTTP request.

## What's Next?

In this example, you are deploying the application from your workstation. The good news is that you can deploy your application using other CI/CD tooling like [AWS CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/tutorial-lambda-sam.html), [Jenkins](https://aws.amazon.com/blogs/compute/building-a-jenkins-pipeline-with-aws-sam/), and [Github Actions](https://aws.amazon.com/blogs/compute/using-github-actions-to-deploy-serverless-applications/).

Now that you've deployed your Python serverless API, you'll explore how it's been [instrumented for observability](./README-OBSERVABILITY.md).
