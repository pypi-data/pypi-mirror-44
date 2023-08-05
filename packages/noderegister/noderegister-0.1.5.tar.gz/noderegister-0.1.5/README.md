![PyPI](https://img.shields.io/pypi/v/noderegister.svg?color=blue&label=pypi%20release)

[![Build Status](https://travis-ci.org/avattathil/noderegister.svg?branch=master)](https://travis-ci.org/avattathil/noderegister)

### noderegister
A Simple tool that registers ec2 host information to a DynamoDB Table

### DDB Content Example

| Node Type    | Hostname                                    | Private IP    |
| ------------ | ------------------------------------------- | ------------- |
| seednode1    | ip-172-31-36-196.us-west-2.compute.internal | 172.31.36.196 |
| seednode0    | ip-172-31-36-197.us-west-2.compute.internal | 172.31.36.197 |
| clusternode0 | ip-172-33-36-190.us-west-2.compute.internal | 172.33.36.190 |
| clusternode1 | ip-172-33-36-191.us-west-2.compute.internal | 172.33.36.191 |
| clusternode0 | ip-172-33-36-192.us-west-2.compute.internal | 172.33.36.192 |

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/noderegister.svg?label=Supported%20Python%20Versions&style=for-the-badge)

### Useage

# noderegister
```
usage: noderegister [-h] [-c] [-a ASSIGN | -r | -l] [-D DYNAMODB_TABLE]

optional arguments:
  -h, --help            show this help message and exit
  -c, --create_ddb      Create a new DynamoDB table

actions:
  -a ASSIGN, --assign ASSIGN
                        Set the node type of an existing node
  -r, --register_node   Add a new node to the DynamoDB table
  -l, --list            List Registered Node in given DynamoDB Table

required:
  for (assign|list|register_node) actions

  -D DYNAMODB_TABLE, --dynamodb_table DYNAMODB_TABLE
                        Name of Existing DynamoDB
```
