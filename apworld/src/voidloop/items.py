# Imports.

from __future__ import annotations

from typing import TYPE_CHECKING

from . import constants

import time

import logging

from BaseClasses import Item, ItemClassification

if TYPE_CHECKING:
     from .world import VoidloopWorld

from .constants import ITEM_NAME_TO_ID, ID_TO_ITEM_NAME, DEFAULT_ITEM_CLASSIFICATION, ITEM_COUNT

class VoidloopItem(Item):
    game = "Voidloop"

def get_random_filler_item_name(world: VoidloopWorld) -> str:
    # IMPORTANT: Whenever you need to use a random generator, you must use world.random.
    # This ensures that generating with the same generator seed twice yields the same output.
    # DO NOT use a bare random object from Python's built-in random module.
    random_float = world.random.random()
    if random_float < 0.05:
        return "Voidrock"
    else:
        return  "Random Loot"


def create_item_with_correct_classification(world: VoidloopWorld, name: str) -> VoidloopItem:
    classification = constants.DEFAULT_ITEM_CLASSIFICATION.get(name) or ItemClassification.filler

    return VoidloopItem(name, classification, ITEM_NAME_TO_ID[name], world.player)


def create_all_items(world: VoidloopWorld) -> None:
    itempool = []

    # Currently, there's no options, so we can just ignore everything below and insert items.
    for k, v in ID_TO_ITEM_NAME.items():
        item_count = ITEM_COUNT[k] # Deliberately unsafe. This should error if something goes wrong!
        for i in range(item_count):
            itempool.append(world.create_item(v))

    number_of_items = len(itempool)

    number_of_unfilled_locations = len(world.multiworld.get_unfilled_locations(world.player))

    needed_number_of_filler_items = number_of_unfilled_locations - number_of_items

    itempool += [world.create_filler() for _ in range(needed_number_of_filler_items)]

    world.multiworld.itempool += itempool


