import time
import machine #type: ignore
import rpy.move
#mv=rpy.move.MOVE(offset=(0,0))
#sample lon hon la trang nho hon la den
ty=rpy.move.MOVE(offset=(5,5))		#offset theo thứ tự motor phải -> trái

def main():
    while True:
        ty.run_line()
        val=ty.run_line()
        if val ==1:
            ty.run_cm(13.7)
        if val ==0:
            ty.turn_degree(-90)
            ty.run_cm(15)
            time.sleep(2)
            ty.turn_degree(180)
            time.sleep(2)
            ty.run_cm(8)
            ty.turn_degree(-90)
            ty.nha_hat()
main()