import time
import machine #type: ignore
import run 
import sowing
#cài đặt chân xuất và nhận tín hiệu điêu khiển nhả lạc
__san__=0 #1:sân phải 0:sân trái
s=sowing.SOWING()
#số lượng lạc đã nhả
m=run.RUN()
#lan nha lac
__lan_nha_lac__=2
#Các giai đoạn thực hiện bài thi
def nhalac():
    for _ in range(__lan_nha_lac__):
        s._laylac()
        s._nhalac()

def Layhatgiong():
    m.run_cm(20)
    m.run_find(1)
    m.run_cm(12)
    m.turn_find(__san__)
    m.run_step()
    m.run_cm(5)
    m.run_step()
    m.run_cm(20)
    time.sleep(1)
    m.run_cm(-25)
    m.turn(-45 if __san__ == 1 else 45)
    m.turn_find(0 if __san__ == 1 else 1)
    m.run_step()
    m.run_cm(10)
    m.turn(45 if __san__ == 1 else -45)
    m.turn_find(__san__)
    m.run_step()
def gieohatgiong(ben=0):
    m.run_cm(10)
    if ben == 1 or ben == 0:
        m.turn2(50,1)
        #gieo hat
        nhalac()
        m.turn2(-55,1)
    if ben == 2 or ben == 0:
        m.turn2(60,0)
        #gieo hat
        nhalac()
        m.turn2(-60,0)
    m.run_step()

def quaben():
    m.run_cm(10)
    m.turn(-45 if __san__ == 1 else 45)
    m.turn_find(0 if __san__ == 1 else 1)
    m.run_step()
    m.run_cm(10)
    m.turn(-45 if __san__ == 1 else 45)
    m.turn_find(0 if __san__ == 1 else 1)
    m.turn(20 if __san__ == 1 else -20)
    
    

def Layhatgiongmoi(r):  #số ô trắng là r
    for n in range(r):
        m.run_find(1)
        m.run_cm(5)
    m.run_cm(25)
    m.turn(97 if __san__==1 else -97)
    m.run_find(1)
    m.run_cm(5)
    m.run_cm(50)
    time.sleep(0.5)
    ### nhận hạt###
    m.run_find(0)
    m.run_cm(-10)
    m.run_find(0)
    m.run_cm(10)
    m.turn_find(-1 if __san__ ==1 else 1)
    m.turn(20 if __san__==1 else -20)
    m.run_find(1)
    m.run_cm(20)
    m.run_find(1)
    m.run_step()
    
    
    
    
def main():
    Layhatgiongmoi(1)
    for _ in range(4):
        gieohatgiong()
    quaben()
    for _ in range(4):
        gieohatgiong(2 if __san__ == 1 else 1)
    m.run_step()
    m.run_cm(10)
    m.run_step()
    m.run_cm(10)
    m.run_step()
    m.run_cm(10)
    m.stop()
if __name__ == '__main__':
    main()