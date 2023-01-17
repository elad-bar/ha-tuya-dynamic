"""Device's mapper."""
from __future__ import annotations

import json
import logging

from homeassistant.components.switch import SwitchEntityDescription
from homeassistant.components.tuya.alarm_control_panel import ALARM
from homeassistant.components.tuya.binary_sensor import BINARY_SENSORS
from homeassistant.components.tuya.button import BUTTONS
from homeassistant.components.tuya.camera import CAMERAS
from homeassistant.components.tuya.climate import CLIMATE_DESCRIPTIONS
from homeassistant.components.tuya.cover import COVERS
from homeassistant.components.tuya.fan import TUYA_SUPPORT_TYPE
from homeassistant.components.tuya.humidifier import HUMIDIFIERS
from homeassistant.components.tuya.light import LIGHTS
from homeassistant.components.tuya.number import NUMBERS
from homeassistant.components.tuya.select import SELECTS
from homeassistant.components.tuya.sensor import SENSORS, TuyaSensorEntityDescription
from homeassistant.components.tuya.siren import SIRENS
from homeassistant.components.tuya.switch import SWITCHES
from homeassistant.const import Platform, UnitOfMass
from tuya_ce.helpers.const import ELECTRIC_RESISTANCE_OHM, WEATHER_CONDITION
from tuya_ce.models.platform_fields import PlatformFields

from ..helpers.dp_code import ExtendedDPCode
from ..helpers.enhanced_json_encoder import EnhancedJSONEncoder
from ..helpers.tuya_mapping import VACUUMS
from ..mappers.base import TuyaBaseConverter

_LOGGER = logging.getLogger(__name__)


class TuyaDevices(TuyaBaseConverter):
    def __init__(self):
        super().__init__("devices", self._get_devices)

    def _get_devices(self):
        """Do initialization of test dependencies instances, Returns None."""
        _LOGGER.info("Initialize")

        self._add_custom_devices()

        data_mapping = {
            Platform.CAMERA: list(CAMERAS),
            Platform.FAN: list(TUYA_SUPPORT_TYPE),
            Platform.VACUUM: list(VACUUMS),
        }

        data_items = {
            Platform.ALARM_CONTROL_PANEL: ALARM,
            Platform.BINARY_SENSOR: BINARY_SENSORS,
            Platform.BUTTON: BUTTONS,
            Platform.CLIMATE: CLIMATE_DESCRIPTIONS,
            Platform.COVER: COVERS,
            Platform.HUMIDIFIER: HUMIDIFIERS,
            Platform.LIGHT: LIGHTS,
            Platform.NUMBER: NUMBERS,
            Platform.SELECT: SELECTS,
            Platform.SENSOR: SENSORS,
            Platform.SIREN: SIRENS,
            Platform.SWITCH: SWITCHES,
        }

        platform_fields = {
            Platform.ALARM_CONTROL_PANEL: PlatformFields.ALARM_CONTROL_PANEL,
            Platform.BINARY_SENSOR: PlatformFields.BINARY_SENSOR,
            Platform.BUTTON: PlatformFields.BUTTON,
            Platform.CLIMATE: PlatformFields.CLIMATE,
            Platform.COVER: PlatformFields.COVER,
            Platform.HUMIDIFIER: PlatformFields.HUMIDIFIER,
            Platform.LIGHT: PlatformFields.LIGHT,
            Platform.NUMBER: PlatformFields.NUMBER,
            Platform.SELECT: PlatformFields.SELECT,
            Platform.SENSOR: PlatformFields.SENSOR,
            Platform.SIREN: PlatformFields.SIREN,
            Platform.SWITCH: PlatformFields.SWITCH,
        }

        devices = {}

        for domain in data_items:
            device_categories = data_items.get(domain)

            for device_category_key in device_categories:
                device_category_items = device_categories.get(device_category_key)

                if device_category_key not in devices:
                    devices[device_category_key] = {}

                domain_fields = platform_fields.get(domain, [])

                device_category_items_json = json.dumps(
                    device_category_items, cls=EnhancedJSONEncoder, indent=4
                )
                objs = json.loads(device_category_items_json)

                if not isinstance(objs, list):
                    objs = [objs]

                for obj in objs:
                    keys = list(obj)

                    for field in keys:
                        value = obj[field]
                        if (
                            field not in domain_fields or value is None
                        ) and field != "key":
                            del obj[field]

                devices[device_category_key][domain] = objs

        for domain in data_mapping:
            device_categories = data_mapping.get(domain)

            for device_category_key in device_categories:
                if device_category_key not in devices:
                    devices[device_category_key] = {}

                devices[device_category_key][domain] = True

        return devices

    @staticmethod
    def _add_custom_devices():
        SENSORS["ggq"] = (
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.SMART_WEATHER,
                name="Smart Weather",
                icon="mdi:sun-wireless",
                device_class=WEATHER_CONDITION,
            ),
        )

        SENSORS["sfkzq"] = (
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.WEATHER,
                name="Weather",
                icon="mdi:sun-wireless",
                device_class=WEATHER_CONDITION,
            ),
        )

        SENSORS["qt"] = (
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.WEIGHT_COUNT,
                name="Weight Count",
                icon="mdi:cached",
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.WEIGHT,
                name="Weight",
                icon="mdi:scale-bathroom",
                native_unit_of_measurement=UnitOfMass.KILOGRAMS,
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.LEFT_HAND_RESISTANCE,
                name="Left Hand Resistance",
                icon="mdi:hand-back-left",
                native_unit_of_measurement=ELECTRIC_RESISTANCE_OHM,
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.LEFT_LEG_RESISTANCE,
                name="Left Leg Resistance",
                icon="mdi:foot-print",
                native_unit_of_measurement=ELECTRIC_RESISTANCE_OHM,
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.RIGHT_HAND_RESISTANCE,
                name="Right Hand Resistance",
                icon="mdi:hand-back-right",
                native_unit_of_measurement=ELECTRIC_RESISTANCE_OHM,
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.RIGHT_LEG_RESISTANCE,
                name="Right Leg Resistance",
                icon="mdi:foot-print",
                native_unit_of_measurement=ELECTRIC_RESISTANCE_OHM,
            ),
            TuyaSensorEntityDescription(
                key=ExtendedDPCode.BODY_RESISTANCE,
                name="Body Resistance",
                icon="mdi:omega",
                native_unit_of_measurement=ELECTRIC_RESISTANCE_OHM,
            ),
        )

        SWITCHES["sfkzq"] = (
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_1,
                name="Zone 1",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_2,
                name="Zone 2",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_3,
                name="Zone 3",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_4,
                name="Zone 4",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_5,
                name="Zone 5",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_6,
                name="Zone 6",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_7,
                name="Zone 7",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.AREA_8,
                name="Zone 8",
                icon="mdi:water-pump",
            ),
            SwitchEntityDescription(
                key=ExtendedDPCode.QUICK_START,
                name="Quick Start",
                icon="mdi:water-pump",
            ),
        )

        SWITCHES["ggq"] = (
            SwitchEntityDescription(
                key=ExtendedDPCode.START,
                name="Start",
                icon="mdi:water-pump",
            ),
        )
