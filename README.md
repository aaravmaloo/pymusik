# pymusik

A production-grade Python library for modular music synthesis, algorithmic composition, and offline rendering.

built for programmers, researchers, and audio engineers who want to create music entirely through code.

## Core Features

- **Sample-Accurate DSP**: NumPy-powered synthesis engine for deterministic, high-quality audio.
- **Declarative Composition**: Expressive API for notes, scales, chords, and patterns.
- **50+ Instruments**: Orchestral strings, brass, woodwinds, world instruments, electronic synths, and more.
- **Professional Output**: Direct rendering to WAV (32-bit float/16-bit PCM) and MIDI export.

---

## Technical Documentation

### Core Components

| Class | Description | Key Parameters |
| :--- | :--- | :--- |
| `Note` | Single musical event | `pitch`, `duration` (beats), `velocity` (0-1) |
| `Scale` | Musical scale generator | `root`, `scale_type` (major, minor, phrygian, etc.) |
| `Chord` | Harmonic collection | `root`, `chord_type` (maj7, min7, etc.), `octave` |
| `Pattern` | Sequence of events | `elements`, `loop`, `length_beats` |
| `Song` | Global composition | `name`, `bpm`, `sample_rate`, `duration_beats` |

### Synthesis Engine

| Module | Components | Description |
| :--- | :--- | :--- |
| `oscillators` | Sine, Saw, Square, Noise | Mathematical waveform generators with phase maintenance. |
| `envelopes` | ADSR | Attack, Decay, Sustain, Release curves. |
| `filters` | LowPass, HighPass, BandPass | Butterworth filters for spectrum shaping. |
| `effects` | Distortion, Reverb, Delay, Chorus | Signal processing for grit, space, and width. |

---

## Included Instruments (50+)

### Strings
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `Violin` | Harmonic + Vibrato | Bright, expressive with fast vibrato. |
| `Viola` | Harmonic + Vibrato | Warmer than violin, slightly slower vibrato. |
| `Cello` | Harmonic + Vibrato | Rich, warm low register with deep vibrato. |
| `Contrabass` | Harmonic + Vibrato | Deep fundamental with slow, subtle vibrato. |
| `Harp` | Karplus-Strong | Plucked string with long sustain and gentle decay. |
| `GuitarInstrument` | Karplus-Strong | Acoustic guitar with low-pass warmth. |
| `AtmosphericStrings` | Detuned Ensemble | Lush pad with ensemble detuning and noise floor. |

### Brass
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `Trumpet` | Harmonic + Breath | Bright, piercing with overtone series and breath noise. |
| `Trombone` | Harmonic | Rich mid-range with strong low harmonics. |
| `FrenchHorn` | Harmonic + LPF | Warm, mellow tone with heavy low-pass filtering. |
| `Tuba` | Harmonic + LPF | Deep, powerful bass brass. |

### Woodwinds
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `Flute` | Harmonic + Vibrato + Breath | Pure, airy tone with gentle vibrato. |
| `Piccolo` | Harmonic + HPF | High, bright flute with extended upper range. |
| `Clarinet` | Odd Harmonics | Hollow, woody tone emphasizing odd harmonics. |
| `Oboe` | Harmonic | Reed-like double-reed character. |
| `Bassoon` | Harmonic + LPF | Deep, reedy low woodwind. |
| `Recorder` | Harmonic + Breath | Simple, breathy end-blown flute. |
| `SaxInstrument` | Harmonic + Vibrato + LPF | Soulful sax with procedural vibrato. |

### Keys & Mallets
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `PianoInstrument` | Karplus-Strong | Physical model piano with natural decay. |
| `MellowPiano` | Sine + Triangle + Tremolo | Dreamy Rhodes-style electric piano. |
| `Rhodes` | Sine + Triangle + Bell | Classic electric piano with bell overtones and tremolo. |
| `Clavinet` | Harmonic + Pluck | Funky, percussive Hohner-style keyboard. |
| `Celesta` | Harmonic + Decay | Bell-like keyboard with shimmering decay. |
| `Glockenspiel` | High Harmonic | Bright, metallic mallet instrument. |
| `MusicBox` | Harmonic + Tine | Delicate, nostalgic with tine attack noise. |
| `Marimba` | Harmonic + Decay | Warm, resonant wooden mallet instrument. |
| `Xylophone` | High Harmonic + Decay | Bright, sharp wooden bars. |
| `Vibraphone` | Harmonic + Tremolo | Metallic bars with motor-driven tremolo. |

### Percussion
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `DrumInstrument` | Procedural | Basic kick, snare, hi-hat synthesis. |
| `ProDrums` | Saturated Procedural | High-impact saturated drums for professional mixes. |
| `Timpani` | Pitched + Noise | Orchestral kettle drum with pitch envelope. |
| `Gong` | Inharmonic + Noise | Rich, complex metallic with long sustain. |
| `Tambourine` | Noise + HPF | Jingly percussion with high-frequency emphasis. |
| `Shaker` | Noise + HPF | High-frequency rhythmic shaker. |
| `Conga` | Pitched + Noise | Afro-Cuban hand drum with pitch sweep. |
| `Bongo` | Pitched + Noise | High-pitched hand drum with fast pitch envelope. |
| `Tabla` | Pitched + Harmonic | Indian hand drum with complex harmonic decay. |

### Organ
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `PipeOrgan` | Full Harmonic Drawbars | Cathedral-style with 9 harmonic drawbars. |
| `HammondOrgan` | Drawbars + Rotary | Classic B3 with rotary speaker simulation. |
| `Accordion` | Harmonic + Tremolo | Bellows-driven with characteristic tremolo. |
| `Harmonium` | Harmonic + Drone | Reed organ with drone and warm low-pass. |

### Bass
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `Bass808` | Sine + Distortion | Heavy sub-bass with harmonic grit. |
| `AcidBass` | Saw + Filter Sweep | Resonant sawtooth with filter envelope (303-style). |
| `FretlessBass` | Harmonic + Glide | Smooth, singing bass with pitch glide. |
| `UprightBass` | Karplus-Strong | Acoustic double bass with warm low-pass. |
| `SubBass` | Sine + LPF | Ultra-low sine fundamental for sub-heavy mixes. |
| `WobbleBass` | Saw + LFO Filter | Dubstep-style wobble with LFO-driven filter sweeps. |

### Electronic
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `SynthInstrument` | Subtractive | Flexible oscillators + ADSR + LPF. |
| `SuperSawLead` | 7-Voice Detuned | Wide, detuned dance lead. |
| `HyperPluck` | Sine + Harmonic | Fast, percussive synth for rhythmic arpeggios. |
| `AnalogLead` | Saw + VCO Drift | Warm lead with simulated analog oscillator drift. |
| `TB303` | Saw + Filter Env | Faithful acid bass with resonant filter sweeps. |
| `SupersawPad` | 7-Voice Detuned Pad | Huge, wide supersaw pad with slow envelope. |
| `WavetableLead` | Morphing Sine/Saw | Wavetable-style morphing between waveforms. |
| `FMBass` | FM Synthesis | Frequency modulation bass with decaying mod index. |
| `TranceGate` | Saw + Gate | Gated supersaw for trance arpeggios. |
| `ChiptuneLead` | PWM Square | 8-bit lead with pulse-width modulation. |
| `ChiptuneBass` | Saw 8-bit | Retro game bass with fast envelope. |
| `PhonkCowbell` | Detuned Square | Iconic Memphis-style detuned square cowbells. |
| `DarkPad` | Detuned Sine + LFO | Deep, detuned atmospheric textures. |

### Folk & World
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `Banjo` | Karplus-Strong + LPF | Bright, fast-decay 5-string banjo. |
| `Mandolin` | Double-Course K-S | Paired strings with slight detune for chorus. |
| `Ukulele` | Karplus-Strong + LPF | Warm, mellow plucked island sound. |
| `Sitar` | Karplus-Strong + Buzz | Indian string with sympathetic buzz harmonics. |
| `Duduk` | Harmonic + Vibrato + Breath | Armenian reed with wide vibrato and breath. |
| `Bagpipes` | Harmonic + Drone | Celtic drone instrument with constant bass. |
| `HurdyGurdy` | Harmonic + Drone + Buzz | Cranked string instrument with drone and buzz. |

### Vocal & Pads
| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `ChoirPad` | Detuned Ensemble + BPF | Lush, wide choir pad with formant filtering. |
| `VocalOoh` | Harmonic + Formants | "Ooh" vowel with formant resonances. |
| `VocalAah` | Harmonic + Formants | "Aah" vowel with rich formant spectrum. |
| `VinylEffect` | Noise + Pops | High-fidelity vinyl crackle and pop texture. |

---

## Quick Start

### 1. Installation
```bash
pip install pymusik
```

### 2. Basic Usage
```python
from pymusik.core.pitch import Note
from pymusik.composition.pattern import Pattern
from pymusik.instruments.piano import PianoInstrument
from pymusik.engine.audio_graph import Song

# Initialize song
song = Song(bpm=120)

# Create a piano melody
piano = song.create_track("Piano", PianoInstrument())
melody = Pattern(["C4", "E4", "G4", "B4"], loop=True, length_beats=4.0)
piano.set_pattern(melody)

# Render
song.render("output.wav")
```

### 3. Orchestral Composition
```python
from pymusik.instruments.strings import Violin, Cello
from pymusik.instruments.brass import FrenchHorn
from pymusik.instruments.woodwinds import Flute

song = Song(bpm=72)
violin = song.create_track("Violin", Violin())
cello = song.create_track("Cello", Cello())
horn = song.create_track("Horn", FrenchHorn())
flute = song.create_track("Flute", Flute())
# ... add patterns ...
song.render("orchestral.wav")
```

### 4. Electronic Production (Sidechaining & Saturation)
```python
from pymusik.instruments.electronic import TB303, SupersawPad
from pymusik.instruments.bass import WobbleBass
from pymusik.instruments.pro import ProDrums

song = Song(bpm=128)
drums = song.create_track("Drums", ProDrums())
acid = song.create_track("Acid", TB303())
acid.sidechain = True  # Duck when kick hits
wobble = song.create_track("Wobble", WobbleBass())
wobble.sidechain = True
pad = song.create_track("Pad", SupersawPad())
song.render("banger.wav")
```

### 5. World Music
```python
from pymusik.instruments.folk import Sitar, Duduk
from pymusik.instruments.percussion import Tabla, Conga
from pymusik.instruments.organ import Harmonium

song = Song(bpm=100)
sitar = song.create_track("Sitar", Sitar())
tabla = song.create_track("Tabla", Tabla())
duduk = song.create_track("Duduk", Duduk())
song.render("world.wav")
```

### 6. Pro Hi-Fi Mixing (Sidechaining & Saturation)
```python
# Enable sidechain ducking on any track
bass_track.sidechain = True 

# The Renderer automatically applies:
# - Beat-synced volume ducking
# - Master soft-saturation and limiting
song.render("pro_mix.wav")
```

---

## Examples

| File | Description |
| :--- | :--- |
| `demo.py` | Basic synth + piano + drums techno track |
| `drum_example.py` | Drum pattern showcase |
| `phonk_demo.py` | Phonk cowbell + 808 bass |
| `heavy_phonk.py` | Heavy phonk production |
| `lofi_demo.py` | Lo-fi chill with vinyl, mellow piano, guitar |
| `production_master.py` | Professional mixing techniques |
| `ultimate_showcase.py` | Full instrument showcase |
| `orchestral_demo.py` | Full orchestra: strings, brass, woodwinds, timpani |
| `electronic_showcase.py` | TB303, FM bass, wobble, supersaw, chiptune |
| `world_music_demo.py` | Sitar, tabla, duduk, bagpipes, congas, banjo |
| `jazz_ensemble.py` | Rhodes, upright bass, trumpet, sax, clavinet |

---

## Project Structure
```text
pymusik/
├── core/          # Pitch, Time, Events, Constants
├── composition/   # Pattern, Chord, Progression
├── synthesis/     # Oscillators, Envelopes, Filters (LP/HP/BP)
├── instruments/   # 50+ instruments across 11 modules
│   ├── base.py        # Instrument ABC
│   ├── synth.py       # SynthInstrument
│   ├── piano.py       # PianoInstrument
│   ├── drums.py       # DrumInstrument
│   ├── phonk.py       # PhonkCowbell, Bass808, DarkPad
│   ├── lofi.py        # Guitar, Sax, Vinyl, MellowPiano
│   ├── pro.py         # AcidBass, ProDrums, SuperSawLead, etc.
│   ├── strings.py     # Violin, Viola, Cello, Contrabass, Harp
│   ├── brass.py       # Trumpet, Trombone, FrenchHorn, Tuba
│   ├── woodwinds.py   # Flute, Piccolo, Clarinet, Oboe, Bassoon, Recorder
│   ├── percussion.py  # Timpani, Marimba, Xylophone, Vibraphone, Gong, etc.
│   ├── organ.py       # PipeOrgan, HammondOrgan, Accordion, Harmonium
│   ├── bass.py        # FretlessBass, UprightBass, SubBass, WobbleBass
│   ├── electronic.py  # TB303, SupersawPad, WavetableLead, FM, Chiptune, etc.
│   ├── folk.py        # Banjo, Mandolin, Ukulele, Sitar, Duduk, Bagpipes, etc.
│   ├── keys.py        # Clavinet, Celesta, Glockenspiel, MusicBox, Rhodes
│   └── choir.py       # ChoirPad, VocalOoh, VocalAah
├── effects/       # Distortion, Reverb, Delay, Chorus
├── engine/        # Renderer, AudioGraph
└── output/        # WAV, MIDI Export
```
