import redis
import config
import ComputerStats
import pickle


class RedisConnection:

    def __init__(self,name=None):

        self.cache = redis.Redis(host= config.CacheHost , port= config.CachePort)
        if name:
            self.pcName = name
        else:
            self.pcName = ComputerStats.getPcName()
        self.saveCapacity()

    def saveCapacity(self):
        pcCapacity = {}
        disks = ComputerStats.getDiskPartitions()
        for disk in disks:
            pcCapacity["disk-cap:"+disk]=disks[disk]["total"]
        
        totalMemory = ComputerStats.getMemoryStats()["total"]
        pcCapacity["memory"]=totalMemory

        self.cache.hmset(name= self.pcName, mapping= pcCapacity)

    def broadcast(self,data):
        '''
        Pickle dict: data to bytes and publish
        '''
        toSend = pickle.dumps(data) #becomes bytes
        return self.cache.publish(channel="PC-"+self.pcName , message= toSend)
