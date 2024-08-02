import DeltaX2Lib
import time

DeltaX2 = DeltaX2Lib.Deltax2Cmd()
Conveyor = DeltaX2Lib.ConveyorCmd()
DeltaX2.Home()
DeltaX2.SetAcceleration(1200)
DeltaX2.SetSpeed(200)
for x in range(5):
    DeltaX2.MoveTo(Z=-300)
    DeltaX2.MoveTo(X=0,Y=0)
    DeltaX2.MoveTo(X=-100,Z=-350)
    DeltaX2.MoveTo(Z=-300)
    DeltaX2.MoveTo(X=0,Y=0)
    DeltaX2.MoveTo(X=100,Z=-350)
DeltaX2.Home()
DeltaX2.MoveTo(Z=-350)
DeltaX2.MoveTo(X=50)
DeltaX2.ArcMove(1,X=-50,Y=0,I=-50,J=0)
DeltaX2.ArcMove(0,X=50,Y=0,I=50,J=0)

Conveyor.stop()
time.sleep(1)
Conveyor.SetPosition(150,-200)
time.sleep(1)
Conveyor.SetPosition(150,-200)
time.sleep(1)
Conveyor.SetPosition(150,-200)
time.sleep(1)
Conveyor.SetSpeed(100)
time.sleep(5)
Conveyor.stop()
time.sleep(1)
Conveyor.SetPosition(150,200)
time.sleep(1)
Conveyor.SetPosition(150,200)
time.sleep(1)
Conveyor.SetPosition(150,200)
time.sleep(1)






