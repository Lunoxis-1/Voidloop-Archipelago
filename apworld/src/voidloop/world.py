from collections.abc import Mapping
from typing import Any

from BaseClasses import MultiWorld
from worlds.AutoWorld import World

from . import items, constants, locations, options, regions, rules, web_world

from Utils import visualize_regions


# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/world%20api.md

# The world class is the heart and soul of an apworld implementation.
# It holds all the data and functions required to build the world and submit it to the multiworld generator.
# You could have all your world code in just this one class, but for readability and better structure,
# it is common to split up world functionality into multiple files.
# This implementation in particular has the following additional files, each covering one topic:
# regions.py, locations.py, rules.py, items.py, options.py and web_world.py.
# It is recommended that you read these in that specific order, then come back to the world class.
class VoidloopWorld(World):


    """
    PLACEHOLDER: Voidloop....

    """


    # The docstring should contain a description of the game, to be displayed on the WebHost.

    # You must override the "game" field to say the name of the game.
    game = "Voidloop"

    # The WebWorld is a definition class that governs how this world will be displayed on the website.
    web = web_world.VoidloopWebWorld()

    # This is how we associate the options defined in our options.py with our world.
    options_dataclass = options.VoidloopOptions
    options: options.VoidloopOptions  # Common mistake: This has to be a colon (:), not an equals sign (=).

    # Our world class must have a static location_name_to_id and item_name_to_id defined.
    # We define these in regions.py and items.py respectively, so we just set them here.
    location_name_to_id = locations.LOCATION_NAME_TO_ID
    item_name_to_id = constants.ITEM_NAME_TO_ID

    # There is always one region that the generator starts from & assumes you can always go back to.
    # This defaults to "Menu", but you can change it by overriding origin_region_name.
    origin_region_name = "Menu"

    item_name_groups = {
        "Pickaxe Upgrades": {"Pickaxe Damage Upgrade", "Pickaxe Speed Upgrade", "Pickaxe Range Upgrade"},
        "Sword Upgrades": {"Sword Damage Upgrade", "Sword Speed Upgrade", "Sword Range Upgrade"},
        "Player Upgrades": {"Player Luck Upgrade", "Player Health Upgrade", "Player Speed Upgrade", "Player Resistance Upgrade"},
        "Blast Upgrades": {"Blast Evolution", "Blast Cooldown", "Blast Damage", "Blast Size"},
        "Dash Upgrades": {"Dash Evolution", "Dash Cooldown", "Dash Damage", "Dash Power"},
        "Energise Upgrades": {"Energise Evolution", "Energise Cooldown", "Energise Multiplier", "Energise Duration"},
        "Ability Evolutions": {"Blast Evolution", "Dash Evolution", "Energise Evolution"},
    }

    def create_regions(self) -> None:
        regions.create_and_connect_regions(self)
        locations.create_all_locations(self)

        visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")

    def set_rules(self) -> None:
        rules.set_all_rules(self)

    def create_items(self):
        items.create_all_items(self)
        self.multiworld.early_items[self.player]["Progressive Region Gem"] = 1

    def create_item(self, name: str) -> items.VoidloopItem:
        return items.create_item_with_correct_classification(self, name)

    # For features such as item links and panic-method start inventory, AP may ask your world to create extra filler.
    # The way it does this is by calling get_filler_item_name.
    # For this purpose, your world *must* have at least one infinitely repeatable item (usually filler).
    # You must override this function and return this infinitely repeatable item's name.
    # In our case, we defined a function called get_random_filler_item_name for this purpose in our items.py.
    def get_filler_item_name(self) -> str:
        return items.get_random_filler_item_name(self)

    # There may be data that the game client will need to modify the behavior of the game.
    # This is what slot_data exists for. Upon every client connection, the slot's slot_data is sent to the client.
    # slot_data is just a dictionary using basic types, that will be converted to json when sent to the client.
    # def fill_slot_data(self) -> Mapping[str, Any]:
    #     pass
    #     # If you need access to the player's chosen options on the client side, there is a helper for that.
    #     # return self.options.as_dict(
    #     #     #"hard_mode", "hammer", "extra_starting_chest", "confetti_explosiveness", "player_sprite"
    #     # )



