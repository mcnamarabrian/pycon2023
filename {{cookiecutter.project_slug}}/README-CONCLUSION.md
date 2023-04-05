# Conclusion

Congrats to making it this far! You've come a long way!

![Celebrate](https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif)

Let's review some things you should remember as you build and operate serverless applications:

* **Shift-left as much as possible**. Make the local developer experience a good one. Using tools like AWS SAM CLI will help a lot.

* **Test your serverless applications**. You can use the same great Python testing tools you've come to know and love.

* **Use infrastructure as code**. In this example we used AWS SAM. You could use [Hashicorp Terraform](https://www.terraform.io/), [AWS Cloud Development Kit](https://aws.amazon.com/cdk/), the [Serverless Framework](https://www.serverless.com/). Use what works to ensure you have versionable artifacts that can be deployed consistently.

* **Use automated mechanisms to deploy your serverless application**. There are a number of options like [AWS CodeDeploy](https://docs.aws.amazon.com/codedeploy/latest/userguide/tutorial-lambda-sam.html), [Jenkins](https://aws.amazon.com/blogs/compute/building-a-jenkins-pipeline-with-aws-sam/), and [Github Actions](https://aws.amazon.com/blogs/compute/using-github-actions-to-deploy-serverless-applications/).

* **Ensure you have good visibility into your serverless application**. You can't rely on traditional tooling to help you understand what is happening. AWS has a number of services that make it easy to emit and consume helpful data. There are a number of third-party vendors that also have capabilities to create and analyze logs, metrics, and traces.
