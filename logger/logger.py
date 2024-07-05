import sentry_sdk

sentry_sdk.init(
    dsn="https://3ba26ee363edade36c762dfa12c48718@o4507547686666240.ingest.de.sentry.io/4507547688042576",
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
)
