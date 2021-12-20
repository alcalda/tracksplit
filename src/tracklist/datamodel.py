#!/usr/bin/env python
import re
import logging
from typing import Optional
from datetime import timedelta
from datetime import datetime
from dataclasses import dataclass


DATEFMT = "%Y-%m-%d"
re_tl = r"^(?:\[(?P<Time>(?:[0-9]{1,2}):[0-5][0-9])\] )?(?:(?P<Number>\d*)\. )?(?P<Artist>.*) - (?P<Title>.*?)(?: \[(?P<Label>.*)\])?$"
pat = re.compile(re_tl, flags=re.RegexFlag.MULTILINE)


@dataclass
class Track:
    Title: str
    Artist: str
    Number: Optional[int] = None
    StartTime: Optional[timedelta] = None
    # StartTime: Optional[str] = None


@dataclass
class Disc:
    Title: str
    Genre: Optional[list[str]] = None
    Tracks: Optional[list[Track]] = None
    Year: Optional[datetime] = None

    @classmethod
    def from_tracklist(cls, fn: str):
        logger = logging.getLogger()
        with open(fn) as fh:
            line = fh.readline().rstrip("\r\n")
            disc = Disc(
                Title=(parts := line.rpartition(" "))[0],
                Year=datetime.strptime(parts[-1], DATEFMT),
            )
            fh.readline()
            disc.Tracks = [
                Track(
                    Title=m.groupdict().get("Title"),
                    Artist=m.groupdict().get("Artist"),
                    Number=idx,
                    StartTime=datetime.strptime(m.groupdict().get("Time"), "%M:%S") - datetime(1900, 1, 1),
                    # StartTime=m.groupdict().get("Time"),
                )
                for idx, m in enumerate(pat.finditer(fh.read()), start=1)
            ]
            return disc


if __name__ == "__main__":
    d = Disc.from_tracklist("res/PDM - SLAM.txt")
