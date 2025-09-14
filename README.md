# Rom-Cleaner-Python-Script | !! WORKING ON GUI UPDATE !!

brief: Python script for cleaning ROM collections. Removes duplicates while keeping best versions based on region/build quality. USA-first priority, supports all systems (NES-Switch), 40+ file formats. Preview mode, cross-platform. Made for my overly large ROM collection. MIT license.
.............................................................................

Hello everyone! I made this script to clean up my own massive ROM collection (10,000+ games with tons of duplicates), and figured it might be useful for others dealing with the same problem. After spending way too much time manually sorting through “Game (USA).zip vs Game (Europe) (Rev 1).zip” files, I decided automating the whole process is definitely far simpler and am honestly surprised on the little tools we have for ROMset cleaning.

its a python script that carefully removes duplicate ROMs from your collection while preserving the best versions based on my own regional preference, build quality, and revision priority. 

# { Features } 

- By default USA-First Region Priority 🇺🇸

- Designed primarily for English speakers

- prioritizes USA releases by default

- Configurable region ranking (USA → Europe → UK → Others)

- Perfect for North American collectors who only want English ROMs

- Keeps your preferred language/region versions consistently
# Duplicate Detection 🙅‍♂️

- Groups ROMs by base game title (ignoring regional/version tags)

- Treats special editions as separate games (GameCube Edition, Virtual Console, Limited Run Games, etc.)

- Handles multi-disc games properly (keeps all discs of a set)
  
# Careful Version Ranking 🆚

Priority Order;
1. Special Editions GameCube Edition, Virtual Console)

2. Build Quality (Rev B/Rev 2 → Original → Rev A/Rev 1→ Beta → Alpha)

3. Region Preference (USA → Europe → UK → Others)

4. Version Numbers (Higher versions preferred)

# Conservative Approach 🛡️

- Maximum 2 ROMs per game: Best version + Original (if different)

- Preview mode by default 

- shows what will be deleted before doing it

- Special “Original + Rev B” rule

- keeps both if significantly different

- Multi-disc support

- never breaks up disc sets

# Supported Systems:

Works with all gaming systems and file formats

- Retro: NES, SNES, Genesis, Game Boy, N64, 
PlayStation 1-2

- Modern: GameCube, Wii, Nintendo Switch, PlayStation 3+

- Arcade: MAME (ZIP files)

- All formats: ROM files, disc images, compressed archives

File Extensions: `.nes`, `.smc`, `.iso`, `.zip`, `.7z`, `.chd`, `.wbfs`, `.nsp`, `.xci`, and 40+ more

# { How It Works } 

Example: Super Mario Bros Collection

Before:

```
Super Mario Bros. (USA).nes
Super Mario Bros. (USA) (Rev 1).nes  
Super Mario Bros. (Europe).nes
Super Mario Bros. (GameCube Edition) (USA).nes
Super Mario Bros. (Virtual Console) (USA).nes
```

After:

```
✅ Super Mario Bros. (USA) (Rev 1).nes  [KEEP - Best revision]
✅ Super Mario Bros. (USA).nes  [KEEP - Original + Rev pair]
✅ Super Mario Bros. (GameCube Edition) (USA).nes [KEEP - Special edition]
✅ Super Mario Bros. (Virtual Console) (USA).nes  [KEEP - Special edition]
❌ Super Mario Bros. (Europe).nes [REMOVE - USA preferred]
```

# Regional Priority Example 

```
❌ Contra (Europe).zip          [REMOVE]
❌ Contra (Japan).zip           [REMOVE] 
✅ Contra (USA).zip             [KEEP - USA priority]
```

# { Prerequisites & System Requirements }

- Python 3.6 or higher (check with `python --version` or `python3 --version`)

- Operating System: Windows, Mac, Linux, Android, or any system that runs Python

- Storage: Enough free space to backup your ROM collection (not necessary but recommended)

- Permissions: Read/write access to your ROM directories

# { !! Before You Start !! } 

1. BACKUP YOUR ROM COLLECTION - This script deletes files when enabled to TRUE 

2. Know your ROM directory path - You’ll need to edit this in the script

This is what you’ll need to change
Just one line at the top of the script:

```
ROM_DIR = '/path/to/your/roms' << UPDATE TO THE ROM DIRECTORY YOU WANT TO SCRAPE
```

3. Test on a small folder first - Try it on 10-20 ROMs before your full collection

4. Check Python installation - Run `python --version` in terminal/command prompt

# { Getting Python (if needed) ver 3.6+ }

- Windows: Download from [python.org](https://python.org) or Microsoft Store

- Mac: Use Homebrew (`brew install python3`) or download from python.org

- Linux: Usually pre-installed, or use your package manager (`sudo apt install python3`)

- Android: Install QPython 3 or Termux from Play Store

# { File System Access }

- Make sure Python can access your ROM directory
- On newer Android versions, you may need to grant storage permissions
- Windows users: avoid OneDrive/cloud synced folders during processing

# { ✅ Quick Start ✅ }

1. Download the Rom_Cleaner.py script in your preferred text editor (for android I recommend QPython3)

2. Edit the path at the top:
   
   ```python
   ROM_DIR = '/path/to/your/roms'  # Change this!
   ```
3. Run preview mode:
   
   ```bash
   python rom_cleaner.py
   ```
4. Run to review your results, then go back and edit the file again to enable deletion if satisfied:

   ```python
   DELETE_FILES = True  # Change this when ready to delete  roms
   ```
   
# { Customization }

Region Preferences:

```python
REGIONS = ['U', 'E', 'UK']  # USA → Europe → UK priority
REGIONS = ['J', 'U', 'E']   # Japan → USA → Europe priority
REGIONS = ['U']             # USA only
```

Example Output:

```
Action 52.zip
  [KEEP  ] 0.8MB - Action 52 (USA) (Rev B) (Unl).zip
    -> Reason: Best version
  [REMOVE] 0.8MB - Action 52 (USA) (Rev A) (Unl).zip
  [KEEP  ] 0.8MB - Action 52 (USA) (Unl).zip
    -> Reason: Original + Rev B pair

SUMMARY
========
Unique titles: 883
Total files: 1373 
After cleanup: 1156 files
Space saved: 54.4 MB
```

# { Safety Features }

-  Preview mode by default - never deletes without confirmation

- Detailed reasoning - explains why each ROM is kept/removed

-  Conservative logic - when in doubt, keeps the ROM

- Special edition protection - treats variants as separate games

- Multi-disc protection - never splits disc sets

 Perfect For :

- Large ROM collections with many duplicates

- Multi-region collectors who want consistent regional choices

- Quality-focused users who want the best version of each game

- Storage optimization without losing important variants

# { Tested Systems }

Successfully tested on:
- MAME up to SWITCH collections (5000+ ROMs)
- Multi-system RetroPie setups
- Android devices (QPython)
- Windows/Mac/Linux

# **⚠️ IMPORTANT ⚠️**
- Always backup your ROM collection before running with `DELETE_FILES = True`

License: - Free to use and modify
Please enjoy :)
