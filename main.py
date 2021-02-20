import machine,   time, math, network, utime ,      json,gc
from machine import Pin, SoftI2C
import ssd1306
import urequests
from machine import WDT
import ntptime 

wifi=network.WLAN(network.STA_IF) 
wifi.active(True) 
wifi.connect("YOUR SSID NAME","YOUR WIFI PASSWOrD") 
time.sleep(8)

i2c = SoftI2C(scl=Pin(18), sda=Pin(19), freq=100000)

oled_width = 128                                                                                                                                  
oled_height = 64                                                                                                                                  
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
#oled.text('abc, World 1!', 0, 0)                                                                                                                
#oled.text('def, World 2!', 0, 10)                                                                                                               
#oled.text('3Hello, World 3!', 0, 20)                                                                                                                 
#oled.show() 

ddd={'Bitcoin':'btc_btcbitstamp'}
fontn={
'1':
[0x00,0x00,0x00,0x08,0x38,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x08,0x3E,0x00,0x00],#"1",0*/
'2':
[0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x02,0x04,0x08,0x10,0x20,0x42,0x7E,0x00,0x00],#"2",1*/
'3':
[0x00,0x00,0x00,0x3C,0x42,0x42,0x02,0x04,0x18,0x04,0x02,0x42,0x42,0x3C,0x00,0x00],#"3",2*/
'4':
[0x00,0x00,0x00,0x04,0x0C,0x0C,0x14,0x24,0x24,0x44,0x7F,0x04,0x04,0x1F,0x00,0x00],#"4",3*/
'5':
[0x00,0x00,0x00,0x7E,0x40,0x40,0x40,0x78,0x44,0x02,0x02,0x42,0x44,0x38,0x00,0x00],#"5",4*/
'6':
[0x00,0x00,0x00,0x18,0x24,0x40,0x40,0x5C,0x62,0x42,0x42,0x42,0x22,0x1C,0x00,0x00],#"6",5*/
'7':
[0x00,0x00,0x00,0x7E,0x42,0x04,0x04,0x08,0x08,0x10,0x10,0x10,0x10,0x10,0x00,0x00],#"7",6*/
'8':
[0x00,0x00,0x00,0x3C,0x42,0x42,0x42,0x24,0x18,0x24,0x42,0x42,0x42,0x3C,0x00,0x00],#"8",7*/
'9':
[0x00,0x00,0x00,0x38,0x44,0x42,0x42,0x42,0x46,0x3A,0x02,0x02,0x24,0x18,0x00,0x00],#"9",8*/
'0':
[0x00,0x00,0x00,0x18,0x24,0x42,0x42,0x42,0x42,0x42,0x42,0x42,0x24,0x18,0x00,0x00],#"0",9*/	 
'.':
[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x60,0x60,0x00,0x00],#".",10*/
'"':
[0x00,0x12,0x24,0x24,0x48,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],#""",11*/
'\'':
[0x00,0x60,0x20,0x20,0x40,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00],#"'",12*/
':':
[0x00,0x00,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00,0x00,0x00,0x18,0x18,0x00,0x00], #":",13*/
'$':
[0x00,0x00,0x08,0x3C,0x4A,0x4A,0x48,0x38,0x0C,0x0A,0x0A,0x4A,0x4A,0x3C,0x08,0x08], #"$",14*/
}



def chinese4(ch_str, x_axis, y_axis): 
    offset_ = 0 
    y_axis = y_axis*8  # 中文高度一行占8个  
    x_axis = (x_axis*16)  # 中文宽度占16个 
    code = 0x00  # 将中文转成16进制编码 
    #data_code = k.encode("utf-8") 
    #code |= data_code[0] << 16     
    mask=1
    for k in ch_str:
        #code = 0x00  # 将中文转成16进制编码 
        #
        byte_data = fontn[k]
        #print(byte_data)
        for y in range(0, 16):
            b =byte_data[y]
            #a =byte_data[y+16]
            for x in range(0, 8)[::-1]:
                #r1= a & mask
                #oled.pixel(x_axis+offset_+x, y+y_axis, r1)
                #a=a>>1
                r2= b & mask
                oled.pixel(x_axis+offset_+x+8, y+y_axis, r2)
                b=b>>1
                #oled.pixel(x_axis+offset_+x+8, y+y_axis, int(b_[x]))      
        offset_ += 8        
    #oled.show()
url = 'https://finnhub.io/api/v1/crypto/symbol?exchange=binance&token=%s'
url2 = 'https://finnhub.io/api/v1/quote?symbol=BINANCE:BTCUSDC&token=%s'
#baseurl = 'https://finnhub.io/api/v1/quote?symbol=BINANCE:%s&token=%s' 
baseurl = 'http://202.91.32.138:18080/api/v1/quote?symbol=BINANCE:%s&token=%s' 
token = 'YOUR TOKEN HERE'
url = url % token
url2 = url2 % token  #ETHUSDC
url3 = baseurl % ('ETHUSDC',token)

def bit(name):
    url2 = baseurl % (name,token)
    r =  urequests.get(url2)
    j=r.json()
    #print(j['c'])
    return(j['c'])

def rr(name,tag):
    #f=parse2(ddd)
    b=bit(tag)
    t=str(utime.localtime()[3])+':'+str(utime.localtime()[4])+':'+str(utime.localtime()[5])
    oled.fill(0)
    oled.text(name,0,1)
    #oled.text(t, 2, 35)
    chinese4(t,0,2)
    if b is not None:
        chinese4('$:'+str(b),0,5)
    oled.show()     

rr('BitCoin Price ','BTCUSDC')  


def formats(str1):
    if len(str1)==1:
        return('0'+str1)
    return(str1)
    
def r():
    #f=parse2(ddd)
    b=bit()
    t=formats(str(utime.localtime()[3]))+':'+formats(str(utime.localtime()[4]))+':'+formats(str(utime.localtime()[5]))
    oled.fill(0)
    oled.text('BitCoin Price ',0,1)
    #oled.text(t, 2, 35)
    chinese4(t,0,2)
    if b is not None:
        chinese4('$:'+str(b),0,5)
    oled.show()     

ntptime.settime() 

wdt = WDT(timeout=60000 * 10)  # enable it with a timeout of 2s
wdt.feed()



timer = machine.Timer(0) 
def handleInterrupt(timer):
    rr('BitCoin Price','BTCUSDC')  
    time.sleep(10)
    rr('ETH Price','ETHUSDC')      

timer.init(period=20000, mode=machine.Timer.PERIODIC, callback=handleInterrupt)  


#while True:
#    rr('BitCoin Price','BTCUSDC')  
#    time.sleep(10)
#    rr('ETH Price','ETHUSDC')  
#    time.sleep(10)
