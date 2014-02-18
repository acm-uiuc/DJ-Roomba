{-# LANGUAGE NoMonomorphismRestriction #-}

import Diagrams.Prelude
import Diagrams.Backend.Cairo.CmdLine
import Data.List

driveR = "roomba.drive"
driveT = "turret.drive"
driveA = "audio.drive"

sensorR = "roomba.sensor"
sensorT = "turret.sensor"
sensorA = "audio.sensor"

joystick = "joystick"
lcd = "lcd"
turret = "turret"

qName = (++ ".queue")
displayQ = qName lcd

subsystemNames = [driveR, joystick, lcd, sensorR, sensorT, turret]
drivers = [driveR, driveT, driveA]
sensors = [sensorR, sensorT, sensorA]

arrows = queuesToNode drivers joystick
         ++ queuesToNode sensors lcd
         ++ [(joystick, displayQ ), (displayQ, lcd)]
         where queuesToNode queues node = zip (map qName queues) (repeat node)

node :: String -> Diagram B R2
node name = text name # scale 0.05 # fc white
            <> circle 0.2 # fc green # named name

queueH name = scale 0.04 (text name) === strutY 0.04 === (centerXY queueH')
               where queueH' = centerXY (hcat (replicate 5 (square 1 # fc blue)))
                               # translate (r2 (-2, 0))
                               # scaleY (1/4) # scaleX (1/20) 
                               # named name

queueV name = rotateBy (1/4) $ queueH name

directQ name = vcat [node name, strutY 0.2, queueV (qName')]
          # connectOutside' (with & tailSize .~ 0.05
                             & headSize  .~ 0.1
                             & shaftStyle %~ lw 0.001 ) name qName'
          where qName' = qName name

subsystemGroup names = hcat $ intersperse (strutX 0.1) (map directQ names)

joystickLCD = centerXY $ queueH displayQ === strutY 0.2 ===
              centerXY (node joystick ||| strutX 0.2 ||| node lcd) 
uiGroup = joystickLCD <> square 1 # dashing [0.2,0.05] 0

subsystems = centerXY $ subsystemGroup drivers ||| strutX 0.5 ||| subsystemGroup sensors

world :: Diagram B R2
world = (subsystems === strutY 0.3 === uiGroup)
        # applyAll [myConnect x y | (x,y) <- arrows]
       where myConnect = connectOutside' (with & tailSize .~ 0.05
                                          & headSize  .~ 0.1
                                          & shaftStyle %~ lw 0.001 )

main = mainWith world
