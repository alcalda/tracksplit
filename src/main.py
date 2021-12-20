import logging

from src.cuesheet import CueSheet, CueTrack
from src.tracklist.datamodel import Disc


def write_cuesheet(fn: str):
    FORMAT = '%(message)s'
    logging.basicConfig(format=FORMAT)
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    disc = Disc.from_tracklist(fn)

    cuesheet = CueSheet(title=disc.Title)

    for it in disc.Tracks:
        track = CueTrack(track=it.Number, title=it.Title)
        track.performer = it.Artist
        track.index = it.StartTime
        cuesheet.tracks.append(track)

    cuesheet.write("gen/PDM - SLAM.cue")


if __name__ == "__main__":
    write_cuesheet("res/PDM - SLAM.txt")