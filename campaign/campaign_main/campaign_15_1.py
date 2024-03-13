from module.logger import logger
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids

from .campaign_15_base import CampaignBase
from .campaign_15_base import Config as ConfigBase

MAP = CampaignMap('15-1')
MAP.shape = 'H7'
MAP.camera_data = ['D2', 'D5', 'E2', 'E5']
MAP.camera_data_spawn_point = ['D5']
MAP.map_data = """
    Me -- ME ++ ME MB ++ ++
    ME ME -- ME Me -- MB ++
    ++ -- ME -- Me -- -- MB
    ++ ME -- -- -- __ Me --
    -- ME -- ME ME Me -- ME
    ME -- -- ME ++ -- ME --
    -- SP SP -- Me -- ME --
"""
MAP.weight_data = """
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
    50 50 50 50 50 50 50 50
"""
MAP.spawn_data = [
    {'battle': 0, 'enemy': 5},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 1},
    {'battle': 3},
    {'battle': 4},
    {'battle': 5},
    {'battle': 6, 'boss': 1},
]
A1, B1, C1, D1, E1, F1, G1, H1, \
A2, B2, C2, D2, E2, F2, G2, H2, \
A3, B3, C3, D3, E3, F3, G3, H3, \
A4, B4, C4, D4, E4, F4, G4, H4, \
A5, B5, C5, D5, E5, F5, G5, H5, \
A6, B6, C6, D6, E6, F6, G6, H6, \
A7, B7, C7, D7, E7, F7, G7, H7, \
    = MAP.flatten()

# W15 has special enemy spawn mechanism
# After entering map, additional enemies spawn on these nodes:
# ['C2', 'B3'] must spawns an enemy.
# Additionally, 'B1' spawns a special carrier 
# which allows mob air reinforcement.
OVERRIDE = CampaignMap('15-1')
OVERRIDE.map_data = """
    ME ME ME -- ME -- -- --
    ME ME ME ME ME -- -- --
    -- ME ME -- ME -- -- --
    -- ME -- -- -- -- ME --
    -- ME -- ME ME ME -- ME
    ME -- -- ME -- -- ME --
    -- -- -- -- ME -- ME --
"""


class Config:
    # ===== Start of generated config =====
    # MAP_SIREN_TEMPLATE = ['0']
    # MOVABLE_ENEMY_TURN = (2,)
    # MAP_HAS_SIREN = True
    # MAP_HAS_MOVABLE_ENEMY = True
    MAP_HAS_MAP_STORY = False
    MAP_HAS_FLEET_STEP = False
    MAP_HAS_AMBUSH = True
    # MAP_HAS_MYSTERY = True
    # ===== End of generated config =====

    MAP_WALK_USE_CURRENT_FLEET = True


class Campaign(CampaignBase):
    MAP = MAP
    
    def map_data_init(self, map_):
        super().map_data_init(map_)
        for override_grid in OVERRIDE:
            # Set may_enemy, but keep may_ambush
            self.map[override_grid.location].may_enemy = override_grid.may_enemy

    def battle_0(self):
        self.mob_move(B3, C3)

        if self.clear_filter_enemy('3S', preserve=0):
            return True

        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=1):
            return True

        return self.battle_default()

    def battle_1(self):
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=1):
            return True
        
        return self.battle_default()

    def battle_5(self):
        if self.clear_filter_enemy(self.ENEMY_FILTER, preserve=0):
            return True

        return self.battle_default()

    def battle_6(self):
        return self.fleet_boss.clear_boss()
