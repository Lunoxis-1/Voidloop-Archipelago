using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using Archipelago.MultiClient.Net;
using Archipelago.MultiClient.Net.BounceFeatures.DeathLink;
using Archipelago.MultiClient.Net.Enums;
using Archipelago.MultiClient.Net.Helpers;
using Archipelago.MultiClient.Net.MessageLog.Messages;
using Archipelago.MultiClient.Net.Packets;
using Archipelago.MultiClient.Net.Models;
using UnityEngine;
using Voidloop_Archipelago.Utils;
using System.Runtime.CompilerServices;
using Newtonsoft.Json;
using System.IO;
using System.Threading.Tasks;
using BepInEx;
using System.Collections.Concurrent;
using Newtonsoft.Json.Linq;

namespace Voidloop_Archipelago.Archipelago;


public static class PlayerUpgrades
{

    
    // On client restart or reconnection, every stat type is resynced in case of missed checks. This ensures that happens.
    public static List<string> ResyncedStatTypes { get; set; } = [];


    public static int Filler_VoidrocksRecieved { get; set; } = 0;
    public static int Filler_RandomGoldenLootRecieved { get; set; } = 0;
    public static int Filler_RandomLootRecieved { get; set; } = 0;

    // Voidloop Variables
    public static int ProgressiveRegionGemCount { get; set; } = 0;

    public static int SkillPointCount { get; set; } = 0;

    // Grouped variables
    public static int PickaxeDamage { get; set; } = 0;
    public static int PickaxeSpeed { get; set; } = 0;
    public static int PickaxeRange { get; set; } = 0;

    public static int SwordDamage { get; set; } = 0;
    public static int SwordSpeed { get; set; } = 0;
    public static int SwordRange { get; set; } = 0;

    public static int Luck { get; set; } = 0;
    public static int MaxHealth { get; set; } = 0;
    public static int Speed { get; set; } = 0;
    public static int Resistance { get; set; } = 0;

    public static int BlastPhase { get; set; } = 0;
    public static int BlastCooldown { get; set; } = 0;
    public static int BlastDamage { get; set; } = 0;
    public static int BlastSize { get; set; } = 0;

    public static int DashPhase { get; set; } = 0;
    public static int DashCooldown { get; set; } = 0;
    public static int DashDamage { get; set; } = 0;
    public static int DashPower { get; set; } = 0;

    public static int EnergisePhase { get; set; } = 0;
    public static int EnergiseCooldown { get; set; } = 0;
    public static int EnergiseMultiplier { get; set; } = 0;
    public static int EnergiseDuration { get; set; } = 0;
    
}

public class APData
{
    public int ProcessedVoidrocks { get; set; } = 0;
    public int ProcessedRandomGoldenLoot { get; set; } = 0;
    public int ProcessedRandomLoot { get; set; } = 0;
}

public class SlotData
{
    [JsonProperty("leversanity")]
    public int Leversanity { get; set; } = 0;

    [JsonProperty("exits_are_levers")]
    public bool ExitsAreLevers { get; set; } = false;

}

public class ArchipelagoClient
{
    public const string APVersion = "0.5.0";
    private const string Game = "Voidloop";

    public static bool Authenticated;
    private bool attemptingConnection;

    public static ArchipelagoData ServerData = new();
    public static Dictionary<long, ScoutedItemInfo> scoutedLocationList;
    private DeathLinkHandler DeathLinkHandler;
    public ArchipelagoSession session;

    public APData apData = new APData();
    public SlotData slotData = new SlotData();

    public bool readingItems = false;
    public bool doneHatSync = false;
    private List<long> alreadyHinted = [];

    public ConcurrentQueue<long> itemQueue = [];

    public Dictionary<string, long> CatagoryToBaseId = new Dictionary<string, long>()
    {
        {"PickaxeDamage", 110100},
        {"PickaxeSpeed", 110200},
        {"PickaxeRange", 110300},

        {"SwordDamage", 111100},
        {"SwordSpeed", 111200},
        {"SwordRange", 111300},
    
        {"Luck", 112100},
        {"MaxHealth", 112200},
        {"Speed", 112300},
        {"Resistance", 112400},

        {"BlastPhase", 113100},
        {"BlastCooldown", 113200},
        {"BlastDamage", 113300},
        {"BlastSize", 113400},

        {"DashPhase", 114100},
        {"DashCooldown", 114200},
        {"DashDamage", 114300},
        {"DashPower", 114400},

        {"EnergisePhase", 115100},
        {"EnergiseCooldown", 115200},
        {"EnergiseMultiplier", 115300},
        {"EnergiseDuration", 115400},
    };


    /// <summary>
    /// call to connect to an Archipelago session. Connection info should already be set up on ServerData
    /// </summary>
    /// <returns></returns>
    public void Connect()
    {
        if (Authenticated || attemptingConnection) return;

        try
        {
            session = ArchipelagoSessionFactory.CreateSession(ServerData.Uri);
            SetupSession();
        }
        catch (Exception e)
        {
            Plugin.BepinLogger.LogError(e);
        }

        TryConnect();
    }

    /// <summary>
    /// add handlers for Archipelago events
    /// </summary>
    private void SetupSession()
    {
        session.MessageLog.OnMessageReceived += message => ArchipelagoConsole.LogMessage(message.ToString());
        session.Items.ItemReceived += OnItemReceived;
        session.Socket.ErrorReceived += OnSessionErrorReceived;
        session.Socket.SocketClosed += OnSessionSocketClosed;
    }

    /// <summary>
    /// attempt to connect to the server with our connection info
    /// </summary>
    private void TryConnect()
    {
        try
        {
            // it's safe to thread this function call but unity notoriously hates threading so do not use excessively
            ThreadPool.QueueUserWorkItem(
                _ => HandleConnectResult(
                    session.TryConnectAndLogin(
                        Game,
                        ServerData.SlotName,
                        ItemsHandlingFlags.NoItems, // Delay until ready
                        new Version(APVersion),
                        password: ServerData.Password,
                        requestSlotData: ServerData.NeedSlotData
                    )));
        }
        catch (Exception e)
        {
            Plugin.BepinLogger.LogError(e);
            HandleConnectResult(new LoginFailure(e.ToString()));
            attemptingConnection = false;
        }
    }

    /// <summary>
    /// handle the connection result and do things
    /// </summary>
    /// <param name="result"></param>
    private void HandleConnectResult(LoginResult result)
    {
        string outText;
        if (result.Successful)
        {
            var success = (LoginSuccessful)result;
            
            if (success is LoginSuccessful loginSuccess)
            {
                slotData = JObject.FromObject(loginSuccess.SlotData).ToObject<SlotData>();
            }

            ServerData.SetupSession(success.SlotData, session.RoomState.Seed);
            Authenticated = true;

            DeathLinkHandler = new(session.CreateDeathLinkService(), ServerData.SlotName);
            session.Locations.CompleteLocationChecksAsync(ServerData.CheckedLocations.ToArray());
            outText = $"Successfully connected to {ServerData.Uri} as {ServerData.SlotName}!";

            ArchipelagoConsole.LogMessage(outText);

            PlayerUpgrades.ResyncedStatTypes = [];

            ScoutForShops(); // Scout a bunch of locations we need to for the purpose of shops

            string saveName = "MultiWorld_Data_" + session.RoomState.Seed + "_" + session.ConnectionInfo.Slot+".data";

            doneHatSync = false;

            _ = LoadAPData();
        }
        else
        {
            var failure = (LoginFailure)result;
            outText = $"Failed to connect to {ServerData.Uri} as {ServerData.SlotName}.";
            outText = failure.Errors.Aggregate(outText, (current, error) => current + $"\n    {error}");

            Plugin.BepinLogger.LogError(outText);

            Authenticated = false;
            Disconnect();
        }

        ArchipelagoConsole.LogMessage(outText);
        attemptingConnection = false;
    }

    /// <summary>
    /// something went wrong, or we need to properly disconnect from the server. cleanup and re null our session
    /// </summary>
    private void Disconnect()
    {
        Plugin.BepinLogger.LogDebug("disconnecting from server...");
        session?.Socket.DisconnectAsync();
        session = null;
        Authenticated = false;
    }

    public void SendMessage(string message)
    {
        session.Socket.SendPacketAsync(new SayPacket { Text = message });
    }

    public SlotData GetSlotData()
    {
        return slotData;
    }

    public void SendLocations(List<long> locationIds)
    {
        session.Locations.CompleteLocationChecks(locationIds.ToArray());
    }

    public async Task SaveAPData()
    {

        // apData.ProcessedVoidrocks = PlayerUpgrades.Filler_VoidrocksRecieved;
        // apData.ProcessedRandomGoldenLoot = PlayerUpgrades.Filler_RandomGoldenLootRecieved;
        // apData.ProcessedRandomLoot = PlayerUpgrades.Filler_RandomLootRecieved;

        if (session is null || session.RoomState?.Seed is null || session.ConnectionInfo?.Slot is null) return;
        string saveName = "MultiWorld_Data_" + session.RoomState.Seed + "_" + session.ConnectionInfo.Slot;

        string path = UnityEngine.Application.persistentDataPath;
        path = Path.Combine(path, "multiworldmetadata");

        try
        {
            string jsonString = JsonConvert.SerializeObject(apData, Formatting.Indented);
            Directory.CreateDirectory(path);
            await File.WriteAllTextAsync(Path.Combine(path, saveName+".apdata"), jsonString);
            Plugin.BepinLogger.LogInfo("AP: Saved Data");
        }
        catch (Exception ex)
        {
            Plugin.BepinLogger.LogWarning("Warning: Data Save Failed! "+ex.ToString());
        }
    }

    // CALL ONLY ONCE! Calling this also enables item reciving, regardless of output (unless the game crashes. Lol!)
    public async Task LoadAPData()
    {
        if (session is null || session.RoomState?.Seed is null || session.ConnectionInfo?.Slot is null) return;


        // Wait for the gameData

        GameData gameData = Plugin.GetGameData();
        while (gameData is null)
        {
            await Task.Delay(100);
            gameData = Plugin.GetGameData();
        }

        Inventory inventory = gameData.playerInventory;
        while (inventory is null)
        {
            await Task.Delay(100);
            inventory = gameData.playerInventory;
        }

        // Never used for anything, but we need to wait for it to exist or some item rewards will fail.
        LootManager lootManager = Plugin.GetLootManager();
        while (lootManager is null)
        {
            await Task.Delay(100);
            lootManager = Plugin.GetLootManager();
        }

        await Task.Delay(1000);
        
        
        string saveName = "MultiWorld_Data_" + session.RoomState.Seed + "_" + session.ConnectionInfo.Slot;

        string path = UnityEngine.Application.persistentDataPath;
        path = Path.Combine(path, "multiworldmetadata");

        Directory.CreateDirectory(path);

        string filePath = Path.Combine(path, saveName+".apdata");

        if (!File.Exists(filePath))
        {
            Plugin.BepinLogger.LogWarning("AP: No JSON found. Likely a new file.");
            session.ConnectionInfo.UpdateConnectionOptions(ItemsHandlingFlags.AllItems);
            return;
        }
        try
        {
            string jsonString = await File.ReadAllTextAsync(filePath);
            if (jsonString is null) ArchipelagoConsole.LogMessage("JSON might be corrupted or invalid! Please try again, and if that doesn't work, delete "+path);
            apData = JsonConvert.DeserializeObject<APData>(jsonString);
            Plugin.BepinLogger.LogInfo("AP: Loaded Data");
        }
        catch (Exception ex)
        {
            session.ConnectionInfo.UpdateConnectionOptions(ItemsHandlingFlags.AllItems);
            Plugin.BepinLogger.LogError("Error: APData Load Failed! "+ex.ToString());
            throw new IOException("AP: Failed to read JSON.", ex);
        }

        // PlayerUpgrades.Filler_VoidrocksRecieved = apData.ProcessedVoidrocks;
        // PlayerUpgrades.Filler_RandomGoldenLootRecieved= apData.ProcessedRandomGoldenLoot;
        // PlayerUpgrades.Filler_RandomLootRecieved = apData.ProcessedRandomLoot;

        session.ConnectionInfo.UpdateConnectionOptions(ItemsHandlingFlags.AllItems);

    }

    async public void ViewedShopID(long itemId)
    {
        if (alreadyHinted.Contains(itemId)) return;

        // We do not care about the result, because we have it elsewhere. This is just making it a real hint.
        // Duplications from race conditions don't matter. Contains doesn't care.
        alreadyHinted.Add(itemId);
        try
        {
        await session.Locations.ScoutLocationsAsync(HintCreationPolicy.CreateAndAnnounceOnce, [itemId]);
        }
        catch (Exception ex)
        {
            alreadyHinted.Remove(itemId);
            Plugin.BepinLogger.LogWarning("Error while hinting: " + ex.ToString());
        }
    }

    async private void ScoutForShops()
    {
        scoutedLocationList = [];

        List<int> locationIdsToScout = [];
        // Pickaxe
        locationIdsToScout.AddRange(Enumerable.Range(110101, 10)); // 10 total
        locationIdsToScout.AddRange(Enumerable.Range(110201, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(110301, 5)); // 5 total
        
        // Sword
        locationIdsToScout.AddRange(Enumerable.Range(111101, 10)); // 10 total
        locationIdsToScout.AddRange(Enumerable.Range(111201, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(111301, 5)); // 5 total

        // Player
        locationIdsToScout.AddRange(Enumerable.Range(112101, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(112201, 3)); // 3 total
        locationIdsToScout.AddRange(Enumerable.Range(112301, 3)); // 3 total
        locationIdsToScout.AddRange(Enumerable.Range(112401, 3)); // 3 total

        // Blast
        locationIdsToScout.AddRange(Enumerable.Range(113101, 2)); // 2 total
        locationIdsToScout.AddRange(Enumerable.Range(113201, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(113301, 10)); // 10 total
        locationIdsToScout.AddRange(Enumerable.Range(113401, 6)); // 6 total

        // Dash
        locationIdsToScout.AddRange(Enumerable.Range(114101, 2)); // 2 total
        locationIdsToScout.AddRange(Enumerable.Range(114201, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(114301, 6)); // 6 total
        locationIdsToScout.AddRange(Enumerable.Range(114401, 10)); // 10 total

        // Energise
        locationIdsToScout.AddRange(Enumerable.Range(115101, 2)); // 2 total
        locationIdsToScout.AddRange(Enumerable.Range(115201, 5)); // 5 total
        locationIdsToScout.AddRange(Enumerable.Range(115301, 10)); // 10 total
        locationIdsToScout.AddRange(Enumerable.Range(115401, 6)); // 6 total

        List<long> longLocationIdsToScout = locationIdsToScout.ConvertAll(i => (long)i); 
        long[] locationIdsArray = longLocationIdsToScout.ToArray();

        scoutedLocationList = await session.Locations.ScoutLocationsAsync(HintCreationPolicy.None, locationIdsArray);


        // TODO: use list.Intersect(listOfOnlyValidCandidates)
    }


    /// <summary>
    /// we received an item so reward it here
    /// </summary>
    /// <param name="helper">item helper which we can grab our item from</param>
    private void OnItemReceived(ReceivedItemsHelper helper)
    {
        var receivedItem = helper.DequeueItem();

        if (helper.Index <= ServerData.Index) return;

        ServerData.Index++;

        long itemId = receivedItem.ItemId;

        //Plugin.BepinLogger.LogInfo("Got itemId: "+itemId.ToString());

        //Plugin.CheckThread("AP_OnItemRecieved");

        itemQueue.Enqueue(itemId);

    }

    /// <summary>
    /// something went wrong with our socket connection
    /// </summary>
    /// <param name="e">thrown exception from our socket</param>
    /// <param name="message">message received from the server</param>
    private void OnSessionErrorReceived(Exception e, string message)
    {
        Plugin.BepinLogger.LogError(e);
        ArchipelagoConsole.LogMessage(message);
    }

    /// <summary>
    /// something went wrong closing our connection. disconnect and clean up
    /// </summary>
    /// <param name="reason"></param>
    private void OnSessionSocketClosed(string reason)
    {
        Plugin.BepinLogger.LogError($"Connection to Archipelago lost: {reason}");
        Disconnect();
    }
}