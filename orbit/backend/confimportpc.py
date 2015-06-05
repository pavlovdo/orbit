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

confpcsel = ("SELECT distinct CS.Name0, CS.Manufacturer0, CS.Model0, CS.SystemType0, REPLACE(CS.UserName0,'FORUM\',''),"
             " BIOS.Manufacturer0, BIOS.Name0, SE.SerialNumber0, OS.Caption0, RAM.TotalPhysicalMemory0/1000/1000,"
             " sum(isnull(LDisk.Size0,'0'))/1024, CPU.Name0, CPU.NormSpeed0, CPU.SocketDesignation0, VC.Name0,"
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

dbcursor.execute(confpcsel)
rows = dbcursor.fetchone()

print rows

dbcursor.close()
dbconn.close()

