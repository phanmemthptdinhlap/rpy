import machine #type: ignore

class LOG:
    def __init__(self,filename):
        self.file=open(filename,"a")
    def __call__(self,values):
        self.file.write(f"{values[0]}, {values[1]}, {values[2]}, {values[3]}\n")

class ADCS:
    def __init__(self, pin=[33,34,35,36],
                 sample=[1300,1700,2100,1700]):
        self.adcs=[machine.ADC(machine.Pin(pin[0])),
                   machine.ADC(machine.Pin(pin[1])),
                   machine.ADC(machine.Pin(pin[2])),
                   machine.ADC(machine.Pin(pin[3]))]
        self.sample=sample 
        for adc in self.adcs:
            adc.atten(machine.ADC.ATTN_11DB)
        #self.log=LOG("data.txt")

    def set_sample(self,sample):
        self.sample=sample

    def get_raw(self,pin=None):
        if pin is not None:
            return self.adcs[pin].read()
        else:
            return [adc.read() for adc in self.adcs]

    def line(self):
        adcs=self.get_raw()
        #print(adcs)
        #self.log(adcs)
        return ((True if adcs[0]<self.sample[0] else False),
                (True if adcs[1]<self.sample[1] else False),
                (True if adcs[2]<self.sample[2] else False),
                (True if adcs[3]<self.sample[3] else False))
