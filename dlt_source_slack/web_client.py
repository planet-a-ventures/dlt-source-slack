import dlt
from slack_sdk import WebClient
from slack_sdk.http_retry.builtin_handlers import (
    RateLimitErrorRetryHandler,
    ServerErrorRetryHandler,
)

rate_limit_handler = RateLimitErrorRetryHandler(max_retry_count=1)
server_error_handler = ServerErrorRetryHandler(max_retry_count=2)


client: WebClient | None = None


def get_web_client(
    token: str = dlt.secrets["slack_bot_token"],
):
    global client

    if client is None:
        # WebClient instantiates a client that can call API methods
        # When using Bolt, you can use either `app.client` or the `client` passed to listeners.
        client = WebClient(token=token, user_agent_prefix="dlt-source-slack")
        # Enable rate limited error retries as well
        client.retry_handlers.append(rate_limit_handler)
        client.retry_handlers.append(server_error_handler)
    return client
