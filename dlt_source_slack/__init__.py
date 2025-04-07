"""A source loading entities from slack (slack.com)"""

from slack_sdk.errors import SlackApiError
from enum import StrEnum
from typing import Any, Dict, Iterable, List, Sequence
import dlt
from dlt.common.typing import TDataItem
from dlt.sources import DltResource
from .web_client import get_web_client


class Table(StrEnum):
    USERS = "users"
    BOTS = "bots"
    PROFILES = "profiles"


def use_id(entity: Dict[str, Any], **kwargs) -> dict:
    return entity | {"_dlt_id": __get_id(entity)}


@dlt.resource(
    selected=True,
    parallelized=True,
    primary_key="id",
)
def users() -> Iterable[TDataItem]:
    web_client = get_web_client()
    result = web_client.users_list()

    if not result.get("ok"):
        raise SlackApiError(result.get("error"))
    yield result.get("members")


# TODO: Workaround for the fact that when `add_limit` is used, the yielded entities
# become dicts instead of first-class entities
def __get_id(obj):
    if isinstance(obj, dict):
        return obj.get("id")
    return getattr(obj, "id", None)


@dlt.transformer(
    max_table_nesting=1,
    parallelized=True,
)
async def user_details(users: List[Any]):
    for user in users:
        is_bot = user.get("is_bot")
        table_name = Table.BOTS.value if is_bot else Table.USERS.value

        yield dlt.mark.with_hints(
            item=use_id(
                {key: user[key] for key in user if key not in ["profile", "is_bot"]}
            ),
            hints=dlt.mark.make_hints(
                table_name=table_name,
                primary_key="id",
                merge_key="id",
                write_disposition="merge",
            ),
            # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
            create_table_variant=True,
        )
        profile = {**user["profile"], "id": user["id"]}
        print(profile)
        yield dlt.mark.with_hints(
            item=use_id(profile),
            hints=dlt.mark.make_hints(
                table_name=Table.PROFILES.value,
                primary_key="id",
                merge_key="id",
                write_disposition="merge",
            ),
            # needs to be a variant due to https://github.com/dlt-hub/dlt/pull/2109
            create_table_variant=True,
        )


@dlt.source(name="slack")
def source(limit=-1) -> Sequence[DltResource]:
    person_list = users()
    if limit > 0:
        person_list = person_list.add_limit(limit)

    return person_list | user_details()


__all__ = ["source"]
