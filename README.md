# thundra-examples-lambda-chaos
Chaos engineering examples using Thundra's span listener feature.

## Python
Examples usage of the span listeners in Python. For more detailed explanation and the API reference check out the official [documentation](https://docs.thundra.io/v1.0.0/docs/span-listeners).

### [1. Error injection example](https://github.com/thundra-io/thundra-examples-lambda-chaos/blob/master/python/error_injection_example/app.py)
We are doing a basic cache operation in this example. First, we are looking for `user_id` in redis. If user is not found in redis, then we are making a request to the DynamoDB to find the `user_id`. However, the code has some missing points that escape the attention. Using Thundra's `FilteringSpanListener` we inject error to the redis call. When redis call is failed because of the error that we inject using `FilteringSpanListener`, the executions fails. However, even if the cache fails for some user we should have been able to get user from the DynamoDB. That was the point which escaped the attention, and we were able to notice that problem before this code goes to live. Thanks to Thundra's new span listeners!