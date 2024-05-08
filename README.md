# Streamlit app for Amazon Bedrock

## Features

- **CloudFormation Stack**: The project is implemented using AWS CloudFormation, making it easy to deploy and manage in different AWS accounts. You can quickly set up the entire infrastructure with just a few clicks.

- **Agent Testing**: The project allows users to provide an Agent ID and Agent Alias ID, enabling seamless testing of Bedrock agents created in your AWS account. This feature simplifies the process of validating and verifying agent functionality.

- **Scalable and Reliable Hosting**: The Streamlit application is hosted on Amazon ECS (Elastic Container Service) Fargate, providing excellent scalability and reliability. Your application can automatically scale based on demand, ensuring optimal performance and availability.

- **CI/CD Pipeline Integration**: The project seamlessly integrates with AWS CodeCommit repository, enabling a robust CI/CD pipeline. Whenever you update the code in the CodeCommit repository, the project automatically triggers a rebuild and deployment process, ensuring your application is always up to date with the latest changes. 

## Prerequisites
- Have an AWS account and have access to AWS regions that support Amazon Bedrock Agents. [link](https://docs.aws.amazon.com/bedrock/latest/userguide/agents-supported.html) 

## Installation 

Follow these steps to set up and deploy the project using AWS CodeCommit and CloudFormation:

1. Clone the repository to your local machine:
   ```
   git clone https://github.com/yhou-uk/streamlit-app-for-amazon-bedrock.gitt
   ```

2. Create a new repository in AWS CodeCommit:
   - Open the AWS Management Console and navigate to the CodeCommit service.
   - Click on "Create repository" and provide a name for your repository.
   - Upload the cloned repository to your new CodeCommit repository.

3. Open the AWS Management Console and navigate to the CloudFormation service.

4. Add a public extension in your CloudFormation service to delete non-empty S3 buckets when deleting the entire stack: 
   - Deploy [this CloudFormation template](https://github.com/aws-cloudformation/community-registry-extensions/blob/main/resources/S3_DeleteBucketContents/resource-role-prod.yaml) to create the required IAM role with the necessary permissions.
   - Once the stack is successfully created, copy the ARN of the created IAM role.
   - In the AWS CloudFormation console, select 'Public extensions' from the left menu.
   - Under the 'Publisher' dropdown, choose 'Third party'.
   - Search for 'AwsCommunity::S3::DeleteBucketContents' and select it.
   - In the 'Execution role' field, provide the ARN of the IAM role created earlier.
   - Click 'Activate' to enable the extension.

5. Go back to the Cloudformation service main page, and click on "Create stack".

6. In the "Specify template" section, choose "Upload a template file" and select the `codepipeline.yaml` file from your cloned repository.

7. On the next page, provide the following parameters:
   - **Stack name**: Enter a name for your CloudFormation stack.
   - **CodeCommitURL**: Enter the URL of your CodeCommit repository.
   - **RepoName**: Enter the name of your CodeCommit repository.
   - **EnvironmentName**: Enter a unique identifier (1-4 characters) for the installed applications in your AWS account.
   - **DeployVPCInfrastructure**: Select "true" if this is the first time you are installing this project in your AWS account. Otherwise, select "false".

8. Leave the remaining settings as their default values.

9. Review your settings and click on "Create stack" to start the deployment process.

CloudFormation will now create the necessary resources and deploy your application based on the provided template and parameters.


## Clean up 

To clean up the resources created by this project and avoid incurring ongoing costs, follow these steps:

1. Delete the main CloudFormation stack:
   - Open the AWS CloudFormation console.
   - Find the stack with the name you provided during the installation process.
   - Select the stack and click on the "Delete" button.

2. Delete the deployment stack:
   - In the AWS CloudFormation console, find the stack with the name `<stack_name>deploy<EnvironmentName>`, where `<stack_name>` is the name you provided during installation and `<EnvironmentName>` is the unique identifier you specified.
   - Select the stack and click on the "Delete" button.

3. Delete the infrastructure stack:
   - In the AWS CloudFormation console, find the stack with the name `<stack_name>-infrastructure-<xxx>`, where `<stack_name>` is the name you provided during installation and `<xxx>` is a unique identifier.
   - Select the stack and click on the "Delete" button.

After deleting these three stacks, all the resources created by the project will be removed from your AWS account.

Note: Deleting the stacks will permanently remove all the associated resources. Make sure you have backed up any important data or configurations before proceeding with the cleanup process.

## Acknowledgements
   This project is based on the excellent work done in the [Customer relationship management (CRM) Bedrock Agent](https://github.com/aws-samples/amazon-bedrock-samples/tree/function_calling/agents/customer-relationship-management-agent). We would like to express our sincere appreciation to the authors and contributors of that repository for their effort and inspiration.

## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.
