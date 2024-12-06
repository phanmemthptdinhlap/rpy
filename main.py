import time
import machine #type: ignore
import run 
#cài đặt chân xuất và nhận tín hiệu điêu khiển nhả lạc
__p_in__=15
__p_out__=17
#số lượng lạc đã nhả
__count__=0

m=run.RUN()
p_in=machine.Pin(__p_in__,machine.Pin.IN,machine.Pin.PULL_UP)
p_out=machine.Pin(__p_out__,machine.Pin.OUT)
def nhalac():
    p_out.off()
    time.time(0.5)
    p_out.on()
def setup():
    m.stop()
    p_out.on()
    p_in.irq(trigger=machine.Pin.IRQ_FALLING, handler=nha_irq)
def nha_irq(pin):
    __count__ = __count__ + 1
    print("Số lạc: ",__count__)
#Các giai đoạn thực hiện bài thi
def Layhatgiong():
    m.run_cm(20)
    m.run_find(1)
    m.run_cm(15)
    print("quay phải")
    m.turn_find(1)
    time.sleep(3)
    print("quay thêm")
    m.turn(10)
    time.sleep(3)
    m.run_step()
    time.sleep(3)

def main():
    Layhatgiong()















if __name__ == '__main__':
    setup()
    main()