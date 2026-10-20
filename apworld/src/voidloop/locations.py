from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Location

from . import constants
#from .. import voidloop

if TYPE_CHECKING:
    from .world import VoidloopWorld


class VoidloopLocation(Location):
     game = "Voidloop"

from rule_builder.rules import True_
from .constants import LOCATION_NAME_TO_ID
from .items import VoidloopItem


# Let's make one more helper method before we begin actually creating locations.
# Later on in the code, we'll want specific subsections of LOCATION_NAME_TO_ID.
# To reduce the chance of copy-paste errors writing something like {"Chest": LOCATION_NAME_TO_ID["Chest"]},
# let's make a helper method that takes a list of location names and returns them as a dict with their IDs.
# Note: There is a minor typing quirk here. Some functions want location addresses to be an "int | None",
# so while our function here only ever returns dict[str, int], we annotate it as dict[str, int | None].
def get_location_names_with_ids(location_names: list[str]) -> dict[str, int | None]:
    return {location_name: LOCATION_NAME_TO_ID[location_name] for location_name in location_names}


def create_all_locations(world: VoidloopWorld) -> None:
    create_regular_locations(world)
    create_events(world)


def create_regular_locations(world: VoidloopWorld) -> None:
    # Finally, we need to put the Locations ("checks") into their regions.
    # Once again, before we do anything, we can grab our regions we created by using world.get_region()
    #menu = world.get_region("Menu")
    craggy_cavern = world.get_region("Craggy Cavern")
    desolate_dungeon = world.get_region("Desolate Dungeon")
    jagged_jungle = world.get_region("Jagged Jungle")
    slippery_sanctuary = world.get_region("Slippery Sanctuary")
    molten_mineshaft = world.get_region("Molten Mineshaft")
    the_void = world.get_region("The Void")

    # Some notes
    # Unique items per region: 22, 13, 10, 11, 10, 1
    # 20% of total: 14, Novice hoarder can be obtained in first region.
    # 50% of total: 34, Advanced hoarder can be obtained in second region.
    # Master hoarder requires all items which includes the void key, so it's effectively locked behind default goal.

    # Most hats are considered in logic by the ice layer.
    # The legendary and mythic hats comes in at magma.
    # Until then, everything you get from hat crates is out of logic. This is fine.

    # DOUBLE CHECK PLACEMENTS FOR:
    # Sweet Revenge, Exotic Killer, Destroy All Tiles in a Resource Room, Millionaire, Anti-Demolishionist.


    # Always accessible, regardless of options.
    # Achievements first, achievement order, except for the floor 20 achievements because those have to be moved at some point.

    # Every location here should be accessible in sphere 0.
    craggy_cavern_locations = get_location_names_with_ids([
        "Happy Camper",
        "Memento",
        "Novice Hoarder",
        "Novice Traveller",
        "Novice Slayer",
        "Novice Upgrader",
        "Novice Brewer",
        "Novice Learner",
        "Novice Smelter",
        "Advanced Smelter",
        "Novice Contractor",
        "Return to Sender",

        "Dungeon Gem",

        "Pickaxe Damage Upgrade 1",
        "Pickaxe Damage Upgrade 2",
        "Pickaxe Damage Upgrade 3",
        "Pickaxe Speed Upgrade 1",
        "Pickaxe Range Upgrade 1",

        "Sword Damage Upgrade 1",
        "Sword Damage Upgrade 2",
        "Sword Speed Upgrade 1",
        "Sword Range Upgrade 1",

        "Player Luck Upgrade 1",
        "Player Health Upgrade 1",
        "Player Speed Upgrade 1",

        "Dash Evolution 1",
        "Energise Evolution 1",

        "Blast Cooldown Upgrade 1",
        "Blast Damage Upgrade 1",
        "Blast Damage Upgrade 2",
        "Blast Size Upgrade 1",
        "Blast Size Upgrade 2",

        "Dash Cooldown Upgrade 1",
        "Dash Damage Upgrade 1",
        "Dash Damage Upgrade 2",
        "Dash Power Upgrade 1",
        "Dash Power Upgrade 2",

        "Energise Cooldown Upgrade 1",
        "Energise Multiplier Upgrade 1",
        "Energise Multiplier Upgrade 2",
        "Energise Duration Upgrade 1",
        "Energise Duration Upgrade 2",

        "Craggy Conquerer",
    ])
    desolate_dungeon_locations = get_location_names_with_ids([
        "Novice Explorer",
        "Advanced Hoarder",
        "Advanced Brewer",
        "Advanced Contractor",
        "Sweet Revenge",

        "Jungle Gem",

        "Pickaxe Damage Upgrade 4",
        "Pickaxe Damage Upgrade 5",
        "Pickaxe Speed Upgrade 2",
        "Pickaxe Range Upgrade 2",

        "Sword Damage Upgrade 3",
        "Sword Damage Upgrade 4",
        "Sword Speed Upgrade 2",
        "Sword Range Upgrade 2",

        "Player Luck Upgrade 2",
        "Player Health Upgrade 2",
        "Player Resistance Upgrade 1",

        "Blast Evolution 1",

        "Blast Cooldown Upgrade 2",
        "Blast Damage Upgrade 3",
        "Blast Damage Upgrade 4",
        "Blast Size Upgrade 3",

        "Dash Cooldown Upgrade 2",
        "Dash Damage Upgrade 3",
        "Dash Power Upgrade 3",
        "Dash Power Upgrade 4",

        "Energise Cooldown Upgrade 2",
        "Energise Multiplier Upgrade 3",
        "Energise Multiplier Upgrade 4",
        "Energise Duration Upgrade 3",

        "Dungeon Destroyer",
    ])
    jagged_jungle_locations = get_location_names_with_ids([
        "Apprentice Explorer",
        "Advanced Traveller",
        "Advanced Upgrader",
        "Master Brewer",
        "Advanced Learner",
        "Master Smelter",
        "Entomophobia",
        "Overloaded",

        "Ice Gem",

        "Pickaxe Damage Upgrade 6",
        "Pickaxe Speed Upgrade 3",
        "Pickaxe Range Upgrade 3",

        "Sword Damage Upgrade 5",
        "Sword Damage Upgrade 6",
        "Sword Speed Upgrade 3",
        "Sword Range Upgrade 3",

        "Player Luck Upgrade 3",
        "Player Speed Upgrade 2",
        "Player Resistance Upgrade 2",

        # No evolutions at this tier.

        "Blast Cooldown Upgrade 3",
        "Blast Damage Upgrade 5",
        "Blast Damage Upgrade 6",
        "Blast Size Upgrade 4",

        "Dash Cooldown Upgrade 3",
        "Dash Damage Upgrade 4",
        "Dash Power Upgrade 5",
        "Dash Power Upgrade 6",
        
        "Energise Cooldown Upgrade 3",
        "Energise Multiplier Upgrade 5",
        "Energise Multiplier Upgrade 6",
        "Energise Duration Upgrade 4",

        "Jungle Jogger",
    ])
    slippery_sanctuary_locations = get_location_names_with_ids([
        "Advanced Explorer",
        "Advanced Slayer",
        "Master Contractor",
        "Bad Businessman",
        "Good Businessman",
        "Ability Abuser",
        "Ability Appreciator",
        "Anti-Demolisionist",

        "Lava Gem",

        "Pickaxe Damage Upgrade 7",
        "Pickaxe Damage Upgrade 8",
        "Pickaxe Speed Upgrade 4",
        "Pickaxe Range Upgrade 4",

        "Sword Damage Upgrade 7",
        "Sword Damage Upgrade 8",
        "Sword Speed Upgrade 4",
        "Sword Range Upgrade 4",

        "Player Luck Upgrade 4",
        "Player Health Upgrade 3",

        "Dash Evolution 2",

        "Blast Cooldown Upgrade 4",
        "Blast Damage Upgrade 7",
        "Blast Damage Upgrade 8",
        "Blast Size Upgrade 5",

        "Dash Cooldown Upgrade 4",
        "Dash Damage Upgrade 5",
        "Dash Power Upgrade 7",
        "Dash Power Upgrade 8",
        
        "Energise Cooldown Upgrade 4",
        "Energise Multiplier Upgrade 7",
        "Energise Multiplier Upgrade 8",
        "Energise Duration Upgrade 5",

        "Hat: Beak",
        "Hat: Boat",
        "Hat: Cupids Arrow",
        "Hat: Disguise",
        "Hat: Eyepatch",
        "Hat: Mohawk",
        "Hat: Smile Mask",
        "Hat: Bunny Ears",
        "Hat: Cat Ears",
        "Hat: Cowboy Hat",
        "Hat: Dog Ears",
        "Hat: Fedora",
        "Hat: Hardhat",
        "Hat: Heart Pin",
        "Hat: Mushroom Cap",
        "Hat: Pumpkin",
        "Hat: Reginald Mask",
        "Hat: Shades",
        "Hat: Space Helmet",
        "Hat: Tophat",
        "Hat: Traffic Cone",
        "Hat: Wizard Hat",
        "Hat: Chef Hat",
        "Hat: Cooler Cowboy Hat",
        "Hat: Crown",
        "Hat: Frog Hat",
        "Hat: Propeller Hat",
        "Hat: Robot Head",

        "Sanctuary Soldier",
    ])
    molten_mineshaft_locations = get_location_names_with_ids([
        "Master Explorer",
        "Master Traveller",
        "Master Slayer",
        "Master Upgrader",
        "Master Learner",

        "Voidgem",

        "Pickaxe Damage Upgrade 9",
        "Pickaxe Damage Upgrade 10",
        "Pickaxe Speed Upgrade 5",
        "Pickaxe Range Upgrade 5",

        "Sword Damage Upgrade 9",
        "Sword Damage Upgrade 10",
        "Sword Speed Upgrade 5",
        "Sword Range Upgrade 5",

        "Player Luck Upgrade 5",
        "Player Speed Upgrade 3",
        "Player Resistance Upgrade 3",

        "Blast Evolution 2",
        "Energise Evolution 2",

        "Blast Cooldown Upgrade 5",
        "Blast Damage Upgrade 9",
        "Blast Damage Upgrade 10",
        "Blast Size Upgrade 6",

        "Dash Cooldown Upgrade 5",
        "Dash Damage Upgrade 6",
        "Dash Power Upgrade 9",
        "Dash Power Upgrade 10",
        
        "Energise Cooldown Upgrade 5",
        "Energise Multiplier Upgrade 9",
        "Energise Multiplier Upgrade 10",
        "Energise Duration Upgrade 6",

        "Hat: Blonde Hair",
        "Hat: Capybara",
        "Hat: Voidcrown",

        "Molten Maniac",
        "Keen Eye",
        "Exotic Killer",
        "Millionaire",
        "Destroy All Tiles in a Resource Room",
    ])
    the_void_locations = get_location_names_with_ids([
        "Welcome Home",
        "Master Hoarder",
        "Voidloop",
    ])
    craggy_cavern.add_locations(craggy_cavern_locations, VoidloopLocation)
    desolate_dungeon.add_locations(desolate_dungeon_locations, VoidloopLocation)
    jagged_jungle.add_locations(jagged_jungle_locations, VoidloopLocation)
    slippery_sanctuary.add_locations(slippery_sanctuary_locations, VoidloopLocation)
    molten_mineshaft.add_locations(molten_mineshaft_locations, VoidloopLocation)
    the_void.add_locations(the_void_locations, VoidloopLocation)

    # Locations may be in different regions depending on the player's options.
    # # In our case, the hammer option puts the Top Middle Chest into its own room called Top Middle Room.
    # top_middle_room_locations = get_location_names_with_ids(["Top Middle Chest"])
    # if world.options.hammer:
    #     top_middle_room = world.get_region("Top Middle Room")
    #     top_middle_room.add_locations(top_middle_room_locations, FractalBlockWorldLocation)
    # else:
    #     overworld.add_locations(top_middle_room_locations, FractalBlockWorldLocation)

    # Locations may exist only if the player enables certain options.
    # # In our case, the extra_starting_chest option adds the Bottom Left Extra Chest location.
    # if world.options.extra_starting_chest:
    #     # Once again, it is important to stress that even though the Bottom Left Extra Chest location doesn't always
    #     # exist, it must still always be present in the world's location_name_to_id.
    #     # Whether the location actually exists in the seed is purely determined by whether we create and add it here.
    #     bottom_left_extra_chest = get_location_names_with_ids(["Bottom Left Extra Chest"])
    #     overworld.add_locations(bottom_left_extra_chest, FractalBlockWorldLocation)


def create_events(world: VoidloopWorld) -> None:
    the_void = world.get_region("The Void")

    # the_void region already has its own region logic.
    # Entering the void automatically checks the "Welcome Home" location.
    the_void.add_event("Welcome Home", "Goal Clear", True_(), location_type=VoidloopLocation, item_type=VoidloopItem)

    # Sometimes, the player may perform in-game actions that allow them to progress which are not related to Items.
    # In our case, the player must press a button in the top left room to open the final boss door.
    # AP has something for this purpose: "Event locations" and "Event items".
    # An event location is no different than a regular location, except it has the address "None".
    # It is treated during generation like any other location, but then it is discarded.
    # # This location cannot be "sent" and its item cannot be "received", but the item can be used in logic rules.
    # # Since we are creating more locations and adding them to regions, we need to grab those regions again first.
    # top_left_room = world.get_region("Top Left Room")
    # final_boss_room = world.get_region("Final Boss Room")
    #
    # # One way to create an event is simply to use one of the normal methods of creating a location.
    # button_in_top_left_room = FractalBlockWorldLocation(world.player, "Top Left Room Button", None, top_left_room)
    # top_left_room.locations.append(button_in_top_left_room)
    #
    # # We then need to put an event item onto the location.
    # # An event item is an item whose code is "None" (same as the event location's address),
    # # and whose classification is "progression". Item creation will be discussed more in items.py.
    # # Note: Usually, items are created in world.create_items(), which for us happens in items.py.
    # # However, when the location of an item is known ahead of time (as is the case with an event location/item pair),
    # # it is common practice to create the item when creating the location.
    # # Since locations also have to be finalized after world.create_regions(), which runs before world.create_items(),
    # # we'll create both the event location and the event item in our locations.py code.
    # button_item = items.FractalBlockWorldItem("Top Left Room Button Pressed", ItemClassification.progression, None, world.player)
    # button_in_top_left_room.place_locked_item(button_item)
    #
    # # A way simpler way to do create an event location/item pair is by using the region.create_event helper.
    # # Luckily, we have another event we want to create: The Victory event.
    # # We will use this event to track whether the player can win the game.
    # # The Victory event is a completely optional abstraction - This will be discussed more in set_rules().
    # final_boss_room.add_event(
    #     "Final Boss Defeated", "Victory", location_type=FractalBlockWorldLocation, item_type=items.FractalBlockWorlItem
    # )
    #
    # # If you create all your regions and locations line-by-line like this,
    # # the length of your create_regions might get out of hand.
    # # Many worlds use more data-driven approaches using dataclasses or NamedTuples.
    # # However, it is worth understanding how the actual creation of regions and locations works,
    # # That way, we're not just mindlessly copy-pasting! :)
    #

# ###
#   p.add("st_yw_tutorial_dragon")
#     p.add("st_yw_tutorial_pink_rings")
#     p.add("st_yw_tutorial_yellow_key")
#     p.add("st_yw_noob_maze_large")
#     p.add("st_yw_imp_dungeon_above")
#     p.add("st_yw_small_yellow_flower_blue")
#     p.add("st_yw_small_yellow_flower_dungeon")
#     p.add("st_yw_air_red_cube")
#     p.add("st_yw_lib_below")
#     p.add("st_yw_jumbo_large_cannon_pyramid")
#     p.add("st_yw_spider_air")
#     p.add("st_yw_unremembered_tower_1")
#     p.add("st_yw_unremembered_tower_2")
#     p.add("st_yw_shell_green_island")
#     p.add("st_yw_emergency_wp")

#     --Midway.
#     p.add("st_mid_oak_tree_dungeon_1")
#     p.add("st_mid_oak_tree_dungeon_2")
#     p.add("st_mid_laser_fort_small")
#     p.add("st_mid_laser_fort_small_secret")
#     p.add("st_mid_basic_laser_maze")
#     p.add("st_mid_richmond_building_top")
#     p.add("st_mid_richmond_building_secret")
#     p.add("st_mid_richmond_lib_secret")
#     p.add("st_mid_stoney_air_totem_secret")
#     p.add("st_mid_stoney_air_yellow_cube_island_1")
#     p.add("st_mid_stoney_air_yellow_cube_island_2")
#     p.add("st_mid_stoney_church_blackberry")
#     p.add("st_mid_stoney_church_lib_yellow_key")
#     p.add("st_mid_stoney_church_lib_yellow_guard")
#     p.add("st_mid_stoney_church_column")
#     p.add("st_mid_stoney_church_wig_explanation")
#     p.add("st_mid_stoney_church_tower")
#     p.add("st_mid_blackberry_big_room")
#     p.add("st_mid_blackberry_secret_wp")
#     p.add("st_mid_jericho_secret")
#     p.add("st_mid_catacombs_secret")
#     p.add("st_mid_camels_hump")
#     p.add("st_mid_orange_outer_mantle")
#     p.add("st_mid_mossy_basement")
#     p.add("st_mid_mossy_cellar")
#     p.add("st_mid_tweed_haunted")
#     p.add("st_mid_huntington_blue_secret")

#     --I1.
#     p.add("st_i1_botany_caves_red_cube")
#     p.add("st_i1_lib_vault")
#     p.add("st_i1_inf_flower_secret_entrance")
#     p.add("st_i1_williston_pyramid_secret")
#     p.add("st_i1_williston_building_top")
#     p.add("st_i1_bristol_maze_start")

#     --I2.
#     p.add("st_i2_lib_vault")
#     p.add("st_i2_fanatic_island_secret")
#     p.add("st_i2_fanatic_island_well_secret")
#     p.add("st_i2_spruce_tree")
#     p.add("st_i2_mini_ammo_purple_pod")
#     p.add("st_i2_fanatic_blue")
#     p.add("st_i2_emp_city")
#     p.add("st_i2_bubble_cave_core")
#     p.add("st_i2_i2vb_lbv")
#     p.add("st_i2_i2vb_toronto")
#     p.add("st_i2_i2vb_yellow")
#     p.add("st_i2_toronto_maze_secret_1")
#     p.add("st_i2_toronto_maze_secret_2")
#     p.add("st_i2_toronto_maze_secret_3")
#     p.add("st_i2_small_blue_flower_quaternary")
#     p.add("st_i2_violets_secret_1")
#     p.add("st_i2_violets_secret_2")
#     p.add("st_i2_violets_secret_3")
#     p.add("st_i2_woody_basement")
#     p.add("st_i2_earthy_basement")
#     p.add("st_i2_damp_basement")
#     p.add("st_i2_moldy_basement")
#     p.add("st_i2_woody_cellar")
#     p.add("st_i2_earthy_cellar")
#     p.add("st_i2_damp_cellar")
#     p.add("st_i2_wig_prison_2")
#     p.add("st_i2_pink_puzzle")

#     --I3.
#     p.add("st_i3_colchester_secret")
#     p.add("st_i3_essex")
#     p.add("st_i3_carrots")
#     p.add("st_i3_pumpkin")
#     p.add("st_i3_grow_temple")
#     p.add("st_i3_forest_museum")
#     p.add("st_i3_desert_flower_cloud")
#     p.add("st_i3_mahogany_inside")
#     p.add("st_i3_treetop")
#     p.add("st_i3_turnips")
#     p.add("st_i3_beets_above")
#     p.add("st_i3_mahogany_basement")
#     p.add("st_i3_root_veg_basement")
#     p.add("st_i3_mahogany_cellar")

#     --Burlington.
#     p.add("st_bur_tower")
#     p.add("st_bur_green_apple_club_hell")

#     --Space.
#     p.add("st_space_lib_secret_1")
#     p.add("st_space_lib_secret_2")
#     p.add("st_space_tau_caves_moon_secret")
#     p.add("st_space_high_gold_asteroid")
#     p.add("st_space_galaxy_flower_secret")
#     p.add("st_space_grand_lockbox")
#     p.add("st_space_root_secret")
#     p.add("st_space_root_pink_prison")

#     --Mylantis.
#     p.add("st_my_under")
#     p.add("st_my_city_hol")
#     p.add("st_my_city_secret_nuke_room")
#     p.add("st_my_caves_lib_secret")
#     p.add("st_my_jade_museum")

#     --Hell.
#     p.add("st_hell_secret_wolf_forest")
#     p.add("st_hell_moon_flower")
#     p.add("st_hell_credits_inf2_story")

#     --No waypoint (NWP).
#     p.add("st_nwp_small_white_flower_maze")
#     p.add("st_nwp_small_black_flower_bottom")
#     p.add("st_nwp_health_tower_secret")
#     p.add("st_nwp_paper_box")
#     p.add("st_nwp_cardboard_box")
#     p.add("st_nwp_wood_box")
#     p.add("st_nwp_steel_box")
#     p.add("st_nwp_quicksand_purple_house")
#     p.add("st_nwp_quicksand_basement")
#     p.add("st_nwp_red_rose")
#     p.add("st_nwp_white_rose")
#     p.add("st_nwp_beta_cube")
###