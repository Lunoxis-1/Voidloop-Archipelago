#nullable enable

using BepInEx;
using BepInEx.Logging;
using Voidloop_Archipelago.Archipelago;
using Voidloop_Archipelago.Utils;
using UnityEngine;
using HarmonyLib;
using Archipelago.MultiClient.Net.Exceptions;

using System.Collections.Generic;
using Archipelago.MultiClient.Net.Helpers;
using UnityEngine.Assertions;
using Archipelago.MultiClient.Net;
using System;
using System.Reflection;

using TMPro;
using UnityEngine.UIElements.Collections;
using System.Collections;
using System.Data.Common;
using Archipelago.MultiClient.Net.Models;
using UnityEngine.Rendering;
using System.Threading.Tasks;
using Newtonsoft.Json;
using UnityEngine.InputSystem;
using System.Linq;
using UnityEngine.Pool;

namespace Voidloop_Archipelago;


[BepInPlugin(PluginGUID, PluginName, PluginVersion)]
[BepInProcess("Voidloop.exe")]
public class Plugin : BaseUnityPlugin
{
    public const string PluginGUID = "com.lunoxis.voidloopArchipelago";
    public const string PluginName = "Voidloop_Archipelago";
    public const string PluginVersion = "0.0.1";

    public const string ModDisplayInfo = $"{PluginName} v{PluginVersion}";
    private const string APDisplayInfo = $"Archipelago v{ArchipelagoClient.APVersion}";
    public static ManualLogSource BepinLogger = null!;
    public static ArchipelagoClient ArchipelagoClient = null!;

    public static LootManager? lootManagerCache = null!;
    public static GameData? gameDataCache = null!;
    public static Plugin plugin = null!;

    public static JsonSerializerSettings settings = new JsonSerializerSettings()
                {
                    ReferenceLoopHandling = ReferenceLoopHandling.Ignore
                };

    private void Awake()
    {
        plugin = this;

        // Plugin startup logic
        BepinLogger = Logger;
        ArchipelagoClient = new ArchipelagoClient();
        ArchipelagoConsole.Awake();

        ArchipelagoConsole.LogMessage($"{ModDisplayInfo} loaded!");

        var harmony = new Harmony(PluginGUID);
        harmony.PatchAll();
        ArchipelagoConsole.LogMessage("Loading! is loaded!");
    }

    private void Update()
    {

            
            // This is temporary
            // This also means that not having an inventory will block item handling
            // Good news: I have a keyboard. not my problem!
            // // (remove before production release)
            // if (Keyboard.current == null) return; 

            // if (Keyboard.current.f4Key.wasPressedThisFrame)
            // {
            //     ArchipelagoClient.itemQueue.Enqueue(101);
            // }
            // if (Keyboard.current.f5Key.wasPressedThisFrame)
            // {
            //     ArchipelagoClient.itemQueue.Enqueue(102);
            // }
            
            // if (Keyboard.current.f6Key.wasPressedThisFrame)
            // {
            //     ArchipelagoClient.itemQueue.Enqueue(110);
            // }

            // "variable declaration can be inlined" yeah but my eyes can't so uhh skill issue
            long itemId;
            bool success = ArchipelagoClient.itemQueue.TryDequeue(out itemId);
            if (!success) return;

            // Yes this only does one item per frame. At most this will take 5 seconds, so it's not a big deal.
            // Besides the sound it makes ingame with the item popups is cooler this way.

            switch (itemId)
            {
                case 1:
                    ArchipelagoConsole.LogMessage("You have beaten your game!");
                    ArchipelagoClient.session.SetGoalAchieved();
                    break;

                // These need to be saved otherwise loot will be duplicated when the client restarts
                // As filler items, they dont matter that much though.
                // Random Loot
                case 101:
                    PlayerUpgrades.Filler_RandomLootRecieved += 1;
                    if (PlayerUpgrades.Filler_RandomLootRecieved <= ArchipelagoClient.apData.ProcessedRandomLoot) return;
                    ArchipelagoClient.apData.ProcessedRandomLoot += 1;
                    GivePlayerLoot(false);
                    _ = ArchipelagoClient.SaveAPData();
                    break;

                // GOLDEN CHEST...
                case 102:
                    PlayerUpgrades.Filler_RandomGoldenLootRecieved += 1;
                    if (PlayerUpgrades.Filler_RandomGoldenLootRecieved <= ArchipelagoClient.apData.ProcessedRandomGoldenLoot) return;
                    ArchipelagoClient.apData.ProcessedRandomGoldenLoot += 1;
                    GivePlayerLoot(true);
                    _ = ArchipelagoClient.SaveAPData();
                    break;

                // Voidrock
                case 110:
                    PlayerUpgrades.Filler_VoidrocksRecieved += 1;
                    if (PlayerUpgrades.Filler_VoidrocksRecieved <= ArchipelagoClient.apData.ProcessedVoidrocks) return;
                    ArchipelagoClient.apData.ProcessedVoidrocks += 1;
                    GivePlayerItem("voidrock", 1);
                    _ = ArchipelagoClient.SaveAPData();
                    break;


                // These should not be saved, they are to be reevaluated on client restart, as the variables reset too.
                // Doing it this way prevents against softlocking if the archipelago servers go down mid check. 
                // Skill Point + Force Update. 
                case 900:
                    PlayerUpgrades.SkillPointCount += 1;
                    GameData? gameData = Plugin.GetGameData();
                    if (gameData is null) break;
                    SkillsDatabase? skillsDatabase = gameData.skillsDatabase;
                    if (skillsDatabase is null) break;
                    AchievementDatabase? achievementDatabase = gameData.achievementDatabase;
                    if (achievementDatabase is null) break;
                    skillsDatabase.CalculateSkillPoints(achievementDatabase);
                    break;

                // Player Pickaxe Upgrades.
                case 1101:
                    PlayerUpgrades.PickaxeDamage += 1;
                    break;
                case 1102:
                    PlayerUpgrades.PickaxeSpeed += 1;
                    break;
                case 1103:
                    PlayerUpgrades.PickaxeRange += 1;
                    break;

                // Player Sword Upgrades.
                case 1111:
                    PlayerUpgrades.SwordDamage += 1;
                    break;
                case 1112:
                    PlayerUpgrades.SwordSpeed += 1;
                    break;
                case 1113:
                    PlayerUpgrades.SwordRange += 1;
                    break;

                // Player Upgrades.
                case 1121:
                    PlayerUpgrades.Luck += 1;
                    break;
                case 1122:
                    PlayerUpgrades.MaxHealth += 1;
                    break;
                case 1123:
                    PlayerUpgrades.Speed += 1;
                    break;
                case 1124:
                    PlayerUpgrades.Resistance += 1;
                    break;

                // Blast Ability Upgrades.
                case 1131:
                    PlayerUpgrades.BlastPhase += 1;
                    break;
                case 1132:
                    PlayerUpgrades.BlastCooldown += 1;
                    break;
                case 1133:
                    PlayerUpgrades.BlastDamage += 1;
                    break;
                case 1134:
                    PlayerUpgrades.BlastSize += 1;
                    break;

                // Dash Ability Upgrades.
                case 1141:
                    PlayerUpgrades.DashPhase += 1;
                    break;
                case 1142:
                    PlayerUpgrades.DashCooldown += 1;
                    break;
                case 1143:
                    PlayerUpgrades.DashDamage += 1;
                    break;
                case 1144:
                    PlayerUpgrades.DashPower += 1;
                    break;

                // Energise Ability Upgrades.
                case 1151:
                    PlayerUpgrades.EnergisePhase += 1;
                    break;
                case 1152:
                    PlayerUpgrades.EnergiseCooldown += 1;
                    break;
                case 1153:
                    PlayerUpgrades.EnergiseMultiplier += 1;
                    break;
                case 1154:
                    PlayerUpgrades.EnergiseDuration += 1;
                    break;
                
                
                // Progressive Region Gem
                case 1190:
                    PlayerUpgrades.ProgressiveRegionGemCount += 1;
                    BepinLogger.LogWarning("GEM COUNT: "+PlayerUpgrades.ProgressiveRegionGemCount.ToString());

                    // For each gem type, if they don't have it or the resulting key, grant the gem.
                    // Thankfully the game already has a helper function that does exactly this.
                    if (PlayerUpgrades.ProgressiveRegionGemCount >= 1)
                    {
                        GivePlayerGem("Dungeon");
                    }
                    if (PlayerUpgrades.ProgressiveRegionGemCount >= 2)
                    {
                        GivePlayerGem("Jungle");
                    }
                    if (PlayerUpgrades.ProgressiveRegionGemCount >= 3)
                    {
                        GivePlayerGem("Ice");
                    }
                    if (PlayerUpgrades.ProgressiveRegionGemCount >= 4)
                    {
                        GivePlayerGem("Lava");
                    }
                    if (PlayerUpgrades.ProgressiveRegionGemCount >= 5)
                    {
                        GivePlayerGem("Void");
                    }


                    break;


                // Log Unknown ID.
                default:
                    ArchipelagoConsole.LogMessage("Bad Item ID: "+itemId.ToString());
                    break;
            }

    }

    private void OnGUI()
    {
        // show the mod is currently loaded in the corner
        GUI.Label(new Rect(16, 16, 300, 20), ModDisplayInfo);
        ArchipelagoConsole.OnGUI();

        string statusMessage;
        // show the Archipelago Version and whether we're connected or not
        if (ArchipelagoClient.Authenticated)
        {
            // if your game doesn't usually show the cursor this line may be necessary
            // Cursor.visible = false;

            statusMessage = " Status: Connected";
            GUI.Label(new Rect(16, 50, 300, 20), APDisplayInfo + statusMessage);
        }
        else
        {
            // if your game doesn't usually show the cursor this line may be necessary
            // Cursor.visible = true;

            
            float fieldGap = 20f;
            float centerX = UnityEngine.Screen.width/2;
            float centerY = (UnityEngine.Screen.height/2)-10; 

            statusMessage = " Status: Disconnected";
            GUI.Label(new Rect(16, 50, 300, 20), APDisplayInfo + statusMessage);
            GUI.Label(new Rect(centerX - 75, centerY - (fieldGap*4), 150, 20), "Host: ");
            GUI.Label(new Rect(centerX - 75, centerY - (fieldGap*1), 150, 20), "Player Name: ");
            GUI.Label(new Rect(centerX - 75, centerY + (fieldGap*2), 150, 20), "Password: ");



            ArchipelagoClient.ServerData.Uri = GUI.TextField(new Rect(centerX - 75, centerY + 10 - (fieldGap*3) - 10, 150, 20),
                ArchipelagoClient.ServerData.Uri);
            ArchipelagoClient.ServerData.SlotName = GUI.TextField(new Rect(centerX - 75, centerY, 150, 20),
                ArchipelagoClient.ServerData.SlotName);
            ArchipelagoClient.ServerData.Password = GUI.TextField(new Rect(centerX - 75, centerY + 10 + (fieldGap*3) - 10, 150, 20),
                ArchipelagoClient.ServerData.Password);

            // requires that the player at least puts *something* in the slot name
            if (GUI.Button(new Rect(centerX - 50, centerY + 10 + (fieldGap*4), 100, 20), "Connect") &&
                !ArchipelagoClient.ServerData.SlotName.IsNullOrWhiteSpace())
            {
                ArchipelagoClient.Connect();
            }
        }
        // this is a good place to create and add a bunch of debug buttons
    }

    public static GameData? GetGameData()
    {
        if (gameDataCache is not null)
        {
            return gameDataCache;
        }   
        else
        {
            gameDataCache = FindFirstInstanceOfClass<GameData>() ?? null;
            return gameDataCache;
        }
    }

    public static LootManager? GetLootManager()
    {
        if (lootManagerCache is not null)
        {
            return lootManagerCache;
        }   
        else
        {
            lootManagerCache = FindFirstInstanceOfClass<LootManager>() ?? null;
            return lootManagerCache;
        }
    }

    public static LevelManager.CaveVariants GetCurrentRegion()
    {
        GameData? gameData = GetGameData();
        if (gameData is null) return LevelManager.CaveVariants.Default; // dotting i and crossing t's. this condition is impossible to reach but the linter complains without it.

        if (gameData.IsCaveUnlocked(LevelManager.CaveVariants.Lava))
        {
            return LevelManager.CaveVariants.Lava;
        }
        else if (gameData.IsCaveUnlocked(LevelManager.CaveVariants.Frozen))
        {
            return LevelManager.CaveVariants.Frozen;
        }
        else if (gameData.IsCaveUnlocked(LevelManager.CaveVariants.Jungle))
        {
            return LevelManager.CaveVariants.Jungle; 
        }
        else if (gameData.IsCaveUnlocked(LevelManager.CaveVariants.Dungeon))
        {
            return LevelManager.CaveVariants.Dungeon;   
        }

        // Even if the player is in the tutorial and has no caves unlocked, we should return the default cave.
        return LevelManager.CaveVariants.Default;
    }

    public static C? FindFirstInstanceOfClass<C>() where C : UnityEngine.Object
    {
        C classInstance = FindAnyObjectByType<C>(FindObjectsInactive.Include);
        if (classInstance is null)
        {
            BepinLogger.LogWarning("Warning: " + typeof(C).Name + " is not ready yet!");
            return null;
        }
        return classInstance;
    }




    private static void SubmitCheck(List<long> locationIds)
    {
        try
        {
            ArchipelagoClient.SendLocations(locationIds);
        }
        catch (ArchipelagoSocketClosedException) {
            ArchipelagoConsole.LogMessage("WARNING: Not connected, a packet was dropped! Please restart the application to resync!");
        }
    }

    public static void GivePlayerGem(string gemType)
    {
        GameData? gameData = GetGameData();
        if (gameData is null) return;

        Inventory? inventoryInstance = gameData.playerInventory;
        if (inventoryInstance is null) return;

        string? gemId = gemType switch
        {
            "Dungeon" => "dungeon_gem",
            "Jungle" => "jungle_gem",
            "Ice" => "ice_gem",
            "Lava" => "lava_gem",
            "Void" => "voidgem", // you troll...
            _ => null,
        };

        BepinLogger.LogWarning("GIVING GEM "+gemId);

        if (gemId is null)
        {
            BepinLogger.LogError("Unknown Gem: "+gemType.ToString());
            return;
        };

        // Check that the player doesn't already own the gem.
        bool hasGem = inventoryInstance.GetDictionary().ContainsKey(gemId) && inventoryInstance.GetDictionary()[gemId].count > 0;
        if (hasGem)
        {
            // BepinLogger.LogWarning("HAS GEM!!");
            // BepinLogger.LogWarning("HAS KEY: "+inventoryInstance.GetDictionary().ContainsKey(gemId).ToString());
            // BepinLogger.LogWarning("HAS GEM: "+(inventoryInstance.GetDictionary()[gemId].count > 0).ToString());
        }
        else
        {
            GivePlayerItem(gemId, 1);
        }

        
    }

    // Generates random loot for the player
    public static void GivePlayerLoot(bool isGolden)
    {
        LootManager? lootManager = GetLootManager();
        if (lootManager is null) return;

        Dictionary<ILoot, int> generatedLoot = [];
        if (isGolden)
        {
            generatedLoot = lootManager.GenerateGoldenChest();
        }else
        {
            generatedLoot = lootManager.GenerateChestLoot(GetCurrentRegion());
        }

        foreach (var(key, value) in generatedLoot)
        {
            if (!(key is ItemScriptableObject item)) 
            {
                BepinLogger.LogError("Invalid item! Cannot be converted to usable form.");
                continue;
            }
            GivePlayerItem(item.itemId, value);
        }
        
    }



    // The code goblins weren't paid enough to accept a list. 
    // Stop being lazy and just call it multiple times instead.    
    // Unoptimized? Yes. Does it need to be optimized? It's called maybe... 10 times a minute?
    // Look just save it for the hotfix if it's really that bad.
    public static void GivePlayerItem(string? itemId, int count)
    {
        if (itemId is null)
        {
            BepinLogger.LogError("Missing itemID when trying to add player item! Traceback: "+Environment.StackTrace);
        }
        GameData? gameData = GetGameData();
        if (gameData is null) return;

        Inventory? inventoryInstance = gameData.playerInventory;
        if (inventoryInstance is null) return;

        inventoryInstance.AddToDictionary(itemId, count);
    }


    public static void AwardHatByName(string hatName)
    {
        long locationID = hatName switch
        {
            "beak" => 801,
            "boat" => 802,
            "cupid" => 803,
            "disguise" => 804,
            "eyepatch" => 805,
            "mohawk" => 806,
            "smile" => 807,
            "bunny" => 808,
            "cat" => 809,
            "cowboy" => 810,
            "dog" => 811,
            "fedora" => 812,
            "hardhat" => 813,
            "heart" => 814,
            "mushroom" => 815,
            "pumpkin" => 816,
            "reginald" => 817,
            "shades" => 818,
            "spaceman" => 819,
            "tophat" => 820,
            "cone" => 821,
            "wizard" => 82,
            "chef" => 823,
            "pink-cowboy" => 824,
            "crown" => 825,
            "frog" => 826,
            "propeller" => 827,
            "robot" => 828,
            "blonde" => 829,
            "capybara" => 830,
            "voidcrown" => 831,
            _ => -1,
        };

        SubmitCheck([locationID]);
    }

    public static void AwardAchievementByInternalName(string achievementName)
    {
        long locationId = achievementName switch
        {
            "happy-camper" => 901,
            "memento" => 902,
            "novice-explorer" => 903,
            "apprentice-explorer" => 904,
            "advanced-explorer" => 905,
            "master-explorer" => 906,
            "craggy-conquerer" => 907,
            "dungeon-destroyer" => 908,
            "jungle-jogger" => 909,
            "sanctuary-soldier" => 910,
            "molten-maniac" => 911,
            "welcome-home" => 912, // Unique as it's technically last on the ingame Ids, but this is placed by achievement menu order. This one got special treatment in the code i guess.
            "novice-hoarder" => 913,
            "advanced-hoarder" => 914,
            "master-hoarder" => 915,
            "novice-traveller" => 916,
            "advanced-traveller" => 917,
            "master-traveller" => 918,
            "novice-slayer" => 919,
            "advanced-slayer" => 920,
            "master-slayer" => 921,
            "novice-upgrader" => 922,
            "advanced-upgrader" => 923,
            "master-upgrader" => 924,
            "novice-brewer" => 925,
            "advanced-brewer" => 926,
            "master-brewer" => 927,
            "novice-learner" => 928,
            "advanced-learner" => 929,
            "master-learner" => 930,
            "novice-smelter" => 931,
            "advanced-smelter" => 932,
            "master-smelter" => 933,
            "novice-contractor" => 934,
            "advanced-contractor" => 935,
            "master-contractor" => 936,
            "bad-businessman" => 937,
            "good-businessman" => 938,
            "ability-appreciator" => 939,
            "ability-abuser" => 940,
            "entomophobia" => 941,
            "keen-eye" => 942,
            "exotic-killer" => 943,
            "millionaire" => 944,
            "anti-demolisionist" => 945, // [SIC]. Internal name is spelt wrong.
            "voidloop" => 946,
            "sweet-revenge" => 947,
            "overloaded" => 948,
            "return-to-sender" => 949,
            "empty" => 950,
            _ => -1000000 // Invalid ID
        };

        if (locationId <= -1)
        {
            achievementName ??= "Null";
            ArchipelagoConsole.LogMessage("ERROR! Bad Achievemnt Name: "+achievementName.ToString());
            return;
        }

        List<long> listLocationId = [locationId];
        SubmitCheck(listLocationId);
    }

    public static void AwardStatUpgradeByNameAndIndex(string statName, int upgradeNumber)
    {
        Assert.IsTrue(upgradeNumber <= 99, "Error: Upgrade number too large!");

        long baseLocationId = ArchipelagoClient.CatagoryToBaseId.GetValueOrDefault(statName, -1);

        if (baseLocationId <= -1)
        {
            statName ??= "Null";
            ArchipelagoConsole.LogMessage("ERROR! Bad Stat Name: "+statName.ToString());
            return;
        }

        
        List<long> listLocationId = [];

        // Go backwards, this will catch any missed checks.
        for (int i = upgradeNumber; i >= 1; i--)
        {
            listLocationId.Add(baseLocationId + i);
        }

        SubmitCheck(listLocationId);
    }


    public static int GetArchiUpgradeCountForStat(string statName)
    {
       var amount = typeof(PlayerUpgrades).GetProperty(statName, BindingFlags.Public | BindingFlags.Static)?.GetValue(null);
       return (int?)amount ?? -1;
    }


    [HarmonyPatch(typeof(GameManager), "TryEnterCamp")]
    public static class GameManager_TryEnterCamp_Patch
    {
        public static void Postfix()
        {

            _ = ArchipelagoClient.LoadAPData();
        }

    }


    // grab the game's gamedata at creation and get gamedata from it
    [HarmonyPatch(typeof(GameData))]
    public static class GameData_Constructor_Patch
    {
        // This has no awake(). Workaround!
        [HarmonyPatch(MethodType.Constructor)]
        [HarmonyPrefix]
        public static bool Prefix(GameData __instance)
        {
            if (gameDataCache)
            {
                //BepinLogger.LogWarning("Ignoring new GameData with handle: "+ __instance.GetInstanceID().ToString());
                return true;
            }
            gameDataCache = __instance;
            BepinLogger.LogInfo("Found GameData! GameData Handle: " + __instance.GetInstanceID().ToString());
            return true;
        }

    }

    // repeat for lootmanager
    [HarmonyPatch(typeof(LootManager))]
    public static class LootManager_Constructor_Patch
    {
        [HarmonyPatch(MethodType.Constructor)]
        [HarmonyPrefix]
        public static bool Prefix(LootManager __instance)
        {
            if (lootManagerCache)
            {
                //BepinLogger.LogWarning("Ignoring new LootManager with handle: "+ __instance.GetInstanceID().ToString());
                return true;
            }
            lootManagerCache = __instance;
            BepinLogger.LogInfo("Found LootManager! LootManager Handle: " + __instance.GetInstanceID().ToString());
            return true;
        }

    }



    [HarmonyPatch(typeof(GameData), "GetFullPath")]
    public static class GameData_GetFullPath_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(GameData __instance, ref string  __0)
        {
            if (ArchipelagoClient.session is null)
            {
                string saveName = "MultiWorld_Invalid"; // Tell the game to save here until we get our shit together
                __0 = saveName;
            }
            else
            {
                string saveName = "MultiWorld_Data_" + ArchipelagoClient.session.RoomState.Seed + "_" + ArchipelagoClient.session.ConnectionInfo.Slot + ".data"; 
                __0 = saveName;
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(Init), "CanStartGame")]
    public static class Init_CanStartGame_Patch
    {
        [HarmonyPostfix]
        public static void Postfix(Init __instance, ref bool __result)
        {
            bool isReady = ArchipelagoClient.session is not null;
            __result = isReady;
        }
    }


    [HarmonyPatch(typeof(Inventory), "SoundLogic")]
    public static class Inventory_SoundLogic_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(Inventory __instance, ItemScriptableObject item)
        {
	        {
                if (!AudioManager.Instance)
                {
                    return false;
                }
                if (!__instance.popupSoundInstance.isValid() || !__instance.rarePopupSoundInstance.isValid())
                {
                    __instance.SoundSetup();
                }
                if (!__instance.popupSoundInstance.isValid() || !__instance.rarePopupSoundInstance.isValid())
                {
                    // This means the sound init got canceled by the menu protection.
                    return false;
                }
                return true;
	        }
        }

    }

    public static void CheckThread(string? name)
    {
            BepinLogger.LogWarning("CHECKING THREAD TYPE FOR " + (name ?? "(no name given)"));
            if (ThreadingHelper.Instance.InvokeRequired)
            {
                BepinLogger.LogWarning("ON WORKER");
            }
            else
            {
                BepinLogger.LogWarning("ON MAIN");
            }
    }


    // Prevents bad itemIds from crashing. Shouldn't happen but im scraed to remove this now.
    [HarmonyPatch(typeof(Inventory), "AddToDictionary")]
    public static class Inventory_AddToDictionary_Patch
    {
        [HarmonyPrefix]
    	public static bool Prefix(Inventory __instance, string loot, ref int count)
        {
            // Guard against bad itemIDs taking down the entire program
            ItemScriptableObject? itemScriptableObject = LootManager.GetLootScriptableObject(loot) as ItemScriptableObject;
            if (itemScriptableObject is null)
            {
                BepinLogger.LogError("UNKNOWN ITEM: "+(loot ?? "Null"));
                return false;
            }
            BepinLogger.LogWarning(loot);
            // count *= 10; // temp for testing
            //CheckThread("Inventory_AddToDictionary");

            return true;
        }
    }

    
    // Anytime the achievements update themselves, check if it's ready :eyes:
    [HarmonyPatch(typeof(AchievementPanel), "SetUnlocked")]
    public static class AchievementPanel_SetUnlocked_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(AchievementPanel __instance)
        {

            var isUnlocked = __instance.database.achievementStates[__instance.achievement.id].unlocked;

            if (isUnlocked)
            {
                AwardAchievementByInternalName(__instance.achievement.id);
            }

            return true;
        }

    }


    // HAT CHECKS...
    [HarmonyPatch(typeof(HatDatabaseSO), "UnlockHat")]
    public static class HatDatabaseSO_UnlockHat_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(HatDatabaseSO __instance, HatSO __0)
        {
            AwardHatByName(__0.hatID);

            if (ArchipelagoClient.doneHatSync) return true;
            ArchipelagoClient.doneHatSync = true;

            foreach ((string name, HatDatabaseSO.HatState hatstate) in __instance.hatStates)
            {
                if (hatstate.unlocked)
                {
                    AwardHatByName(__0.hatID);
                }
            }

            return true;
        }

    }
 

    // This patch intercepts text generation for the upgrade shop and replaces it with Archipelago infomation.
    [HarmonyPatch(typeof(UnlockPanel), "SetPanel")]
    public static class UnlockPanel_SetPanel_Patch
    {
        [HarmonyPostfix]
        public static void Postfix(UnlockPanel __instance) 
        {

            // why is this like the only subclass in the entire game
            if (__instance is PotionUnlockPanel p) return;

            // Call me confused cause i'm ?.?.?.?.?? false
            if (__instance.unlockable.itemReward?.Attributes.HasFlag(ItemScriptableObject.ItemAttributes.IsKey) ?? false) return;
            
            
            string statName = __instance.unlockable.unlockType.ToString();

            long internalBaseId = ArchipelagoClient.CatagoryToBaseId.Get(statName, -1000000);
            int nextUpgradeId = __instance.unlockable.statReward.StatIndex + 1;
            
            ScoutedItemInfo? scouteditemInfo = null;
            if (ArchipelagoClient.scoutedLocationList is not null)
            {
            scouteditemInfo = ArchipelagoClient.scoutedLocationList.Get(internalBaseId + nextUpgradeId, null);
            }

            string? itemTagline = null;
            if (scouteditemInfo is not null)
            {
                itemTagline = scouteditemInfo.Player?.Alias + "'s " + scouteditemInfo.ItemName;
            }
            else
            {

                itemTagline = "Unknown Archipelago Item";
            }


            var valueText = string.Concat([
                    "<style=SubheaderPrimary>",
                    "<color=#",
                    ColorUtility.ToHtmlStringRGB(__instance.previewPreviousColor),
                    ">",
                    "Value: ",
                    // Offset 0 from current index. This function was overridden elsewhere so it will return the archipelago appropiate value
                    __instance.unlockable.statReward.GetStatValue(0),
                    " (AP Upgrades: ",
                    GetArchiUpgradeCountForStat(statName).ToString(),
                    "/",
                    __instance.unlockable.statReward.MaxValue.ToString(),
                    ")",
                    "</color>"
                ]);
            

            var newText = string.Concat([
                    "<style=SubheaderPrimary>",
                    "<color=#",
                    ColorUtility.ToHtmlStringRGB(__instance.previewNextColor),
                    ">",
                    "+ ",
                    itemTagline,
                    "</color>"
                ]);



            if (__instance.unlockPreviewText is not null)
            {
                __instance.unlockPreviewText.text = newText;
            }
            else
            {
			    __instance.unlockDesc.text = valueText + "\n" + newText;//__instance.unlockDesc.text + "\n" + newText;
            }



            return;
        }
    }

    // This patch overwrites upgrade indexes with the value from PlayerUpgrades in ArchipelagoClient
    [HarmonyPatch(typeof(StatSO), "GetStatValue")]
    public static class StatSO_GetStatValue_Patch
    {
        [HarmonyPostfix]
        public static void Postfix(StatSO __instance, ref float __result, int __0) // __0 = int offset
        {
            StatSO.StatTypes statType = __instance.statType;
            string statName = statType.ToString();
            if (statName is null) {statName = "Null";}
            
            int upgradeAmount = GetArchiUpgradeCountForStat(statName);

            if (upgradeAmount == -1)
            {
                ArchipelagoConsole.LogMessage("field is null for "+statName.ToString());
                return;
            }

            if (!PlayerUpgrades.ResyncedStatTypes.Contains(statName))
            {
                // Quick unrelated check: Resync any upgrades that were missed.
                // In this case, we actually want the real upgrade number.
                var realUpgradeCount = __instance.StatIndex;

                PlayerUpgrades.ResyncedStatTypes.Add(statName);
                AwardStatUpgradeByNameAndIndex(statName, realUpgradeCount);

            }


            // If this errors, it's really the game's fault. But ill try catch it anyways.
            try 
            {
                float statValue = __instance.statValues[upgradeAmount + __0];
                __result = statValue;
            }
            catch (IndexOutOfRangeException)
            {
                // List will never be empty
                float statValue = __instance.statValues[^1];
                __result = statValue;
            }

            return;
            
        }
    }

     
    // This patch intercepts the skill point calculation, and injects the base value of the amount of skill points recieved from the archipelago server.
    [HarmonyPatch(typeof(SkillsDatabase), "CalculateSkillPoints")]
    public static class SkillsDatabase_CalculateSkillPoints_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(SkillsDatabase __instance, AchievementDatabase achievementDatabase)
        {
            // Fetch from archipelago the amount of skill points we should have.
            int num = PlayerUpgrades.SkillPointCount;
            //BepinLogger.LogInfo(num.ToString() + " skill points");

            // Iterate skills, subtract their cost.
            foreach (KeyValuePair<string, bool> skillState in __instance.skillStates)
            {
                if (skillState.Value)
                {
                    // Finder loop that breaks when it finds a match.
                    SkillSO skillSO = null!;
                    foreach (var s in __instance.skills!)
                    {
                        if (s != null && s.skillId == skillState.Key)
                        {
                            skillSO = s;
                            break;
                        }
                    }

                    // If valid and not null, subtract cost.
                    if (skillState.Value)
                    {
                        if (skillSO != null)
                        {
                            num -= skillSO.cost;
                        }
                    }
                }
            }
            if (__instance.skillPoints is null)
            {
                __instance.skillPoints = new IntVariable();
            }
            __instance.skillPoints.Value = num;


            return false;
        }
    }


    // This patch turns upgrades into checks.
    [HarmonyPatch(typeof(UnlockableSO), "BuyUnlock")]
    public static class UnlockableSO_BuyUnlock_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(UnlockableSO __instance)
        {
            // Ignore stats that are not specifically upgrades.
            // Item rewards are keys (which are not randoed) and potion rewards are... take a guess.
            if (__instance.isItemReward | __instance.isPotionReward)
            {
                return true;
            }

            StatSO statSO = __instance.statReward;
            StatSO.StatTypes statType = statSO.statType;

            int futureStatIndex = statSO.StatIndex + 1;

            AwardStatUpgradeByNameAndIndex(statType.ToString(), futureStatIndex);

            // Important that this runs anyway, since it progresses the upgrade counter.
            return true; 
        }
    }



    // This patch turns the level 20 gem of each floor into a check. The game already handles most of the heavy lifting here.
    [HarmonyPatch(typeof(GemLootTable), "TryAddGem")]
    public static class GemLootTable_TryAddGem_Patch
    {
        [HarmonyPrefix]
        public static bool Prefix(GemLootTable __instance, ref LevelManager.CaveVariants variant, ItemScriptableObject gem, Dictionary<ILoot, int> lootList)
        {
            string variantName = variant.ToString();

            switch (variantName)
            {
                case "Default":
                    SubmitCheck([119002]);
                    break;

                case "Dungeon":
                    SubmitCheck([119003]);
                    break;

                case "Jungle":
                    SubmitCheck([119004]);
                    break;

                case "Frozen":
                    SubmitCheck([119005]);
                    break;

                case "Lava":
                    SubmitCheck([119006]);
                    break;

                default:
                    ArchipelagoConsole.LogMessage("Warning: No cavevarient "+(variantName.ToString() ?? "Null"));
                    break;
            }

            return false;
        }
    }



}


