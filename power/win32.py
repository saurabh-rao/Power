# coding=utf-8
"""
    Imports Power Management functions of Windows Vista and higher into Python.
    Refer to http://msdn.microsoft.com/en-us/library/windows/desktop/aa373163(v=vs.85).aspx
    for the most recent documentation.
"""
__author__ = 'kulakov.ilya@gmail.com'

from ctypes import Structure, wintypes, POINTER, windll, GetLastError, WinError, pointer, c_ubyte
import common


class SYSTEM_POWER_STATUS(Structure):
    _fields_ = [
        ('ACLineStatus', c_ubyte),
        ('BatteryFlag', c_ubyte),
        ('BatteryLifePercent', c_ubyte),
        ('Reserved1', c_ubyte),
        ('BatteryLifeTime', wintypes.DWORD),
        ('BatteryFullLifeTime', wintypes.DWORD),
        ]

LPSYSTEM_POWER_STATUS = POINTER(SYSTEM_POWER_STATUS)


GetSystemPowerStatus = windll.kernel32.GetSystemPowerStatus
GetSystemPowerStatus.argtypes = [LPSYSTEM_POWER_STATUS]
GetSystemPowerStatus.restype = wintypes.BOOL


POWER_TYPE_MAP = {
    0: common.POWER_TYPE_BATTERY,
    1: common.POWER_TYPE_AC,
    255: common.POWER_TYPE_AC
}


class PowerManagement(common.PowerManagementBase):
    def get_providing_power_source_type(self):
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()
        return POWER_TYPE_MAP[power_status.ACLineStatus]

    def get_low_battery_warning_level(self):
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()

        if POWER_TYPE_MAP[power_status.ACLineStatus] == common.POWER_TYPE_AC:
            return common.LOW_BATTERY_WARNING_NONE
        else:
            if power_status.BatteryLifeTime != -1 and power_status.BatteryLifeTime <= 600:
                return common.LOW_BATTERY_WARNING_FINAL
            elif power_status.BatteryLifePercent <= 22:
                return common.LOW_BATTERY_WARNING_EARLY
            else:
                return common.LOW_BATTERY_WARNING_NONE

    def get_time_remaining_estimate(self):
        power_status = SYSTEM_POWER_STATUS()
        if not GetSystemPowerStatus(pointer(power_status)):
            raise WinError()

        if POWER_TYPE_MAP[power_status.ACLineStatus] == common.POWER_TYPE_AC:
            return common.TIME_REMAINING_UNLIMITED
        elif power_status.BatteryLifeTime == -1:
            return common.TIME_REMAINING_UNKNOWN
        else:
            return float(power_status.BatteryLifeTime) / 60

    def get_external_power_adapter_info(self):
        pass

    def get_power_sources_info(self):
        pass

    def add_observer(self, observer):
        pass

    def remove_observer(self, observer):
        pass
