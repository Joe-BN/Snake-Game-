The code runs from a file structure as shown in the README.md file.(though the __pycache__ creates its self along with scores.db)

The [executable](https://github.com/Joe-BN/Snake-Game-/releases/) can be downloaded and played no code experience required 😄

This command compiles the game (for windows) and makes sure it runs as a single .exe file (run while in the main directory of the game files)
```bash
$ pyinstaller --onefile --add-data "sounds;sounds" --add-data "images;images" game.py
```

after compiling, there will be some new folders, but the only one you need to know about is: ```dist/``` coz that's where the ```game.exe``` file is located

For more info on the compiling process you could always check out the [manual](https://pyinstaller.org/en/stable/)

Feel free to customize the script and executable