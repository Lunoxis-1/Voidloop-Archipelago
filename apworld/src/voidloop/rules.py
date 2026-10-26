from __future__ import annotations

from typing import TYPE_CHECKING

from rule_builder.options import OptionFilter
from rule_builder.rules import Has, HasGroup, HasAll, Rule, True_

# from .options import HardMode

if TYPE_CHECKING:
    from .world import VoidloopWorld

def set_all_rules(world: VoidloopWorld) -> None:
    set_all_entrance_rules(world)
    set_all_location_rules(world)
    set_completion_condition(world)


def set_all_entrance_rules(world: VoidloopWorld) -> None:
    entrance_craggy_cavern = world.get_entrance("Entrance: Craggy Cavern")
    entrance_desolate_dungeon = world.get_entrance("Entrance: Desolate Dungeon")
    entrance_jagged_jungle = world.get_entrance("Entrance: Jagged Jungle")
    entrance_slippery_sanctuary = world.get_entrance("Entrance: Slippery Sanctuary")
    entrance_molten_mineshaft = world.get_entrance("Entrance: Molten Mineshaft")
    entrance_the_void = world.get_entrance("Entrance: The Void")


    world.set_rule(entrance_craggy_cavern, True_())
    world.set_rule(entrance_desolate_dungeon,
                   HasGroup("Pickaxe Upgrades", count=3) &
                   HasGroup("Sword Upgrades", count=2) &
                   HasGroup("Player Upgrades", count=2) &
                   Has("Progressive Region Gem", count=1)
                   )
    world.set_rule(entrance_jagged_jungle,
                   HasGroup("Pickaxe Upgrades", count=6) &
                   HasGroup("Sword Upgrades", count=4) &
                   HasGroup("Player Upgrades", count=4) &
                   Has("Progressive Region Gem", count=2)
                   )
    world.set_rule(entrance_slippery_sanctuary,
                   Has("Player Luck Upgrade", count=1) &
                   HasGroup("Ability Evolutions", count=1) &
                   HasGroup("Pickaxe Upgrades", count=9) &
                   HasGroup("Sword Upgrades", count=6) &
                   HasGroup("Player Upgrades", count=6) &
                   Has("Progressive Region Gem", count=3)
                   )
    world.set_rule(entrance_molten_mineshaft,
                   Has("Player Luck Upgrade", count=2) &
                   HasGroup("Ability Evolutions", count=2) &
                   HasGroup("Pickaxe Upgrades", count=12) &
                   HasGroup("Sword Upgrades", count=9) &
                   HasGroup("Player Upgrades", count=8) &
                   Has("Progressive Region Gem", count=4)
                   )
    world.set_rule(entrance_the_void,
                   Has("Player Luck Upgrade", count=3) &  # Max obtainable: 5
                   HasGroup("Ability Evolutions", count=3) &  # Max obtainable: 6
                   HasGroup("Pickaxe Upgrades", count=15) &  # Max obtainable: 20
                   HasGroup("Sword Upgrades", count=12) &  # Max obtainable: 20
                   HasGroup("Player Upgrades", count=8) &  # Max obtainable: 14
                   Has("Progressive Region Gem", count=5)  # Max obtainable: 5, absolute requirement
                   )



    # Some entrance rules may only apply if the player enabled certain options.
    # In our case, if the hammer option is enabled, we need to add the Hammer requirement to the Entrance from
    # Overworld to the Top Middle Room.
    #if world.options.hammer:
        #overworld_to_top_middle_room = world.get_entrance("Overworld to Top Middle Room")
        #can_smash_brick = Has("Hammer")
        #world.set_rule(overworld_to_top_middle_room, can_smash_brick)



def set_all_location_rules(world: VoidloopWorld) -> None:

    return_to_sender = world.get_location("Return to Sender")
    # Given worst possible actions, max skill points needed for master ninja is 23.
    world.set_rule(return_to_sender, Has("Skill Point", 23))

    #craggy_cavern_treasure = world.get_location("Dungeon Gem")

    # Each dash upgrade (Group: "Dash Upgrades") is 1 point,
    # each dash evolution (Item: "Dash Evolution") is 3 (technically 2, since it's also in the dash upgrades group),
    # and each movement speed upgrade (Item: "Player Speed Upgrade") is 3.
    # This location should be accessible if the player has at least 4 of these points.
    # (Other regions will need more.)

    #can_reach_craggy_cavern_floor_20: Rule = Has("")
    #world.set_rule(craggy_cavern_treasure, can_reach_craggy_cavern_floor_20)


def set_completion_condition(world: VoidloopWorld) -> None:
    world.set_completion_rule(Has("Home"))