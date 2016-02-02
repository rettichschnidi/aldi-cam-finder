This script searches for unprotected "security" IP cams.

Supported cameras
=================
* [Maginon IPC-100AC](http://ipc-info.com/#ipc-100ac)
* [Maginon IPC-10AC](http://ipc-info.com/#ipc-10ac)
* [Maginon IPC-1A](http://ipc-info.com/#ipc-1a)
* [Maginon IPC-20C](http://ipc-info.com/#ipc-20c)
* [Rollei SafetyCam-10 HD](http://www.rollei.de/produkte/foto/ueberwachungskameras/rollei-safetycam-10-hd-schwarz,p169447)
* [Rollei SafetyCam-20 HD](http://www.rollei.de/produkte/foto/ueberwachungskameras/rollei-safetycam-20-hd-ueberwachungskamera,p169449)
* [Rollei Security Cam Mini](http://www.rollei.de/produkte/foto/ueberwachungskameras/rollei-w-lan-ueberwachungskamera-mini-mit-steuerungs-app-schwarz,p312819)

The Maginon devices are sold by ALDI and produced/labeled by [supra Foto-Elektronik-Vertriebs-GmbH](http://supra-electronics.com/). The Rolleis use pretty  much the same firmware and the hardware also is essentially (exactly!?) the same.

Number of devices
=================
According to Shodan:
 * 2015-12-25: [6409](https://www.shodan.io/report/vSF13CgE)
 * 2015-12-28: [7271](https://www.shodan.io/report/vaovOsJ8)
 * 2015-12-30: [7997](https://www.shodan.io/report/JZsc3ZBq)
 * 2016-01-02: [8653](https://www.shodan.io/report/EqkBgELE)
 * 2016-01-05: [9536](https://www.shodan.io/report/eJTZWpam)
 * 2016-01-15: [11754](https://www.shodan.io/report/HU5cL0Nf)

Out of those, the following devices deny remote logins without set password (mcdhttpd 1.2):
 * 2016-01-15: [2012](https://www.shodan.io/report/1Ml5dkWv)

Usage
=====
* Get search results from [shodan.io](https://www.shodan.io/search?query=mcdhttpd) (or use an old one in this repo)
* Install the requirements listed in [requirements.txt](https://raw.githubusercontent.com/rettichschnidi/aldi-cam-drama/master/requirements.txt)
* execute `python3 ipcam.py mcdhttpd-2016-01-05.json.gz results.db`

The resulting data in results.db can be queried using SQLite.

Ugly: Telnet
============
All those CAMs are running a telnet daemon with hardcoded credentials (root/123456). The user can neither disable the
service nor change the password. Luckily, the cameras do not forward this port using UPnP.

Ugly: Interesting unprotected paths
===================================
 * `/probe_megracloud.cgi`: Cloud related; identifier (?)
```
<480703318277756463148679646116>
```
 * /get_status.cgi: Camera name, mac addresses, etc.
```
var id="006E0790B3FE";
var sys_ver="81.2.1.163";
var app_ver="3.1.5.0";
var eth_mac="006E09914FDE";
var wifi_mac="006E0890A3DF";
var alias="Baby";
var now=1452871872;
var timezone=-3600;
var dst=0;
var status_alarm=0;
var status_ddns=0;
var status_upnp=1;
var status_network=1;
var status_record=0;
var feature_sd=1;
var feature_hd=0;
var feature_record=0;
var feature_discovery=0;
```
