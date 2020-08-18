# Environment

Used env: Cloud9 - amazon linux

Already up-and-running:
* AWS-cli
* AWS SAM
* Docker

To be installed:
* AWS CloudFormation CLI
* Python update
* Pip update


# Testing
```
cfn generate
cfn validate
cfn submit --dry-run

sam local start-lambda

# a) test all
# but has bugs: https://github.com/aws-cloudformation/cloudformation-cli-python-plugin/issues/112
cfn test

# b)
cfn invoke CREATE test/test-invoke.json  -vvv


```