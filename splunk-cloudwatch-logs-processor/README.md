## The cloudwatch_to_splunk lambda function

# TODO: Were is the cloudwatch_to_splunk name in this repo? The name seems to
# be splunk-cloudwatch-logs-processor? It is. Look at: lambda.json

This lambda function is designed to forward log events to
[Splunk](https://www.splunk.com/) from an arbitrary number of
[CloudWatch log
groups](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CloudWatchLogsConcepts.html)
in the same region.  Each log group requires a [CloudWatch subscription
filter](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CreateSubscriptionFilter.html)
and configuration using [AWS Systems Manager Parameter
Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-paramstore.html)
(SSM). The lambda function also requires environment variables for
global configuration.

### Configuration

The environment variable `SSM_PREFIX` is an SSM path used by the
lambda function to find the configuration root. This environment
variable is required. See [SSM Configuration
Layout](#SSM-Configuration-Layout) for details on the layout of
this configuration tree.

The environment variable `SPLUNK_CACHE_TTL` is a required variable
that is used to configure the SSM cache in milliseconds. A log group's
SSM configuration is only loaded as needed. After it is loaded the
lambda code will not reload the configuration from SSM till the TTL
expires even if Splunk logging is failing due to bad credentials.

Variable | Required | Description
-------- | -------- | ------------
`SSM_PREFIX` | True | SSM path to the configuration root |
`SPLUNK_CACHE_TTL` | True | Time in milliseconds to cache SSM configuration |

### SSM Configuration Layout

Each CloudWatch log group event processed by the lambda function
requires configuration in SSM. This configuration is rooted at
`$SSM_PREFIX/logGroup`. Three parameters are expected:

SSM Parameter | Required | SSM description
------------- | -------- | -------------
| `hec_endpoint` | True | Splunk [HEC endpoint](http://dev.splunk.com/view/event-collector/SP-CAAAE7G) url |
| `hec_token` | True | Splunk [HEC token](http://dev.splunk.com/view/event-collector/SP-CAAAE7C) |
| `sourcetype` | True | Splunk [sourcetype](https://docs.splunk.com/Documentation/Splunk/7.2.3/Data/Listofpretrainedsourcetypes) |

For example, if `SSM_PREFIX` is set to `/cloudwatch_to_splunk`, and
the CloudWatch log group is named `/service/authman`, then the
necessary configuration will be stored at
`/cloudwatch_to_splunk/service/authman`:

SSM Parameter  | SSM Description
------------- | -------------
| `/cloudwatch_to_splunk/service/authman/hec_endpoint` | Splunk HEC endpoint for handling of log group `/service/authman` |
| `/cloudwatch_to_splunk/service/authman/hec_token` | Splunk HEC token for handling of log group `/service/authman` |
| `/cloudwatch_to_splunk/service/authman/sourcetype` | Splunk sourcetype value to apply for logs of log group `/service/authman` |

### CloudWatch Subscription Filter

In order to establish a relationship between a CloudWatch log group
and the lambda function, the creation of a [CloudWatch subscription
filter](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CreateSubscriptionFilter.html)
is necessary. The filter specifies two elements:

* The name of the target lambda function
* An expression on which to filter CloudWatch log messages; log
messages matching the filter are collected for transmission to the
lambda function. The expression defaults to an empty string, meaning
that the filter matches *all* log messages in the specified log
group.
