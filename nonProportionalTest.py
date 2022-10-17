from PID import PID
import matplotlib.pyplot as plt
import math


class delay:#this class delays data
    previousData=[]
    def __init__(self,items,initial):
        for i in range(int(items)):
            self.previousData.append(initial)
    def get(self,value):
        self.previousData.append(value)
        return self.previousData.pop(0)

def pow(x,power):
    if x>=0:
        return math.pow(x,power)
    return -math.pow(abs(x),power)
class tank:
    acidAdded=0
    reductionRate=5

    def addAcid(self,amount):
        if amount>0:
            self.acidAdded+=amount
    def calculateStep(self,time):
        if self.acidAdded>=time*self.reductionRate:
            self.acidAdded-=time*self.reductionRate


    def getpH(self):
        offset=-500
        multiplier=-1.5
        power=1/101

        return multiplier*pow((self.acidAdded+offset),power)+7


def run(P,I,D,time,delayTime):
    tickTime=0.1#time between updates
    times=[]#used to store outputs for graphing
    pHs=[]
    Ps=[]
    Is=[]
    Ds=[]
    t=tank()
    controller=PID(P,I,D,4,0,t.getpH())

    delayer=delay(delayTime/tickTime,t.getpH())

    for i in range(int(time/tickTime)):
        pH=t.getpH()
        response=controller.update(7,delayer.get(pH),tickTime*i,1)
        t.addAcid(1)

        t.calculateStep(tickTime)

        #log values for graphing
        times.append(i*tickTime)
        pHs.append(pH)
        Ps.append(controller.PTerm)
        Is.append(controller.ITerm)
        Ds.append(controller.DTerm)


    return [times,pHs,Ps,Is,Ds]


def main():
    fig,ax=plt.subplots()
    time=200#time to run simulation
    delayTime=1#lag between the observed value and wht is sent to the controller

    #values of P I and D to be used
    test=[0.4,0.001,0.3]

    r=run(test[0],test[1],test[2],time,delayTime)
    ax.plot(r[0], r[1],label="value P="+str(test[0])+"   I="+str(test[1])+"   D="+str(test[2]),color="black")
    ax2=ax.twinx()
    ax2.plot(r[0], r[2],label="P")
    ax2.plot(r[0], r[3],label="I")
    ax2.plot(r[0], r[4],label="D")

    ax.set_xlabel('time')
    ax.set_ylabel('pH')
    ax2.set_ylabel("control response")
    ax2.legend()
    plt.show()
if __name__=="__main__":
    main()