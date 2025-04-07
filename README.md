# dlt-source-slack

[![PyPI version](https://img.shields.io/pypi/v/dlt-source-slack)](https://pypi.org/project/dlt-source-slack/)

[DLT](https://dlthub.com/) source for [slack](https://www.slack.com/).

Currently loads the following data:

| Table | Contains |
| -- | -- |
| `users` | Items of the `users` model |

## Why are you not using the `dlt-hub/verified-sources` slack source / Differences

The [official verified source](https://github.com/dlt-hub/verified-sources/tree/master/sources/slack)
has a few drawbacks:

- on usage of the verified source, a copy of the current state of
  the `dlt-hub/verified-sources` repository is copied into your project;
  Once you make changes to it, it effectively becomes a fork,
  making it hard to update after the fact.
- This makes use of a preexisting client implementation

## Usage

Create a `.dlt/secrets.toml` with your API token
(see `dlt_source_slack/manifest.yml` for a Slack
app manifest that has the necessary credentials):

```toml
slack_bot_token = "xoxb-..."
```

and then run the default source with optional list references:

```py
from dlt_source_slack import source as slack_source

pipeline = dlt.pipeline(
   pipeline_name="slack_pipeline",
   destination="duckdb",
   dev_mode=True,
)
slack_data = slack_source()
pipeline.run(slack_data)
```

## Development

This project is using [devenv](https://devenv.sh/).

Commands:

| Command | What does it do? |
| -- | -- |
| `format` | Formats & lints all code |
| `sample-pipeline-run` | Runs the sample pipeline. |
| `sample-pipeline-show` | Starts the streamlit-based dlt hub |

### Run the sample

```sh
SLACK_BOT_TOKEN=[xoxb-...] \
  sample-pipeline-run
```

alternatively you can also create a `.dlt/secrets.toml`
(excluded from git) with the following content:

```toml
slack_bot_token = "xoxb-..."
```
