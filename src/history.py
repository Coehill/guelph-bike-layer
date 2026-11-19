"""Keep the gap counts of every compare run.

Each live comparison appends one line to data/history.jsonl: the date, which
OSM data it saw, and the counts from the summary. That is the whole record of
the observer -- a handful of numbers a week -- and gaps/history.html charts it.
A run that fell back to cached OSM observed nothing new and is not recorded,
so the chart never shows a false plateau.

The parks layer can rebuild its past from Overpass attic queries; this one
deliberately cannot. An attic query for every road and path in Guelph is a heavy
ask of a shared instance for each week reconstructed, so the record starts
with the first weekly build and grows from there.
"""


import requests

from layerkit import history as _kit

from src import config

FIELDS = ("work", "new", "missing", "says_no", "nosep", "nobike",
          "unsigned_route", "lane_absent_km", "lane_no_km", "recent_gap_km",
          "city_km")


def record(summary, day=None):
    """Append the run's row (replacing an earlier row from the same day)."""
    return _kit.record(summary, FIELDS, path=config.HISTORY_PATH, seed=seed,
                       day=day)


def load():
    """All rows, oldest first. An absent file is an empty history."""
    return _kit.load(config.HISTORY_PATH)


def seed():
    """Start a checkout that has no history from the published copy."""
    return _kit.seed(config.HISTORY_PATH, config.HISTORY_URL, config.USER_AGENT)


def _write(rows):
    _kit.write(config.HISTORY_PATH, rows)
