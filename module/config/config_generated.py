import datetime

# This file was automatically generated by module/config/config_updater.py.
# Don't modify it manually.


class GeneratedConfig:
    """
    Auto generated configuration
    """

    # Group `Scheduler`
    Scheduler_Enable = False  # True, False
    Scheduler_NextRun = datetime.datetime(2020, 1, 1, 0, 0)
    Scheduler_Command = 'Alas'
    Scheduler_SuccessInterval = 0
    Scheduler_FailureInterval = 120
    Scheduler_ServerUpdate = '00:00'

    # Group `Emulator`
    Emulator_Serial = 'auto'
    Emulator_PackageName = 'auto'  # auto, com.bilibili.azurlane, com.YoStarEN.AzurLane, com.YoStarJP.AzurLane, com.hkmanjuu.azurlane.gp, com.bilibili.blhx.huawei, com.bilibili.blhx.mi, com.tencent.tmgp.bilibili.blhx, com.bilibili.blhx.baidu, com.bilibili.blhx.qihoo, com.bilibili.blhx.nearme.gamecenter, com.bilibili.blhx.vivo, com.bilibili.blhx.mz, com.bilibili.blhx.dl, com.bilibili.blhx.lenovo, com.bilibili.blhx.uc, com.bilibili.blhx.mzw, com.yiwu.blhx.yx15, com.bilibili.blhx.m4399, com.bilibili.blhx.bilibiliMove, com.hkmanjuu.azurlane.gp.mc
    Emulator_ServerName = 'disabled'  # disabled, cn_android-0, cn_android-1, cn_android-2, cn_android-3, cn_android-4, cn_android-5, cn_android-6, cn_android-7, cn_android-8, cn_android-9, cn_android-10, cn_android-11, cn_android-12, cn_android-13, cn_android-14, cn_android-15, cn_android-16, cn_android-17, cn_android-18, cn_android-19, cn_android-20, cn_android-21, cn_android-22, cn_android-23, cn_android-24, cn_ios-0, cn_ios-1, cn_ios-2, cn_ios-3, cn_ios-4, cn_ios-5, cn_ios-6, cn_ios-7, cn_ios-8, cn_ios-9, cn_ios-10, cn_channel-0, cn_channel-1, cn_channel-2, cn_channel-3, cn_channel-4, en-0, en-1, en-2, en-3, en-4, en-5, jp-0, jp-1, jp-2, jp-3, jp-4, jp-5, jp-6, jp-7, jp-8, jp-9, jp-10, jp-11, jp-12, jp-13, jp-14, jp-15, jp-16, jp-17
    Emulator_ScreenshotMethod = 'auto'  # auto, ADB, ADB_nc, uiautomator2, aScreenCap, aScreenCap_nc, DroidCast, DroidCast_raw, scrcpy, nemu_ipc, ldopengl
    Emulator_ControlMethod = 'MaaTouch'  # ADB, uiautomator2, minitouch, Hermit, MaaTouch
    Emulator_ScreenshotDedithering = False
    Emulator_AdbRestart = False

    # Group `EmulatorInfo`
    EmulatorInfo_Emulator = 'auto'  # auto, NoxPlayer, NoxPlayer64, BlueStacks4, BlueStacks5, BlueStacks4HyperV, BlueStacks5HyperV, LDPlayer3, LDPlayer4, LDPlayer9, MuMuPlayer, MuMuPlayerX, MuMuPlayer12, MEmuPlayer
    EmulatorInfo_name = None
    EmulatorInfo_path = None

    # Group `Error`
    Error_HandleError = True
    Error_SaveError = True
    Error_OnePushConfig = 'provider: null'
    Error_ScreenshotLength = 1

    # Group `Optimization`
    Optimization_ScreenshotInterval = 0.3
    Optimization_CombatScreenshotInterval = 1.0
    Optimization_TaskHoardingDuration = 0
    Optimization_WhenTaskQueueEmpty = 'goto_main'  # stay_there, goto_main, close_game

    # Group `DropRecord`
    DropRecord_SaveFolder = './screenshots'
    DropRecord_AzurStatsID = None
    DropRecord_API = 'default'  # default, cn_gz_reverse_proxy
    DropRecord_ResearchRecord = 'do_not'  # do_not, save, upload, save_and_upload
    DropRecord_CommissionRecord = 'do_not'  # do_not, save, upload, save_and_upload
    DropRecord_CombatRecord = 'do_not'  # do_not, save
    DropRecord_OpsiRecord = 'do_not'  # do_not, save, upload, save_and_upload
    DropRecord_MeowfficerBuy = 'do_not'  # do_not, save
    DropRecord_MeowfficerTalent = 'do_not'  # do_not, save, upload, save_and_upload

    # Group `Retirement`
    Retirement_RetireMode = 'one_click_retire'  # one_click_retire, enhance, old_retire

    # Group `OneClickRetire`
    OneClickRetire_KeepLimitBreak = 'keep_limit_break'  # keep_limit_break, do_not_keep

    # Group `Enhance`
    Enhance_ShipToEnhance = 'all'  # all, favourite
    Enhance_Filter = None
    Enhance_CheckPerCategory = 5

    # Group `OldRetire`
    OldRetire_N = True
    OldRetire_R = True
    OldRetire_SR = False
    OldRetire_SSR = False
    OldRetire_RetireAmount = 'retire_all'  # retire_all, retire_10

    # Group `Campaign`
    Campaign_Name = '12-4'
    Campaign_Event = 'campaign_main'  # campaign_main
    Campaign_Mode = 'normal'  # normal, hard
    Campaign_UseClearMode = True
    Campaign_UseFleetLock = True
    Campaign_UseAutoSearch = True
    Campaign_Use2xBook = False
    Campaign_AmbushEvade = True

    # Group `StopCondition`
    StopCondition_OilLimit = 1000
    StopCondition_RunCount = 0
    StopCondition_MapAchievement = 'non_stop'  # non_stop, 100_percent_clear, map_3_stars, threat_safe, threat_safe_without_3_stars
    StopCondition_StageIncrease = False
    StopCondition_GetNewShip = False
    StopCondition_ReachLevel = 0

    # Group `Fleet`
    Fleet_Fleet1 = 1  # 1, 2, 3, 4, 5, 6
    Fleet_Fleet1Formation = 'double_line'  # line_ahead, double_line, diamond
    Fleet_Fleet1Mode = 'combat_auto'  # combat_auto, combat_manual, stand_still_in_the_middle, hide_in_bottom_left
    Fleet_Fleet1Step = 3  # 2, 3, 4, 5
    Fleet_Fleet2 = 2  # 0, 1, 2, 3, 4, 5, 6
    Fleet_Fleet2Formation = 'double_line'  # line_ahead, double_line, diamond
    Fleet_Fleet2Mode = 'combat_auto'  # combat_auto, combat_manual, stand_still_in_the_middle, hide_in_bottom_left
    Fleet_Fleet2Step = 2  # 2, 3, 4, 5
    Fleet_FleetOrder = 'fleet1_mob_fleet2_boss'  # fleet1_mob_fleet2_boss, fleet1_boss_fleet2_mob, fleet1_all_fleet2_standby, fleet1_standby_fleet2_all

    # Group `Submarine`
    Submarine_Fleet = 0  # 0, 1, 2
    Submarine_Mode = 'do_not_use'  # do_not_use, hunt_only, boss_only, hunt_and_boss, every_combat
    Submarine_AutoSearchMode = 'sub_standby'  # sub_standby, sub_auto_call
    Submarine_DistanceToBoss = '2_grid_to_boss'  # to_boss_position, 1_grid_to_boss, 2_grid_to_boss, use_open_ocean_support

    # Group `Emotion`
    Emotion_Mode = 'calculate'  # calculate, ignore, calculate_ignore
    Emotion_Fleet1Value = 119
    Emotion_Fleet1Record = datetime.datetime(2020, 1, 1, 0, 0)
    Emotion_Fleet1Control = 'prevent_yellow_face'  # keep_exp_bonus, prevent_green_face, prevent_yellow_face, prevent_red_face
    Emotion_Fleet1Recover = 'not_in_dormitory'  # not_in_dormitory, dormitory_floor_1, dormitory_floor_2
    Emotion_Fleet1Oath = False
    Emotion_Fleet2Value = 119
    Emotion_Fleet2Record = datetime.datetime(2020, 1, 1, 0, 0)
    Emotion_Fleet2Control = 'prevent_yellow_face'  # keep_exp_bonus, prevent_green_face, prevent_yellow_face, prevent_red_face
    Emotion_Fleet2Recover = 'not_in_dormitory'  # not_in_dormitory, dormitory_floor_1, dormitory_floor_2
    Emotion_Fleet2Oath = False

    # Group `HpControl`
    HpControl_UseHpBalance = False
    HpControl_UseEmergencyRepair = False
    HpControl_UseLowHpRetreat = False
    HpControl_HpBalanceThreshold = 0.2
    HpControl_HpBalanceWeight = '1000, 1000, 1000'
    HpControl_RepairUseSingleThreshold = 0.3
    HpControl_RepairUseMultiThreshold = 0.6
    HpControl_LowHpRetreatThreshold = 0.3

    # Group `EnemyPriority`
    EnemyPriority_EnemyScaleBalanceWeight = 'default_mode'  # default_mode, S3_enemy_first, S1_enemy_first

    # Group `C11AffinityFarming`
    C11AffinityFarming_RunCount = 32

    # Group `C72MysteryFarming`
    C72MysteryFarming_StepOnA3 = True

    # Group `C122MediumLeveling`
    C122MediumLeveling_LargeEnemyTolerance = 1  # 0, 1, 2, 10

    # Group `C124LargeLeveling`
    C124LargeLeveling_NonLargeEnterTolerance = 1  # 0, 1, 2
    C124LargeLeveling_NonLargeRetreatTolerance = 1  # 0, 1, 2, 10
    C124LargeLeveling_PickupAmmo = 3  # 3, 4, 5

    # Group `GemsFarming`
    GemsFarming_ChangeFlagship = 'ship'  # ship, ship_equip
    GemsFarming_CommonCV = 'any'  # any, langley, bogue, ranger, hermes
    GemsFarming_ChangeVanguard = 'ship'  # disabled, ship, ship_equip
    GemsFarming_CommonDD = 'any'  # any, favourite, aulick_or_foote, cassin_or_downes, z20_or_z21
    GemsFarming_CommissionLimit = True

    # Group `EventGeneral`
    EventGeneral_PtLimit = 0
    EventGeneral_TimeLimit = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `TaskBalancer`
    TaskBalancer_Enable = False
    TaskBalancer_CoinLimit = 10000
    TaskBalancer_TaskCall = 'Main'  # Main, Main2, Main3

    # Group `EventDaily`
    EventDaily_StageFilter = 'A1 > A2 > A3'
    EventDaily_LastStage = 0

    # Group `Raid`
    Raid_Mode = 'hard'  # easy, normal, hard, ex
    Raid_UseTicket = False

    # Group `RaidDaily`
    RaidDaily_StageFilter = 'hard > normal > easy'

    # Group `MaritimeEscort`
    MaritimeEscort_Enable = True

    # Group `Coalition`
    Coalition_Mode = 'hard'  # easy, normal, hard, ex
    Coalition_Fleet = 'single'  # single, multi

    # Group `Commission`
    Commission_PresetFilter = 'cube'  # cube, cube_24h, chip, chip_24h, oil, custom
    Commission_CustomFilter = 'DailyEvent > Gem-4 > Gem-2 > Gem-8 > ExtraCube-0:30\n> UrgentCube-1:30 > UrgentCube-1:45 > UrgentCube-3\n> ExtraDrill-5:20 > ExtraDrill-2 > ExtraDrill-3:20\n> UrgentCube-2:15 > UrgentCube-4\n> ExtraDrill-1 > UrgentCube-6 > ExtraCube-1:30\n> ExtraDrill-2:40 > ExtraDrill-0:20\n> Major > DailyChip > DailyResource\n> ExtraPart-0:30 > ExtraOil-1 > UrgentBox-6\n> ExtraCube-3 > ExtraPart-1 > UrgentBox-3\n> ExtraCube-4 > ExtraPart-1:30 > ExtraOil-4\n> UrgentBox-1 > ExtraCube-5 > UrgentBox-1\n> ExtraCube-8 > ExtraOil-8\n> UrgentDrill-4 > UrgentDrill-2:40 > UrgentDrill-2\n> UrgentDrill-1 > UrgentDrill-1:30 > UrgentDrill-1:10\n> Extra-0:20 > Extra-0:30 > Extra-1:00 > Extra-1:30 > Extra-2:00\n> shortest'
    Commission_DoMajorCommission = False

    # Group `Tactical`
    Tactical_TacticalFilter = 'SameT4 > SameT3 > SameT2 > SameT1\n> BlueT2 > YellowT2 > RedT2\n> BlueT3 > YellowT3 > RedT3\n> BlueT4 > YellowT4 > RedT4\n> BlueT1 > YellowT1 > RedT1\n> first'
    Tactical_RapidTrainingSlot = 'do_not_use'  # do_not_use, slot_1, slot_2, slot_3, slot_4

    # Group `ControlExpOverflow`
    ControlExpOverflow_Enable = True
    ControlExpOverflow_T4Allow = 100
    ControlExpOverflow_T3Allow = 100
    ControlExpOverflow_T2Allow = 200
    ControlExpOverflow_T1Allow = 200

    # Group `AddNewStudent`
    AddNewStudent_Enable = False
    AddNewStudent_Favorite = True

    # Group `Research`
    Research_UseCube = 'only_05_hour'  # always_use, only_05_hour, only_no_project, do_not_use
    Research_UseCoin = 'always_use'  # always_use, only_05_hour, only_no_project, do_not_use
    Research_UsePart = 'always_use'  # always_use, only_05_hour, only_no_project, do_not_use
    Research_AllowDelay = True
    Research_PresetFilter = 'series_7_blueprint_la9'  # custom, series_7_blueprint_la9, series_7_blueprint_only, series_7_la9_only, series_6_blueprint_203, series_6_blueprint_only, series_6_203_only, series_5_blueprint_152, series_5_blueprint_only, series_5_152_only, series_4_blueprint_tenrai, series_4_blueprint_only, series_4_tenrai_only, series_3_blueprint_234, series_3_blueprint_only, series_3_234_only, series_2_than_3_457_234, series_2_blueprint_457, series_2_blueprint_only, series_2_457_only
    Research_CustomFilter = 'S7-DR0.5 > S7-PRY0.5 > S7-Q0.5 > S7-H0.5 > Q0.5 > S7-DR2.5\n> S7-G1.5 > S7-Q1 > S7-DR5 > 0.5 > S7-G4 > S7-Q2 > S7-PRY2.5 > reset\n> S7-DR8 > Q1 > 1 > S7-E-315 > S7-G2.5 > G1.5 > 1.5 > S7-E-031\n> S7-Q4 > Q2 > E2 > 2 > DR2.5 > PRY2.5 > G2.5 > 2.5 > S7-PRY5\n> S7-PRY8 > Q4 > G4 > 4 > S7-C6 > DR5 > PRY5 > 5 > C6 > 6 > S7-C8\n> S7-C12 > DR8 > PRY8 > C8 > 8 > C12 > 12'

    # Group `Dorm`
    Dorm_Collect = True
    Dorm_Feed = True
    Dorm_FeedFilter = '20000 > 10000 > 5000 > 3000 > 2000 > 1000'

    # Group `BuyFurniture`
    BuyFurniture_Enable = False
    BuyFurniture_BuyOption = 'all'  # set, all
    BuyFurniture_LastRun = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `Meowfficer`
    Meowfficer_BuyAmount = 1
    Meowfficer_FortChoreMeowfficer = True

    # Group `MeowfficerTrain`
    MeowfficerTrain_Enable = False
    MeowfficerTrain_Mode = 'seamlessly'  # seamlessly, once_a_day
    MeowfficerTrain_RetainTalentedGold = True
    MeowfficerTrain_RetainTalentedPurple = True
    MeowfficerTrain_EnhanceIndex = 1

    # Group `GuildLogistics`
    GuildLogistics_Enable = True
    GuildLogistics_SelectNewMission = False
    GuildLogistics_ExchangeFilter = 'PlateTorpedoT1 > PlateAntiAirT1 > PlatePlaneT1 > PlateGunT1 > PlateGeneralT1\n> PlateTorpedoT2 > PlateAntiAirT2 > PlatePlaneT2 > PlateGunT2 > PlateGeneralT2\n> PlateTorpedoT3 > PlateAntiAirT3 > PlatePlaneT3 > PlateGunT3 > PlateGeneralT3\n> OxyCola > Coolant > Merit > Coin > Oil'

    # Group `GuildOperation`
    GuildOperation_Enable = True
    GuildOperation_SelectNewOperation = False
    GuildOperation_NewOperationMaxDate = 15
    GuildOperation_JoinThreshold = 1
    GuildOperation_AttackBoss = True
    GuildOperation_BossFleetRecommend = False

    # Group `Reward`
    Reward_CollectOil = True
    Reward_CollectCoin = True
    Reward_CollectExp = True
    Reward_CollectMission = True
    Reward_CollectWeeklyMission = True

    # Group `GeneralShop`
    GeneralShop_UseGems = False
    GeneralShop_Refresh = False
    GeneralShop_BuySkinBox = False
    GeneralShop_ConsumeCoins = False
    GeneralShop_Filter = 'BookRedT3 > BookYellowT3 > BookBlueT3 > BookRedT2\n> Cube\n> FoodT6 > FoodT5'

    # Group `GuildShop`
    GuildShop_Refresh = True
    GuildShop_Filter = 'PlateT4 > BookT3 > PR > CatT3 > Chip > BookT2 > Retrofit > FoodT6 > FoodT5 > CatT2 > BoxT4'
    GuildShop_BOX_T3 = 'ironblood'  # eagle, royal, sakura, ironblood
    GuildShop_BOX_T4 = 'ironblood'  # eagle, royal, sakura, ironblood
    GuildShop_BOOK_T2 = 'red'  # red, blue, yellow
    GuildShop_BOOK_T3 = 'red'  # red, blue, yellow
    GuildShop_RETROFIT_T2 = 'cl'  # dd, cl, bb, cv
    GuildShop_RETROFIT_T3 = 'cl'  # dd, cl, bb, cv
    GuildShop_PLATE_T2 = 'general'  # general, gun, torpedo, antiair, plane
    GuildShop_PLATE_T3 = 'general'  # general, gun, torpedo, antiair, plane
    GuildShop_PLATE_T4 = 'gun'  # general, gun, torpedo, antiair, plane
    GuildShop_PR1 = 'neptune'  # neptune, monarch, ibuki, izumo, roon, saintlouis
    GuildShop_PR2 = 'seattle'  # seattle, georgia, kitakaze, gascogne
    GuildShop_PR3 = 'cheshire'  # cheshire, mainz, odin, champagne

    # Group `MedalShop2`
    MedalShop2_Filter = 'DR > PR\n> BookRedT3 > BookYellowT3 > BookBlueT3\n> BookRedT2 > BookYellowT2 > BookBlueT2\n> RetrofitT3\n> FoodT6 > FoodT5\n> PlateGeneralT3 > PlateWildT3'
    MedalShop2_RETROFIT_T1 = 'cl'  # dd, cl, bb, cv
    MedalShop2_RETROFIT_T2 = 'cl'  # dd, cl, bb, cv
    MedalShop2_RETROFIT_T3 = 'cl'  # dd, cl, bb, cv
    MedalShop2_PLATE_T1 = 'general'  # general, gun, torpedo, antiair, plane
    MedalShop2_PLATE_T2 = 'general'  # general, gun, torpedo, antiair, plane
    MedalShop2_PLATE_T3 = 'general'  # general, gun, torpedo, antiair, plane

    # Group `MeritShop`
    MeritShop_Refresh = False
    MeritShop_Filter = 'Cube'

    # Group `CoreShop`
    CoreShop_Filter = 'Array'

    # Group `ShipyardDr`
    ShipyardDr_ResearchSeries = 2  # 2, 3
    ShipyardDr_ShipIndex = 0  # 0, 1, 2, 3, 4, 5, 6
    ShipyardDr_BuyAmount = 2
    ShipyardDr_LastRun = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `Shipyard`
    Shipyard_ResearchSeries = 1  # 1, 2, 3, 4
    Shipyard_ShipIndex = 0  # 0, 1, 2, 3, 4, 5, 6
    Shipyard_BuyAmount = 2
    Shipyard_LastRun = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `Gacha`
    Gacha_Pool = 'light'  # light, heavy, special, event, wishing_well
    Gacha_Amount = 1  # 1, 2, 3, 4, 5, 6, 7, 8, 9, 10
    Gacha_UseTicket = True
    Gacha_UseDrill = False

    # Group `BattlePass`
    BattlePass_Collect = True

    # Group `DataKey`
    DataKey_Collect = True
    DataKey_ForceCollect = False

    # Group `Mail`
    Mail_ClaimMerit = True
    Mail_ClaimMaintenance = False
    Mail_ClaimTradeLicense = False
    Mail_DeleteCollected = True

    # Group `SupplyPack`
    SupplyPack_Collect = True
    SupplyPack_DayOfWeek = 0  # 0, 1, 2, 3, 4, 5, 6

    # Group `Minigame`
    Minigame_Collect = False

    # Group `Daily`
    Daily_UseDailySkip = True
    Daily_EscortMission = 'first'  # skip, first, second, third
    Daily_EscortMissionFleet = 1  # 1, 2, 3, 4, 5, 6
    Daily_AdvanceMission = 'first'  # skip, first, second, third
    Daily_AdvanceMissionFleet = 1  # 1, 2, 3, 4, 5, 6
    Daily_FierceAssault = 'first'  # skip, first, second, third
    Daily_FierceAssaultFleet = 1  # 1, 2, 3, 4, 5, 6
    Daily_TacticalTraining = 'second'  # skip, first, second, third
    Daily_TacticalTrainingFleet = 1  # 1, 2, 3, 4, 5, 6
    Daily_SupplyLineDisruption = 'second'  # skip, first, second, third
    Daily_ModuleDevelopment = 'first'  # skip, first, second
    Daily_ModuleDevelopmentFleet = 1  # 1, 2, 3, 4, 5, 6
    Daily_EmergencyModuleDevelopment = 'first'  # skip, first, second
    Daily_EmergencyModuleDevelopmentFleet = 1  # 1, 2, 3, 4, 5, 6

    # Group `Hard`
    Hard_HardStage = '11-4'
    Hard_HardFleet = 1  # 1, 2

    # Group `Exercise`
    Exercise_OpponentChooseMode = 'max_exp'  # max_exp, easiest, leftmost, easiest_else_exp
    Exercise_OpponentTrial = 1
    Exercise_ExerciseStrategy = 'aggressive'  # aggressive, fri18, sat0, sat12, sat18, sun0, sun12, sun18
    Exercise_LowHpThreshold = 0.4
    Exercise_LowHpConfirmWait = 0.1
    Exercise_OpponentRefreshValue = 0
    Exercise_OpponentRefreshRecord = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `Sos`
    Sos_Chapter = 3  # 3, 4, 5, 6, 7, 8, 9, 10

    # Group `OpsiAshAssist`
    OpsiAshAssist_Tier = 15

    # Group `OpsiGeneral`
    OpsiGeneral_UseLogger = True
    OpsiGeneral_BuyActionPointLimit = 0  # 0, 1, 2, 3, 4, 5
    OpsiGeneral_OilLimit = 1000
    OpsiGeneral_RepairThreshold = 0.4
    OpsiGeneral_DoRandomMapEvent = True
    OpsiGeneral_AkashiShopFilter = 'ActionPoint > PurpleCoins'

    # Group `OpsiAshBeacon`
    OpsiAshBeacon_AttackMode = 'current'  # current, current_dossier
    OpsiAshBeacon_OneHitMode = True
    OpsiAshBeacon_DossierAutoAttackMode = False
    OpsiAshBeacon_RequestAssist = True
    OpsiAshBeacon_EnsureFullyCollected = True

    # Group `OpsiFleetFilter`
    OpsiFleetFilter_Filter = 'Fleet-4 > CallSubmarine > Fleet-2 > Fleet-3 > Fleet-1'

    # Group `OpsiFleet`
    OpsiFleet_Fleet = 1  # 1, 2, 3, 4
    OpsiFleet_Submarine = False

    # Group `OpsiExplore`
    OpsiExplore_SpecialRadar = False
    OpsiExplore_ForceRun = False
    OpsiExplore_LastZone = 0

    # Group `OpsiShop`
    OpsiShop_PresetFilter = 'max_benefit_meta'  # max_benefit, max_benefit_meta, no_meta, all, custom
    OpsiShop_CustomFilter = 'LoggerAbyssalT6 > LoggerAbyssalT5 > LoggerObscure > LoggerAbyssalT4 > ActionPoint > PurpleCoins\n> GearDesignPlanT3 > PlateRandomT4 > DevelopmentMaterialT3 > GearDesignPlanT2 > GearPart\n> OrdnanceTestingReportT3 > OrdnanceTestingReportT2 > DevelopmentMaterialT2 > OrdnanceTestingReportT1\n> METARedBook > CrystallizedHeatResistantSteel > NanoceramicAlloy > NeuroplasticProstheticArm > SupercavitationGenerator'

    # Group `OpsiVoucher`
    OpsiVoucher_Filter = 'LoggerAbyssal > LoggerObscure > Book > Coin > Fragment'

    # Group `OpsiDaily`
    OpsiDaily_DoMission = True
    OpsiDaily_UseTuningSample = True
    OpsiDaily_CollectTargetReward = False

    # Group `OpsiObscure`
    OpsiObscure_ForceRun = False

    # Group `OpsiAbyssal`
    OpsiAbyssal_ForceRun = False

    # Group `OpsiStronghold`
    OpsiStronghold_ForceRun = False

    # Group `OpsiMonthBoss`
    OpsiMonthBoss_Mode = 'normal'  # normal, normal_hard
    OpsiMonthBoss_CheckAdaptability = True
    OpsiMonthBoss_ForceRun = False

    # Group `OpsiMeowfficerFarming`
    OpsiMeowfficerFarming_ActionPointPreserve = 1000
    OpsiMeowfficerFarming_HazardLevel = 5  # 3, 4, 5, 6, 10

    # Group `OpsiTarget`
    OpsiTarget_TargetFarming = False
    OpsiTarget_TargetZone = 0
    OpsiTarget_LastRun = datetime.datetime(2020, 1, 1, 0, 0)

    # Group `OpsiHazard1Leveling`
    OpsiHazard1Leveling_TargetZone = 0  # 0, 44, 22

    # Group `Daemon`
    Daemon_EnterMap = True

    # Group `OpsiDaemon`
    OpsiDaemon_RepairShip = True
    OpsiDaemon_SelectEnemy = True

    # Group `Benchmark`
    Benchmark_DeviceType = 'emulator'  # emulator, plone_cloud_with_adb, phone_cloud_without_adb, android_phone, android_phone_vmos
    Benchmark_TestScene = 'screenshot_click'  # screenshot_click, screenshot, click

    # Group `AzurLaneUncensored`
    AzurLaneUncensored_Repository = 'https://gitee.com/LmeSzinc/AzurLaneUncensored'

    # Group `GameManager`
    GameManager_AutoRestart = True

    # Group `Storage`
    Storage_Storage = {}
