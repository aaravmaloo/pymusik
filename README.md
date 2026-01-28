# pymusik

A production-grade Python library for modular music synthesis, algorithmic composition, and offline rendering. 

built for programmers, researchers, and audio engineers who want to create music entirely through code.

## Core Features

- **Sample-Accurate DSP**: NumPy-powered synthesis engine for deterministic, high-quality audio.
- **Declarative Composition**: Expressive API for notes, scales, chords, and patterns.
- **Modular Instruments**: Procedural synths, physical modeling pianos, and drum synthesis.
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
| `filters` | LowPass | Butterworth filters for spectrum shaping. |
| `effects` | Distortion, Delay, Chorus | Signal processing for grit, space, and width. |

### Included Instruments

| Instrument | Type | Characteristics |
| :--- | :--- | :--- |
| `SynthInstrument` | Subtractive | Flexible oscillators + ADSR + LPF. |
| `PianoInstrument` | Physical Model | Karplus-Strong string synthesis. |
| `DrumInstrument` | Procedural | Mathematical kick, snare, and hi-hat synthesis. |
| `PhonkCowbell` | Procedural | Iconic Memphis-style detuned square cowbells. |
| `Bass808` | Hybrid | Low-frequency sine fundamental with harmonic distortion. |
| `AcidBass` | Resonant | Sawtooth with filter envelope sweeps (303-style). |
| `ProDrums` | High-Fi | Saturated kicks and snares for professional impact. |

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

### 3. Advanced Phonk Demo (808s & Cowbells)
```python
from pymusik.instruments.phonk import PhonkCowbell, Bass808
# ... setup song ...
bell = song.create_track("Cowbell", PhonkCowbell())
bass = song.create_track("808", Bass808())
# ... add patterns ...
song.render("phonk_drift.wav")
```

### 4. Pro Hi-Fi Mixing (Sidechaining & Saturation)
```python
# Enable sidechain ducking on any track
bass_track.sidechain = True 

# The Renderer automatically applies:
# - Beat-synced volume ducking
# - Master soft-saturation and limiting
song.render("pro_mix.wav")
```

---

## Project Structure
```text
pymusik/
├── core/          # Pitch, Time, Events
├── composition/   # Pattern, Chord, Progression
├── synthesis/     # Oscillators, Envelopes, Filters
├── instruments/   # Synth, Piano, Drums, Phonk
├── effects/       # Distortion, Reverb
├── engine/        # Renderer, AudioGraph
└── output/        # WAV, MIDI Export
```
