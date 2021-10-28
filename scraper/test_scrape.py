from datetime import datetime

import bs4
import requests

import scrape

TIMESTAMP = datetime.now()


def test_request_html(monkeypatch):
    class MockResponse:
        text = "<html></html>"

    def mock_post(url, data):
        return MockResponse()

    monkeypatch.setattr(requests, "post", mock_post)

    html = scrape.request_html()

    assert html == "<html></html>"


def test_process_html():
    html = (
        '<canvas data-occupancy="25" data-ratio="0.25" data-remaining="100"></canvas>'
    )
    tag = scrape.process_html(html)

    assert tag["data-occupancy"] == "25"
    assert tag["data-remaining"] == "100"
    assert tag["data-ratio"] == "0.25"


def test_transform():
    tag = bs4.Tag(
        name="canvas",
        attrs={"data-occupancy": "25", "data-remaining": "100", "data-ratio": "0.25"},
    )
    record = scrape.transform(tag, TIMESTAMP)

    assert record.timestamp == TIMESTAMP
    assert record.occupancy == 25
    assert record.remaining == 100
    assert record.ratio == 0.25


def test_load(monkeypatch):
    def mock_post(url, data):
        assert data["timestamp"] == TIMESTAMP
        assert data["occupancy"] == 25
        assert data["remaining"] == 100
        assert data["ratio"] == 0.25

    monkeypatch.setattr(requests, "post", mock_post)

    record = scrape.Record(TIMESTAMP, 25, 100, 0.25)
    scrape.load(record)
