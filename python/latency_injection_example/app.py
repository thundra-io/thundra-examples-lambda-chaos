import json
import boto3
import time
from config import cnf
from thundra.thundra_agent import Thundra
from thundra.plugins.log.thundra_log_handler import ThundraLogHandler


# Setup thundra
thundra_cnf = cnf['thundra']
thundra = Thundra(api_key=thundra_cnf.get('api_key'))

# Enable following commented out lines to
# programatically add span listeners

# from thundra.listeners import *
# from thundra.plugins.trace import trace_support
# from thundra.listeners.thundra_span_filterer import ThundraSpanFilterer, ThundraSpanFilter

# f1 = ThundraSpanFilter(class_name='AWS-Lambda', tags={'aws.lambda.name': 'upstream-lambda'})
# filterer = ThundraSpanFilterer(span_filters=[f1])

# latency_sl = LatencyInjectorSpanListener(
#     delay=2000,
#     sigma=1000,
#     distribution='normal'
# )

# filtering_sl = FilteringSpanListener(
#     listener=latency_sl,
#     filterer=filterer
# )

# trace_support.register_span_listener(filtering_sl)


@thundra
def handler(event, context):
    time.sleep(1)
    lambda_client = boto3.client('lambda', region_name='eu-west-2')
    resp = lambda_client.invoke(
        FunctionName='upstream-lambda',
        InvocationType='RequestResponse',
        Payload=b"{\"name\": \"hamit\"}"
    )

    payload = resp['Payload'].read().decode('utf-8')
    parsed_payload = json.loads(payload)

    return {"upstream_response": parsed_payload['response']}
