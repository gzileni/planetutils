import urllib
import urlparse
import subprocess
import json
import urllib2

class Tilepack(object):
    HOST = 'https://app.interline.io'
    def download(self, outpath, version='latest', api_token=None, compressed=False):
        # Endpoint
        url = '%s/valhalla_planet_tilepacks/%s/download'%(self.HOST, version)
        if version == 'latest':
            url = '%s/valhalla_planet_tilepacks/download_latest'%(self.HOST)
        # Make url
        u = list(urlparse.urlsplit(url))
        q = urlparse.parse_qs(u[3])
        if api_token:
            q['api_token'] = api_token
        u[3] = urllib.urlencode(q)
        url = urlparse.urlunsplit(u)
        # Download
        args = ['curl', '-L', '--fail', '-o', outpath, url]
        if not compressed:
            args.append('--compressed')
        print "Downloading to %s"%outpath
        p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = p.communicate()
        e = p.wait()
        if e != 0:
            print "Error downloading: %s"%err.split("curl:")[-1]
        else:
            print "Done"
    
    def list(self):
        url = "%s/valhalla_planet_tilepacks.json"%(self.HOST)
        contents = urllib2.urlopen(url).read()
        tilepacks = json.loads(contents).get('data', [])
        tilepacks = sorted(tilepacks, key=lambda x:int(x.get('id')))
        for tilepack in tilepacks:
            a = tilepack.get('attributes', {})
            if a.get('bucket_provider') == 'gcp':
                bucket = 'gs://%s/%s'%(a['bucket_name'], a['bucket_key'])
            elif a.get('bucket_provider') == 's3':
                bucket = 's3://%s/%s'%(a['bucket_name'], a['bucket_key'])
            print """
Tilepack ID: %s
    Timestamp: %s
    Filename: %s
    Storage provider: %s
    Data sources: %s
    URL: %s
    Versions:
        valhalla: %s
        planetutils: %s
        tilepack_cutter: %s
            """%(
                tilepack['id'],
                a['osm_planet_datetime'],
                a['bucket_key'],
                a['bucket_provider'],
                ", ".join(a.get('data_contents', [])),
                tilepack.get('links',{}).get('self'),
                a['valhalla_version'],
                a['interline_planetutils_version'],
                a['interline_valhalla_tile_cutter_version']
            )