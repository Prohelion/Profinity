export interface BMUData {
  HeartbeatSerialNumber: {
    SerialNumber: string;
    DeviceId: string;
  };
  ExtendedPackStatus: {
    StatusCmuExtraCell: string;
    StatusContactorStuck: string;
    Status12vSupplyLow: string;
    StatusSOCMeasurementInvalid: string;
    StatusPackIsolationTestFail: string;
    StatusCmuCanBusPower: string;
    StatusBMUSetupMode: string;
    StatusVehicleCommsTimeout: string;
    StatusCmuCommsTimeout: string;
    StatusMeasurementUntrusted: string;
    StatusCellOverTemp: string;
    StatusCellUnderVolt: string;
    StatusCellOverVolt: string;
    Unused16: string;
    BmuModelId: string;
    BmuHardwareVersion: string;
  };
  FanStatus: {
    CmuCurrent: string;
    FanAndContactorsCurrent: string;
    FanSpeed1: string;
    FanSpeed0: string;
  };
  BatteryPackStatus: {
    StatusCmuCanBusPower: string;
    StatusBMUSetupMode: string;
    StatusVehicleCommsTimeout: string;
    StatusCmuCommsTimeout: string;
    StatusMeasurementUntrusted: string;
    StatusCellOverTemp: string;
    StatusCellUnderVolt: string;
    StatusCellOverVolt: string;
    BmsBmuFirmwareBuildNo: string;
    BmsCmuCount: string;
    VoltageThresholdFalling: string;
    VoltageThresholdRising: string;
  };
  PackVoltageCurrent: {
    Current: string;
    Voltage: string;
  };
  MinMaxCellTemp: {
    Unused8_2: string;
    Unused8: string;
    MaxCellTempCMU: string;
    MinCellTempCMU: string;
    MaxCellTemp: string;
    MinCellTemp: string;
  };
  MinMaxCellVoltage: {
    MaximumCellVoltageCellNo: string;
    MaximumCellVoltageCMU: string;
    MinimumCellVoltageCellNo: string;
    MinimumCellVoltageCMU: string;
    MaximumCellVoltage: string;
    MinimumCellVoltage: string;
  };
  PrechargeStatus: {
    Unused16: string;
    PrechargeTimerCounter: string;
    PrechargeTimerElapsed: string;
    Contactor12VSupply_v4_BMU: string;
    PrechargeState: string;
    PrechargeContactorDriverStatus: string;
  };
  ChargerControlInformation: {
    TotalPackCapacity: string;
    DischargingCellVoltageError: string;
    CellTemperatureMargin: string;
    ChargingCellVoltageError: string;
  };
  BalanceStateOfCharge: {
    BalanceSOCPercent: string;
    BalanceSOCAh: string;
  };
  PackStateOfCharge: {
    SOCPercent: string;
    SOCAh: string;
  };
} 