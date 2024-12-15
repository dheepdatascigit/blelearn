import asyncio
import devclassconn


def notification_handler(sender, data):
    """Simple notification handler which prints the data received."""
    output_numbers = list(data)
    print(output_numbers)

'''
async def main(address):
    async with BleakClient(address) as client:
        await client.start_notify(UUID, notification_handler)
        await asyncio.sleep(10.0)
        await client.stop_notify(UUID)
'''

async def main():
    device = devclassconn.DeviceBle()
    try:
        await device.connect()
        battery_level = await device.read_battery_level()
        await device.disconnect()
    except Exception as e:
        print(e)

asyncio.run(main())