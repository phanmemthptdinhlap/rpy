from asyncio import Event #type: ignore

import time #type: ignore
import _thread #type: ignore
import machine #type: ignore

class STEP:
    def __init__(self,pin=[35,36,37,38],tps=1):
        self.pin=[machine.Pin(pin[0],machine.Pin.OUT),
                  machine.Pin(pin[1],machine.Pin.OUT),
                  machine.Pin(pin[2],machine.Pin.OUT),
                  machine.Pin(pin[3],machine.Pin.OUT)]
        self.tps=tps
        self.steps=[[1,1,0,0],
                    [0,1,1,0],
                    [0,0,1,1],
                    [1,0,0,1]]
        self.index=0
        self.event=Event()

    def _run_step(self):
        for i in range(4):
            self.pin[i].value(self.steps[self.index][i])
        time.sleep(self.tps)
        self.index=self.index+1 if self.index<3 else 0

    def run(self):
        self.event.clear()
        def run_thread(self):
            while not self.event.is_set():
                self._run_step()
        self.running=_thread.start_new_thread(run_thread, (self,))

    def __call__(self):
        self.run()

    def stop(self):
        self.event.set()
