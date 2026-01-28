# pymusik Usage Guide 🎵

Welcome to `pymusik`, a code-first engine for high-fidelity music production. This guide explains how to move beyond basic synthesis to create "real" sounding music.

## How it Fits Together

1.  **`Song`**: The global container. It manages the BPM (tempo) and the main timeline.
2.  **`Track`**: A single instrument layer. You can have unlimited tracks (e.g., Drums, Bass, Lead, Chords).
3.  **`Instrument`**: The sound source. Each track needs one.
4.  **`Pattern`**: The musical instructions (notes and rests) for a track.
5.  **`Renderer`**: The engine that sums all tracks, applies global effects (like Sidechain and Saturation), and renders the final audio.

---

## Instrument Guide

### Foundation
- **`ProDrums`**: A high-impact, saturated drum kit.
  - *Tip*: Use `sidechain=True` on other tracks to make the kick slam.
- **`Bass808`**: Heavy sub-bass with harmonic grit.
- **`AcidBass`**: Resonant sawtooth bass with filter sweeps.

### Atmosphere & Texture
- **`VinylEffect`**: Generates high-fidelity background crackle and noise.
- **`MellowPiano`**: A dreamy Rhodes-style electric piano.
- **`DarkPad`**: Deep, detuned atmospheric textures.

### Leads & Strings
- **`GuitarInstrument`**: Physical modeling of acoustic strings.
- **`SaxInstrument`**: Soulful sax with procedural vibrato.
- **`SuperSawLead`**: Wide, detuned dance leads.
- **`HyperPluck`**: Fast, percussive synth for rhythmic arpeggios.

---

## Achieving "Real" Music (Pro Tips)

### 1. The Pumping Effect (Sidechain)
In modern production, the "pumping" feel is essential.
```python
track = song.create_track("Bass", AcidBass())
track.sidechain = True  # The song will now duck when the kick hits
```

### 2. Humanization
- **Velocity Jitter**: Vary the `velocity` of your notes (e.g., `0.7` instead of `1.0`).
- **Timing Jitter**: (Coming in next update) Slight offsets in note positions.

### 3. Harmonic Layering
Don't just play one note. Layer a `MellowPiano` chord with a `DarkPad` texture to create a "thick" professional sound.

### 4. Frequency Management
Use the internal **Master Limiter**. The renderer automatically saturates and limits the audio so you can push your track's volume without digital clipping (crackling).

---

## Example: The Perfect Mix
```python
from pymusik import Song, ProDrums, AcidBass, MellowPiano

song = Song(bpm=124)

# Layer 1: Drums
drums = song.create_track("Drums", ProDrums())

# Layer 2: Pumping Bass
bass = song.create_track("Bass", AcidBass())
bass.sidechain = True # Crucial for that professional feel

# Layer 3: Atmospheric Chords
keys = song.create_track("Keys", MellowPiano())
keys.gain = 0.4
```
