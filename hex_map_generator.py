"""
Hex Map Generator for West Marches D&D Campaigns (CustomTkinter Edition)
A modern desktop application for generating hex-based exploration maps
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import tkinter as tk
import json
import math
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional

# Set CustomTkinter appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Terrain types with colors and symbols
STANDARD_TERRAINS = {
    'PLAINS': {'name': 'Plains', 'color': '#86efac', 'symbol': '·', 'grimdark': False},
    'FOREST': {'name': 'Forest', 'color': '#166534', 'symbol': '♠', 'grimdark': False},
    'HILLS': {'name': 'Hills', 'color': '#a16207', 'symbol': '∩', 'grimdark': False},
    'MOUNTAINS': {'name': 'Mountains', 'color': '#78716c', 'symbol': '▲', 'grimdark': False},
    'SWAMP': {'name': 'Swamp', 'color': '#4d7c0f', 'symbol': '≋', 'grimdark': False},
    'DESERT': {'name': 'Desert', 'color': '#fbbf24', 'symbol': '∴', 'grimdark': False},
    'TUNDRA': {'name': 'Tundra', 'color': '#e0f2fe', 'symbol': '❄', 'grimdark': False},
    'LAKE': {'name': 'Lake', 'color': '#3b82f6', 'symbol': '~', 'grimdark': False},
}

GRIMDARK_TERRAINS = {
    'BLIGHTED': {'name': 'Blighted Lands', 'color': '#3f1f3f', 'symbol': '☠', 'grimdark': True},
    'CORRUPTED': {'name': 'Corrupted Forest', 'color': '#1a1a2e', 'symbol': '†', 'grimdark': True},
    'SHADOWLANDS': {'name': 'Shadowlands', 'color': '#16213e', 'symbol': '◆', 'grimdark': True},
    'DEADLANDS': {'name': 'Deadlands', 'color': '#4a4a4a', 'symbol': '✝', 'grimdark': True},
    'CURSED': {'name': 'Cursed Wastes', 'color': '#5a1f5a', 'symbol': '⚠', 'grimdark': True},
    'ABYSSAL': {'name': 'Abyssal Depths', 'color': '#0d1117', 'symbol': '⚉', 'grimdark': True},
}

ALL_TERRAINS = {**STANDARD_TERRAINS, **GRIMDARK_TERRAINS}

# Biome progression rules
BIOME_TRANSITIONS = {
    'PLAINS': ['PLAINS', 'FOREST', 'HILLS', 'DESERT', 'SWAMP', 'LAKE', 'BLIGHTED'],
    'FOREST': ['FOREST', 'PLAINS', 'HILLS', 'SWAMP', 'LAKE', 'CORRUPTED'],
    'HILLS': ['HILLS', 'PLAINS', 'FOREST', 'MOUNTAINS', 'DESERT', 'DEADLANDS'],
    'MOUNTAINS': ['MOUNTAINS', 'HILLS', 'TUNDRA', 'SHADOWLANDS'],
    'SWAMP': ['SWAMP', 'FOREST', 'PLAINS', 'LAKE', 'CORRUPTED', 'CURSED'],
    'DESERT': ['DESERT', 'PLAINS', 'HILLS', 'CURSED'],
    'TUNDRA': ['TUNDRA', 'MOUNTAINS', 'DEADLANDS'],
    'LAKE': ['LAKE', 'PLAINS', 'FOREST', 'SWAMP'],
    'BLIGHTED': ['BLIGHTED', 'PLAINS', 'CORRUPTED', 'SHADOWLANDS', 'DEADLANDS', 'CURSED'],
    'CORRUPTED': ['CORRUPTED', 'FOREST', 'SWAMP', 'BLIGHTED', 'SHADOWLANDS', 'CURSED'],
    'SHADOWLANDS': ['SHADOWLANDS', 'MOUNTAINS', 'BLIGHTED', 'CORRUPTED', 'DEADLANDS'],
    'DEADLANDS': ['DEADLANDS', 'HILLS', 'TUNDRA', 'BLIGHTED', 'SHADOWLANDS', 'CURSED'],
    'CURSED': ['CURSED', 'DESERT', 'SWAMP', 'BLIGHTED', 'CORRUPTED', 'DEADLANDS'],
}

# POI Generation - Adjectives and Nouns by biome
POI_ADJECTIVES = {
    'PLAINS': ['Ancient', 'Forgotten', 'Hidden', 'Mysterious', 'Lost', 'Abandoned', 'Weathered', 'Crumbling', 'Sacred'],
    'FOREST': ['Verdant', 'Enchanted', 'Twisted', 'Overgrown', 'Mossy', 'Ancient', 'Shadowy', 'Whispering', 'Tangled'],
    'HILLS': ['Windswept', 'Rocky', 'Echoing', 'Lonely', 'Rugged', 'Steep', 'Towering', 'Ancient', 'Crumbling'],
    'MOUNTAINS': ['Frozen', 'Treacherous', 'Sky-Piercing', 'Snow-Capped', 'Perilous', 'Jagged', 'Lofty', 'Storm-Wracked'],
    'SWAMP': ['Fetid', 'Murky', 'Mist-Shrouded', 'Decaying', 'Stagnant', 'Poisonous', 'Sodden', 'Rotting', 'Reeking'],
    'DESERT': ['Scorched', 'Buried', 'Sun-Bleached', 'Desiccated', 'Windswept', 'Barren', 'Parched', 'Shifting', 'Miraging'],
    'TUNDRA': ['Frozen', 'Icy', 'Howling', 'Desolate', 'Bitter', 'Glacial', 'Frostbitten', 'Wind-Scoured'],
    'LAKE': ['Serene', 'Deep', 'Crystalline', 'Mist-Covered', 'Reflective', 'Tranquil', 'Sunken', 'Rippling'],
    'BLIGHTED': ['Cursed', 'Corrupted', 'Diseased', 'Withered', 'Accursed', 'Tainted', 'Plagued', 'Malevolent', 'Festering'],
    'CORRUPTED': ['Twisted', 'Dark', 'Corrupted', 'Malformed', 'Warped', 'Profane', 'Vile', 'Unholy', 'Defiled'],
    'SHADOWLANDS': ['Shadowy', 'Darkened', 'Umbral', 'Tenebrous', 'Gloomy', 'Shrouded', 'Pitch-Black', 'Nightmarish'],
    'DEADLANDS': ['Lifeless', 'Ashen', 'Barren', 'Skeletal', 'Deathly', 'Bone-Strewn', 'Macabre', 'Necrotic'],
    'CURSED': ['Hexed', 'Damned', 'Doomed', 'Forsaken', 'Accursed', 'Bewitched', 'Ill-Fated', 'Jinxed'],
}

POI_NOUNS = {
    'PLAINS': ['Ruins', 'Tower', 'Shrine', 'Stones', 'Monument', 'Cairn', 'Settlement', 'Battlefield', 'Outpost', 'Well'],
    'FOREST': ['Grove', 'Glade', 'Hollow', 'Circle', 'Tree', 'Path', 'Glen', 'Thicket', 'Bower', 'Dell'],
    'HILLS': ['Keep', 'Fort', 'Lookout', 'Cave', 'Mine', 'Warren', 'Barrow', 'Tumulus', 'Stronghold'],
    'MOUNTAINS': ['Peak', 'Pass', 'Cave', 'Mine', 'Monastery', 'Refuge', 'Aerie', 'Cavern', 'Grotto', 'Chasm'],
    'SWAMP': ['Bog', 'Fen', 'Marsh', 'Mire', 'Pool', 'Grove', 'Hut', 'Hovel', 'Shack', 'Hideout'],
    'DESERT': ['Oasis', 'Tomb', 'Temple', 'Pyramid', 'Ruins', 'Vault', 'Crypt', 'Shrine', 'Monument'],
    'TUNDRA': ['Cave', 'Shelter', 'Outpost', 'Cairn', 'Barrow', 'Tomb', 'Shrine', 'Monolith'],
    'LAKE': ['Island', 'Dock', 'Shipwreck', 'Grotto', 'Spring', 'Falls', 'Reef', 'Wreck'],
    'BLIGHTED': ['Altar', 'Site', 'Ground', 'Zone', 'Field', 'Pit', 'Scar', 'Wound', 'Blight'],
    'CORRUPTED': ['Tree', 'Grove', 'Circle', 'Shrine', 'Pool', 'Spring', 'Hollow', 'Heart'],
    'SHADOWLANDS': ['Portal', 'Gate', 'Rift', 'Void', 'Nexus', 'Well', 'Abyss', 'Chasm'],
    'DEADLANDS': ['Graveyard', 'Crypt', 'Ossuary', 'Barrow', 'Tomb', 'Grave', 'Boneyard', 'Mausoleum'],
    'CURSED': ['Circle', 'Ground', 'Altar', 'Stone', 'Monument', 'Site', 'Place', 'Nexus'],
}


class HexGrid:
    """Manages hex grid calculations and rendering"""
    
    @staticmethod
    def axial_to_pixel(q: int, r: int, hex_size: int) -> Tuple[float, float]:
        """Convert axial coordinates to pixel coordinates for rectangular grid with pointy-top hexes"""
        # Pointy-top hexes: columns offset by half hex height for proper meshing
        x = hex_size * math.sqrt(3) * q
        y = hex_size * 2 * r + (q % 2) * hex_size
        return x, y
    
    @staticmethod
    def get_hex_corners(x: float, y: float, size: int) -> List[Tuple[float, float]]:
        """Get the corner points of a hexagon (pointy-top orientation)"""
        corners = []
        for i in range(6):
            # Pointy-top hexes: start at 0 degrees (pointing right)
            angle = math.pi / 3 * i
            corner_x = x + size * math.cos(angle)
            corner_y = y + size * math.sin(angle)
            corners.append((corner_x, corner_y))
        return corners
    
    @staticmethod
    def get_neighbors(q: int, r: int) -> List[Tuple[int, int]]:
        """Get neighboring hex coordinates (aligned rectangular layout)"""
        # Aligned rectangular layout - all hexes use same neighbor pattern
        return [
            (q, r - 1), (q + 1, r - 1),
            (q - 1, r), (q + 1, r),
            (q - 1, r + 1), (q, r + 1)
        ]


class MapGenerator:
    """Handles map generation logic with improved biome clustering"""
    
    def __init__(self, width: int, height: int, start_dir: str, factions: List[str], custom_locations: List[str]):
        self.width = width
        self.height = height
        self.start_dir = start_dir
        self.factions = factions
        self.custom_locations = custom_locations
        self.grid = []
    
    def generate_poi_name(self, terrain: str) -> str:
        """Generate a POI name from adjectives and nouns based on terrain"""
        adjectives = POI_ADJECTIVES.get(terrain, POI_ADJECTIVES['PLAINS'])
        nouns = POI_NOUNS.get(terrain, POI_NOUNS['PLAINS'])
        
        adjective = random.choice(adjectives)
        noun = random.choice(nouns)
        
        return f"{adjective} {noun}"
    
    def get_opposite_direction(self) -> Tuple[int, int]:
        """Get the opposite quadrant from starting direction"""
        if self.start_dir == 'N':
            return (self.width // 2, self.height - 1)
        elif self.start_dir == 'S':
            return (self.width // 2, 0)
        elif self.start_dir == 'E':
            return (0, self.height // 2)
        else:  # W
            return (self.width - 1, self.height // 2)
    
    def distance_from_start(self, q: int, r: int, start_q: int, start_r: int) -> float:
        """Calculate distance from starting position"""
        return math.sqrt((q - start_q) ** 2 + (r - start_r) ** 2)
    
    def is_valid_transition(self, from_terrain: str, to_terrain: str) -> bool:
        """Check if a terrain transition is allowed"""
        return to_terrain in BIOME_TRANSITIONS.get(from_terrain, [])
    
    def generate_biome_cluster(self, start_q: int, start_r: int, terrain: str, min_size: int = 5) -> set:
        """Generate a cluster of at least min_size hexes of the same terrain"""
        cluster = set()
        cluster.add((start_q, start_r))
        
        # Different generation patterns based on terrain
        if terrain == 'MOUNTAINS':
            # Mountains form in linear ranges
            return self._generate_mountain_range(start_q, start_r, min_size)
        elif terrain in ['FOREST', 'SWAMP', 'LAKE']:
            # Forests, swamps, and lakes form in blobs (more clustered)
            return self._generate_blob(start_q, start_r, terrain, min_size)
        else:
            # Standard cluster generation for other terrains
            return self._generate_standard_cluster(start_q, start_r, min_size)
    
    def _generate_mountain_range(self, start_q: int, start_r: int, min_size: int) -> set:
        """Generate mountains in a linear range pattern"""
        cluster = set()
        cluster.add((start_q, start_r))
        
        # Pick a primary direction (vertical, horizontal, or diagonal)
        direction_type = random.choice(['horizontal', 'vertical', 'diagonal'])
        
        current_q, current_r = start_q, start_r
        length = random.randint(min_size, min_size + 5)
        
        for _ in range(length):
            # Move in the chosen direction with some variation
            if direction_type == 'horizontal':
                current_q += random.choice([-1, 0, 1])
                current_r += random.choice([0, 1]) if random.random() < 0.3 else 0
            elif direction_type == 'vertical':
                current_r += random.choice([-1, 0, 1])
                current_q += random.choice([0, 1]) if random.random() < 0.3 else 0
            else:  # diagonal
                current_q += random.choice([-1, 0, 1])
                current_r += random.choice([-1, 0, 1])
            
            # Keep within bounds
            current_q = max(0, min(self.width - 1, current_q))
            current_r = max(0, min(self.height - 1, current_r))
            
            cluster.add((current_q, current_r))
            
            # Add some width to the range occasionally
            if random.random() < 0.4:
                for nq, nr in HexGrid.get_neighbors(current_q, current_r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if random.random() < 0.5:
                            cluster.add((nq, nr))
        
        return cluster
    
    def _generate_blob(self, start_q: int, start_r: int, terrain: str, min_size: int) -> set:
        """Generate terrain in a blob pattern (more circular/organic)"""
        cluster = set()
        cluster.add((start_q, start_r))
        
        # Blobs are rounder and more cohesive
        target_size = random.randint(min_size, min_size + 8)
        expansion_chance = 0.8  # Higher expansion chance for blobs
        
        while len(cluster) < target_size:
            candidates = []
            for q, r in cluster:
                for nq, nr in HexGrid.get_neighbors(q, r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if (nq, nr) not in cluster:
                            # Prefer hexes closer to the center for rounder blobs
                            distance = abs(nq - start_q) + abs(nr - start_r)
                            weight = max(1, 10 - distance)
                            candidates.extend([(nq, nr)] * weight)
            
            if not candidates:
                break
            
            new_hex = random.choice(candidates)
            cluster.add(new_hex)
        
        # Extra expansion for very organic blobs
        while random.random() < expansion_chance and len(cluster) < target_size + 5:
            candidates = set()
            for q, r in cluster:
                for nq, nr in HexGrid.get_neighbors(q, r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if (nq, nr) not in cluster:
                            candidates.add((nq, nr))
            
            if not candidates:
                break
            
            new_hex = random.choice(list(candidates))
            cluster.add(new_hex)
            expansion_chance *= 0.75
        
        return cluster
    
    def _generate_standard_cluster(self, start_q: int, start_r: int, min_size: int) -> set:
        """Standard cluster generation for most terrains"""
        cluster = set()
        cluster.add((start_q, start_r))
        
        # Grow cluster to minimum size
        while len(cluster) < min_size:
            candidates = set()
            for q, r in cluster:
                for nq, nr in HexGrid.get_neighbors(q, r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if (nq, nr) not in cluster:
                            candidates.add((nq, nr))
            
            if not candidates:
                break
            
            new_hex = random.choice(list(candidates))
            cluster.add(new_hex)
        
        # Possibly expand beyond minimum size
        expansion_chance = 0.6
        while random.random() < expansion_chance:
            candidates = set()
            for q, r in cluster:
                for nq, nr in HexGrid.get_neighbors(q, r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if (nq, nr) not in cluster:
                            candidates.add((nq, nr))
            
            if not candidates:
                break
            
            new_hex = random.choice(list(candidates))
            cluster.add(new_hex)
            expansion_chance *= 0.7
        
        return cluster
    
    def generate(self) -> List[List[Dict]]:
        """Generate the complete map using cluster-based terrain generation"""
        self.grid = [[None for _ in range(self.width)] for _ in range(self.height)]
        
        # Determine starting position
        if self.start_dir == 'N':
            start_q, start_r = self.width // 2, 0
        elif self.start_dir == 'S':
            start_q, start_r = self.width // 2, self.height - 1
        elif self.start_dir == 'E':
            start_q, start_r = self.width - 1, self.height // 2
        else:  # W
            start_q, start_r = 0, self.height // 2
        
        # Calculate max distance for grimdark threshold
        max_distance = self.distance_from_start(*self.get_opposite_direction(), start_q, start_r)
        grimdark_threshold = max_distance * 0.6
        
        # Track which hexes have been assigned
        assigned = set()
        
        # Start with plains cluster at starting location
        plains_cluster = self.generate_biome_cluster(start_q, start_r, 'PLAINS', min_size=7)
        for q, r in plains_cluster:
            self.grid[r][q] = {
                'terrain': 'PLAINS',
                'poi': None,
                'settlement': None,
                'explored': True if (q, r) == (start_q, start_r) else False,
                'notes': ''
            }
            assigned.add((q, r))
        
        # Place large settlement at starting location
        faction = self.factions[0] if self.factions else 'Imperial'
        self.grid[start_r][start_q]['settlement'] = {
            'type': 'City',
            'name': f"{faction} City",
            'faction': faction
        }
        
        # Generate terrain clusters
        attempts = 0
        max_attempts = self.width * self.height * 3
        
        while len(assigned) < self.width * self.height and attempts < max_attempts:
            attempts += 1
            
            # Find an unassigned hex adjacent to assigned terrain
            border_hexes = []
            for q, r in assigned:
                for nq, nr in HexGrid.get_neighbors(q, r):
                    if 0 <= nq < self.width and 0 <= nr < self.height:
                        if (nq, nr) not in assigned:
                            border_hexes.append((nq, nr, self.grid[r][q]['terrain']))
            
            if not border_hexes:
                # No border hexes, pick a random unassigned hex
                unassigned = [(q, r) for q in range(self.width) for r in range(self.height) 
                             if (q, r) not in assigned]
                if not unassigned:
                    break
                seed_q, seed_r = random.choice(unassigned)
                
                # Determine if grimdark zone
                distance = self.distance_from_start(seed_q, seed_r, start_q, start_r)
                is_grimdark = distance > grimdark_threshold
                
                if is_grimdark:
                    new_terrain = random.choice(list(GRIMDARK_TERRAINS.keys()))
                else:
                    new_terrain = random.choice(list(STANDARD_TERRAINS.keys()))
            else:
                seed_q, seed_r, adjacent_terrain = random.choice(border_hexes)
                
                # Determine if grimdark zone
                distance = self.distance_from_start(seed_q, seed_r, start_q, start_r)
                is_grimdark = distance > grimdark_threshold
                
                # Choose terrain based on transitions and zone
                valid_transitions = BIOME_TRANSITIONS.get(adjacent_terrain, [])
                
                if is_grimdark:
                    # Filter for grimdark terrains
                    grimdark_options = [t for t in valid_transitions if t in GRIMDARK_TERRAINS]
                    if grimdark_options:
                        new_terrain = random.choice(grimdark_options)
                    else:
                        new_terrain = random.choice(list(GRIMDARK_TERRAINS.keys()))
                else:
                    # Filter for standard terrains
                    standard_options = [t for t in valid_transitions if t in STANDARD_TERRAINS]
                    if standard_options:
                        new_terrain = random.choice(standard_options)
                    else:
                        new_terrain = random.choice(list(STANDARD_TERRAINS.keys()))
            
            # Generate cluster
            cluster_size = random.randint(5, 12)
            cluster = self.generate_biome_cluster(seed_q, seed_r, new_terrain, min_size=cluster_size)
            
            # Assign terrain to cluster
            for q, r in cluster:
                if (q, r) not in assigned:
                    self.grid[r][q] = {
                        'terrain': new_terrain,
                        'poi': None,
                        'settlement': None,
                        'explored': False,
                        'notes': ''
                    }
                    assigned.add((q, r))
        
        # Fill any remaining hexes
        for r in range(self.height):
            for q in range(self.width):
                if (q, r) not in assigned:
                    # Use nearest neighbor's terrain
                    for nq, nr in HexGrid.get_neighbors(q, r):
                        if 0 <= nq < self.width and 0 <= nr < self.height:
                            if self.grid[nr][nq]:
                                self.grid[r][q] = {
                                    'terrain': self.grid[nr][nq]['terrain'],
                                    'poi': None,
                                    'settlement': None,
                                    'explored': False,
                                    'notes': ''
                                }
                                break
        
        self._place_settlements()
        self._place_pois()
        
        return self.grid
    
    def _place_settlements(self):
        """Place settlements on the map"""
        num_settlements = max(3, (self.width * self.height) // 50 + random.randint(0, 3))
        settlement_types = ['Village', 'Town', 'Outpost', 'Fort', 'Keep', 'Hamlet']
        
        placed = 0
        attempts = 0
        max_attempts = 1000
        
        while placed < num_settlements and attempts < max_attempts:
            attempts += 1
            q = random.randint(0, self.width - 1)
            r = random.randint(0, self.height - 1)
            
            if self.grid[r][q] and not self.grid[r][q]['settlement'] and not self.grid[r][q]['poi']:
                terrain = self.grid[r][q]['terrain']
                # Settlements prefer non-grimdark, habitable areas
                if terrain in ['PLAINS', 'FOREST', 'HILLS', 'LAKE'] and not ALL_TERRAINS[terrain]['grimdark']:
                    settlement_type = random.choice(settlement_types)
                    faction = random.choice(self.factions) if self.factions else None
                    
                    self.grid[r][q]['settlement'] = {
                        'type': settlement_type,
                        'name': f"{faction} {settlement_type}" if faction else settlement_type,
                        'faction': faction
                    }
                    placed += 1
    
    def _place_pois(self):
        """Place points of interest on the map - 50% chance per hex"""
        for r in range(self.height):
            for q in range(self.width):
                if not self.grid[r][q] or self.grid[r][q]['settlement']:
                    continue
                
                # 50% chance for each hex to have POI(s)
                if random.random() < 0.5:
                    terrain = self.grid[r][q]['terrain']
                    
                    # Determine number of POIs (1-3, weighted towards 1)
                    num_pois = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
                    
                    pois = []
                    for _ in range(num_pois):
                        # 30% chance to use custom location if available
                        if self.custom_locations and random.random() < 0.3:
                            poi_name = random.choice(self.custom_locations)
                        else:
                            # Generate procedural POI name
                            poi_name = self.generate_poi_name(terrain)
                        
                        pois.append(poi_name)
                    
                    # Store as single POI or list
                    if len(pois) == 1:
                        self.grid[r][q]['poi'] = {
                            'name': pois[0],
                            'type': 'poi'
                        }
                    else:
                        self.grid[r][q]['poi'] = {
                            'name': ', '.join(pois),
                            'type': 'multiple',
                            'count': len(pois)
                        }


class HexMapApp:
    """Main application class using CustomTkinter"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Hex Map Generator - West Marches")
        self.root.geometry("1200x800")
        
        # Application state
        self.current_screen = 'menu'
        self.map_data = None
        self.settings = {
            'hex_size': 25,
            'show_grid': True,
            'show_coordinates': False
        }
        self.setup_data = {
            'start_direction': 'W',
            'factions': [],
            'custom_locations': [],
            'map_width': 25,
            'map_height': 20
        }
        self.selected_hex = None
        
        # Create main container
        self.container = ctk.CTkFrame(root)
        self.container.pack(fill='both', expand=True)
        
        self.show_menu()
    
    def clear_screen(self):
        """Clear the current screen"""
        for widget in self.container.winfo_children():
            widget.destroy()
    
    def show_menu(self):
        """Display the main menu"""
        self.clear_screen()
        self.current_screen = 'menu'
        
        # Menu frame
        menu_frame = ctk.CTkFrame(self.container)
        menu_frame.place(relx=0.5, rely=0.5, anchor='center')
        
        # Title
        title = ctk.CTkLabel(
            menu_frame,
            text="Hex Map Generator",
            font=("Arial", 32, "bold")
        )
        title.pack(pady=(20, 10))
        
        subtitle = ctk.CTkLabel(
            menu_frame,
            text="West Marches Campaign Tool",
            font=("Arial", 14)
        )
        subtitle.pack(pady=(0, 30))
        
        # Buttons
        btn_new = ctk.CTkButton(
            menu_frame,
            text="📍 New Map",
            font=("Arial", 14, "bold"),
            height=50,
            width=300,
            command=self.show_setup
        )
        btn_new.pack(pady=10)
        
        btn_load = ctk.CTkButton(
            menu_frame,
            text="📂 Load Map",
            font=("Arial", 14, "bold"),
            height=50,
            width=300,
            command=self.load_map
        )
        btn_load.pack(pady=10)
        
        btn_settings = ctk.CTkButton(
            menu_frame,
            text="⚙ Settings",
            font=("Arial", 14, "bold"),
            height=50,
            width=300,
            command=self.show_settings
        )
        btn_settings.pack(padx=20, pady=(10, 20))
    
    def show_setup(self):
        """Display the map setup screen"""
        self.clear_screen()
        self.current_screen = 'setup'
        
        # Setup frame
        setup_frame = ctk.CTkFrame(self.container)
        setup_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Back button
        btn_back = ctk.CTkButton(
            setup_frame,
            text="← Back",
            width=80,
            command=self.show_menu
        )
        btn_back.pack(anchor='nw', pady=(0, 10))
        
        # Title
        title = ctk.CTkLabel(
            setup_frame,
            text="Map Setup",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Create a scrollable frame for the content
        scrollable_frame = ctk.CTkScrollableFrame(setup_frame, width=700, height=600)
        scrollable_frame.pack(fill='both', expand=True)
        
        # Map Size Section
        size_frame = ctk.CTkFrame(scrollable_frame)
        size_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        size_label = ctk.CTkLabel(
            size_frame,
            text="Map Size",
            font=("Arial", 14, "bold")
        )
        size_label.pack(pady=10)
        
        size_inner = ctk.CTkFrame(size_frame)
        size_inner.pack(fill='x', padx=20, pady=10)
        
        # Width
        width_frame = ctk.CTkFrame(size_inner)
        width_frame.pack(side='left', expand=True, fill='x', padx=10)
        
        ctk.CTkLabel(
            width_frame,
            text="Width (hexes):",
            font=("Arial", 11)
        ).pack(anchor='w')
        
        self.width_var = tk.IntVar(value=self.setup_data['map_width'])
        width_entry = ctk.CTkEntry(
            width_frame,
            textvariable=self.width_var,
            width=100
        )
        width_entry.pack(fill='x', pady=5)
        
        # Height
        height_frame = ctk.CTkFrame(size_inner)
        height_frame.pack(side='left', expand=True, fill='x', padx=10)
        
        ctk.CTkLabel(
            height_frame,
            text="Height (hexes):",
            font=("Arial", 11)
        ).pack(anchor='w')
        
        self.height_var = tk.IntVar(value=self.setup_data['map_height'])
        height_entry = ctk.CTkEntry(
            height_frame,
            textvariable=self.height_var,
            width=100
        )
        height_entry.pack(fill='x', pady=5)
        
        # Starting Direction
        dir_frame = ctk.CTkFrame(scrollable_frame)
        dir_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        dir_label = ctk.CTkLabel(
            dir_frame,
            text="Starting Direction",
            font=("Arial", 14, "bold")
        )
        dir_label.pack(pady=10)
        
        self.dir_var = tk.StringVar(value=self.setup_data['start_direction'])
        
        dir_buttons = ctk.CTkFrame(dir_frame)
        dir_buttons.pack(pady=10)
        
        directions = [('North', 'N'), ('South', 'S'), ('East', 'E'), ('West', 'W')]
        for text, value in directions:
            ctk.CTkRadioButton(
                dir_buttons,
                text=text,
                variable=self.dir_var,
                value=value
            ).pack(side='left', padx=10)
        
        # Factions
        faction_frame = ctk.CTkFrame(scrollable_frame)
        faction_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        faction_label = ctk.CTkLabel(
            faction_frame,
            text="Factions",
            font=("Arial", 14, "bold")
        )
        faction_label.pack(pady=10)
        
        faction_entry_frame = ctk.CTkFrame(faction_frame)
        faction_entry_frame.pack(fill='x', padx=20, pady=10)
        
        self.faction_entry = ctk.CTkEntry(
            faction_entry_frame,
            placeholder_text="Enter faction name",
            width=200
        )
        self.faction_entry.pack(side='left', padx=(0, 10))
        self.faction_entry.bind('<Return>', lambda e: self.add_faction())
        
        ctk.CTkButton(
            faction_entry_frame,
            text="Add",
            width=80,
            command=self.add_faction
        ).pack(side='left')
        
        # Create a frame for the listbox (using tkinter Listbox since CTk doesn't have one)
        listbox_frame = ctk.CTkFrame(faction_frame)
        listbox_frame.pack(fill='x', padx=20, pady=(0, 10))
        
        self.faction_listbox = tk.Listbox(
            listbox_frame,
            height=4,
            font=("Arial", 10)
        )
        self.faction_listbox.pack(fill='x')
        
        for faction in self.setup_data['factions']:
            self.faction_listbox.insert(tk.END, faction)
        
        ctk.CTkButton(
            faction_frame,
            text="Remove Selected",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.remove_faction
        ).pack(pady=5)
        
        # Custom Locations
        location_frame = ctk.CTkFrame(scrollable_frame)
        location_frame.pack(fill='x', pady=(0, 15), padx=10)
        
        location_label = ctk.CTkLabel(
            location_frame,
            text="Custom Locations",
            font=("Arial", 14, "bold")
        )
        location_label.pack(pady=10)
        
        location_entry_frame = ctk.CTkFrame(location_frame)
        location_entry_frame.pack(fill='x', padx=20, pady=10)
        
        self.location_entry = ctk.CTkEntry(
            location_entry_frame,
            placeholder_text="Enter location name",
            width=200
        )
        self.location_entry.pack(side='left', padx=(0, 10))
        self.location_entry.bind('<Return>', lambda e: self.add_location())
        
        ctk.CTkButton(
            location_entry_frame,
            text="Add",
            width=80,
            command=self.add_location
        ).pack(side='left')
        
        listbox_frame2 = ctk.CTkFrame(location_frame)
        listbox_frame2.pack(fill='x', padx=20, pady=(0, 10))
        
        self.location_listbox = tk.Listbox(
            listbox_frame2,
            height=4,
            font=("Arial", 10)
        )
        self.location_listbox.pack(fill='x')
        
        for location in self.setup_data['custom_locations']:
            self.location_listbox.insert(tk.END, location)
        
        ctk.CTkButton(
            location_frame,
            text="Remove Selected",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.remove_location
        ).pack(pady=5)
        
        # Generate button
        ctk.CTkButton(
            scrollable_frame,
            text="▶ Generate Map",
            font=("Arial", 16, "bold"),
            height=50,
            fg_color="green",
            hover_color="dark green",
            command=self.generate_map
        ).pack(pady=20)
    
    def add_faction(self):
        """Add a faction to the list"""
        faction = self.faction_entry.get().strip()
        if faction:
            self.setup_data['factions'].append(faction)
            self.faction_listbox.insert(tk.END, faction)
            self.faction_entry.delete(0, tk.END)
    
    def remove_faction(self):
        """Remove selected faction"""
        selection = self.faction_listbox.curselection()
        if selection:
            index = selection[0]
            self.faction_listbox.delete(index)
            self.setup_data['factions'].pop(index)
    
    def add_location(self):
        """Add a custom location to the list"""
        location = self.location_entry.get().strip()
        if location:
            self.setup_data['custom_locations'].append(location)
            self.location_listbox.insert(tk.END, location)
            self.location_entry.delete(0, tk.END)
    
    def remove_location(self):
        """Remove selected location"""
        selection = self.location_listbox.curselection()
        if selection:
            index = selection[0]
            self.location_listbox.delete(index)
            self.setup_data['custom_locations'].pop(index)
    
    def show_settings(self):
        """Display settings screen"""
        self.clear_screen()
        self.current_screen = 'settings'
        
        # Settings frame
        settings_frame = ctk.CTkFrame(self.container)
        settings_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Back button
        btn_back = ctk.CTkButton(
            settings_frame,
            text="← Back",
            width=80,
            command=self.show_menu
        )
        btn_back.pack(anchor='nw', pady=(0, 10))
        
        # Title
        title = ctk.CTkLabel(
            settings_frame,
            text="Settings",
            font=("Arial", 24, "bold")
        )
        title.pack(pady=(0, 20))
        
        # Content
        content = ctk.CTkFrame(settings_frame)
        content.pack(pady=20)
        
        # Hex size
        hex_size_frame = ctk.CTkFrame(content)
        hex_size_frame.pack(fill='x', pady=10, padx=20)
        
        ctk.CTkLabel(
            hex_size_frame,
            text="Hex Size (pixels):",
            font=("Arial", 12)
        ).pack(side='left', padx=10)
        
        hex_size_var = tk.IntVar(value=self.settings['hex_size'])
        hex_slider = ctk.CTkSlider(
            hex_size_frame,
            from_=15,
            to=50,
            variable=hex_size_var,
            width=200
        )
        hex_slider.pack(side='left', padx=10)
        
        hex_value_label = ctk.CTkLabel(
            hex_size_frame,
            text=str(self.settings['hex_size']),
            width=40
        )
        hex_value_label.pack(side='left')
        
        def update_hex_label(value):
            hex_value_label.configure(text=str(int(float(value))))
        
        hex_slider.configure(command=update_hex_label)
        
        # Show grid
        show_grid_var = tk.BooleanVar(value=self.settings['show_grid'])
        ctk.CTkCheckBox(
            content,
            text="Show Grid Lines",
            variable=show_grid_var,
            font=("Arial", 12)
        ).pack(pady=10, padx=20)
        
        # Show coordinates
        show_coords_var = tk.BooleanVar(value=self.settings['show_coordinates'])
        ctk.CTkCheckBox(
            content,
            text="Show Coordinates",
            variable=show_coords_var,
            font=("Arial", 12)
        ).pack(pady=10, padx=20)
        
        # Save button
        def save_settings():
            self.settings['hex_size'] = int(hex_size_var.get())
            self.settings['show_grid'] = show_grid_var.get()
            self.settings['show_coordinates'] = show_coords_var.get()
            messagebox.showinfo("Settings", "Settings saved!")
        
        ctk.CTkButton(
            content,
            text="Save Settings",
            font=("Arial", 14, "bold"),
            height=40,
            fg_color="green",
            hover_color="dark green",
            command=save_settings
        ).pack(pady=20)
    
    def generate_map(self):
        """Generate a new map"""
        # Update setup data from UI
        self.setup_data['start_direction'] = self.dir_var.get()
        
        try:
            self.setup_data['map_width'] = int(self.width_var.get())
            self.setup_data['map_height'] = int(self.height_var.get())
        except:
            messagebox.showerror("Error", "Please enter valid numbers for width and height")
            return
        
        # Generate map
        generator = MapGenerator(
            self.setup_data['map_width'],
            self.setup_data['map_height'],
            self.setup_data['start_direction'],
            self.setup_data['factions'],
            self.setup_data['custom_locations']
        )
        
        grid = generator.generate()
        
        self.map_data = {
            'grid': grid,
            'width': self.setup_data['map_width'],
            'height': self.setup_data['map_height'],
            'start_direction': self.setup_data['start_direction'],
            'factions': self.setup_data['factions'],
            'custom_locations': self.setup_data['custom_locations'],
            'created_at': datetime.now().isoformat(),
            'fog_of_war_enabled': True
        }
        
        self.show_map()
    
    def show_map(self):
        """Display the map view"""
        if not self.map_data:
            return
        
        self.clear_screen()
        self.current_screen = 'map'
        self.selected_hex = None
        
        # Create main layout
        top_bar = ctk.CTkFrame(self.container, height=60)
        top_bar.pack(fill='x', padx=10, pady=5)
        
        ctk.CTkButton(
            top_bar,
            text="← Menu",
            width=100,
            command=self.show_menu
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            top_bar,
            text="💾 Export",
            width=100,
            command=self.export_map
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            top_bar,
            text="👁 Reveal Selected",
            width=150,
            fg_color="green",
            hover_color="dark green",
            command=self.reveal_selected_hex
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            top_bar,
            text="🔒 Hide Selected",
            width=150,
            fg_color="red",
            hover_color="dark red",
            command=self.hide_selected_hex
        ).pack(side='left', padx=5)
        
        ctk.CTkButton(
            top_bar,
            text="🌫️ Toggle Fog of War",
            width=150,
            fg_color="#8b5cf6",
            hover_color="#7c3aed",
            command=self.toggle_fog_of_war
        ).pack(side='left', padx=5)
        
        # Main content area
        content_frame = ctk.CTkFrame(self.container)
        content_frame.pack(fill='both', expand=True, padx=10, pady=5)
        
        # Canvas frame (left) - using tk.Canvas since CTk doesn't have canvas
        canvas_container = ctk.CTkFrame(content_frame)
        canvas_container.pack(side='left', fill='both', expand=True, padx=(0, 5))
        
        self.canvas = tk.Canvas(
            canvas_container,
            bg='#1f2937',
            highlightthickness=0
        )
        
        h_scroll = tk.Scrollbar(canvas_container, orient='horizontal', command=self.canvas.xview)
        v_scroll = tk.Scrollbar(canvas_container, orient='vertical', command=self.canvas.yview)
        
        self.canvas.configure(xscrollcommand=h_scroll.set, yscrollcommand=v_scroll.set)
        
        h_scroll.pack(side='bottom', fill='x')
        v_scroll.pack(side='right', fill='y')
        self.canvas.pack(side='left', fill='both', expand=True)
        
        # Sidebar (right)
        sidebar = ctk.CTkFrame(content_frame, width=350)
        sidebar.pack(side='right', fill='y', padx=(5, 0))
        sidebar.pack_propagate(False)
        
        # Legend
        legend_label = ctk.CTkLabel(
            sidebar,
            text="Legend",
            font=("Arial", 16, "bold")
        )
        legend_label.pack(pady=(10, 5))
        
        # Scrollable legend
        legend_scroll_frame = ctk.CTkScrollableFrame(sidebar, width=330, height=250)
        legend_scroll_frame.pack(fill='x', pady=(0, 10), padx=10)
        
        for terrain_key, terrain in ALL_TERRAINS.items():
            item_frame = ctk.CTkFrame(legend_scroll_frame)
            item_frame.pack(fill='x', pady=2)
            
            color_box = ctk.CTkLabel(
                item_frame,
                text="  ",
                fg_color=terrain['color'],
                width=30
            )
            color_box.pack(side='left', padx=5)
            
            ctk.CTkLabel(
                item_frame,
                text=terrain['name'],
                font=("Arial", 10),
                anchor='w'
            ).pack(side='left', fill='x', expand=True)
        
        # Symbols
        ctk.CTkLabel(
            legend_scroll_frame,
            text="⌂ Settlement",
            font=("Arial", 10),
            anchor='w'
        ).pack(fill='x', pady=2, padx=5)
        
        ctk.CTkLabel(
            legend_scroll_frame,
            text="★ Point of Interest",
            font=("Arial", 10),
            anchor='w'
        ).pack(fill='x', pady=2, padx=5)
        
        ctk.CTkLabel(
            legend_scroll_frame,
            text="★★ Multiple POIs",
            font=("Arial", 10),
            anchor='w'
        ).pack(fill='x', pady=2, padx=5)
        
        # Notes section
        notes_label = ctk.CTkLabel(
            sidebar,
            text="Notes",
            font=("Arial", 16, "bold")
        )
        notes_label.pack(pady=(15, 5))
        
        notes_instructions = ctk.CTkLabel(
            sidebar,
            text="Select a hex to view/edit notes",
            font=("Arial", 10)
        )
        notes_instructions.pack(pady=(0, 5))
        
        # Notes text area
        self.notes_text = ctk.CTkTextbox(
            sidebar,
            width=330,
            height=250,
            font=("Arial", 10)
        )
        self.notes_text.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # Add default text to notes
        self.notes_text.insert('0.0', 'Click a hex to view details and edit notes...')
        self.notes_text.configure(state='disabled')
        
        # Save notes button
        self.save_notes_btn = ctk.CTkButton(
            sidebar,
            text="💾 Save Notes",
            font=("Arial", 12, "bold"),
            height=35,
            fg_color="green",
            hover_color="dark green",
            command=self.save_notes,
            state='disabled'
        )
        self.save_notes_btn.pack(pady=(0, 10), padx=10)
        
        # Draw the map
        self.draw_map()
        
        # Bind click event
        self.canvas.bind('<Button-1>', self.on_canvas_click)
    
    def save_notes(self):
        """Save notes from the notes text area to the selected hex"""
        if not self.selected_hex:
            return
        
        q, r = self.selected_hex
        # Get all text content
        full_content = self.notes_text.get('0.0', 'end-1c')
        
        # Find the notes section (after the separator line)
        notes_separator = "NOTES:\n" + "-" * 30 + "\n"
        if notes_separator in full_content:
            # Extract only the notes portion
            notes_content = full_content.split(notes_separator, 1)[1]
        else:
            notes_content = ""
        
        self.map_data['grid'][r][q]['notes'] = notes_content
        messagebox.showinfo("Saved", "Notes saved successfully!")
    
    def reveal_selected_hex(self):
        """Reveal the currently selected hex"""
        if self.selected_hex:
            q, r = self.selected_hex
            self.map_data['grid'][r][q]['explored'] = True
            self.draw_map()
            self.update_info_panel(q, r, self.map_data['grid'][r][q])
    
    def hide_selected_hex(self):
        """Hide the currently selected hex"""
        if self.selected_hex:
            q, r = self.selected_hex
            self.map_data['grid'][r][q]['explored'] = False
            self.draw_map()
            self.update_info_panel(q, r, self.map_data['grid'][r][q])
    
    def toggle_fog_of_war(self):
        """Toggle fog of war on/off without affecting explored state"""
        if not self.map_data:
            return

        # Toggle the fog of war state
        current_state = self.map_data.get('fog_of_war_enabled', True)
        self.map_data['fog_of_war_enabled'] = not current_state

        # Redraw the map to reflect the change
        self.draw_map()

        # Update the info panel if a hex is selected
        if self.selected_hex:
            q, r = self.selected_hex
            hex_data = self.map_data['grid'][r][q]
            self.update_info_panel(q, r, hex_data)

        # Show message
        if self.map_data['fog_of_war_enabled']:
            messagebox.showinfo("Fog of War", "Fog of War enabled - unexplored hexes are now hidden")
        else:
            messagebox.showinfo("Fog of War", "Fog of War disabled - all hexes are now visible")
    
    def draw_map(self):
        """Draw the hex map on canvas"""
        if not self.map_data:
            return
        
        self.canvas.delete('all')
        hex_size = self.settings['hex_size']
        
        # Calculate canvas size with extra padding
        max_x = (self.map_data['width'] + 0.5) * hex_size * math.sqrt(3) + 200
        max_y = self.map_data['height'] * hex_size * 1.5 + 200
        
        self.canvas.configure(scrollregion=(0, 0, max_x, max_y))
        
        # Store hex positions for click detection
        self.hex_positions = []
        
        # Draw hexes
        for r in range(self.map_data['height']):
            for q in range(self.map_data['width']):
                hex_data = self.map_data['grid'][r][q]
                if not hex_data:
                    continue
                
                x, y = HexGrid.axial_to_pixel(q, r, hex_size)
                pixel_x = x + 100
                pixel_y = y + 100

                terrain = ALL_TERRAINS[hex_data['terrain']]
                # Show terrain color if either explored OR fog of war is disabled
                fog_enabled = self.map_data.get('fog_of_war_enabled', True)
                is_visible = hex_data['explored'] or not fog_enabled
                color = terrain['color'] if is_visible else '#374151'
                
                # Draw hexagon
                corners = HexGrid.get_hex_corners(pixel_x, pixel_y, hex_size)
                
                # Highlight selected hex
                if self.selected_hex and self.selected_hex == (q, r):
                    outline_color = '#fbbf24'
                    outline_width = 3
                else:
                    outline_color = color
                    outline_width = 0
                
                self.canvas.create_polygon(
                    corners,
                    fill=color,
                    outline=outline_color,
                    width=outline_width
                )
                
                # Draw symbols - show if either explored OR fog of war is disabled
                if is_visible:
                    if hex_data['settlement']:
                        self.canvas.create_text(
                            pixel_x, pixel_y,
                            text='⌂',
                            font=('Arial', int(hex_size * 0.6)),
                            fill='white'
                        )
                    elif hex_data['poi']:
                        # Show different symbol for multiple POIs
                        if hex_data['poi'].get('type') == 'multiple':
                            symbol = '★★'  # Double star for multiple
                        else:
                            symbol = '★'  # Single star
                        self.canvas.create_text(
                            pixel_x, pixel_y,
                            text=symbol,
                            font=('Arial', int(hex_size * 0.5)),
                            fill='white'
                        )
                    else:
                        self.canvas.create_text(
                            pixel_x, pixel_y,
                            text=terrain['symbol'],
                            font=('Arial', int(hex_size * 0.5)),
                            fill='white'
                        )

                    if self.settings['show_coordinates']:
                        self.canvas.create_text(
                            pixel_x, pixel_y + hex_size * 0.6,
                            text=f"{q},{r}",
                            font=('Arial', int(hex_size * 0.3)),
                            fill='#9ca3af'
                        )
                
                # Store position for click detection
                self.hex_positions.append({
                    'q': q, 'r': r,
                    'x': pixel_x, 'y': pixel_y,
                    'size': hex_size
                })
    
    def on_canvas_click(self, event):
        """Handle canvas click events"""
        # Get click coordinates relative to canvas
        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)
        
        # Find clicked hex
        for hex_pos in self.hex_positions:
            distance = math.sqrt(
                (canvas_x - hex_pos['x']) ** 2 +
                (canvas_y - hex_pos['y']) ** 2
            )
            
            if distance < hex_pos['size']:
                q, r = hex_pos['q'], hex_pos['r']
                hex_data = self.map_data['grid'][r][q]
                
                # Select this hex
                self.selected_hex = (q, r)
                
                # Update info panel
                self.update_info_panel(q, r, hex_data)
                
                # Redraw to show selection
                self.draw_map()
                break
    
    def update_info_panel(self, q, r, hex_data):
        """Update the notes panel with hex details and notes"""
        terrain = ALL_TERRAINS[hex_data['terrain']]

        # Enable text widget for editing
        self.notes_text.configure(state='normal')

        # Clear notes text area
        self.notes_text.delete('0.0', 'end')

        # Check if hex is unexplored and fog of war is enabled
        fog_enabled = self.map_data.get('fog_of_war_enabled', True)
        is_hidden = fog_enabled and not hex_data['explored']

        if is_hidden:
            # Show minimal info for unexplored hexes
            info_text = f"Hex ({q}, {r})\n"
            info_text += f"{'='*30}\n\n"
            info_text += f"Status: UNEXPLORED\n\n"
            info_text += "This hex has not been explored yet.\n"
            info_text += "Reveal it to view terrain, POIs, and notes."

            self.notes_text.insert('0.0', info_text)
            self.notes_text.configure(state='disabled')
            self.save_notes_btn.configure(state='disabled')
        else:
            # Add hex info at the top
            info_text = f"Hex ({q}, {r})\n"
            info_text += f"{'='*30}\n\n"
            info_text += f"Terrain: {terrain['name']}\n\n"

            if hex_data['settlement']:
                info_text += f"Settlement: {hex_data['settlement']['name']}\n"
                info_text += f"Type: {hex_data['settlement']['type']}\n"
                if hex_data['settlement']['faction']:
                    info_text += f"Faction: {hex_data['settlement']['faction']}\n"
                info_text += f"\n"

            if hex_data['poi']:
                if hex_data['poi'].get('type') == 'multiple':
                    info_text += f"POIs ({hex_data['poi']['count']}): {hex_data['poi']['name']}\n\n"
                else:
                    info_text += f"POI: {hex_data['poi']['name']}\n\n"

            status_text = "EXPLORED" if hex_data['explored'] else "UNEXPLORED"
            info_text += f"Status: {status_text}\n"
            info_text += f"{'='*30}\n\n"

            # Add notes separator
            info_text += "NOTES:\n"
            info_text += f"{'-'*30}\n"

            # Insert info
            self.notes_text.insert('0.0', info_text)

            # Add existing notes after the separator
            if 'notes' in hex_data and hex_data['notes']:
                self.notes_text.insert('end', hex_data['notes'])

            # Enable save button
            self.save_notes_btn.configure(state='normal')
    
    def export_map(self):
        """Export map to JSON file"""
        if not self.map_data:
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension='.json',
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')],
            initialfile=f"hex-map-{datetime.now().strftime('%Y-%m-%d')}.json"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    json.dump(self.map_data, f, indent=2)
                messagebox.showinfo("Export", "Map exported successfully!")
            except Exception as e:
                messagebox.showerror("Export Error", f"Failed to export map:\n{str(e)}")
    
    def load_map(self):
        """Load map from JSON file"""
        filename = filedialog.askopenfilename(
            filetypes=[('JSON files', '*.json'), ('All files', '*.*')]
        )
        
        if filename:
            try:
                with open(filename, 'r') as f:
                    self.map_data = json.load(f)
                
                # Add notes field to hexes that don't have it (backwards compatibility)
                for r in range(self.map_data['height']):
                    for q in range(self.map_data['width']):
                        if self.map_data['grid'][r][q] and 'notes' not in self.map_data['grid'][r][q]:
                            self.map_data['grid'][r][q]['notes'] = ''

                # Add fog_of_war_enabled field if it doesn't exist (backwards compatibility)
                if 'fog_of_war_enabled' not in self.map_data:
                    self.map_data['fog_of_war_enabled'] = True
                
                self.show_map()
            except Exception as e:
                messagebox.showerror("Load Error", f"Failed to load map:\n{str(e)}")


def main():
    """Main entry point"""
    root = ctk.CTk()
    app = HexMapApp(root)
    root.mainloop()


if __name__ == '__main__':
    main()
