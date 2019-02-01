import logging
import time
from config import cnf
from thundra.listeners import *
from thundra.thundra_agent import Thundra
from thundra.plugins.trace import trace_support
from thundra.plugins.trace.traceable import Traceable
from thundra.plugins.log.thundra_log_handler import ThundraLogHandler
from thundra.listeners.thundra_span_filterer import ThundraSpanFilterer, ThundraSpanFilter

# Setup thundra
thundra_cnf = cnf['thundra']
thundra = Thundra(api_key=thundra_cnf.get('api_key'))

# Create a custom span listener
class MySpanListener(ThundraSpanListener):
    def __init__(self):
        logger = logging.getLogger('MySpanListenerLogger')
        logger.setLevel(logging.DEBUG)
        logger.addHandler(ThundraLogHandler())
        self.logger = logger
    
    def on_span_started(self, span):
        self.logger.info('on_span_started called with {}'.format(span.operation_name))

    def on_span_finished(self, span):
        self.logger.info('on_span_finished called with {}'.format(span.operation_name))
    
    def from_config(config):
        pass



f1 = ThundraSpanFilter(operation_name='my_func')
filterer = ThundraSpanFilterer(span_filters=[f1])

my_sl = MySpanListener()

filtering_sl = FilteringSpanListener(
    listener=my_sl,
    filterer=filterer
)

trace_support.register_span_listener(filtering_sl)

@Traceable()
def my_func():
    time.sleep(1)


@thundra
def handler(event, context):
    time.sleep(1)

    my_func()
    
    return {"result": "Done!"}

