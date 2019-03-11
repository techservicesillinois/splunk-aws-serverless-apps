https://splunk-on-ramp.machinedata.illinois.edu:8000/

### LOG IN TO AWS FIRST!

```
# Deps
pip install jinja2 attrdict
npm install aws-sdk splunk-logging

export SPLUNK_CACHE_TTL=6000
export SSM_PREFIX=/cloudwatch_to_splunk
export AWS_REGION=us-east-2

mkdir -p /var/tmp/roma
mkfifo /var/tmp/roma/splunk.pipe

node debug.js < mkfifo /var/tmp/roma/splunk.pipe

# Generate new log message
./make_random_cloudwatch_json | \
	./build_payload > /var/tmp/roma/splunk.pipe


```
