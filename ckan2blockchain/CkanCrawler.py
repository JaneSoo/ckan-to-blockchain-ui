#!/usr/bin/python3

import hashlib, json, time, sys, urllib.request, urllib.parse, pdb

class CkanCrawler:
    # def __init__(self, cli_args, ini_args, logger):
    #     self.cli_args = cli_args
    #     self.ini_args = ini_args
    #     self.logger = logger

    #     self.base_url = self.ini_args.get('ckan', 'url').rstrip('/') + '/api/3'
    
    def __init__(self, package):
        self.package = package


    # get list of all published packages (ids)
    def get_package_list(self):
        for retry in range(1,self.ini_args.getint('ckan','retries')):
            try: 
                url = self.base_url + '/action/package_list'
                res = urllib.request.urlopen(url).read()
                res_json = json.loads(res.decode())
                return res_json['result']

            except Exception as e:
                self.__error_sleep("failed to get package list (will retry): "+str(e))

        raise Exception("failed to get package list")


    # get list of all resource urls from specified package
    def get_package_resources(self, url, package):
        for retry in range(1, 5):
            try:
                newurl = url + '/action/package_show?' + urllib.parse.urlencode({'id' :package})
                res = urllib.request.urlopen(newurl).read()
                res_json = json.loads(res.decode())
                resource_urls = []
                for resource in res_json['result']['resources']:
                    resource_urls.append(resource['url'])
                return resource_urls
            
            except Exception as e:
                print('Failed to get package details (will try): ' + str(e))
        
        raise Exception("failed to get package details id=%s" %package)

    # compute hash of remote content
    def hash_url(self, url):
        for retry in range(1, 5):
            try:
                hdata = hashlib.sha256()
                f = urllib.request.urlopen(url)
                for chunk in iter(lambda: f.read(4096), b""):
                    hdata.update(chunk)
            
                return hdata.hexdigest()
            
            except Exception as e:
                print("error download")
            
        print("success: hash_url")
        raise Exception("Failed to download resource")

    # compute hash from a (sorted) list of remote urls    
    def hash_urls(self, urls):
        hashes = []
        urls.sort()
        for url in urls:
            h = self.hash_url(url)
            hashes.append(h)
        hashes_json = json.dumps(hashes)
        print("success: hash_urls")
        return hashlib.sha256(hashes_json.encode('utf-8')).hexdigest()

    def __error_sleep(self, message):
        self.logger.error(message)
        time.sleep(self.ini_args.getint('ckan','retry_delay'))

    def hash_package1(self, url, package):
        resource_urls = self.get_package_resources(url, package)
        h = self.hash_urls(resource_urls)
        id_hash = hashlib.md5(package.encode('utf-8')).hexdigest()
        return(id_hash, h)

    def hash_all_packages(self):
        # get list of published packages
        packages = self.get_package_list()

        package_hashes = {}

        for package in packages:
            try: 
                (id_hash, h) = self.hash_package(package)
                package_hashes[id_hash] = h
            except Exception as e:
                self.logger.warn("package " + package + " is unavailable... skipped")
        print("success: hash_all_packages")
        return package_hashes

# vim: ai ts=4 sts=4 et sw=4 ft=python
