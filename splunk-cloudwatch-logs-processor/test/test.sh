#!/bin/sh

generate_post_data_hybrid()
{
cat <<EOF
{
    "host": "taskid-hybrid-224588347132",
    "source": "aws-location/unstructured/apache-test/061dc7ef-1f20-4634-87eb-a8cbf5b8ff85",
    "event": "10.224.242.91 - - [21/Jan/2019:15:25:03 +0000] \"GET / HTTP/1.1\" 200 45 DDR10",
    "fields": {
        "logGroup": "david's hybrid log group",
        "severity": "INFO",
        "docker_taskid": "224588347132",
    }
}
EOF
}

curl -k -H "Authorization: Splunk $TOKEN" $ENDPOINT -d "$(generate_post_data_hybrid)" #-v
