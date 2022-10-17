import math
import random
import matplotlib.pyplot as plt

#for plotting


class boat:
    angle = 0
    currentTurningRate = 0  # radians per second

    randomForceRange = [0.0, 0.0]
    Force = .5
    dragConstant =0.2
    mass = 10

    rudderPosition = 0
    rudderForceMult = 6
    rudderForce = 0

    totalForce=0
    def __init__(self,angle,force,randomForce):
        self.angle=angle
        self.Force=force
        self.randomForceRange=randomForce


    def setRudder(self, pos):
        if pos > math.pi / 4:
            pos = math.pi / 4
        if pos < -math.pi / 4:
            pos = -math.pi / 4
        self.rudderPosition = pos
        self.calculateRudderForce()

    def calculateRudderForce(self):
        self.rudderForce = self.rudderForceMult * self.rudderPosition


    def calculateStep(self, time):
        randomForce = random.uniform(self.randomForceRange[0], self.randomForceRange[1])
        self.totalForce = randomForce + self.Force + self.rudderForce
        self.totalForce -= self.dragConstant * (self.currentTurningRate + self.totalForce / self.mass * time / 2)
        # force is assumed to be constant over the time period

        #print(self.rudderForce,self.totalForce,self.angle,self.rudderForce/self.angle)
        finalTurningSpeed=self.currentTurningRate+self.totalForce/self.mass
        self.angle+=(finalTurningSpeed+self.currentTurningRate)/2*time
        self.currentTurningRate=finalTurningSpeed



class PID:
    intergral=0
    previousTime=0
    previous=0#used to calculate derivative

    #constants
    P=1
    I=1
    D=1

    min=-4
    max=4

    PTerm=0#keep track of the value of the individual terms
    ITerm=0
    DTerm=0

    def __init__(self,p,i,d,max,min,initialValue):
        self.P=p
        self.I=i
        self.D=d
        self.max=max
        self.min=min
        self.previous=initialValue

    def update(self,aim,value,time,multiplier):
        #update derivative
        if time-self.previousTime>0:
            derivative=(value-self.previous)/(time-self.previousTime)
        else:
            derivative=0#should only happen when t=0
        self.previous=value

        #update intergral
        self.intergral+=(value+self.previous-2*aim)


        out=self.P*(value-aim)+self.I*self.intergral+self.D*derivative*(time-self.previousTime)
        if out > self.max:
            out=self.max
        if out<self.min:
            out=self.min
        #print(value,aim,self.PTerm)
        self.PTerm=self.P*(value-aim)
        self.ITerm=self.I*self.intergral
        self.DTerm=self.D*derivative

        self.previousTime=time
        return out*multiplier



def run(P,I,D,time,startAngle,force,randomForce):
    tickTime=0.1#time between updates
    times=[]#stores the outputs so they can be graphed
    angles=[]
    rudderAngles=[]
    b=boat(startAngle,force,randomForce)
    controller=PID(P,I,D,math.pi/4,-math.pi/4,b.angle)
    random.seed(10)


    for i in range(int(time/tickTime)):
        times.append(i*tickTime)
        angles.append(b.angle)


        rudderAngle=controller.update(0,b.angle,tickTime*(1+i),-1)
        b.setRudder(rudderAngle)
        rudderAngles.append(rudderAngle)
        b.calculateStep(tickTime)
    return [times,angles,rudderAngles]


def main():
    time=160#time to run simulation

    startAngle=0#angle at start
    force=1#constant force to be aplied
    randomforce=[0,0]#range of random force to be aplied [min,max]
    #values of P I and D to be used
    tests=[[0.4,0,0.2],[0.4,0.001,0.2]]

    for t in tests:
        r=run(t[0],t[1],t[2],time,startAngle,force,randomforce)
        plt.plot(r[0], r[1],label="P="+str(t[0])+"   I="+str(t[1])+"   D="+str(t[2]))
    plt.xlabel('time (s)')
    plt.ylabel('angle (radians)')
    plt.legend()
    plt.show()
if __name__=="__main__":
    main()