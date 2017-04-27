import cx_Freeze

cx_Freeze.setup(
    name = "Chicken Chaser HD",
    options = {"build.exe": {"packages": ["pygame"], "include_files": ["chicken_icon.png", "tractor_sprite.png", "chicken_sprite.png", "crash.wav", "squish.wav", "chicken_dance.wav", "blood.png", "fixedsys.ttf"]}},
    executables = [cx_Freeze.Executable("ChickenChaser.py")]
)
