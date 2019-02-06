import redis
import psycopg2
import logging
from config import cnf
from thundra.thundra_agent import Thundra
from thundra.plugins.log.thundra_log_handler import ThundraLogHandler

# Setup logger
logger = logging.getLogger('handler')
logger.setLevel(logging.DEBUG)
logger.addHandler(ThundraLogHandler())

# Setup redis and psql connections
redis_cnf = cnf['redis']
redis_conn = redis.Redis(
    host=redis_cnf.get('host'),
    port=int(redis_cnf.get('port')),
    password=redis_cnf.get('password')
)

psql_cnf = cnf['postgresql']
psql_conn = psycopg2.connect(
    user=psql_cnf.get('user'),
    host=psql_cnf.get('host'),
    password=psql_cnf.get('password'),
    dbname=psql_cnf.get('dbname')
)

# Setup thundra
thundra_cnf = cnf['thundra']
thundra = Thundra(api_key=thundra_cnf.get('api_key'))


# Enable following commented out lines to
# programatically add span listeners

# from thundra.listeners import *
# from thundra.plugins.trace import trace_support
# from thundra.listeners.thundra_span_filterer import ThundraSpanFilterer, ThundraSpanFilter

# f1 = ThundraSpanFilter(class_name='Redis')
# filterer = ThundraSpanFilterer(span_filters=[f1])

# error_sl = ErrorInjectorSpanListener(
#     error_type=redis.ConnectionError,
#     inject_on_finish=False,
# )

# filtering_sl = FilteringSpanListener(
#     listener=error_sl,
#     filterer=filterer
# )

# trace_support.register_span_listener(filtering_sl)

@thundra
def handler(event, context):
    user_id = event['user_id']
    
    user = redis_conn.get(user_id)
    
    # try:
    #     user = redis_conn.get(user_id)
    # except Exception as e:
    #     user = None
    #     logger.error("error while getting user from redis: {}".format(e))
    
    found = user is not None

    if not found:
        query = "SELECT u FROM users u WHERE u.id = %s"
        data = (user_id, )
        
        cur = psql_conn.cursor()
        cur.execute(query, data)

        user = cur.fetchone()
        found = user is not None

        cur.close()
    
    return {"userFound": found}

