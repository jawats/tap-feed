"""Feed tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_feed.streams import (
    FeedStream,
)

STREAM_TYPES = [
    FeedStream,
]


class TapFeed(Tap):
    """TapFeed class."""

    name = "tap-feed"

    config_jsonschema = th.PropertiesList(
        th.Property(
            "feed_urls",
            th.ArrayType(th.StringType),
            required=True,
            description="A list of one or more feed paths.",
        ),
        th.Property(
            "feed_fields",
            th.ArrayType(th.StringType),
            default=["title", "subtitle"],
            description="A list of field level data fields to capture.",
        ),
        th.Property(
            "feed_entry_fields",
            th.ArrayType(th.StringType),
            default=["id", "title", "summary", "link"],
            description="A list of entry level data fields to capture.",
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
