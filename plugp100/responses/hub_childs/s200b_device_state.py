import base64
from dataclasses import dataclass
from typing import Any, Union

import semantic_version

from plugp100.common.functional.tri import Try


@dataclass
class S200BDeviceState:
    hardware_version: str
    firmware_version: str
    device_id: str
    parent_device_id: str
    mac: str
    type: str
    model: str
    status: str
    rssi: int
    signal_level: int
    at_low_battery: bool
    nickname: str
    last_onboarding_timestamp: int
    report_interval_seconds: int  # Seconds between each report

    @staticmethod
    def try_from_json(kwargs: dict[str, Any]) -> Try["S200BDeviceState"]:
        return Try.of(
            lambda: S200BDeviceState(
                firmware_version=kwargs["fw_ver"],
                hardware_version=kwargs["hw_ver"],
                device_id=kwargs["device_id"],
                parent_device_id=kwargs["parent_device_id"],
                mac=kwargs["mac"],
                type=kwargs["type"],
                model=kwargs["model"],
                status=kwargs.get("status", False),
                rssi=kwargs.get("rssi", 0),
                signal_level=kwargs.get("signal_level", 0),
                at_low_battery=kwargs.get("at_low_battery", False),
                nickname=base64.b64decode(kwargs["nickname"]).decode("UTF-8"),
                last_onboarding_timestamp=kwargs.get("lastOnboardingTimestamp", 0),
                report_interval_seconds=kwargs.get("report_interval", 0),
            )
        )

    def get_semantic_firmware_version(self) -> semantic_version.Version:
        pieces = self.firmware_version.split("Build")
        try:
            if len(pieces) > 0:
                return semantic_version.Version(pieces[0].strip())
            else:
                return semantic_version.Version("0.0.0")
        except ValueError:
            return semantic_version.Version("0.0.0")


@dataclass
class RotationEvent:
    id: int
    timestamp: int
    degrees: int


@dataclass
class SingleClickEvent:
    id: int
    timestamp: int


@dataclass
class DoubleClickEvent:
    id: int
    timestamp: int


S200BEvent = Union[RotationEvent, SingleClickEvent, DoubleClickEvent]


def parse_s200b_event(item: dict[str, Any]) -> S200BEvent:
    event_type = item["event"]
    if event_type == "singleClick":
        return SingleClickEvent(item["id"], item["timestamp"])
    elif event_type == "doubleClick":
        return DoubleClickEvent(item["id"], item["timestamp"])
    else:
        return RotationEvent(
            item.get("id"), item.get("timestamp"), item.get("params")["rotate_deg"]
        )
