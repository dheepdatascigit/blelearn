import asyncio
from bleak import BleakScanner, BleakClient
#from PyObjCTools import KeyValueCoding

uuid_battery_level_characteristic = '0000180f-0000-1000-8000-00805f9b34fb'

async def main():
    myDevice = ''
    devices = await BleakScanner.discover(5.0, return_adv=True)
    for d in devices:
        if(devices[d][1].local_name == "This Device"):
            print("Found it")
            myDevice = d

    address = myDevice
    async with BleakClient(address) as client:
        svcs = client.services
        print("Services")
        for service in svcs:
            print(service)

        getsrv = await client.get_services()
        # battery_level = await client.read_gatt_char(uuid_battery_level_characteristic)
        # print(int.from_bytes(battery_level))
        print(getsrv)    
asyncio.run(main())
