# README

## Communication:
Port diagram
```
    [FMC]                               [Controller]
                        -------------
    Video ->            |2000   2400| -> Video
                        |       2500| <- Video heartBit
                        |           |
    Data ->             |2100   2600| -> Data
                        |       2700| <- Data heartBit
                        |           |
    Command <-          |2200   2800| <- Command
    Command heartBit -> |2300       |
                        -------------
```
