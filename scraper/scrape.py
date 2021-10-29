import os
from dataclasses import dataclass
from datetime import datetime

import bs4
import requests


@dataclass
class Record:
    timestamp: datetime
    occupancy: int
    remaining: int
    ratio: float


def request_html() -> str:
    """Returns the HTML from the FacilityOccupancy API"""
    url = "https://recshop.ohio.edu/FacilityOccupancy/GetFacilityData"
    data = {
        "facilityId": "caf740dd-8722-4b9d-84de-073706aa2450",
        "occupancyDisplayType": "00000000-0000-0000-0000-000000004489",
    }
    r = requests.post(url, data)
    html = r.text
    return html


def process_html(html: str) -> bs4.Tag:
    """Extracts the tag element with occupancy data from html"""
    soup = bs4.BeautifulSoup(html, "html.parser")
    tag = soup.canvas
    return tag


def extract() -> bs4.Tag:
    """Returns a tag element with occupancy data"""
    html = request_html()
    tag = process_html(html)
    return tag


def transform(tag: bs4.Tag, timestamp: datetime) -> Record:
    """Transforms a tag element into a Record"""
    occupancy = int(tag["data-occupancy"])
    remaining = int(tag["data-remaining"])
    ratio = float(tag["data-ratio"])
    record = Record(timestamp, occupancy, remaining, ratio)
    return record


def load(record: Record) -> None:
    """POSTs record data to the app API"""
    url = os.environ["API_ENDPOINT"]
    data = {
        "timestamp": record.timestamp.isoformat(),
        "occupancy": record.occupancy,
        "remaining": record.remaining,
        "ratio": record.ratio,
    }
    requests.post(url, json=data)


if __name__ == "__main__":
    tag = extract()
    timestamp = datetime.now()
    record = transform(tag, timestamp)
    load(record)
