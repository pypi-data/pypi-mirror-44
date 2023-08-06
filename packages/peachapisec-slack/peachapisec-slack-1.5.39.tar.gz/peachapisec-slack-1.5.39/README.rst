Slack Notification Integration
==============================

This tool provides notification ability via
Slack, the popular messaging application.

Installation
------------

  Installation of this tool has two steps.
  
  1. Create the app and webhook in Slack. See documentation for steps.
  2. Install peach2slack

    pip install peachapisec-slack
  
  3. Start using the tool

Syntax
------

  peach2slack \
    --api http://192.168.1.100 \
    --api_token=xxxx \
    --slack_webhook https://hooks.slack.com/services/xxxxx

All parameters can also be provided via environment variables.
This is especially usefull for the Slack webhook url, which can then
be stored in your CI secrets store.

Parameters
~~~~~~~~~~

:api: Peach API Security API URL. Defaults to PEACH_API environ.
:api_token: Peach API Security API Token. Defaults to PEACH_API_TOKEN environ.
:slack_webhook: Slack webhook URL. Defaults to PEACH_SLACK_WEBHOOK environ.
:msg:
  [optional] Message template to post when no issues are found. Defaults to PEACH_MSG environ.

  Defaults to: Security testing completed succesfully, no issues found after {{tests_count}} tests.
:failmsg:
  [optional] Message template to post when issues are found. Defaults to PEACH_FAILMSG environ.

  Defaults to: A total of {{failure_count}} failures from {{tests_count}} tests were found.
:errormsg:
  [optional] Error message template to post when job did't complete. Defaults to PEACH_ERRORMSG environ.

  Defaults to: Error: {{reason}}

Message Template
----------------

A message template is provided using any of the following placeholders:

:{{failure_count}}: Count of failured identified during job
:{{job_id}}: Job Identifier (GUID)
:{{job_url}}: Url to job details. Requires 'baseurl' be provided.
:{{job_tags}}: Tags set on job
:{{project}}: Project name
:{{reason}}: Job completion reason. Succes or error message.
:{{tests_count}}: Count of security tests performed during testing

