from module.campaign.campaign_base import CampaignBase
from module.map.map_base import CampaignMap
from module.map.map_grids import SelectedGrids, RoadGrids
from module.logger import logger


MAP = CampaignMap()
MAP.map_data = '''
    -- ME ME MM ME -- ++ ++
    SP ME ++ ++ ME ME ++ ++
    SP -- ++ ++ -- ME ME MB
'''
MAP.camera_data = ['C1', 'E1']
MAP.camera_data_spawn_point = ['C1']
MAP.weight_data = '''
    40 30 21 20 17 15 50 50
    40 40 50 50 16 13 50 50
    40 40 50 50 14 12 11 10
'''
MAP.spawn_data = [
    {'battle': 0, 'enemy': 3},
    {'battle': 1, 'enemy': 2},
    {'battle': 2, 'enemy': 2},
    {'battle': 3, 'enemy': 1, 'mystery': 1},
    {'battle': 4},
    {'battle': 5, 'boss': 1},
]


class Config:
    SUBMARINE = 0
    FLEET_BOSS = 2

    INTERNAL_LINES_HOUGHLINES_THRESHOLD = 40
    EDGE_LINES_HOUGHLINES_THRESHOLD = 40
    COINCIDENT_POINT_ENCOURAGE_DISTANCE = 1.5
    MID_DIFF_RANGE_H = (140 - 3, 140 + 3)
    MID_DIFF_RANGE_V = (143 - 3, 143 + 3)

    INTERNAL_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (150, 255 - 24),
        'width': (0.5, 20),
        'prominence': 10,
        'distance': 35,
        'wlen': 100,
    }
    EDGE_LINES_FIND_PEAKS_PARAMETERS = {
        'height': (255 - 24, 255),
        'prominence': 10,
        'distance': 50,
        'wlen': 1000
    }


class Campaign(CampaignBase):
    MAP = MAP
    MAP_AMBUSH_OVERLAY_TRANSPARENCY_THRESHOLD = 0.45
    MAP_AIR_RAID_OVERLAY_TRANSPARENCY_THRESHOLD = 0.45

    def battle_0(self):
        self.clear_all_mystery()
        self.fleet_2_push_forward()

        return self.battle_default()

    def battle_5(self):
        self.clear_all_mystery()

        return self.fleet_2.brute_clear_boss()

    def handle_boss_appear_refocus(self):
        for data in self.map.spawn_data:
            if data.get('battle') == self.battle_count and data.get('boss', 0):
                self.map_swipe((-3, -2))
        return super().handle_boss_appear_refocus()
