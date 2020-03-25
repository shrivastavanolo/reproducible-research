#!/usr/bin/python

"""
Before running this script please stop network-manager:
service network-manager stop
This example shows how to create multiple SSID at the same AP and ideas
around SSID-based packet forwarding
            --------
             ssid-4
            --------
               |
               |
  ------      (5)     -------
  ssid-1---(2)ap1(4)---ssid-3
  ------      (3)     -------
               |
               |
            --------
             ssid-2
            --------
"""

from mn_wifi.net import Mininet_wifi
from mn_wifi.node import UserAP
from mn_wifi.cli import CLI
from mininet.node import  Controller
from mininet.log import setLogLevel, info


def topology():
    "Create a network."
    net = Mininet_wifi( controller=Controller, accessPoint=UserAP,
                        autoAssociation=False )

    info("*** Creating nodes\n")
    sta1 = net.addStation( 'sta1', position='10,60,0' )
    sta2 = net.addStation( 'sta2', position='20,15,0' )
    sta3 = net.addStation( 'sta3', position='10,25,0' )
    sta4 = net.addStation( 'sta4', position='50,30,0' )
    sta5 = net.addStation( 'sta5', position='45,65,0' )
    ap1 = net.addAccessPoint( 'ap1', vssids=4, ssid="ssid,ssid1,ssid2,ssid3,ssid4",
                              mode="g", channel="1", position='30,40,0' )
    c0 = net.addController('c0' )

    net.setPropagationModel(model='logDistance', exp=5)

    info("*** Configuring wifi nodes\n")
    net.configureWifiNodes()

    "plotting graph"
    net.plotGraph(max_x=100, max_y=100)

    info("*** Starting network\n")
    net.build()
    c0.start()
    ap1.start( [c0] )

    sta1.setRange(15)
    sta2.setRange(15)
    sta3.setRange(15)
    sta4.setRange(15)
    sta5.setRange(15)

    sta1.cmd('iwconfig sta1-wlan0 essid %s ap %s' % (ap1.params['ssid'][1], ap1.params['mac'][1]))
    sta2.cmd('iwconfig sta2-wlan0 essid %s ap %s' % (ap1.params['ssid'][2], ap1.params['mac'][2]))
    sta3.cmd('iwconfig sta3-wlan0 essid %s ap %s' % (ap1.params['ssid'][2], ap1.params['mac'][2]))
    sta4.cmd('iwconfig sta4-wlan0 essid %s ap %s' % (ap1.params['ssid'][3], ap1.params['mac'][3]))
    sta5.cmd('iwconfig sta5-wlan0 essid %s ap %s' % (ap1.params['ssid'][4], ap1.params['mac'][4]))

    ap1.cmd('dpctl unix:/tmp/ap1 meter-mod cmd=add,flags=1,meter=1 drop:rate=100')
    ap1.cmd('dpctl unix:/tmp/ap1 meter-mod cmd=add,flags=1,meter=2 drop:rate=200')
    ap1.cmd('dpctl unix:/tmp/ap1 meter-mod cmd=add,flags=1,meter=3 drop:rate=300')
    ap1.cmd('dpctl unix:/tmp/ap1 meter-mod cmd=add,flags=1,meter=4 drop:rate=400')
    ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=2 meter:1 apply:output=flood')
    ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=3 meter:2 apply:output=flood')
    ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=4 meter:3 apply:output=flood')
    ap1.cmd('dpctl unix:/tmp/ap1 flow-mod table=0,cmd=add in_port=5 meter:4 apply:output=flood')

    info("*** Running CLI\n")
    CLI( net )

    info("*** Stopping network\n")
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    topology()
