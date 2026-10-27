from tornado import template

from BaseClasses import Item, ItemClassification as IClass
import warnings
import traceback
import math

# This just lists IDs. It's up to the items.py and locations.py file to look at the player options to
# actually decide if to include them.

ID_TO_ITEM_NAME = {}

ITEM_NAME_TO_ID = {}

DEFAULT_ITEM_CLASSIFICATION = {

}

ITEM_COUNT = {

}

LOCATION_NAME_TO_ID = {

}

# Helper
def _count_trailing_zeros(num):
    raw = str(num)
    stripped = raw.rstrip("0")
    return len(raw) - len(stripped)

def _add_item(item_id: int, item_count: int, item_name: str, item_classification: IClass):
    if ID_TO_ITEM_NAME.get(item_id):
        raise ValueError(f"Item {item_id} already exists.")
    ID_TO_ITEM_NAME[item_id] = item_name
    ITEM_NAME_TO_ID[item_name] = item_id
    DEFAULT_ITEM_CLASSIFICATION[item_name] = item_classification
    ITEM_COUNT[item_id] = item_count

def _add_location(location_id: int, location_count: int, location_name: str, name_template: str | None = None, exclude: list[int] | None = None):
    if name_template is None:
        name_template = " [ID]"
    if exclude is None:
        exclude = []

    # if we forget to include [ID] this should error
    # if it didn't that would cause issues later
    if not "[ID]" in name_template: raise ValueError(f"Bad name template for item {location_name}: {name_template}")

    if location_count <= 0:
        raise ValueError(f"Expected positive location count, got {location_count or 'None'}.")
    if location_count == 1:
        # Name template ignored, we don't need an ID.
        # Want a name with a number in it? Just add the number to location_name.
        if LOCATION_NAME_TO_ID.get(location_name):
            raise ValueError(f'Location {location_name} already exists.')
        LOCATION_NAME_TO_ID[location_name] = location_id
    if location_count > 1:
        # Get zero count in location count.
        # Note that a value of 99 returns 2 needed trailing zeros, fitting from 101~199
        # But a value of 100 would need 3, fitting from 1000~1100.
        # Technically, 10 only needs 1 trailing zero. But the 0 case (e.g. 100) is
        # skipped to line up with upgrade numbers.
        # In other words, upgrade number 1 is given id 101, not 100.
        location_name = location_name + name_template

        trailing_zeros_needed = len(str(abs(location_count+1)))
        available_trailing_zeros = _count_trailing_zeros(location_id)
        if trailing_zeros_needed > available_trailing_zeros:
            raise ValueError(f'Location {location_name} was given base ID {location_id} with {available_trailing_zeros} trailing zeros, but {trailing_zeros_needed} are required to fill {location_count} slots.')
        for i in range(1, location_count+1):
            # This creates a deliberate gap in location ids. This is because the game client calculates ids programmatically
            if i in exclude: continue
            this_location_name = location_name.replace("[ID]", str(i))
            if LOCATION_NAME_TO_ID.get(this_location_name):
                raise ValueError(f'Location {this_location_name} already exists.')
            LOCATION_NAME_TO_ID[this_location_name] = location_id + i





# Item ID guidelines:
#  1 - Goal!
#  1XX - Filler.

#  1XX Misc/Unclassified
#
#  8NN Hats (hat number is in reading order, starting from 1)
#
#  9NN Achievements/Skillpoints (Achievements are numbered, skill points are 900.)
#
# 1XXX Progressives
#
#  The N here denotes upgrade number, top to bottom.
# 11XX Vanilla based
# 110N Pickaxe upgrades
# 111N Sword upgrades
# 112N Player upgrades
# 113N Blast upgrades
# 114N Dash upgrades
# 115N Energise upgrades
# 119X Other
#
# 12XX Custom
# 121X Timer upgrades

# 1XXXX+ Sanity related
# 11XXX Leversanity

# Register all items.
# Fine to just be done manually.

# This is created and locked to the "Welcome Home" achievement elsewhere (the win con)
# As such it should never be created otherwise.
_add_item(1,     0,  "Home", IClass.progression)

_add_item(101,   0,  "Random Chest Loot", IClass.filler)
_add_item(102,   0,  "Random Golden Chest Loot", IClass.filler)
_add_item(110,   0,  "Voidrock", IClass.filler)

# There is one achievement locked behind skill points. This means that skill points are in logic
# WHICH MEANS THAT EVERY SINGLE SKILL POINT MUST BE MARKED PROGRESSION OR IT WILL FILLERROR
# I hate this so much...
_add_item(900,   50, "Skill Point", IClass.progression_deprioritized_skip_balancing)

_add_item(1101,  10, "Pickaxe Damage Upgrade", IClass.progression_skip_balancing)
_add_item(1102,  5,  "Pickaxe Speed Upgrade", IClass.progression_skip_balancing)
_add_item(1103,  5,  "Pickaxe Range Upgrade", IClass.progression_skip_balancing)

_add_item(1111,  10, "Sword Damage Upgrade", IClass.progression_skip_balancing)
_add_item(1112,  5,  "Sword Speed Upgrade", IClass.progression_skip_balancing)
_add_item(1113,  5,  "Sword Range Upgrade", IClass.progression_skip_balancing)

_add_item(1121,  5,  "Player Luck Upgrade", IClass.progression_skip_balancing)
_add_item(1122,  3,  "Player Health Upgrade", IClass.progression_skip_balancing)
_add_item(1123,  3,  "Player Speed Upgrade", IClass.progression_skip_balancing)
_add_item(1124,  3,  "Player Resistance Upgrade", IClass.progression_skip_balancing)

_add_item(1131,  2,  "Blast Evolution", IClass.progression_skip_balancing)
_add_item(1132,  5,  "Blast Cooldown Upgrade", IClass.useful)
_add_item(1133,  10, "Blast Damage Upgrade", IClass.useful)
_add_item(1134,  6,  "Blast Size Upgrade", IClass.useful)

_add_item(1141,  2,  "Dash Evolution", IClass.progression_skip_balancing)
_add_item(1142,  5,  "Dash Cooldown Upgrade", IClass.useful)
_add_item(1143,  6,  "Dash Damage Upgrade", IClass.useful)
_add_item(1144,  10, "Dash Power Upgrade", IClass.useful)

_add_item(1151,  2,  "Energise Evolution", IClass.progression_skip_balancing)
_add_item(1152,  5,  "Energise Cooldown Upgrade", IClass.useful)
_add_item(1153,  10, "Energise Multiplier Upgrade", IClass.useful)
_add_item(1154,  6,  "Energise Duration Upgrade", IClass.useful)

_add_item(1190,  5,  "Progressive Region Gem", IClass.progression)


# Locations

_add_location(801, 1, "Hat: Beak")
_add_location(802, 1, "Hat: Boat")
_add_location(803, 1, "Hat: Cupids Arrow")
_add_location(804, 1, "Hat: Disguise")
_add_location(805, 1, "Hat: Eyepatch")
_add_location(806, 1, "Hat: Mohawk")
_add_location(807, 1, "Hat: Smile Mask")
_add_location(808, 1, "Hat: Bunny Ears")
_add_location(809, 1, "Hat: Cat Ears")
_add_location(810, 1, "Hat: Cowboy Hat")
_add_location(811, 1, "Hat: Dog Ears")
_add_location(812, 1, "Hat: Fedora")
_add_location(813, 1, "Hat: Hardhat")
_add_location(814, 1, "Hat: Heart Pin")
_add_location(815, 1, "Hat: Mushroom Cap")
_add_location(816, 1, "Hat: Pumpkin")
_add_location(817, 1, "Hat: Reginald Mask")
_add_location(818, 1, "Hat: Shades")
_add_location(819, 1, "Hat: Space Helmet")
_add_location(820, 1, "Hat: Tophat")
_add_location(821, 1, "Hat: Traffic Cone")
_add_location(822, 1, "Hat: Wizard Hat")
_add_location(823, 1, "Hat: Chef Hat")
_add_location(824, 1, "Hat: Cooler Cowboy Hat")
_add_location(825, 1, "Hat: Crown")
_add_location(826, 1, "Hat: Frog Hat")
_add_location(827, 1, "Hat: Propeller Hat")
_add_location(828, 1, "Hat: Robot Head")
_add_location(829, 1, "Hat: Blonde Hair")
_add_location(830, 1, "Hat: Capybara")
_add_location(831, 1, "Hat: Voidcrown")

_add_location(901, 1, "Happy Camper")
_add_location(902, 1, "Memento")
_add_location(903, 1, "Novice Explorer")
_add_location(904, 1, "Apprentice Explorer")
_add_location(905, 1, "Advanced Explorer")
_add_location(906, 1, "Master Explorer")
_add_location(907, 1, "Craggy Conquerer")
_add_location(908, 1, "Dungeon Destroyer")
_add_location(909, 1, "Jungle Jogger")
_add_location(910, 1, "Sanctuary Soldier")
_add_location(911, 1, "Molten Maniac")
_add_location(912, 1, "Welcome Home")
_add_location(913, 1, "Novice Hoarder")
_add_location(914, 1, "Advanced Hoarder")
_add_location(915, 1, "Master Hoarder")
_add_location(916, 1, "Novice Traveller")
_add_location(917, 1, "Advanced Traveller")
_add_location(918, 1, "Master Traveller")
_add_location(919, 1, "Novice Slayer")
_add_location(920, 1, "Advanced Slayer")
_add_location(921, 1, "Master Slayer")
_add_location(922, 1, "Novice Upgrader")
_add_location(923, 1, "Advanced Upgrader")
_add_location(924, 1, "Master Upgrader")
_add_location(925, 1, "Novice Brewer")
_add_location(926, 1, "Advanced Brewer")
_add_location(927, 1, "Master Brewer")
_add_location(928, 1, "Novice Learner")
_add_location(929, 1, "Advanced Learner")
_add_location(930, 1, "Master Learner")
_add_location(931, 1, "Novice Smelter")
_add_location(932, 1, "Advanced Smelter")
_add_location(933, 1, "Master Smelter")
_add_location(934, 1, "Novice Contractor")
_add_location(935, 1, "Advanced Contractor")
_add_location(936, 1, "Master Contractor")
_add_location(937, 1, "Bad Businessman")
_add_location(938, 1, "Good Businessman")
_add_location(939, 1, "Ability Appreciator")
_add_location(940, 1, "Ability Abuser")
_add_location(941, 1, "Entomophobia")
_add_location(942, 1, "Keen Eye")
_add_location(943, 1, "Exotic Killer")
_add_location(944, 1, "Millionaire")
_add_location(945, 1, "Anti-Demolisionist")
_add_location(946, 1, "Voidloop")
_add_location(947, 1, "Sweet Revenge")
_add_location(948, 1, "Overloaded")
_add_location(949, 1, "Return to Sender")
_add_location(950, 1, "Destroy All Tiles in a Resource Room")
# ^ This achievement has no name. Description used instead.




# Generates ids 110101~110110 with names "Pickaxe Damage Upgrade 1", "Pickaxe Damage Upgrade 2", ect..
# All these have two extra digits
_add_location(110100, 10, "Pickaxe Damage Upgrade")
_add_location(110200, 5,  "Pickaxe Speed Upgrade")
_add_location(110300, 5,  "Pickaxe Range Upgrade")

_add_location(111100, 10, "Sword Damage Upgrade")
_add_location(111200, 5,  "Sword Speed Upgrade")
_add_location(111300, 5,  "Sword Range Upgrade")

_add_location(112100, 5,  "Player Luck Upgrade")
_add_location(112200, 3,  "Player Health Upgrade")
_add_location(112300, 3,  "Player Speed Upgrade")
_add_location(112400, 3,  "Player Resistance Upgrade")

_add_location(113100, 2,  "Blast Evolution")
_add_location(113200, 5,  "Blast Cooldown Upgrade")
_add_location(113300, 10, "Blast Damage Upgrade")
_add_location(113400, 6,  "Blast Size Upgrade")

_add_location(114100, 2,  "Dash Evolution")
_add_location(114200, 5,  "Dash Cooldown Upgrade")
_add_location(114300, 6,  "Dash Damage Upgrade")
_add_location(114400, 10, "Dash Power Upgrade")

_add_location(115100, 2,  "Energise Evolution")
_add_location(115200, 5,  "Energise Cooldown Upgrade")
_add_location(115300, 10, "Energise Multiplier Upgrade")
_add_location(115400, 6,  "Energise Duration Upgrade")

_add_location(119002, 1,  "Dungeon Gem")
_add_location(119003, 1,  "Jungle Gem")
_add_location(119004, 1,  "Ice Gem")
_add_location(119005, 1,  "Lava Gem")
_add_location(119006, 1,  "Voidgem")

_add_location(1100100, 20,  "Craggy Cavern Lever", " (Floor [ID])", [20])
_add_location(1100200, 20,  "Desolate Dungeon Lever", " (Floor [ID])", [20])
_add_location(1100400, 20,  "Jagged Jungle Lever", " (Floor [ID])", [20])
_add_location(1100300, 20,  "Slippery Sanctuary Lever", " (Floor [ID])", [20])
_add_location(1100500, 20,  "Molten Mineshaft Lever", " (Floor [ID])", [20])

