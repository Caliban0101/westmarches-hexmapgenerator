# Hex Map Generator - West Marches Campaign Tool (CustomTkinter Edition)

A modern desktop application with a sleek dark theme for generating hex-based exploration maps for D&D West Marches style campaigns.

## ✨ CustomTkinter Version Features

This version uses **CustomTkinter** for a modern, polished user interface with:
- 🎨 **Dark theme** optimized for long sessions
- 🔘 **Modern widgets** with smooth animations
- 📱 **Better scaling** on high-DPI displays
- 🎯 **Improved UX** with clearer visual hierarchy

## Features

- **Dynamic Map Generation** with intelligent terrain continuity
- **Standard Biomes**: Ocean, Coastal, Plains, Forest, Hills, Mountains, Swamp, Desert, Tundra
- **Grimdark Biomes**: Blighted Lands, Corrupted Forest, Shadowlands, Deadlands, Cursed Wastes, Abyssal Depths
  - Grimdark biomes automatically appear on the opposite side of the map from your starting location
- **Configurable Map Size** during map creation (10x10 to 50x50 hexes)
- **Custom Factions** - Name your own factions that will populate settlements
- **Custom Locations** - Add your own points of interest
- **Fog of War** - Click hexes to reveal/hide explored status
- **Save/Load Maps** - Export and import maps as JSON files
- **Notes System** - Add campaign notes to individual hexes

## Installation & Running

### Option 1: Run the Python Script Directly

**Requirements:**
- Python 3.7 or higher
- CustomTkinter library

**Steps:**
1. Install CustomTkinter:
   ```bash
   pip install customtkinter
   ```
   
2. Navigate to the folder containing `hex_map_generator.py`

3. Run the application:
   ```bash
   python hex_map_generator.py
   ```

### Option 2: Install from Requirements File

```bash
pip install -r requirements.txt
python hex_map_generator.py
```

### Option 3: Create a Standalone .EXE File

**Requirements:**
- Python 3.7 or higher
- PyInstaller
- CustomTkinter

**Steps:**

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install pyinstaller
   ```

2. **Use the build script** (Windows)
   ```bash
   build.bat
   ```
   
   Or manually:
   ```bash
   pyinstaller --onefile --windowed --name "HexMapGenerator" hex_map_generator.py
   ```

3. **Find your executable**
   - The .exe file will be in the `dist` folder
   - `dist/HexMapGenerator.exe`

### Building Options

- `--onefile`: Creates a single .exe file (slower startup, easier distribution)
- `--windowed`: Hides the console window (GUI apps only)
- `--name`: Sets the name of the output executable
- `--icon`: Adds a custom icon (you'll need to provide an .ico file)

## How to Use

### 1. Main Menu
- **📍 New Map**: Start creating a new hex map
- **📂 Load Map**: Import a previously saved map (JSON file)
- **⚙ Settings**: Configure hex size and display options

### 2. Map Setup
- **Map Size**: Set the width and height (10-50 hexes each)
- **Starting Direction**: Choose where your players start (North, South, East, West)
  - Grimdark biomes will appear on the opposite side
- **Factions**: Add custom faction names (e.g., "Red Hand", "Silver Circle")
  - These will be randomly assigned to settlements
- **Custom Locations**: Add your own points of interest
  - These will be randomly placed on the map alongside default POIs
- Click **▶ Generate Map** to create your world

### 3. Map View
- **Interactive Canvas**: Click on any hex to select it
  - Use **👁 Reveal Selected** button to mark a hex as explored
  - Use **🔒 Hide Selected** button to mark a hex as unexplored
  - Explored hexes show terrain colors and symbols
  - Unexplored hexes appear dark gray
- **Legend**: Shows all terrain types and their colors
- **Notes Panel**: 
  - Displays hex details (coordinates, terrain, settlements, POIs)
  - Add custom notes for each hex
  - Save notes with the **💾 Save Notes** button
- **💾 Export**: Save your map as a JSON file for later use

### 4. Settings
- **Hex Size**: Adjust the size of hexes (15-50 pixels) using a slider
- **Show Grid Lines**: Toggle hex borders
- **Show Coordinates**: Display coordinate numbers on hexes

## Map Features

### Terrain Continuity
The generator uses a cluster-based system with weighted compatibility to ensure natural terrain transitions:
- Biomes form coherent clusters of 5-12 hexes
- Forests transition through hills and plains before becoming deserts
- Mountains cluster together and connect through hills
- Grimdark biomes form corrupted regions opposite the starting area

### Settlements
- Automatically placed in habitable terrain (plains, forests, coastal, hills)
- Avoided in hostile terrain (oceans, grimdark zones)
- Named with your custom factions (or generic names)
- Types include: Village, Town, Outpost, Fort, Keep, Hamlet
- Starting location gets a City

### Points of Interest
- Mix of standard fantasy locations (ruins, caves, towers, shrines)
- Grimdark POIs in corrupted regions (cursed altars, demon gates, bone pits)
- Your custom locations randomly integrated

## File Format

Maps are saved as JSON files with the following structure:
```json
{
  "grid": [...],
  "width": 25,
  "height": 20,
  "start_direction": "W",
  "factions": ["Red Hand", "Silver Circle"],
  "custom_locations": ["The Crying Tower"],
  "created_at": "2025-01-01T12:00:00"
}
```

Each hex contains:
- `terrain`: Biome type
- `explored`: Whether players have revealed this hex
- `settlement`: Settlement data (if present)
- `poi`: Point of interest data (if present)
- `notes`: Custom campaign notes

## Tips for West Marches Campaigns

1. **Start Small**: Begin with a 15x15 or 20x20 map, you can always generate a larger one later
2. **Use the Notes System**: Track important discoveries, rumors, or quest hooks for each location
3. **Toggle Fog of War**: Only reveal hexes as players explore them using the Reveal/Hide buttons
4. **Export Regularly**: Save your map after each session to track player progress
5. **Custom Content**: Add your campaign's unique factions and locations before generating
6. **Grimdark Zones**: Use these as endgame content - deadly areas far from civilization

## Differences from Standard Version

The CustomTkinter edition includes:
- ✅ Modern dark-themed UI
- ✅ Scrollable frames for better organization
- ✅ Smoother widget interactions
- ✅ Better button styling and visual feedback
- ✅ Slider-based hex size adjustment
- ✅ Improved text display with CTkTextbox

## Troubleshooting

**"No module named 'customtkinter'" error:**
```bash
pip install customtkinter
```

**CustomTkinter installation fails:**
- Ensure you have Python 3.7+
- Try: `pip install --upgrade pip` then retry

**Executable won't run:**
- Ensure all dependencies are installed before building
- Try the `--onefile` build
- Check Windows Defender/antivirus isn't blocking it

**Map looks too small/large:**
- Adjust hex size in Settings before generating
- Or regenerate with different map dimensions

## Dependencies

- **Python 3.7+**
- **customtkinter** >= 5.2.0

## License

This tool is free to use and modify for your campaigns.

## Credits

Created for D&D West Marches campaigns - explore, survive, and map the wilderness!

**CustomTkinter** by Tom Schimansky - https://github.com/TomSchimansky/CustomTkinter
