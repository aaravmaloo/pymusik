from .core.pitch import Note, Pitch, Scale
from .core.time import TimeContext
from .composition.pattern import Pattern
from .composition.chord import Chord
from .engine.audio_graph import Song, Track
from .engine.renderer import Renderer

from .instruments.synth import SynthInstrument
from .instruments.piano import PianoInstrument
from .instruments.drums import DrumInstrument
from .instruments.phonk import PhonkCowbell, Bass808, DarkPad
from .instruments.lofi import GuitarInstrument, SaxInstrument, VinylEffect, MellowPiano
from .instruments.pro import AcidBass, ProDrums, SuperSawLead, HyperPluck, AnalogLead, AtmosphericStrings
from .instruments.strings import Violin, Viola, Cello, Contrabass, Harp
from .instruments.brass import Trumpet, Trombone, FrenchHorn, Tuba
from .instruments.woodwinds import Flute, Piccolo, Clarinet, Oboe, Bassoon, Recorder
from .instruments.percussion import Timpani, Marimba, Xylophone, Vibraphone, Gong, Tambourine, Shaker, Conga, Bongo, Tabla
from .instruments.organ import PipeOrgan, HammondOrgan, Accordion, Harmonium
from .instruments.bass import FretlessBass, UprightBass, SubBass, WobbleBass
from .instruments.electronic import TB303, SupersawPad, WavetableLead, FMBass, TranceGate, ChiptuneLead, ChiptuneBass
from .instruments.folk import Banjo, Mandolin, Ukulele, Sitar, Duduk, Bagpipes, HurdyGurdy
from .instruments.keys import Clavinet, Celesta, Glockenspiel, MusicBox, Rhodes
from .instruments.choir import ChoirPad, VocalOoh, VocalAah

__version__ = "0.2.0"
