from ncclient import manager
from getpass import getpass
import re
import json
import xml.etree.ElementTree as ET

class retrieveSFP():

    def __init__(self):
        self.password = str(getpass())
        self.lis = []
        self.rlist = []
        self.sfpdoc = 'sfpdoc.txt'	

    def loadhosts(self):
        input_file = open('switches.json', 'r')
        json_decode=json.load(input_file)
        for key,val in json_decode.iteritems():
            if val["type"] == "juniper":
                lis.append(key + '.' + FQDN)
        return

    def retreivesfpinfo(self):
        for host in lis:
            with manager.connect(host=host, port=22, username='admin', password=password, hostkey_verify=False, device_params={'name':'junos'}) as m:
                get_inventory = m.dispatch('get-chassis-inventory').data_xml
                root = ET.fromstring(get_inventory)
                for elem in root.findall('.//chassis-module'):
                    for sub_elem in elem:
                        if re.match('FPC', sub_elem.text):
                        fpc = sub_elem.text
                        for sub_sub_elem in elem.findall('./chassis-sub-module/chassis-sub-sub-module'):
                            for sub_sub_sub_elem in sub_sub_elem:
                                if sub_sub_sub_elem.tag == 'name':
                                    val = sub_sub_sub_elem.text
                                elif sub_sub_sub_elem.text == 'NON-JNPR':
                                     rlist.append(host.split('.')[0] + ': ' + sub_elem.text + ' - ' + val + ' - ' + sub_sub_sub_elem.text)
                                else:
                                    pass
                    else:
                        pass
        return self.rlist

    def createfile(self):
        crfile = open(self.sfpdoc, 'w')
        crfile.write('\n'.join(self.rlist))
        crfile.close()
        return

