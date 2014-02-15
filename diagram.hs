{-# LANGUAGE NoMonomorphismRestriction #-}

import Diagrams.Prelude
import Diagrams.Backend.Cairo.CmdLine
import Data.List

driveR = "roomba drive"
joystick = "joystick"
lcd = "lcd"
turret = "turret"
sensorR = "roomba sensor"
sensorT = "turret sensor"

subsystemNames = [driveR, joystick, lcd, sensorR, sensorT, turret]
arrows = [(joystick, driveR)
         ,(joystick, lcd)
         ,(joystick, turret)
         ,(sensorR, lcd)
         ,(sensorT, lcd)]

node :: String -> Diagram B R2
node name = text name # scale 0.1 # fc white
         <> circle 0.2 # fc green # named name

queueH = hcat (replicate 5 (square 1 # fc blue)) 
         # translate (r2 (-2, 0))
         # scaleY (1/4) # scaleX (1/20) 

queueV = rotateBy (1/4) queueH

directQ = vcat [node "x", strutY 0.2, queueV]

subsystemGroup n = hcat $ intersperse (strutX 0.1) (replicate n directQ)

joystickLCD = (node joystick === strutY 0.2 === node lcd) 
              # translate (r2 (0, 0.3)) ||| queueV
uiGroup =  (joystickLCD <> square 1 # dashing [0.2,0.05] 0)
           # translate (r2 (1.5, 0))

subsystems = subsystemGroup 3 ||| strutX 0.5 ||| subsystemGroup 3 

example :: Diagram B R2
example = subsystems === strutY 0.3 === uiGroup

main = mainWith $ example
