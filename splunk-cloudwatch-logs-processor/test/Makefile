.PHONY: curl all

all:

curl: 
	curl -k $(URL) -H "Authorization: Splunk $(TOKEN)" -d '{"event": "Hello, McKinley High 2!", "sourcetype": "_json", "fields": {"club":"glee", "wins":["regionals","nationals"]}}'
#	curl -k $(URL) -H "Authorization: Splunk $(TOKEN)" -d '{"event": "Hello, McKinley High!", "sourcetype": "", "fields": {"club":"glee", "wins":["regionals","nationals"]}}'
