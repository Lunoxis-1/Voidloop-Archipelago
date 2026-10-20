# Imports.

from __future__ import annotations

from typing import TYPE_CHECKING

from BaseClasses import Entrance, Region

if TYPE_CHECKING:
    from .world import VoidloopWorld

def create_and_connect_regions(world: VoidloopWorld) -> None:
    create_all_regions(world)
    connect_regions(world)


def create_all_regions(world: VoidloopWorld) -> None:
    menu = Region("Menu", world.player, world.multiworld)
    craggy_cavern = Region("Craggy Cavern", world.player, world.multiworld)
    desolate_dungeon = Region("Desolate Dungeon", world.player, world.multiworld)
    jagged_jungle = Region("Jagged Jungle", world.player, world.multiworld)
    slippery_sanctuary = Region("Slippery Sanctuary", world.player, world.multiworld)
    molten_mineshaft = Region("Molten Mineshaft", world.player, world.multiworld)
    the_void = Region("The Void", world.player, world.multiworld)

    regions = [menu, craggy_cavern, desolate_dungeon, jagged_jungle, slippery_sanctuary, molten_mineshaft, the_void]
    world.multiworld.regions += regions


def connect_regions(world: VoidloopWorld) -> None:
    menu = world.get_region("Menu")
    craggy_cavern = world.get_region("Craggy Cavern")
    desolate_dungeon = world.get_region("Desolate Dungeon")
    jagged_jungle = world.get_region("Jagged Jungle")
    slippery_sanctuary = world.get_region("Slippery Sanctuary")
    molten_mineshaft = world.get_region("Molten Mineshaft")
    the_void = world.get_region("The Void")

    menu.connect(craggy_cavern, "Entrance: Craggy Cavern")
    menu.connect(desolate_dungeon,"Entrance: Desolate Dungeon")
    menu.connect(jagged_jungle,"Entrance: Jagged Jungle")
    menu.connect(slippery_sanctuary,"Entrance: Slippery Sanctuary")
    menu.connect(molten_mineshaft,"Entrance: Molten Mineshaft")
    menu.connect(the_void,"Entrance: The Void")