 
import os
import sys
import re
from datetime import datetime

# EDIT THESE SETTINGS
ROM_DIR = '/path/to/your/roms'  # << Change this to your ROM folder
REGIONS = ['U', 'E', 'UK']  # Preferred region order: *CHANGEABLE* U=USA, E=Europe, UK=United Kingdom, J=Japan, etc. 
DELETE_FILES = False # Change to True when ready to delete duplicates

# Country codes for region ranking
COUNTRY_CODES = {
    'As': 'Asia', 'A': 'Australia', 'B': 'Brazil', 'C': 'Canada', 'Ch': 'China',
    'D': 'Netherlands', 'E': 'Europe', 'F': 'France', 'Fn': 'Finland', 
    'G': 'Germany', 'Gr': 'Greece', 'Hk': 'Hong Kong', 'I': 'Italy',
    'J': 'Japan', 'K': 'Korea', 'Nl': 'Netherlands', 'No': 'Norway',
    'R': 'Russia', 'S': 'Spain', 'Sw': 'Sweden', 'U': 'USA', 
    'UK': 'United Kingdom', 'W': 'World', 'Unl': 'Unlicensed', 
    'PD': 'Public Domain', 'Unk': 'Unknown'
}

# Release quality ranking (best to worst) - Updated for your preferences
RELEASE_CODES = ['gamecube edition', '!', 'rev b', 'rev 2', 'rev', 'alternate', 'alt', 'v', 'o', 
                'rev a', 'rev 1', 'beta', 'proto', 'alpha', 'promo', 'pirate', 'demo', 
                'sample', 'bootleg', 'b', 'virtual console']

class ROMAnalyzer:
    def __init__(self, rom_path):
        self.full_path = rom_path
        self.filename = os.path.basename(rom_path)
        self.filesize = os.path.getsize(rom_path) if os.path.exists(rom_path) else 0
        self.stripped_name = self._strip_filename()
        self.tags = self._extract_tags()
        
    def _strip_filename(self):
        """Remove everything in parentheses and brackets to get base game name, but keep special editions"""
        # First, identify special editions that should be treated as separate games
        special_editions = [
            'gamecube edition', 'virtual console', 'limited run games', 'iam8bit', 
            'capcom town', 'capcom classics', 'konami collector', 'namco museum',
            'disney classic games', 'aladdin compact cartridge', 'nintendo power'
        ]
        
        # Extract all tags first
        tags = []
        matches = re.findall(r'[\[\(]([^[\]()]+)[\]\)]', self.filename)
        for match in matches:
            tag_list = [tag.strip() for tag in match.split(',')]
            tags.extend(tag_list)
        
        # Check if this ROM has special edition tags
        special_edition_tags = []
        for tag in tags:
            for special in special_editions:
                if special.lower() in tag.lower():
                    special_edition_tags.append(tag)
                    break
        
        # Remove all parentheses content
        stripped = re.sub(r'[\[\(].*?[\]\)]', '', self.filename).strip()
        stripped = re.sub(r'\s+\.', '.', stripped)  # Clean up spaces before extension
        
        # Add back special edition info to make it a unique game title
        if special_edition_tags:
            special_part = ' - ' + ' + '.join(special_edition_tags)
            # Insert before the file extension
            name_part, ext = os.path.splitext(stripped)
            stripped = name_part + special_part + ext
        
        return stripped
    
    def _extract_tags(self):
        """Extract all tags from parentheses and brackets"""
        tags = []
        # Find content in parentheses and brackets
        matches = re.findall(r'[\[\(]([^[\]()]+)[\]\)]', self.filename)
        for match in matches:
            # Split by comma and clean up
            tag_list = [tag.strip() for tag in match.split(',')]
            tags.extend(tag_list)
        return tags
    
    def get_filesize_mb(self):
        """Return file size in MB"""
        return self.filesize / (1024.0 ** 2)
    
    def get_regions(self):
        """Get region codes from tags"""
        regions = []
        for tag in self.tags:
            # Check each tag against all country codes
            if tag in COUNTRY_CODES:
                regions.append(tag)
            # Also check if tag contains the region code
            elif 'USA' in tag:
                regions.append('U')
            elif 'Europe' in tag:
                regions.append('E')
            elif 'United Kingdom' in tag:
                regions.append('UK')
        
        return regions if regions else ['Unk']
    
    def get_build_rank(self):
        """Rank ROM by build quality (higher number = better quality)"""
        build_score = 50  # Default score for unknown builds
        version = float('inf')
        
        # Check all tags for build information
        for tag in self.tags:
            tag_lower = tag.lower()
            
            # Special handling for GameCube Edition (highest priority)
            if 'gamecube edition' in tag_lower or 'gamecube' in tag_lower:
                return (100, version)  # Highest possible score
            
            # Check for revision patterns
            for i, code in enumerate(RELEASE_CODES):
                if code in tag_lower:
                    build_score = 100 - i  # Higher score for better builds
                    # Try to extract version number
                    version_match = re.search(r'(\d+\.?\d*)', tag)
                    if version_match:
                        try:
                            version = float(version_match.group(1))
                        except:
                            version = 0
                    break
        
        return (build_score, version)
    
    def get_region_rank(self, preferred_regions):
        """Rank ROM by region preference (higher score = better)"""
        rom_regions = self.get_regions()
        
        # USA gets highest priority
        if 'U' in rom_regions:
            return 100  # Highest score for USA
        elif 'E' in rom_regions:
            return 90   # Second highest for Europe
        elif 'UK' in rom_regions:
            return 85   # Third for UK
        elif 'W' in rom_regions:
            return 80   # World versions
        elif 'A' in rom_regions:
            return 75   # Australia (English)
        elif 'C' in rom_regions:
            return 70   # Canada (English)
        else:
            return 10   # Other regions get low score
    
    def get_disc_number(self):
        """Extract disc/volume number if present"""
        for tag in self.tags:
            # Look for patterns like "Disk 1", "Disc 2", "Side A", etc.
            match = re.search(r'(disk|disc|side|volume)\s+(\w+)', tag.lower())
            if match:
                disc_part = match.group(2)
                if disc_part.isdigit():
                    return int(disc_part)
                else:
                    # Handle letters (A=1, B=2, etc.)
                    return ord(disc_part[0].upper()) - ord('A') + 1
        return 0
    
    def is_multi_disc_set(self, other_rom):
        """Check if this ROM is part of the same multi-disc set as another ROM"""
        if self.get_disc_number() == 0 or other_rom.get_disc_number() == 0:
            return False
        
        # Check if base names are the same (ignoring disc info)
        self_tags_no_disc = [tag for tag in self.tags if not re.search(r'(disk|disc|side|volume)', tag.lower())]
        other_tags_no_disc = [tag for tag in other_rom.tags if not re.search(r'(disk|disc|side|volume)', tag.lower())]
        
        return (self.stripped_name == other_rom.stripped_name and 
                set(self_tags_no_disc) == set(other_tags_no_disc))
    
    def is_revision_pair(self, other_rom):
        """Check if this ROM and another are an original + Rev B pair that should both be kept"""
        if self.stripped_name != other_rom.stripped_name:
            return False
        
        # Get build info for both
        self_build = self.get_build_rank()
        other_build = other_rom.get_build_rank()
        
        # Check if one is original (high score, no specific revision) and other is Rev B
        self_tags_lower = [tag.lower() for tag in self.tags]
        other_tags_lower = [tag.lower() for tag in other_rom.tags]
        
        self_has_rev_b = any('rev b' in tag or 'rev 2' in tag for tag in self_tags_lower)
        other_has_rev_b = any('rev b' in tag or 'rev 2' in tag for tag in other_tags_lower)
        
        self_is_original = not any(rev in tag for tag in self_tags_lower for rev in ['rev', 'beta', 'alpha', 'proto', 'sample'])
        other_is_original = not any(rev in tag for tag in other_tags_lower for rev in ['rev', 'beta', 'alpha', 'proto', 'sample'])
        
        # Keep both if one is original and other is Rev B
        return (self_is_original and other_has_rev_b) or (other_is_original and self_has_rev_b)

def scan_roms(rom_directory):
    """Scan directory for ROM files"""
    rom_files = []
    # Comprehensive list of ROM and game file extensions
    valid_extensions = {
        # Classic console ROMs
        '.nes', '.fds', '.nsf',  # Nintendo (NES/Famicom)
        '.smc', '.sfc', '.fig',  # Super Nintendo
        '.md', '.gen', '.smd', '.bin', '.32x',  # Sega Genesis/32X
        '.gg', '.sms',  # Game Gear/Master System
        '.gb', '.gbc', '.gba',  # Game Boy family
        '.n64', '.z64', '.v64',  # Nintendo 64
        '.nds', '.3ds', '.cia',  # Nintendo DS/3DS
        '.gcm', '.iso', '.rvz', '.wbfs', '.wia',  # GameCube/Wii
        '.nsp', '.xci',  # Nintendo Switch
        
        # Sony consoles
        '.cue', '.bin', '.chd', '.pbp', '.img',  # PlayStation 1
        '.iso', '.cso',  # PlayStation 1/2/PSP
        '.pkg', '.rap',  # PlayStation 3
        
        # Sega systems
        '.cdi', '.gdi',  # Dreamcast
        '.cue', '.iso',  # Saturn
        
        # Arcade
        '.zip', '.7z',  # MAME/Arcade (often zipped)
        
        # Compressed formats (universal)
        '.rar', '.tar', '.gz', '.bz2',
        
        # Disc images
        '.mdf', '.mds', '.nrg', '.ccd', '.sub',
        
        # Cartridge dumps
        '.rom', '.a78', '.lnx', '.vec', '.int',
        
        # Modern formats
        '.xbe',  # Xbox
        '.dol', '.elf',  # GameCube homebrew
    }
    
    print(f"Scanning: {rom_directory}")
    
    if not os.path.exists(rom_directory):
        print(f"ERROR: Directory not found: {rom_directory}")
        return []
    
    for root, dirs, files in os.walk(rom_directory):
        # Skip common non-ROM directories
        dirs[:] = [d for d in dirs if d.lower() not in ['images', 'videos', 'manuals', 'saves', 
                                                        'screenshots', 'artwork', 'cheats', 'docs']]
        
        for file in files:
            # Skip system/metadata files
            if any(file.lower().startswith(skip) for skip in ['systeminfo', 'desktop.ini', '.ds_store', 'thumbs.db']):
                continue
                
            if any(file.lower().endswith(ext) for ext in valid_extensions):
                full_path = os.path.join(root, file)
                rom_files.append(ROMAnalyzer(full_path))
    
    print(f"Found {len(rom_files)} ROM files")
    return rom_files

def group_roms_by_title(rom_list):
    """Group ROMs by their base title"""
    groups = {}
    for rom in rom_list:
        title = rom.stripped_name
        if title not in groups:
            groups[title] = []
        groups[title].append(rom)
    return groups

def analyze_and_clean(rom_directory, preferred_regions, delete_mode=False):
    """Main function to analyze and optionally clean ROM collection"""
    
    # Scan for ROMs
    all_roms = scan_roms(rom_directory)
    if not all_roms:
        print("No ROM files found!")
        return
    
    # Group by title
    rom_groups = group_roms_by_title(all_roms)
    
    total_files = 0
    total_size = 0
    kept_size = 0
    deleted_count = 0
    
    print("\n" + "="*60)
    print("ROM ANALYSIS RESULTS")
    print("="*60)
    
    for title, roms in sorted(rom_groups.items()):
        if len(roms) > 1:  # Only show titles with duplicates
            print(f"\n{title}")
            
            # Sort ROMs by quality (best first)
            # CRITICAL: Region ranking must come FIRST to ensure USA priority
            sorted_roms = sorted(roms, key=lambda x: (
                x.get_region_rank(preferred_regions),    # REGION FIRST (USA=100, E=90, etc.)
                x.get_build_rank()[0],                    # Then build quality
                x.get_build_rank()[1],                    # Then version number
                -x.get_disc_number()                      # Then disc number
            ), reverse=True)
            
            kept_roms = []
            
            for i, rom in enumerate(sorted_roms):
                should_keep = False
                reason = ""
                
                if i == 0:
                    # Always keep the best ROM
                    should_keep = True
                    reason = "Best version"
                    kept_roms.append(rom)
                else:
                    # Check if it's part of a multi-disc set
                    is_multi_disc = any(rom.is_multi_disc_set(kept_rom) for kept_rom in kept_roms)
                    if is_multi_disc:
                        should_keep = True
                        reason = "Multi-disc set"
                        kept_roms.append(rom)
                    else:
                        # Only allow one original + one Rev B pair maximum
                        # Check if we already have 2 ROMs (original + revision)
                        if len(kept_roms) < 2:
                            # Check if it's an original + Rev B pair
                            is_revision_pair = any(rom.is_revision_pair(kept_rom) for kept_rom in kept_roms)
                            if is_revision_pair:
                                should_keep = True
                                reason = "Original + Rev B pair"
                                kept_roms.append(rom)
                
                status = "KEEP" if should_keep else "REMOVE"
                region_info = f"({', '.join(rom.get_regions())})" if rom.get_regions() != ['Unk'] else ""
                
                print(f"  [{status:6}] {rom.get_filesize_mb():.1f}MB - {rom.filename}")
                if should_keep and reason:
                    print(f"    -> Reason: {reason}")
                
                # Statistics
                total_files += 1
                total_size += rom.get_filesize_mb()
                
                if should_keep:
                    kept_size += rom.get_filesize_mb()
                else:
                    # Delete file if in delete mode
                    if delete_mode:
                        try:
                            os.remove(rom.full_path)
                            print(f"    -> DELETED: {rom.full_path}")
                            deleted_count += 1
                        except Exception as e:
                            print(f"    -> ERROR deleting {rom.full_path}: {e}")
        else:
            # Single ROM, always keep
            rom = roms[0]
            total_files += 1
            total_size += rom.get_filesize_mb()
            kept_size += rom.get_filesize_mb()
    
    # Summary
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Unique titles: {len(rom_groups)}")
    print(f"Total files: {total_files}")
    print(f"Total size: {total_size:.1f} MB")
    print(f"After cleanup: {kept_size:.1f} MB")
    print(f"Space saved: {total_size - kept_size:.1f} MB")
    
    if delete_mode:
        print(f"Files deleted: {deleted_count}")
        print("Cleanup completed!")
    else:
        print("\nNO FILES DELETED (Preview mode)")
        print("To delete duplicates, change DELETE_FILES to True")

# Run the analysis
if __name__ == "__main__":
    print("Android ROM Cleaner - USA PRIORITY + REVISION LOGIC")
    print("="*50)
    print(f"ROM Directory: {ROM_DIR}")
    print(f"Preferred Regions: USA > Europe > UK > Others")
    print(f"Revision Priority: GameCube Edition > Rev B > Original > Rev A")
    print(f"Special Rule: Keep both Original + Rev B versions")
    print(f"Delete Mode: {'ON' if DELETE_FILES else 'OFF (Preview only)'}")
    print()
    
    # Safety check
    if DELETE_FILES:
        print("WARNING: Delete mode is ON!")
        print("This will permanently delete ROM files!")
        print("Make sure you have backups!")
        print()
    
    analyze_and_clean(ROM_DIR, REGIONS, DELETE_FILES)
