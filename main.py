import DeltaX2Lib
import time

DeltaX2 = DeltaX2Lib.Deltax2Cmd()
Conveyor = DeltaX2Lib.ConveyorCmd()

DeltaX2.Home()
DeltaX2.SetAcceleration(1200)
DeltaX2.SetSpeed(200)

DeltaX2.Home()
DeltaX2.MoveTo(Z=-350)
DeltaX2.MoveTo(X=50)
DeltaX2.ArcMove(1,X=-50,Y=0,I=-50,J=0)
DeltaX2.ArcMove(0,X=50,Y=0,I=50,J=0)

Conveyor.SetSpeed(150)
time.sleep(2)
Conveyor.SetSpeed(-150)
time.sleep(2)

Conveyor.stop()
for x in range(4):
    DeltaX2.MoveTo(Z=-280)
    DeltaX2.MoveTo(X=0,Y=0)
    Conveyor.SetPosition(150,200)
    DeltaX2.MoveTo(X=-100,Z=-320)
    DeltaX2.MoveTo(Z=-280)
    DeltaX2.MoveTo(X=0,Y=0)
    Conveyor.SetPosition(150,200)
    DeltaX2.MoveTo(X=100,Z=-320)





