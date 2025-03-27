import rpy.nhalac as nhalac
import time
import machine #type: ignore
import run 
import sowing
#cài đặt chân xuất và nhận tín hiệu điêu khiển nhả lạc
__p_in__=15
__p_out__=17
#số lượng lạc đã nhả
__count__=0

m=run.RUN()
s=sowing.SOWING()
p_in=machine.pin(__p_in__,machine.Pin.IN,machine.Pin.PULL_UP)
p_out=machine.Pin(__p_out__,machine.Pin.OUT)
def nhalac():
    p_out.off()
    time.time(0.5)
    p_out.on()
def setup():
    s.begin()
    m.stop()
    p_out.on()
    p_in.irq(trigger=machine.Pin.IRQ_FALLING, handler=nha_irq)
def nha_irq(pin):
    __count__ = __count__ + 1
    print("Số lạc: ",__count__)
#Các giai đoạn thực hiện bài thi
def giaidoan1()