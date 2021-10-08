import redis
import config
import ComputerStats

cache = redis.Redis(host= config.CacheHost , port= config.CachePort)
pcName = ComputerStats.getPcName()

cache.set('foo','bar')
cache.publish(channel="pc-"+pcName , message= {"name":pcName,"message":"gg"})