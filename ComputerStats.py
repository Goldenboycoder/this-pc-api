#===========================Imports====================================
import os
import psutil
from psutil._common import bytes2human
from time import sleep
from socket import AF_INET
from socket import AF_INET6
from psutil import AF_LINK
import config
import platform
#==========================VARS==========================

loads = psutil.getloadavg()
config.isCpuMonitored = True
#===========================Utils======================================

#-----------------------------CPU--------------------------------------
def getCpuUtilization(detailed=False):
    '''
    By Default return float representing cpu utilization in a 1 second interval.\n
    When detailed = True returns a dict with the cpu core number as key and their utilization as value in a 2 second interval
    '''
    if not detailed:
        return psutil.cpu_percent(interval=1,percpu=False)
    else:
        cpus = psutil.cpu_percent(interval=2,percpu=True)
        cpuCorsUtils = {}
        for index,coreUtil in enumerate(cpus,start=1):
            cpuCorsUtils[index] = coreUtil
        return cpuCorsUtils


def getNumberOfCPUA(logical=False,affinity=False):
    '''
    Return the number of logical CPUs in the system\n
    If logical is False return the number of physical cores only, or None if undetermined.\n
    That can vary in case process CPU affinity has been changed, Linux cgroups are being\n
    used or (in case of Windows) on systems using processor groups or having more than 64 CPUs.
    '''
    if not affinity:
        return psutil.cpu_count(logical=logical)
    else:
        return len(psutil.Process().cpu_affinity())


def getCPUFrequency():
    '''
    Return CPU frequency current, expressed in Mhz. 
    '''
    return psutil.cpu_freq().current


def getCPULoad():
    '''
    Return the average system load over the last 1, 5 and 15 minutes as a dict.\n
    on Windows, the first time this is called and for the next 5 seconds it will return a meaningless (0.0, 0.0, 0.0) tuple.
    '''
    loads = psutil.getloadavg()
    if not config.isCpuMonitored:
        sleep(5.0)
        loads = psutil.getloadavg()
        sleep(5.0)
        loads = psutil.getloadavg()
        config.isCpuMonitored = True
        loads = psutil.getloadavg()

    
    logicalCPUs = getNumberOfCPUA(logical=True)
    percentages = [float(format(x / logicalCPUs *100,'.2f')) for x in loads]
    results = {
        "min1":percentages[0],
        "min5":percentages[1],
        "min15":percentages[2]}
    return results
    


#------------------------Memory-----------------------------

def getMemoryStats():
    '''
    Return statistics about system memory usage as a dict.
    '''
    memStats = psutil.virtual_memory()
    results = {
        "total":bytes2human(memStats.total),
        "available":bytes2human(memStats.available),
        "percentUsage": memStats.percent
    }
    return results



#-----------------------Disks-----------------------------------

def getDiskPartitions():
    '''
    Returns a dict of dicts representing stats of all mounted disk partitions
    '''
    parts = psutil.disk_partitions()
    results={}
    for part in parts:
        if os.name == "nt":
            if 'cdrom' in part.opts or part.fstype == '':
                continue
        diskStats = psutil.disk_usage(part.mountpoint)
        results[part.device] = {
            "fileSystemType": part.fstype,
            "total": bytes2human(diskStats.total),
            "free" : bytes2human(diskStats.free),
            "used": bytes2human(diskStats.used),
        }
    return results


#-----------------------Network-----------------------------------

def getNetIO():
    '''
    Return system-wide network I/O statistics as a dict
    '''
    netIOStats = psutil.net_io_counters()
    results = {
        "bytes_sent": bytes2human(netIOStats.bytes_sent),
        "bytes_recv": bytes2human(netIOStats.bytes_recv),
        "packets_sent": bytes2human(netIOStats.packets_sent),
        "packets_recv": bytes2human(netIOStats.packets_recv),
        "errin": bytes2human(netIOStats.errin),
        "errout" : bytes2human(netIOStats.errout),
        "dropin" : bytes2human(netIOStats.dropin),
        "dropout" : bytes2human(netIOStats.dropout),
    }
    return results

#psutil.net_connections(kind='inet')

def getNetIfData():
    '''
    Return information about each NIC (network interface card)\n
    installed on the system as a dictionary whose keys are the NIC names
    '''
    netIfAddrs = psutil.net_if_addrs()
    netIfStats = psutil.net_if_stats()
    results ={}
    for nic in netIfStats:
        for addr in netIfAddrs[nic]:
            if addr.family == AF_INET:
                results[nic] = {
                    "address" : addr.address,
                    "netmask" : addr.netmask,
                    "broadcast" : addr.broadcast,
                    "ptp" : addr.ptp,
                    "isup" : netIfStats[nic].isup,
                    "speed" : netIfStats[nic].speed
                }
    return results


#-------------------------------Other---------------------------------------

def getCurrentUsers():
    '''
    Returns a list of users currently connected to the system.
    '''
    users = psutil.users()
    results = []
    for user in users:
        results.append(user.name)
    return results

#------------------------------Processes--------------------------------------

def getProcesses():
    '''
    Returns a dict of processes where key is PID and value is a dict.\n
    This might take a while depending on the processes.
    '''
    procs = {p.pid: {
        **p.info,
        'cpu':p.cpu_percent(interval=0.1),
        'memory':p.memory_percent(),
        'threads':p.num_threads(),
        'isRunning':p.is_running(),
        } for p in psutil.process_iter(['name', 'username'])}
    return procs

def getWinServices():
    '''
    Return a dict of dicts where key is service name and value is a dict of the service stats
    '''
    services = {p.name: p for p in psutil.win_service_iter()}
    return services
    
    
def getPcName():
    return platform.node()