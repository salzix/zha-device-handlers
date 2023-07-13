"""Tuya irrigation valve TS0049 _TZ3210_0jxeoadc"""
from typing import Dict

from zigpy.profiles import zha
from zigpy.quirks import CustomDevice
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import Basic, Groups, Identify, OnOff, Ota, Scenes, Time
from zigpy.zcl.clusters.smartenergy import Metering

from zhaquirks import DoublingPowerConfigurationCluster
from zhaquirks.const import (
    DEVICE_TYPE,
    ENDPOINTS,
    INPUT_CLUSTERS,
    MODELS_INFO,
    OUTPUT_CLUSTERS,
    PROFILE_ID,
)
from zhaquirks.tuya import TuyaLocalCluster
from zhaquirks.tuya.mcu import (
    DPToAttributeMapping,
    EnchantedDevice,
    TuyaMCUCluster,
    TuyaOnOff,
    TuyaOnOffNM,
    TuyaPowerConfigurationCluster,
)
class TuyaValveFamilyCluster(TuyaMCUCluster):
    """On/Off Tuya family cluster with extra device attributes."""

    # salzix: I don't know what it does, commented by now.
    #
    # attributes = TuyaMCUCluster.attributes.copy()
    # attributes.update(
    #     {
    #         0xEF01: ("time_left", t.uint32_t, True),
    #         0xEF02: ("state", t.enum8, True),
    #         0xEF03: ("last_valve_open_duration", t.uint32_t, True),
    #         0xEF04: ("dp_6", t.uint32_t, True),
    #     }
    # )

    # salzix: datapoint values may be the same as here: https://github.com/Koenkk/zigbee2mqtt/issues/15124#issuecomment-1345161859
    dp_to_attribute: Dict[int, DPToAttributeMapping] = {
        101: DPToAttributeMapping(
            TuyaOnOff.ep_attribute,
            "on_off",
        ),
        # 5: DPToAttributeMapping(
        #     TuyaValveWaterConsumed.ep_attribute,
        #     "current_summ_delivered",
        # ),
        # 6: DPToAttributeMapping(
        #     TuyaMCUCluster.ep_attribute,
        #     "dp_6",
        # ),
        # 7: DPToAttributeMapping(
        #     DoublingPowerConfigurationCluster.ep_attribute,
        #     "battery_percentage_remaining",
        # ),
        # 11: DPToAttributeMapping(
        #     TuyaMCUCluster.ep_attribute,
        #     "time_left",
        # ),
        #     12: DPToAttributeMapping(
        #     TuyaMCUCluster.ep_attribute,
        #     "state",
        # ),
        # 15: DPToAttributeMapping(
        #     TuyaMCUCluster.ep_attribute,
        #     "last_valve_open_duration",
        # ),
    }

    data_point_handlers = {
        101: "_dp_2_attr_update",
        # 5: "_dp_2_attr_update",
        # 6: "_dp_2_attr_update",
        # 7: "_dp_2_attr_update",
        # 11: "_dp_2_attr_update",
        # 12: "_dp_2_attr_update",
        # 15: "_dp_2_attr_update",
    }

class TuyaIrrigationValve(CustomDevice):
    """Tuya green irrigation valve device."""

    signature = {
        MODELS_INFO: [("_TZ3210_0jxeoadc", "TS0049")],
        # SizePrefixedSimpleDescriptor(endpoint=1, profile=260, device_type=0, device_version=1,
        # input_clusters=[61184, 0], output_clusters=[25, 10])
        ENDPOINTS: {
            1: {
                PROFILE_ID: zha.PROFILE_ID,
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    TuyaValveFamilyCluster.cluster_id,
                    Basic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
            }
        },
    }

    replacement = {
        ENDPOINTS: {
            1: {
                DEVICE_TYPE: zha.DeviceType.ON_OFF_SWITCH,
                INPUT_CLUSTERS: [
                    TuyaOnOff,
                    Basic.cluster_id,
                ],
                OUTPUT_CLUSTERS: [Ota.cluster_id, Time.cluster_id],
            }
        }
    }