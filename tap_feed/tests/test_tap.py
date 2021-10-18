"""Tests tap configuration that is used in other parts of the code base"""

import pytest
from singer_sdk.tap_base import Tap

from tap_feed.tap import TapFeed

SAMPLE_CONFIG = {
    "feed_urls": ["http://feeds.feedburner.com/PythonSoftwareFoundationNews"],
}


class TestConfigJsonSchema:
    """Test suite verifying the config_jsonschema attribute"""

    def test_property_names(self):
        """Verify the property names are the values used elsewhere in the code base"""
        test_tap: Tap = TapFeed(config=SAMPLE_CONFIG)
        expected_properties = [
            "feed_urls",
            "feed_fields",
            "feed_entry_fields",
            "start_date",
        ]
        assert (
            list(test_tap.config_jsonschema["properties"].keys()) == expected_properties
        )

    def test_required_field_feed_urls(self):
        """Verifies an exception is thrown if the feed_urls property is not provided"""
        with pytest.raises(RuntimeError) as excinfo:
            test_tap: Tap = TapFeed()
            print(test_tap.config_jsonschema)

        assert "'feed_urls' is a required property" in str(excinfo.value)

    @pytest.mark.parametrize(
        "property_name,expected_default",
        [
            ("feed_fields", ["title", "subtitle"]),
            ("feed_entry_fields", ["id", "title", "summary", "link"]),
        ],
    )
    def test_default_values(self, property_name, expected_default):
        """Verifies the default values for the json schema properties"""
        test_tap: Tap = TapFeed(config=SAMPLE_CONFIG)
        assert (
            test_tap.config_jsonschema["properties"][property_name]["default"]
            == expected_default
        )


def test_stream_discovery():
    """Verifies the correct stream is discovered by the tap"""
    test_tap: Tap = TapFeed(config=SAMPLE_CONFIG)
    streams_discovered = test_tap.discover_streams()
    assert len(streams_discovered) == 1
    assert streams_discovered[0].name == "feed"
