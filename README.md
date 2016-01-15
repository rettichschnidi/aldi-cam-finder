This script searches for unprotected "security" IP cams.

Supported cameras
=================
* Maginon IPC-100AC
* Maginon IPC-10AC
* Maginon IPC-1A
* Maginon IPC-20C
* Rollei SafetyCam-10 HD
* Rollei SafetyCam-20 HD
* Rollei Security Cam Mini

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

Out of those, the following devices deny remote logging without set password (mcdhttpd 1.2):
 * 2016-01-15: [2012](https://www.shodan.io/search?query=mcdhttpd%2F1.2)

Usage
=====
* Download a search result dump from [shodan.io](https://www.shodan.io/search?query=mcdhttpd) (or use an old one in this repo)
* Install the requirements listed in [requirements.txt](https://raw.githubusercontent.com/rettichschnidi/aldi-cam-drama/master/requirements.txt)
* execute `python3 ipcam.py mcdhttpd-2016-01-05.json.gz results.db`

The resulting data in results.db can be queried using SQLite.
