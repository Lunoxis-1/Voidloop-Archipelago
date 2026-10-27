from dataclasses import dataclass

from Options import Choice, OptionGroup, PerGameCommonOptions, Range, Toggle

# Have to set this up later. Just left the APQuest options as reference.




# In this file, we define the options the player can pick.
# The most common types of options are Toggle, Range and Choice.

# Options will be in the game's template yaml.
# They will be represented by checkboxes, sliders etc. on the game's options page on the website.
# (Note: Options can also be made invisible from either of these places by overriding Option.visibility.
#  APQuest doesn't have an example of this, but this can be used for secret / hidden / advanced options.)

# For further reading on options, you can also read the Options API Document:
# https://github.com/ArchipelagoMW/Archipelago/blob/main/docs/options%20api.md


# The first type of Option we'll discuss is the Toggle.
# A toggle is an option that can either be on or off. This will be represented by a checkbox on the website.
# The default for a toggle is "off".
# If you want a toggle to be on by default, you can use the "DefaultOnToggle" class instead of the "Toggle" class.
class EvilMode(Toggle):
    """
    Does nothing. Exists to satisfy a requirement.
    """
    display_name = "Evil Mode"



# class TrapChance(Range):
#     """
#     Percentage chance that any given Confetti Cannon will be replaced by a Math Trap.
#     """
#
#     display_name = "Trap Chance"
#
#     range_start = 0
#     range_end = 100
#     default = 0
#
#
# class StartWithOneConfettiCannon(Toggle):
#     """
#     Start with a confetti cannon already in your inventory.
#     Why? Because you deserve it. You get to celebrate yourself without doing any work first.
#     """
#
#     display_name = "Start With One Confetti Cannon"


# A Range is a numeric option with a min and max value. This will be represented by a slider on the website.
# class ConfettiExplosiveness(Range):
#     """
#     How much confetti each use of a confetti cannon will fire.
#     """
#
#     display_name = "Confetti Explosiveness"
#
#     range_start = 0
#     range_end = 10
#
#     # Range options must define an explicit default value.
#     default = 3


# A Choice is an option with multiple discrete choices. This will be represented by a dropdown on the website.
# class PlayerSprite(Choice):
#     """
#     The sprite that the player will have.
#     """
#
#     display_name = "Player Sprite"
#
#     option_human = 0
#     option_duck = 1
#     option_horse = 2
#     option_cat = 3
#
#     # Choice options must define an explicit default value.
#     default = option_human
#
#     # For choices, you can also define aliases.
#     # For example, we could make it so "player_sprite: kitty" resolves to "player_sprite: cat" like this:
#     alias_kitty = option_cat

class Leversanity(Choice):
    """
    Enables levers being checks. Adds 19 checks per region (95 total).
    Some special room types don't have levers.
    """

    display_name = "Leversanity"

    option_off = 0
    option_20_per_region = 1

    default = 0



class ExitsAreLevers(Toggle):
    """
    When enabled, the floor exit will also trigger lever checks.
    When disabled, some lever checks will require additional runs, as rooms can occasionally spawn without one.
    Regardless of setting, floor 20 is never a check for Leversanity.
    """

    display_name = "Exits are levers"




# We must now define a dataclass inheriting from PerGameCommonOptions that we put all our options in.
# This is in the format "option_name_in_snake_case: OptionClassName".
@dataclass
class VoidloopOptions(PerGameCommonOptions):
    leversanity: Leversanity
    exits_are_levers: ExitsAreLevers


# If we want to group our options by similar type, we can do so as well. This looks nice on the website.
option_groups = [
    OptionGroup(
        "Sanities",
        [Leversanity, ExitsAreLevers],
    ),
    # OptionGroup(
    #     "Aesthetic Options",
    #     [ConfettiExplosiveness, PlayerSprite],
    # ),
]

# Finally, we can define some option presets if we want the player to be able to quickly choose a specific "mode".
option_presets = {
    "Max Difficulty": {
        "leversanity": Leversanity.option_20_per_region,
        "exits_are_levers": False,
    },
    # "the true way to play": {
    #     "hard_mode": True,
    #     "hammer": True,
    #     "extra_starting_chest": True,
    #     "start_with_one_confetti_cannon": True,
    #     "trap_chance": 50,
    #     "confetti_explosiveness": ConfettiExplosiveness.range_end,
    #     "player_sprite": PlayerSprite.option_duck,
    # },
}