# __author__ = 'pavlov'

from ConfigParser import RawConfigParser
from sys import exit
import pymssql

orbconffile = '../orbit.cfg'

# Read the Orbit configuration file
config = RawConfigParser()
try:
    config.read(orbconffile)
    dbhost = config.get('SCCMDBConfig', 'dbhost')
    dbname = config.get('SCCMDBConfig', 'dbname')
    dbuser = config.get('SCCMDBConfig', 'dbuser')
    dbpass = config.get('SCCMDBConfig', 'dbpass')
except:
    print "Check the configuration file " + orbconffile
    exit(1)

confpcsel = ("SELECT distinct"
             " CS.Name0 as 'Computer Name',"
             " CS.Manufacturer0 as 'Manufacturer Name',"
             " CS.Model0 as 'Model Name',"
             " CS.SystemType0 as 'System Type',"
             " REPLACE(CS.UserName0,'FORUM\','') as 'User',"
             " BIOS.Manufacturer0 as 'Bios Manufacturer',"
             " BIOS.Name0 as 'Bios Name',"
             " SE.SerialNumber0 as 'System Enclosure SN',"
             " OS.Caption0 as 'OS',"
             " RAM.TotalPhysicalMemory0/1000/1000 as 'Total Memory',"
             " sum(isnull(LDisk.Size0,'0'))/1024 as 'Hardrive Size',"
             " CPU.Name0 as 'CPU Name',"
             " CPU.NormSpeed0 as 'CPU Speed',"
             " CPU.SocketDesignation0 as 'CPU Socket',"
             " VC.Name0 as 'Video Controller Name',"
             " VC.VideoProcessor0 as 'Video Processor Name',"
             " VC.VideoModeDescription0 as 'Current Display Resolution',"
             " 'Production' as 'Deployment State',"
             " 'Operational' as 'Incident State' "
             " FROM v_GS_COMPUTER_SYSTEM CS right join v_GS_PC_BIOS BIOS on BIOS.ResourceID = CS.ResourceID"
             " right join v_GS_SYSTEM SYS on SYS.ResourceID = CS.ResourceID"
             " right join v_GS_OPERATING_SYSTEM OS on OS.ResourceID = CS.ResourceID"
             " right join v_RA_System_SMSAssignedSites RAA on RAA.ResourceID = CS.ResourceID"
             " right join V_GS_X86_PC_MEMORY RAM on RAM.ResourceID = CS.ResourceID"
             " right join v_GS_Logical_Disk LDisk on LDisk.ResourceID = CS.ResourceID"
             " right join v_GS_Processor CPU on CPU.ResourceID = CS.ResourceID"
             " right join v_GS_SYSTEM_ENCLOSURE SE on SE.ResourceID = CS.ResourceID"
             " right join v_GS_VIDEO_CONTROLLER VC on VC.ResourceID = CS.ResourceID"
             " WHERE LDisk.DriveType0 =3 and"
             " CPU.DeviceID0 = 'CPU0' and"
             " CPU.SocketDesignation0 is not NULL and"
             " VC.VideoProcessor0 is not NULL and"
             " VC.VideoModeDescription0 is not NULL"
             " group by CS.Name0,"
             " CS.Manufacturer0,"
             " CS.Model0,"
             " CS.SystemType0,"
             " CS.Username0,"
             " BIOS.Manufacturer0,"
             " BIOS.Name0,"
             " SE.SerialNumber0,"
             " OS.Caption0,"
             " RAM.TotalPhysicalMemory0,"
             " CPU.Name0,"
             " CPU.NormSpeed0,"
             " CPU.SocketDesignation0,"
             " VC.Name0,"
             " VC.VideoProcessor0,"
             " VC.VideoModeDescription0" )


# Connect to Orbit database
try:
    dbconn = pymssql.connect(dbhost, dbuser, dbpass, dbname)
except pymssql.OperationalError as e:
    print "Can't connect to %s database. Check connection to server %s" % (dbname, dbhost)
    print e
    exit(1)

dbcursor = dbconn.cursor()

print "OK"

dbcursor.close()
dbconn.close()

