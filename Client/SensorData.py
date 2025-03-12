from dataclasses import dataclass

# Message received [activity_data]: b'00:80:E1:27:BE:19_1741613104000_1741613708000_4_5_0_0000_0000_0000_000_000_000_0000_218'
# b'00:80:E1:27:BE:19_1741613104000_1741613708000_4_5_0_0000_0000_0000_000_000_000_0000_218'
# 00:80:E1:27:BE:19


@dataclass
class Sensordata:
    startTime: int
    endTime: int
    posture: int
    shortTermActivityLevel: int
    longTermActivityLevel: int
    jumps: int
    runs: int
    walkingSteps: int
    squats: int
    situps: int
    pushups: int
    averageSpeed: int
    stepCounter: int
    duration: int


# Constructor

    def __init__(self, data):
        values = data.split("_")

        self.startTime = values[1]
        self.endTime = values[2]
        self.posture = values[3]
        self.shortTermActivityLevel = values[4]
        self.longTermActivityLevel = values[5]
        self.jumps = values[6]
        self.runs = values[7]
        self.walkingSteps = values[8]
        self.squats = values[9]
        self.situps = values[10]
        self.pushups = values[11]
        self.averageSpeed = values[12]
        self.stepCounter = values[13]
        self.duration = self.endTime - self.startTime


@dataclass
class SensordataList:
    sensorList: list

    def append(self, data):
        self.sensorList.append(data)

    def readData(self, data):
        return

    def writeData(self, data):
        return

    def countForDay(self, day) -> int:
        return 0

    def filterForDay() -> list:
        return []
