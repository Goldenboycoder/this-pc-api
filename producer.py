from RedisConnector import RedisConnection
import config
import ComputerStats
from time import sleep

class Producer:

    def __init__(self,name=None):
        self.redis = RedisConnection(name = name)
        self.watched = True
        self.extraTime = 0

    def collectData(self):
        data={}
        data["cpuUtil"] = ComputerStats.getCpuUtilization(detailed=True)
        data["cpuFreq"] = ComputerStats.getCPUFrequency()
        data["cpuLoad"] = ComputerStats.getCPULoad()
        data["memory"] = ComputerStats.getMemoryStats()
        data["disks"] = ComputerStats.getDiskPartitions()
        data["netIO"] = ComputerStats.getNetIO()
        return data
    
    def startProducing(self):
        while config.produce:
            sleep(config.broadcastFrequency + self.extraTime)
            data = self.collectData()
            subs = self.redis.broadcast(data)
            if subs == 0:
                self.extraTime = 300
            else:
                self.extraTime = 0
