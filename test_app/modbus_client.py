from pymodbus.client.sync import ModbusSerialClient as ModbusClient

def get_modbus_client(port, baudrate=9600, timeout=1):
    """
    Setup and return a Modbus RTU client.
    """
    client = ModbusClient(method='rtu', port=port, baudrate=baudrate, timeout=timeout)
    if not client.connect():
        print(f"Unable to connect to the Modbus server at {port}.")
    return client

def get_multiple_holding_registers(client, address, count):
    """
    Read multiple holding registers from the Modbus server.
    """
    try:
        result = client.read_holding_registers(address, count, unit=1)
        if result.isError():
            print(f"Error reading registers at address {address}")
            return None
        return result.registers  # List of register values
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_lift_data(client):
    """
    Fetch lift data from multiple holding registers based on the address allocation.
    """
    address_map = {
        'floor_number': 21,
        'up_arrow': 20,
        'down_arrow': 19,
        'door_open': 18,
        'door_close': 17,
        'out_of_service': 16,
        'normal_mode': 15,
        'fault': 14,
        'alarm': 13,
        'fire_emergency': 12,
        'power_failure': 11,
        'attendance_mode': 10,
        'inspection_mode': 9,
        'independent': 8,
    }

    data = {}
    floor_data = get_multiple_holding_registers(client, address_map['floor_number'], 8)
    if floor_data:
        data['floor_number'] = floor_data
    else:
        data['floor_number'] = None

    for key, address in address_map.items():
        if key != 'floor_number':
            app_data = get_multiple_holding_registers(client, address, 1)
            if app_data:
                data[key] = app_data[0]
            else:
                data[key] = None

    return data
