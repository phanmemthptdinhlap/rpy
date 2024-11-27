import rpy.nhalac as nhalac
import time
import machine #type: ignore
def main():
  nhl=nhalac.NhaLac(6,8,0)
  while True:
    nhl._laylac()
    if nhl.colac():
      print('Lay lac thanh cong')
      nhl.nhalac()
      if not nhl.colac():
        print('Nha lac thanh cong')
      else:
        print('Nha lac khong thanh cong')
    else:
       print('Lay lac khong thanh cong')
    time.sleep(5)
if __name__ == '__main__':
    main()