# brewing

When brewing beer, the concentration of different ions in the water can make a significant difference to flavour. You can adjust these ions by adding salts that contains multiple ions.

Given a desired ppm of ions, this service will calculate how much of each salt is required to get as close to the desired concentration as possible.

app.py hosts an api for the brewing-frontend repo.

main.py hosts a local python gui

## Local Setup

`pip install guietta`

## Build

`pip install pyinstaller`
`sudo pyinstaller --onefile --windowed main.py `
