from siwat_light_control_protocol.siwat_light_control_protocol import siwat_light_control_protocol as slcp
from time import perf_counter as timecounter, sleep

led_map = [30,30]

leds = slcp("COM9",led_map=led_map,baudrate=14400,)

prev_time = timecounter()

for i in range(sum(led_map)):
    leds.set_led_at(i,0x60,0x60,0x60)
leds.show()

elapsed_time = timecounter() - prev_time

print("Benchmark Completed\n"
    + "number of leds: "+str(sum(led_map)) + "\n"
    + "refresh period: "+str(elapsed_time)+" seconds\n"
    + "refresh frequency: "+str(1/elapsed_time)+" Hz")