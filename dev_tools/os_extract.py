from dev_tools.utils import LuaLoader, temp_render, FOLDER
from module.base.utils import location2node
from module.logger import logger  # Change folder automatically
from module.os.map_data import DIC_OS_MAP


class OSChapter:
    def __init__(self):
        self.chapter = {}
        data = LOADER.load('sharecfg/world_chapter_random.lua')
        for index, chapter in data.items():
            if not isinstance(index, int) or index >= 200:
                continue
            self.chapter[index] = {'cn': chapter['name'], 'hazard_level': chapter['hazard_level']}

        for index, name in self.extract_chapter_name('zh-CN').items():
            self.chapter[index]['cn'] = name
        for index, name in self.extract_chapter_name('en-US').items():
            self.chapter[index]['en'] = name
        for index, name in self.extract_chapter_name('ja-JP').items():
            self.chapter[index]['jp'] = name
        for index, name in self.extract_chapter_name('zh-TW').items():
            self.chapter[index]['tw'] = name
        for index, shape in self.extract_map_size().items():
            self.chapter[index]['shape'] = shape
        # hazard_level
        new = {}
        for index, chapter in self.chapter.items():
            new[index] = {
                # The structure of world_chapter_template.lua has changed, so load the old map data
                'shape': chapter.get('shape', DIC_OS_MAP[index]['shape']),
                'hazard_level': chapter['hazard_level'],
                'cn': chapter['cn'],
                'en': chapter['en'],
                'jp': chapter['jp'],
                'tw': chapter['tw'],
            }
        self.chapter = new

        for index, data in self.extract_map_position().items():
            self.chapter[index].update(data)

    def extract_chapter_name(self, server):
        LOADER.server = server
        data = LOADER.load('sharecfg/world_chapter_random.lua')
        out = {}
        for index, chapter in data.items():
            if not isinstance(index, int) or index >= 200:
                continue
            name = chapter['name']
            name = name.replace('é', 'e')  # OCR can't recognize letter "é"
            out[index] = name

        # Zone 40000 is zone 154
        for index, chapter in data.items():
            if index == 40000:
                print(server, chapter['name'])
                out[154] = chapter['name']

        return out

    def extract_map_size(self, server='zh-CN'):
        LOADER.server = server
        data = LOADER.load('sharecfgdata/world_chapter_template.lua')
        out = {}
        for full_index, chapter in data.items():
            if not full_index // 1000000 == 1 or not chapter['map_sight']:
                continue
            index = (full_index % 1000000) // 1000
            if index < 10:
                index -= 1
            shape = self.parse_map_data(chapter['grids'])
            out[index] = location2node(shape)

        return out

    def parse_map_data(self, grids):
        y = [grid[0] for grid in grids.values()]
        x = [grid[1] for grid in grids.values()]
        return (max(x) - min(x), max(y) - min(y))

    def extract_map_position(self, server='zh-CN'):
        LOADER.server = server
        data = LOADER.load('sharecfg/world_chapter_colormask.lua')
        out = {}
        for chapter in data.values():
            if 'serial_number' not in chapter:
                continue
            else:
                index = int(chapter['serial_number'])
                if index < 10:
                    index -= 1
                out[index] = {}

            area = chapter['area_pos']
            out[index]['area_pos'] = (area[0], area[1])
            offset = chapter['offset_pos']
            out[index]['offset_pos'] = (offset[0], offset[1])
            out[index]['region'] = chapter['regions']

        return out

    def encode(self):
        lines = []
        for index, chapter in self.chapter.items():
            lines.append(f'    {index}: {str(chapter)},')
        return lines

    def write(self, file):
        print(f'writing {file}')
        with open(file, 'w', encoding='utf-8') as f:
            for text in self.encode():
                f.write(text + '\n')

    def write_template(self, file):
        print(f'writing {file}')
        res = temp_render('os', Data=self.encode())
        with open(file, 'w', encoding='utf-8') as f:
            f.write(res)


"""
This an auto-tool to extract map data for operation siren.

Git clone https://github.com/AzurLaneTools/AzurLaneLuaScripts, to get the decrypted scripts.
Arguments:
    FILE:  Path to repository, such as 'xxx/AzurLaneLuaScripts'
    SAVE:  File to save, 'module/os/map_data.py'
"""
# FOLDER = ''
SAVE = 'module/os/map_data.py'

LOADER = LuaLoader(FOLDER)
OSChapter().write_template(SAVE)
