import textwrap
from dataclasses import dataclass, field
from datetime import timedelta
from typing import Optional


@dataclass
class CueTrack:
    track: int
    title: str
    performer: Optional[str] = None
    index: Optional[timedelta] = None

    def __str__(self):
        ret = ""
        ret += f"TRACK {self.track} AUDIO\n"
        ret += f"  TITLE \"{self.title}\"\n"
        ret += f"  PERFORMER \"{self.performer}\"\n"
        ret += f"  INDEX 01 \"{'{:0>8}'.format(str(self.index))}\"\n"
        return ret


@dataclass
class CueSheet:
    title: str
    rem: Optional[str] = None
    performer: Optional[str] = None
    file: Optional[str] = None
    tracks: Optional[CueTrack] = field(default_factory=list)

    def __str__(self):
        ret = f"{self.title}\n"
        ret += "\n".join(self.rem) if self.rem else ""
        ret += f"{self.performer}\n" if self.performer else ""
        ret += f"{self.file}\n" if self.file else ""
        for track in self.tracks:

            ret += textwrap.indent(str(track), "  ")
        return ret

    def write(self, fn: str):
        with open(fn, mode="w") as fh:
            fh.write(str(self))
