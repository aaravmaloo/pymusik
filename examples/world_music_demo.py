from pymusik.composition.pattern import Pattern
from pymusik.instruments.folk import Sitar, Duduk, Bagpipes, HurdyGurdy, Banjo, Ukulele, Mandolin
from pymusik.instruments.percussion import Tabla, Conga, Bongo, Shaker, Tambourine
from pymusik.instruments.organ import Harmonium
from pymusik.engine.audio_graph import Song


def main():
    print("=== World Music Demo ===")

    song = Song(name="Global Rhythms", bpm=100)

    # Indian section: Sitar + Tabla + Harmonium
    sitar = song.create_track("Sitar", Sitar())
    sitar.set_pattern(Pattern(["C4", "D4", "E4", "G4", "A4", "G4", "E4", "D4"], loop=True, length_beats=8.0))
    sitar.gain = 0.5

    tabla = song.create_track("Tabla", Tabla())
    tabla.set_pattern(Pattern(["C2", "D2", "C2", None, "D2", "C2", None, "C2"], loop=True, length_beats=8.0))
    tabla.gain = 0.5

    harmonium = song.create_track("Harmonium", Harmonium())
    harmonium.set_pattern(Pattern(["C3", "E3", "G3", "C3"], loop=True, length_beats=8.0))
    harmonium.gain = 0.35

    # Armenian/Middle Eastern: Duduk
    duduk = song.create_track("Duduk", Duduk())
    duduk.set_pattern(Pattern(["D4", "F4", "G4", "A4", "G4", "F4", "D4", None], loop=True, length_beats=8.0))
    duduk.gain = 0.4

    # Celtic: Bagpipes + HurdyGurdy
    pipes = song.create_track("Bagpipes", Bagpipes())
    pipes.set_pattern(Pattern(["A4", "B4", "C5", "A4"], loop=True, length_beats=8.0))
    pipes.gain = 0.3

    gurdy = song.create_track("HurdyGurdy", HurdyGurdy())
    gurdy.set_pattern(Pattern(["D4", "G4", "A4", "D4"], loop=True, length_beats=8.0))
    gurdy.gain = 0.35

    # Latin: Conga + Bongo + Shaker + Tambourine
    conga = song.create_track("Conga", Conga())
    conga.set_pattern(Pattern(["C3", None, "C3", "D3", "C3", None, "C3", None], loop=True, length_beats=8.0))
    conga.gain = 0.45

    bongo = song.create_track("Bongo", Bongo())
    bongo.set_pattern(Pattern([None, "C4", None, "C4", None, "C4", None, "D4"], loop=True, length_beats=8.0))
    bongo.gain = 0.4

    shaker = song.create_track("Shaker", Shaker())
    shaker.set_pattern(Pattern(["C5", "C5", "C5", "C5"], loop=True, length_beats=4.0))
    shaker.gain = 0.25

    tamb = song.create_track("Tambourine", Tambourine())
    tamb.set_pattern(Pattern(["C5", None, "C5", None], loop=True, length_beats=4.0))
    tamb.gain = 0.25

    # American folk: Banjo + Mandolin + Ukulele
    banjo = song.create_track("Banjo", Banjo())
    banjo.set_pattern(Pattern(["G4", "C5", "D5", "G4", "B4", "D5", "G4", "C5"], loop=True, length_beats=8.0))
    banjo.gain = 0.4

    mandolin = song.create_track("Mandolin", Mandolin())
    mandolin.set_pattern(Pattern(["D4", "G4", "B4", "G4"], loop=True, length_beats=4.0))
    mandolin.gain = 0.35

    uke = song.create_track("Ukulele", Ukulele())
    uke.set_pattern(Pattern(["C4", "E4", "G4", "C4"], loop=True, length_beats=4.0))
    uke.gain = 0.35

    print("Rendering world_music_demo.wav...")
    song.render("world_music_demo.wav")
    print("Done!")


if __name__ == "__main__":
    main()
