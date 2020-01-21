from machine import I2C
from machine import Pin
import ssd1306, time, network, gc
# import urequests as requests

# initialize display
i2c = I2C(sda=Pin(21), scl=Pin(23))
display = ssd1306.SSD1306_I2C(128, 32, i2c)

# initialize station interface

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = list(map(lambda nwk: nwk[0].decode('ascii'), wlan.scan()))
offset = 0
offset_incr = 8;
display.fill(0)
for nwk in networks:
    display.text(nwk, 0, offset)
    offset += offset_incr

display.show()

time.sleep(1)

for i in range(5):
    display.fill(0)
    display.text("Connecting"+("." * i), 5, 16)
    display.show()
    time.sleep(0.5)

time.sleep(1)
wlan.connect('akrpg 2', 'reddy002')

display.fill(0)
display.text("essid: akrpg 2", 1, 1)
display.show()

time.sleep(6)
ip_addr = wlan.ifconfig();
display.text("ip addr:", 1, 9)
display.text("%s" % ip_addr[0], 1, 17)

display.show()

newsAPIKey = 'af29a9c53a694edaab4523dda2344b25'
newsEndPoint = 'https://newsapi.org/v2/top-headlines'
newsParams = {
    'country': 'us',
    'apiKey': newsAPIKey,
    'pageSize': 1,
    'page': 1
}
# apikey param
gc.collect()
gc.mem_free()

r = requests.get(newsEndPoint, data=newsParams)
print(r.json())
