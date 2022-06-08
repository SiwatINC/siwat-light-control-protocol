from time import sleep
import serial
from threading import Thread
from siwat_light_control_protocol.siwat_light_control_protocol import siwat_light_control_protocol
from siwat_light_control_protocol.input_validation import index_is_valid, validate_rgb, range_is_valid, LEDOutOfBoundError

class siwat_light_control_protocol_multi_serial(siwat_light_control_protocol):
    def __init__(self, serial_ports: list,led_map: list, baudrate: int = 115200, read_serial: bool = False, flow_control: bool = False) -> None:
        self.led_map = led_map
        self.flow_control = flow_control
        self.serial_ports = serial_ports
        self.serial_adapter = []
        for serial_port in serial_ports:
            self.serial_adapter.append(serial.Serial(serial_port,baudrate=baudrate))
        if read_serial:
            serial_reader = Thread(target=self.read_serial)
            serial_reader.start()
    def read_serial(self):
        while True:
            for i in range(len(self.led_map)):
                if self.serial_adapter[i].in_waiting:
                    data = self.serial_adapter.read_all()
                    print(data)
    
    def turn_off(self) -> None:
        for i in range(len(self.led_map)):
            packet = bytearray()
            packet.append(0x00)
            packet.append(0x01)
            packet.append(0xFF)
            self.serial_adapter[i].write(packet)
            self.show()

    def show(self) -> None:
        for i in range(len(self.led_map)):
            packet = bytearray()
            packet.append(0x00)
            packet.append(0x02)
            packet.append(0xFF)
            self.serial_adapter[i].write(packet)

    def set_led_at(self, led: int, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        r=int(r/255*250)
        g=int(g/255*250)
        b=int(b/255*250)
        slave,address = self.get_slave_address(led)
        packet = bytearray()
        packet.append(0x00)
        packet.append(0x04)
        packet.append(address)
        packet.append(r)
        packet.append(g)
        packet.append(b)
        packet.append(0xFF)
        self.serial_adapter[slave].write(packet)
        if self.flow_control:
            self.serial_adapter[slave].read()

    def rainbow(self):
        for i in range(len(self.led_map)):
            packet = bytearray()
            packet.append(0x00)
            packet.append(0x07)
            packet.append(0xFF)
            self.serial_adapter[i].write(packet)
    def get_slave_address(self,led: int) -> list:
        led_map = self.led_map
        slave = 0
        address =  None
        for i in range(len(led_map)+1):
            if sum(led_map[0:i]) > led:
                slave = i-1
                address = led-sum(led_map[0:i-1])
                break
        if address == None:
            raise LEDOutOfBoundError
        return [slave, address]
    def fill_led_with_color(self, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        for i in range(sum(self.led_map)):
            self.set_led_at(i,r,g,b)
        self.show()
    def fill_segment_with_color(self, segment_start: int, segment_stop: int, r: int, g: int, b: int):
        [r,g,b] = validate_rgb(r,g,b)
        if not range_is_valid(segment_start,segment_stop,sum(self.led_map)):
            raise LEDOutOfBoundError
        for index in range(segment_start,segment_stop+1):
            self.set_led_at(index,r,g,b)

    def is_connected(self) -> bool:
        adapter: serial.Serial
        for adapter in self.serial_adapter:
            if not adapter.isOpen():
                return False
        return True