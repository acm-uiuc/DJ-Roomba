{-# LANGUAGE NoMonomorphismRestriction #-}

import Diagrams.Prelude
import Diagrams.Backend.Cairo.CmdLine

driveR = "roomba drive"
joystick = "joystick"
lcd = "lcd"
turret = "turret"
sensorR = "roomba sensor"
sensorT = "turret sensor"

subsystems = [driveR, joystick, lcd, sensorR, sensorT, turret]
arrows = [(joystick, driveR)
         ,(joystick, lcd)
         ,(joystick, turret)
         ,(sensorR, lcd)
         ,(sensorT, lcd)]

node :: String -> Diagram B R2
node name = text name # scale 0.1 # fc white
         <> circle 0.4 # fc green # named name

tournament :: [String] -> Diagram B R2
tournament sysl = decorateTrail (regPoly n 1.2) (map node sysl)
                  where n = length sysl

queueH = scale (1/10) $ foldr1 (|||) (replicate 5 (square 1 # fc red))
queueV = rotateBy (1/4) queueH

example :: Diagram B R2
example = queueH ||| queueV

main = mainWith $ example
