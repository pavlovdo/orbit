from django.db import models

# Create your models here.


class MACAddress(models.Model):
    mac = models.CharField(max_length=20)
    ip = models.GenericIPAddressField(protocol='IPv4')
    uplink_interface = models.ForeignKey('NetworkInterface')
    class Meta:
        db_table = 'mac_adrresses'


class EthCard(MACAddress):
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=30)
    pc = models.ForeignKey('PC')
    class Meta:
        db_table = 'eth_cards'


class NetworkInterface(models.Model):
    network_device = models.ForeignKey('NetworkActiveDevice')
    description = models.CharField(max_length=100)
    is_switchport = models.BooleanField(default=True)
    is_access = models.BooleanField(default=True)
    is_port_security = models.BooleanField(default=False)
    is_negotiate = models.BooleanField(default=True)
    is_bpduguard = models.BooleanField(default=False)
    is_bpdufilter = models.BooleanField(default=False)
    ps_max = models.PositiveSmallIntegerField(default=1)
    access_vlan = models.ForeignKey('Vlan', related_name='access_vlan')
    voice_vlan = models.ForeignKey('Vlan', related_name='voice_vlan')
    class Meta:
        db_table = 'network_interfaces'


class PC(models.Model):
    name = models.CharField(max_length=20)
    cpu = models.CharField(max_length=50)
    motherboard = models.CharField(max_length=50)
    ram_size = models.PositiveSmallIntegerField()
    hdd_size = models.PositiveSmallIntegerField()
    videocard = models.CharField(max_length=50)
    class Meta:
        db_table = 'personal_computers'


class Phone(MACAddress):
    name = models.CharField(max_length=20)
    model = models.CharField(max_length=50)
    manufacturer = models.CharField(max_length=30)
    class Meta:
        db_table = 'phones'


class NetworkActiveDevice(models.Model):
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


class Vlan(models.Model):
    name = models.CharField(max_length=50)
    vlan_id = models.PositiveSmallIntegerField()
    interfaces = models.ManyToManyField(NetworkInterface)
    class Meta:
        db_table = 'vlans'
    def __unicode__(self):
        return self.name


class Network(models.Model):
    name = models.CharField(max_length=50, verbose_name="Network Name")
    ip = models.GenericIPAddressField(protocol='IPv4', verbose_name="Network IP Address")
    netmask = models.SmallIntegerField()
    class Meta:
        db_table = 'networks'
    def __unicode__(self):
        return self.name