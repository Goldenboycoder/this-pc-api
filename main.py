from typing import Optional
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import ComputerStats
import DynamicHtml
from enum import Enum
import uvicorn
import config



class CompStats(str,Enum):
    cpu = "cpu"
    network = "network"
    memory = "memory"
    processes = "processes"

class IsDetailed(str,Enum):
    simple = "simple"
    detailed = "detailed"

app=FastAPI()

@app.get("/GUI",response_class=HTMLResponse)
def read_rood():
    cpudetailedData = ComputerStats.getCpuUtilization(detailed=True)
    cpugeneralData = ComputerStats.getCpuUtilization()
    memoryStats = ComputerStats.getMemoryStats()
    diskStats = ComputerStats.getDiskPartitions()
    page = DynamicHtml.makeHomePage(cpugeneralData,cpudetailedData,memoryStats,diskStats)
    return page

@app.get("/compstats/cpu/{isdetailed}")
def read_cpuStat(isdetailed: IsDetailed):
    resp = {}
    if isdetailed == IsDetailed.simple:
        cpuUtil = ComputerStats.getCpuUtilization() #float
        physicalCores = ComputerStats.getNumberOfCPUA() #int
        logicalCores = ComputerStats.getNumberOfCPUA(logical=True) #int
        frequency = ComputerStats.getCPUFrequency() # in MHz
        resp = {
            "CPUUtilisation": cpuUtil,
            "PhysicalCores": physicalCores,
            "LogicalCores":logicalCores,
            "Frequency":frequency
        }
        return resp
    else:
        cpuUtil = ComputerStats.getCpuUtilization(detailed=True) #dict
        physicalCores = ComputerStats.getNumberOfCPUA() #int
        logicalCores = ComputerStats.getNumberOfCPUA(logical=True) #int
        frequency = ComputerStats.getCPUFrequency() # in MHz
        load = ComputerStats.getCPULoad() #dict
        resp = {
            "CPUUtilisation": cpuUtil,
            "PhysicalCores": physicalCores,
            "LogicalCores":logicalCores,
            "Frequency":frequency,
            "CPUload":load
        }
        return resp


@app.get("/compstats/memory")
def read_memoryStat():
    resp = ComputerStats.getMemoryStats()
    return resp

@app.get("/compstats/disks")
def read_disks(diskname: str = 'all'):
    diskStats = ComputerStats.getDiskPartitions()
    disks = [disk.replace("\\",'//') for disk in diskStats.keys()]
    tempDiskName = diskname.replace("\\",'/')
    if diskname == 'all':
        return ComputerStats.getDiskPartitions()
    else:
        if tempDiskName in disks:
            return diskStats[diskname.replace('\\\\','\\')]
        else:
            return {"Error" : "disk specified does not exist"} 

@app.get("/compstats/network/io")
def read_netio():
    return ComputerStats.getNetIO()

@app.get("/compstats/network/nic")
def read_nics(nic: str = "all"):
    nics = ComputerStats.getNetIfData()
    if nic == "all":
        return nics
    else:
        if nic in nics:
            return nics[nic]
        else:
            return {"Error" : "nic specified does not exist"}

@app.get("/compstats/users")
def read_users():
    return {"users" : ComputerStats.getCurrentUsers()}


@app.on_event("startup")
def onStartup_event():
    '''
    This runs on startup before anything else
    '''
    print("Starting ThisPcApi ...")

@app.on_event("shutdown")
def onShutdown_event():
    '''
    This runs on shutdown last
    '''
    print("Shutting down ThisPcApi")


def main():
    '''
    cmd : gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
    to run with process manager
    '''
    uvicorn.run("main:app", reload = config.uvicornReload, port = config.uviconrPort)

if __name__ == "__main__":
    main()