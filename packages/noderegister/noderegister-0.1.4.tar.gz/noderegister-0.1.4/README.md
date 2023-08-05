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
