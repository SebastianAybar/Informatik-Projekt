from dataclasses import dataclass
from datetime import datetime

# Message received [activity_data]: b'00:80:E1:27:BE:19_1741613104000_1741613708000_4_5_0_0000_0000_0000_000_000_000_0000_218'
# b'00:80:E1:27:BE:19_1741613104000_1741613708000_4_5_0_0000_0000_0000_000_000_000_0000_218'
# 00:80:E1:27:BE:19


@dataclass
class Sensordata:
    startTime: datetime
    endTime: datetime
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
    duration: int #in secounds


# Constructor

    def __init__(self, data):
        values = data.split("_")

        self.startTime = datetime.strptime(values[1], "%Y-%m-%d %H:%M:%S")
        self.endTime = datetime.strptime(values[2], "%Y-%m-%d %H:%M:%S")
        self.posture = int(values[3])
        self.shortTermActivityLevel = int(values[4])
        self.longTermActivityLevel = int(values[5])
        self.jumps = int(values[6])
        self.runs = int(values[7])
        self.walkingSteps = int(values[8])
        self.squats = int(values[9])
        self.situps = int(values[10])
        self.pushups = int(values[11])
        self.averageSpeed = int(values[12])
        self.stepCounter = int(values[13])
        self.duration = int((self.endTime - self.startTime).total_seconds())


@dataclass
class SensordataList:
    sensorList: list

    def __init__(self):
        self.sensorList = []
        file = open("ReaderData.txt","r")
        for line in file:
            if line:
                self.sensorList.append(Sensordata(line))
   
    def writeData(self, data):
        file = open("ReaderData.txt","a")
        file.write(data+ "\n")
        self.sensorList.append(Sensordata(data))

    def maxForDay(self, date, attribute):
        datalist = self.filterForDay(date)
        total_count = max(getattr(data, attribute, 0) for data in datalist)
        return total_count

    def countForDay(self, date, attribute) -> int:
        datalist = self.filterForDay(date)
        total_count = sum(getattr(data, attribute, 0) for data in datalist)
        return total_count

    def filterForDay(self,date) -> list:
        dayList = []
        for data in self.sensorList:       
            if data.endTime.date() == date.date():
                dayList.append(data)         
        return dayList

    #remove later
    def getData(self):
        print(self.sensorList)
        print("\n")        
        
