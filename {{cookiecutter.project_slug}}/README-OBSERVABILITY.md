# Observability in Your Application

One of the fundamental things that changes with serverless applications is how we observe them. In many respects, these types of application force you to be more disciplined. There is no server or container that you can connect to in order to review logs, or look at network connections, or run local tracing. You have to build this in at the start.

There are three pillars of observability - logging, metrics, and traces. The application you've deployed has mechanisms to emit all three, courtesy of [AWS Lambda Powertools for Python](https://awslabs.github.io/aws-lambda-powertools-python/latest/). 

![PyCon-Observability](https://user-images.githubusercontent.com/17259/230590257-aec9b875-c021-48f4-8428-560e444c0abb.png)

Let's dive into each in turn.

## Logging

Logging captures application events as they occur and are really helpful for troubleshooting systems that are not behaving as expected. You may have experience using Python's [logging module](https://docs.python.org/3/library/logging.html) in other applications you've used or written.

Why use the Logger utility in Powertools instead of another module? Its opinionated design makes it easy to capture both structured event data _and_ context about function execution.

By default data is emitted in JSON format. This simple decision makes it easier to discover data, regardless of whether you're using the simple search field within [CloudWatch Log Groups and Streams](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/SearchDataFilterPattern.html), [Amazon CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html), or downstream services like [Splunk](https://www.splunk.com). JSON keys are autodiscovered, making it possible to use them in your query and filter terms. You don't have to define a complex regular expression so your system can make sense of your log data. You also don't have to maintain a complex logging formatter yourself, either. 

You're logging context data about your function execution through the use of a decorator in your function handlers. This allows you to log [contextual data about your Lambda function](https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/#capturing-lambda-context-info). For example, your [get_balance handler](./src/get_balance/app.py) uses `@logger.inject_lambda_context` to capture things like:

* Whether the invocation was a cold start

* Function name

* Function ARN

* Function memory size

* Request ID

```bash
@logger.inject_lambda_context(
    correlation_id_path=correlation_paths.API_GATEWAY_REST,
    log_event=True
)
```

By default, a simple `log` statement will also include [standard structured keys](https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger/#standard-structured-keys). You can optionally include other keys that will be present in each logged event. Refer to the Powertools documentation for more information about the [Logger](https://awslabs.github.io/aws-lambda-powertools-python/latest/core/logger) utility. The log entry below is generated by single `log.info()` call that is made in the [src/post_payment/app.py](./src/post_payment/app.py) file. 

```json
{
    "level": "INFO",
    "location": "post_payment:45",
    "message": {
        "user_id": "user300",
        "amount": 300,
        "outcome": "success",
        "payment_date": "2023-05-01",
        "timestamp": "2023-04-05T12:11:32.213776"
    },
    "timestamp": "2023-04-05 12:11:32,213+0000",
    "service": "post_payment",
    "sampling_rate": "0.1",
    "cold_start": false,
    "function_name": "pycon-us-2023-PostPaymentFunction-NTbuUbZMbvkx",
    "function_memory_size": "256",
    "function_arn": "arn:aws:lambda:us-east-1:408023262302:function:pycon-us-2023-PostPaymentFunction-NTbuUbZMbvkx",
    "function_request_id": "0139ba78-4028-42c5-88ec-1ef3422588c3",
    "correlation_id": "dfd3cb6e-ebe2-4049-a44b-eabe84e51956",
    "xray_trace_id": "1-642d6574-07d837110210c9ae156a1712"
}
```

### Making Use of Structured Logs

The primary benefit of structured logging is that it becomes much easier to search logs. In this example, you will see how to search for payment requests from specific users using [CloudWatch Logs Insights](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/AnalyzingLogData.html).


The query below uses the **PostPaymentFunctionLogGroup** to retrieve warm invokes where is no cold start. What is interesting is the ability to filter results using the non-standard `cold_start` field.

```bash
fields @timestamp, @message, @logStream, @logStream
| filter cold_start = 0
| filter location like /post_payment/
```

Because your logs are structured, CloudWatch Logs Insights was able to discover fields automatically. Below is a representative image of all the discovered fields in the log streams in this log group.

<img width="2076" alt="log-insights-query-discovered-fields" src="https://user-images.githubusercontent.com/17259/230218205-f6435443-f252-4aab-8275-09681c48879b.png">

Where things get more interesting is that CloudWatch Logs Insights allows you to query _multiple_ log groups. For example, if you wanted to find out the corresponding API Gateway log entry that matches `correlation_id` '193dce91-0e1b-4d4e-8cb2-a7fe5cbafa39' in your Lambda function, you can run the following query:

```bash
fields @timestamp, service, correlation_id, @log, @message
| filter (correlation_id = '193dce91-0e1b-4d4e-8cb2-a7fe5cbafa39' or requestId = '193dce91-0e1b-4d4e-8cb2-a7fe5cbafa39')
```

In this case, `correlation_id` is used in your Lambda log and `requestId` is used in your API Gateway logs. In this example, you can see the relevant access log data.

<img width="2476" alt="log-insights-query-multiple-log-groups" src="https://user-images.githubusercontent.com/17259/230218391-450d3d0b-c708-4b9a-8afe-87b3a9b16122.png">

NOTE: The [post_payment function handler](./src/post_payment/app.py) is making use of the `correlation_id_path=correlation_paths.API_GATEWAY_REST` argument to the `@logger.inject_lambda_context` decorator. This is why the filter makes use of the `correlation_id` (AWS Lambda) and `requestId` (API Gateway). The built-in correlation paths can be found in the [awslabs/aws-lambda-powertools-python](https://github.com/awslabs/aws-lambda-powertools-python/blob/develop/aws_lambda_powertools/logging/correlation_paths.py) repository.

## Metrics

Lambda functions emit a number of [standard metrics related to invocations, performance, and concurrency](https://docs.aws.amazon.com/lambda/latest/dg/monitoring-metrics.html). While this is helpful, there is often time a need to publish custom, business-level metrics. You are collecting such metrics - payment information - in your Lambda application. AWS Lambda Powertools makes this trivial, and does away with the need to use the [boto3 CloudWatch.Client.put_metric_data](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/cloudwatch/client/put_metric_data.html) function.

Powertools emits metric data into CloudWatch logs using [Embedded Metric Format](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/CloudWatch_Embedded_Metric_Format_Specification.html). The CloudWatch Logs service, in turn, consumes these entries asynchronously so your Lambda function can return to providing business value without blocking on a metric write.

<p>
<img src="https://awslabs.github.io/aws-lambda-powertools-python/2.11.0/media/metrics_terminology.png">
</p>

_From [AWS Lambda Powertools for Python](https://awslabs.github.io/aws-lambda-powertools-python/latest/core/metrics/)_

You are writing metrics to the _pycon-us-2023_ namespace in your **PostPayment**. You are collecting the total amount of successful and unsuccessful payment amounts. The Metrics utility emits the following representative data to a log stream in your CloudWatch **PostPaymentFunction** log group.

```json
{
    "_aws": {
        "Timestamp": 1680696692214,
        "CloudWatchMetrics": [
            {
                "Namespace": "pycon-us-2023",
                "Dimensions": [
                    [
                        "service"
                    ]
                ],
                "Metrics": [
                    {
                        "Name": "SuccessfulPayment",
                        "Unit": "Count"
                    }
                ]
            }
        ]
    },
    "service": "post_payment",
    "SuccessfulPayment": [
        300
    ]
}
```

This, in turn, creates a `SuccessfulPayment` CloudWatch Metric in the `pycon-us-2023` namespace.

<img width="2467" alt="metrics-dashboard-with-custom-namespace" src="https://user-images.githubusercontent.com/17259/230218498-8f738276-c2a7-49d0-96f8-ebcca54645d6.png">
<img width="2462" alt="metrics-dashboard-with-dimension" src="https://user-images.githubusercontent.com/17259/230218634-78024157-35eb-4648-ad33-ab34b1ef1a7c.png">
<img width="2462" alt="metrics-dashboard-with-metric-name" src="https://user-images.githubusercontent.com/17259/230218693-29a4dc49-630c-4243-9fca-c8719aeef5c9.png">


## Tracing

The services you are using in your serverless application are integrated with [AWS X-Ray](https://aws.amazon.com/xray/), a service designed to allow engineers to trace requests as they travel through your application. This means that our services can add a trace ID to a new request if one is not already present and it can add to an existing trace. In this manner, requests that flow to your **CardApi** are traced. The downstream **GetBalanceFunction** and **PostPaymentFunction** can add information to these traces.

**NOTE:** AWS X-Ray will sample requests. This means that not all requests will necessarily be traced. Please refer to the [AWS X-Ray documentation](https://docs.aws.amazon.com/xray/latest/devguide/xray-console-sampling.html) for information on configuring sampling rules.

Let's explore the capabilities afforded by using AWS X-Ray.

## Viewing the Service Map

AWS X-Ray will generate a service map our our serverless application because you've enabled tracing in the Globals section of your [SAM template](./template.yaml). Even if you don't instrument your code you will still have a service map generated. Below is a sample map of your application, including the **CardApi** API Gateway and **PostPaymentFunction** and **** Lambda functions.

<img width="2511" alt="traces-service-map-overview" src="https://user-images.githubusercontent.com/17259/230219377-a0b4add7-990f-4821-85dc-60f710f69bd1.png">

You have the ability to drill down into specific nodes if necessary.

<img width="2507" alt="traces-service-map-node-selection" src="https://user-images.githubusercontent.com/17259/230219310-ce1766cc-d324-486a-8b3b-f495d6b19a22.png">

## Viewing and Searching Traces

You can dig deeper into interactions by viewing traces for a given period. The default view presents all traces for the period.

<img width="2432" alt="traces-all-traces" src="https://user-images.githubusercontent.com/17259/230218883-87fc344c-e95b-44ac-a94e-782b30f1f9b8.png">

You can dig into representative traces to get more detailed information. In this example, a request to the **GetBalanceFunction** is explored.

<img width="2719" alt="traces-ColdStart-Service-get_balance" src="https://user-images.githubusercontent.com/17259/230218966-a23d6eb1-7365-45ba-abe9-44507d33b51e.png">

You can see each of the segments of the trace. Each segment includes the service, response code, and duration. In this manner, you can see not just that an interaction occurred but what happened along the way. Because you are using AWS Lambda Powertools, you can also see default annotations added to segments. The decorator `@tracer.capture_lambda_handler` coupled with the `POWERTOOLS_SERVICE_NAME` variable in your [template.yaml](./template.yaml) makes this possible. You don't need to further add to your code - you simply made use of built-in functionality.

If you want to further instrument your code, you can take advantage of annotations and metadata. Your **PostPaymentFunction** includes the same decorator as your **GetBalanceFunction** and _also_ includes an annotation - the `user_id` that made the payment.

<img width="2725" alt="traces-ColdStart-Service-post_payment" src="https://user-images.githubusercontent.com/17259/230219067-d111d602-fb14-48f4-807e-3e49abbec813.png">

<img width="2726" alt="traces-user_id-annotation" src="https://user-images.githubusercontent.com/17259/230219429-567f6090-2afd-418f-aa36-08d844ea3a00.png">

Annotations can be helpful if you need to query your traces to dive deeper along a set of properties. Because you have these annotations in your traces, you can run queries in AWS X-Ray to:

* Find traces for the `post_payment` service

<img width="2436" alt="traces-query-service-post_payment" src="https://user-images.githubusercontent.com/17259/230219186-9a9cdb90-fc00-452d-b6f3-cbb64cc1e1e7.png">

* Find traces of cold starts

<img width="2438" alt="traces-query-ColdStart" src="https://user-images.githubusercontent.com/17259/230219131-39f721b0-4cdc-4fb6-a745-d7c2a7566699.png">

* Find traces that match a specific `user_id`

<img width="2436" alt="traces-query-user_id" src="https://user-images.githubusercontent.com/17259/230219246-37c9c9d8-0d01-48de-ad12-50e0e7f5db72.png">

## What's Next?

Now that you have a sense of how to instrument components of your API for observability, you will [take stock of the ground you've covered in this repository](./README-CONCLUSION.md).
