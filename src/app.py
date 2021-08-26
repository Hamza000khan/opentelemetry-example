import flask
import requests

from opentelemetry import trace
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter  # to export to jaeger

# for otlp official exporter
from opentelemetry.exporter.zipkin.json import ZipkinExporter
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource

from opentelemetry.instrumentation.requests import RequestsInstrumentor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

resource = Resource(attributes={
    "service.name": "Flask Server"
})

trace.set_tracer_provider(TracerProvider(resource=resource))
tracer = trace.get_tracer(__name__)

# Initiation of the exporter object
zipkin_exporter = ZipkinExporter(
    # version=Protocol.V2
    # optional:
    # endpoint="http://localhost:9411/api/v2/spans",
    # local_node_ipv4="192.168.0.1",
    # local_node_ipv6="2001:db8::c001",
    # local_node_port=31313,
    # max_tag_value_length=256
    # timeout=5 (in seconds)
)


# Create a BatchSpanProcessor and add the exporter to it
span_processor = BatchSpanProcessor(zipkin_exporter)

# add to the tracer
trace.get_tracer_provider().add_span_processor(span_processor)

app = flask.Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()


def bar(val):
    return val


def foo(x, y):
    val = x + y
    return bar(val)


@app.route("/", methods=["GET", "POST"])
def hello():
    val = 'hello'
    return val


@app.route("/test")
def test():
    val = foo(4, 5)
    return {'Value': val}


app.run(debug=False, port=5000)
