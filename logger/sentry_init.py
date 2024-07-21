import os
from dotenv import load_dotenv
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration
from sentry_sdk.integrations.fastapi import FastApiIntegration

load_dotenv()
SENTRY_DSN=os.getenv("SENTRY_DSN")

def init():
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
        integrations=[
            StarletteIntegration(),
            FastApiIntegration(),
        ],
    )
