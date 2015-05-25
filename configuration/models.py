from django.db import models

# Create your models here.

class NetworkDevice(models.Model):
    name = models.CharField(max_length=50)
    mac = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(protocol='IPv4')
    class Meta:
        abstract = True
        db_table = 'network_devices'

class NetworkActiveDevice(NetworkDevice):
    model = models.CharField(max_length=30)
    sw_version = models.CharField(max_length=30)
    sw_image = models.CharField(max_length=50)
    ports_number = models.PositiveSmallIntegerField()
    sn = models.CharField(max_length=30)
    default_gateway = models.GenericIPAddressField(protocol='IPv4')
    lldp_is_enabled = models.BooleanField(default=False)
    cdp_is_enabled = models.BooleanField(default=True)
    http_access_is_enabled = models.BooleanField(default=True)
    https_access_is_enabled = models.BooleanField(default=True)
    class Meta:
        db_table = 'network_active_devices'


class NetworkInterface(models.Model):
    network_device = models.ForeignKey('NetworkActiveDevice')
    description = models.CharField(max_length=100)
    is_switchport = models.BooleanField(default=True)
    is_access = models.BooleanField(default=True)
    access_vlan = models.PositiveSmallIntegerField()
    voice_vlan = models.PositiveSmallIntegerField()
    class Meta:
        db_table = 'network_interfaces'


class Vlan(models.Model):
    name = models.CharField(max_length=50)
    vlan_id = models.PositiveSmallIntegerField()
    class Meta:
        db_table = 'vlans'
    def __unicode__(self):
        return self.name


class Computer(NetworkDevice):
    network_interface = models.ForeignKey('NetworkInterface')
    cpu = models.CharField(max_length=50)
    ram_size = models.PositiveSmallIntegerField()
    hdd_model = models.CharField(max_length=50)
    hdd_size = models.PositiveSmallIntegerField()
    motherboard =models.CharField(max_length=50)
    class Meta:
        db_table = 'computers'


class Network(models.Model):
    name = models.CharField(max_length=50, verbose_name="Network Name")
    ip = models.GenericIPAddressField(protocol='IPv4',verbose_name="Network IP Address")
    netmask = models.SmallIntegerField()
    class Meta:
        db_table = 'networks'
    def __unicode__(self):
        return self.name