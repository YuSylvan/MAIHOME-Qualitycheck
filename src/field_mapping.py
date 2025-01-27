# Define mapping between CSV field names and database column names
field_mapping = {
    'utc': 'Timestamp',
    'accMotion': 'AccMotion',
    'active_power': 'ActivePower',
    'battery': 'Battery',
    'co2': 'Co2',
    'current': 'Current',
    'current_tariff': 'CurrentTariff',
    'digital': 'Digital',
    'gas.kuub': 'GasKuub',
    'humidity': 'Humidity',
    'motor.position': 'MotorPosition',
    'motor.range': 'MotorRange',
    'negative_active_power': 'NegativeActivePower',
    'phase_a.current': 'PhaseACurrent',
    'phase_a.negative_active_power': 'PhaseANegativeActivePower',
    'phase_a.positive_active_power': 'PhaseAPositiveActivePower',
    'phase_a.voltage': 'PhaseAVoltage',
    'positive_active_power': 'PositiveActivePower',
    'pressure': 'Pressure',
    'pulseAbs': 'PulseAbs',
    'pulsecounter.pulses': 'PulsecounterPulses',
    'message.rssi': 'RSSI',
    'setTemperature': 'SetTemperature',  
    'message.snr': 'SNR',
    'state': 'State',
    'tariff1.negative_active_energy': 'Tariff1NegativeActiveEnergy',
    'tariff1.positive_active_energy': 'Tariff1PositiveActiveEnergy',
    'tariff2.negative_active_energy': 'Tariff2NegativeActiveEnergy',
    'tariff2.positive_active_energy': 'Tariff2PositiveActiveEnergy',
    'temperature': 'Temperature',
    'temperature.current': 'TemperatureCurrent',
    'temperature.set': 'TemperatureSet',
    'total_active_energy': 'TotalActiveEnergy',
    'tvoc': 'Tvoc',
    'vdd': 'Vdd',
    'voltage': 'Voltage',
    'x': 'X',
    'y': 'Y',
    'z': 'Z',
    'door.status': 'Doorstatus',
    'pir_status': 'Pirstatus',
    'light_level': 'Lightlevel',
    'window.status': 'Windowstatus'
}

# Columns not included
'''
output2
childlock !
max_authorised_power_consumption
power.charge
onewire.temp_C
buzzer_status
max_reduction_peak.value
power.vin_present
door.status   !!!!!!!!!!!!!!
wifi.rssi
power.vin_good
max_authorised_current
max_reduction_peak.timestamp
c03.reset_reason
phase_b.current
network_wan.latency
power_on
pir_status   !!!!!!!!!!!!!!
phase_c.negative_active_power
nb.rssi
postal.code

temperature.status
phase_b.negative_active_power
phase_b.voltage
meters.travelled
firmware.version
pulsecounter1.pulses
phase_c.voltage
motor.status
message.payload
address
memory.free
phase_c.positive_active_power
SensorID
window.status   !!!!!!!!!!!!!!
heading.degree  
speed
SensorType
positive_active_demand.total_current_period
movement.state
Timestamp
position.latitude
motionsensor
onewire.raw
satellites.visible
phase_b.positive_active_power
position.longitude
output1
phase_c.current
'''
