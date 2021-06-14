from module.base.button import ButtonGrid

# Known Guild Items with Secondary Grid
SELECT_ITEMS = [
    'book',
    'box',
    'retrofit',
    'plate',
    'priority',
]

# Known Secondary Grid Items by Category
SELECT_BOOK = {
    'red': 0,
    'blue': 1,
    'yellow': 2,
}

SELECT_BOX = {
    'eagle': 0,
    'royal': 1,
    'sakura': 2,
    'ironblood': 3,
}

SELECT_RETROFIT = {
    'dd': 0,
    'cl': 1,
    'bb': 2,
    'cv': 3,
}

SELECT_PLATE = {
    'general': 0,
    'gun': 1,
    'torpedo': 2,
    'antiair': 3,
    'plane': 4,
}

SELECT_PRIORITY = {
    'neptune': 0,
    'monarch': 1,
    'ibuki': 2,
    'izumo': 3,
    'roon': 4,
    'saintlouis': 5,
    'seattle': 0,
    'georgia': 1,
    'kitakaze': 2,
    'gascogne': 3,
    'cheshire': 0,
    'mainz': 1,
    'odin': 2,
    'champagne': 3,
}

# Known Secondary Grid Items Limits
SELECT_BOOK_LIMIT = 3
SELECT_BOX_LIMIT = 1
SELECT_RETROFIT_LIMIT = 2
SELECT_PLATE_LIMIT = 5
SELECT_PRIORITY_LIMIT = 1

# Known Secondary Grid Sizes
SELECT_GRID_3X1 = ButtonGrid(
    origin=(412, 208), delta=(158, 0), button_shape=(119, 119), grid_shape=(3, 1),
    name='SHOP_SELECT_GRID_3X1')

SELECT_GRID_4X1 = ButtonGrid(
    origin=(334, 208), delta=(158, 0), button_shape=(119, 119), grid_shape=(4, 1),
    name='SHOP_SELECT_GRID_4X1')

SELECT_GRID_5X1 = ButtonGrid(
    origin=(256, 208), delta=(158, 0), button_shape=(119, 119), grid_shape=(5, 1),
    name='SHOP_SELECT_GRID_5X1')

SELECT_GRID_6X1 = ButtonGrid(
    origin=(256, 208), delta=(158, 0), button_shape=(119, 119), grid_shape=(5, 1),
    name='SHOP_SELECT_GRID_6X1')
