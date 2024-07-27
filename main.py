import DeltaX2Lib

DeltaX2 = DeltaX2Lib.Deltax2Cmd()
DeltaX2.Home()
DeltaX2.SetSpeed(F=200)
for x in range(5):
    DeltaX2.MoveTo(Z=-300)
    DeltaX2.MoveTo(X=0,Y=0)
    DeltaX2.MoveTo(X=-100,Z=-350)
    DeltaX2.MoveTo(Z=-300)
    DeltaX2.MoveTo(X=0,Y=0)
    DeltaX2.MoveTo(X=100,Z=-350)
DeltaX2.Home()
