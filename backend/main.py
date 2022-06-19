from fastapi import FastAPI, Request
from router import posts, user, authentication, board, delete
from config import INSTRUMENTATION_KEY
from database import engine

from opencensus.trace.attributes_helper import COMMON_ATTRIBUTES
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.azure.log_exporter import AzureLogHandler
from opencensus.trace.samplers import ProbabilitySampler
from fastapi.middleware.cors import CORSMiddleware
from opencensus.trace.span import SpanKind
from opencensus.trace.tracer import Tracer
import logging
import models

APP_INSIGHT_KEY = INSTRUMENTATION_KEY.value

logger = logging.getLogger(__name__)

app = FastAPI()

tracer = Tracer(
    exporter=AzureExporter(connection_string=f"InstrumentationKey={APP_INSIGHT_KEY}"),
    sampler=ProbabilitySampler(1.0),
)
HTTP_URL = COMMON_ATTRIBUTES["HTTP_URL"]
HTTP_ROUTE = COMMON_ATTRIBUTES["HTTP_ROUTE"]
HTTP_METHOD = COMMON_ATTRIBUTES["HTTP_METHOD"]
HTTP_STATUS_CODE = COMMON_ATTRIBUTES["HTTP_STATUS_CODE"]

logger.addHandler(
    AzureLogHandler(connection_string=f"InstrumentationKey={APP_INSIGHT_KEY}")
)

origins = ["*"]



app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*",
        "http://localhost",
        "http://localhost:8080",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def middlewareOpencensus(request: Request, call_next):
    with tracer.span(name="test") as span:
        span.span_kind = SpanKind.SERVER

        response = await call_next(request)

        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_STATUS_CODE, attribute_value=response.status_code
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_METHOD, attribute_value=str(request.method)
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_URL, attribute_value=str(request.url)
        )
        tracer.add_attribute_to_current_span(
            attribute_key=HTTP_ROUTE, attribute_value=str(request.url.path)
        )
        
    return response

app.include_router(authentication.router)
app.include_router(board.router)
app.include_router(posts.router)
app.include_router(user.router)
app.include_router(delete.router)

models.Base.metadata.create_all(engine)
