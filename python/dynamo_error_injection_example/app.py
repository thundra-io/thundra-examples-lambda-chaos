import boto3
from config import cnf
from thundra.thundra_agent import Thundra

# Setup thundra
thundra_cnf = cnf['thundra']
thundra = Thundra(api_key=thundra_cnf.get('api_key'))


# Enable following commented out lines to
# programatically add span listeners

# from thundra.listeners import *
# from thundra.plugins.trace import trace_support
# from thundra.listeners.thundra_span_filterer import ThundraSpanFilterer, ThundraSpanFilter

# f1 = ThundraSpanFilter(tags={'aws.dynamodb.table.name': 'players-chaos-example-python'})
# filterer = ThundraSpanFilterer(span_filters=[f1])

# error_sl = ErrorInjectorSpanListener(
#     error_type=boto3.exceptions.Boto3Error,
#     inject_on_finish=False,
# )

# filtering_sl = FilteringSpanListener(
#     listener=error_sl,
#     filterer=filterer
# )

# trace_support.register_span_listener(filtering_sl)


@thundra
def handler(event, context):
    item_id = event['item_id']
    player_id = event['player_id']

    dynamo = boto3.resource('dynamodb', region_name='eu-west-2')
    
    items_table = dynamo.Table('items-chaos-example-python')
    players_table = dynamo.Table('players-chaos-example-python')


    # Set item's owned_by value to the player's id
    items_table.update_item(
        Key={'id': item_id},
        UpdateExpression='set owned_by = :player_id',
        ExpressionAttributeValues={
            ':player_id': player_id,
        },
    )

    # Add item to the players inventory
    players_table.update_item(
        Key={'id': player_id},
        UpdateExpression='set inventory = list_append(inventory, :new_item)',
        ExpressionAttributeValues={
            ':new_item': [item_id],
        },
    )
    

    return {"result": "Item is successfully added to the players inventory"}
