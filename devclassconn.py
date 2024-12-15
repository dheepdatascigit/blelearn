import asyncio
from bleak import BleakScanner, BleakClient

class DeviceBle():

    def __init__(self):
        self.client = None
        self.uuid_battery_service = '0000180f-0000-1000-8000-00805f9b34fb'
        # self.uuid_battery_service = '0000181c-0000-1000-8000-00805f9b34fb'
        self.uuid_battery_level_characteristic = '00002a19-0000-1000-8000-00805f9b34fb'
        # self.uuid_battery_level_characteristic = '00002ab4-0000-1000-8000-00805f9b34fb'

        self.client_name = None
        self.client_address = None

    async def discover(self):
        devices = await BleakScanner.discover(5.0, return_adv=True)
        for device in devices:
            print(device, devices[device][1])
            advertisement_data = devices[device][1]
            if(advertisement_data.local_name == "This Device"):
                if(advertisement_data.rssi > -90):
                    self.device = devices[device]
                    self.client_name = advertisement_data.local_name
                    return device
    
    async def connect(self):
        address = await self.discover()
        if address is not None:
            try:
                print(f"Found device at address: {address}")
                self.client_address = address
                print(f"Attmpting to connect...Name: {self.client_name}")
                self.client = BleakClient(address)
                await self.client.connect()
                print(f"Connected to Name: {self.client_name}")
            except:
                raise Exception(f"Failed to connect Name: {self.client_name}")
        else:
            raise Exception("Did not find available devices")
        
    async def disconnect(self):
        try:
            print(f"Disconnecting...Name: {self.client_name}")
            await self.client.disconnect()
            print(f"Disconnected! Name: {self.client_name}")
        except:
            raise Exception(f"Warning: Failed to disconnect Name: {self.client_name}. Check for hanging connection")
    
    def notification_handler(sender, data):
        """Simple notification handler which prints the data received."""
        output_numbers = list(data)
        print(output_numbers)

    async def read_characteristic(self, uuid):
        try:
            await self.client.read_gatt_char(uuid)
            # await self.client.start_notify(uuid, self.notification_handler)
            # await asyncio.sleep(10.0)
            # await self.client.stop_notify(uuid)
        except Exception as e:
            raise Exception(f"Failed to read characteristic.{e}")
        
    async def read_battery_level(self):
        battery_level = await self.read_characteristic(self.uuid_battery_level_characteristic)
        return int.from_bytes(battery_level)
    
