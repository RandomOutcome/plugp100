# Plug P100
This is a fork of work of [@petretiandrea](https://github.com/petretiandrea/plugp100), which in turn is a fork of [@K4CZP3R](https://github.com/K4CZP3R/tapo-p100-python) original work.

The purpose of this fork is to provide a version of the library that is backported to work with python v3.8 and v3.9, as a PyPi package.

The main change is to use ```Dict``` instead of ```dict``` types, as the latter is only handled for the custom types involved from python v3.10 onwards, and implement explicit castings requried.

This is used in [Domoticz plugin project](https://github.com/RandomOutcome/Domoticz-Tapo-P100-Plugin) to support the new TP-Link TAPO communication protocol firmware rolled out to P100 plugs in 2023.

# How to install
Not yet published to PyPI (will be ```pip install plugp100-3.9```)  

# Code example

```python
import asyncio
import os

from plugp100.api.hub.hub_device import HubDevice
from plugp100.api.light_effect_preset import LightEffectPreset
from plugp100.api.tapo_client import TapoClient
from plugp100.common.credentials import AuthCredential


async def main():
    # create generic tapo api
    username = os.getenv("USERNAME", "<tapo_email>")
    password = os.getenv("PASSWORD", "<tapo_password>")

    credentials = AuthCredential(username, password)
    client = TapoClient(credentials, "<tapo_device_ip>")
    await client.initialize()

    print(await client.get_device_info())
    print(await client.get_energy_usage())
    print(await client.get_current_power())
    print(await client.get_child_device_list())
    print(await client.get_child_device_component_list())
    print(await client.set_lighting_effect(LightEffectPreset.Aurora.to_effect()))

    # plug = PlugDevice(TapoClient(username, password), "<tapo_device_ip>")
    # light = LightDevice(TapoClient(username, password), "<tapo_device_ip>")
    # ledstrip = LedStripDevice(TapoClient(username, password), "<tapo_device_ip>")

    # - hub example
    # hub = HubDevice(client)
    # print(await hub.get_children())
    # print(await hub.get_state_as_json())


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()
```

