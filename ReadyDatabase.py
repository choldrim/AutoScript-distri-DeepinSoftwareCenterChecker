#!/usr/bin/env python3
# coding=utf-8

import tarfile
import os

from urllib import request

def readyDatabase():
    # deepinSCVersion = getLastestDSCVersion()
    #deepinSCVersion = "3.0.1+20141230125726~0565641e10"
    #deepinSCUrl = "http://packages.linuxdeepin.com/deepin/pool/main/d/deepin-software-center-data/deepin-software-center-data_%s.tar.gz" % deepinSCVersion
    deepinSCUrl, deepinSCVersion = getLatestPackageUrl()

    print ("Latest deepin-software-center-data deb url: ", deepinSCUrl)
    print ("Version: ", deepinSCVersion)

    print("ready data base...")
    #print("deepin-software-center version:%s" % deepinSCUrl)

    fileName = "deepin-software-center-data_%s.tar.gz" % deepinSCVersion
    if not os.path.exists(os.path.join(os.getcwd(), fileName)):
        try:
            response = request.urlopen(deepinSCUrl)
            data = response.read()
            print("finish download")
            response.close()

        except request.URLError as e:
            print("Can't get software-center-data, abort.")
            print("Err:\n %s" % e.output)
            raise e

        with open(fileName, "wb") as f:
            f.write(data)
    else:
        print("file %s is exists, skip download." % fileName)

    # tar download file
    with tarfile.open(fileName) as tar:
        def is_within_directory(directory, target):
            
            abs_directory = os.path.abspath(directory)
            abs_target = os.path.abspath(target)
        
            prefix = os.path.commonprefix([abs_directory, abs_target])
            
            return prefix == abs_directory
        
        def safe_extract(tar, path=".", members=None, *, numeric_owner=False):
        
            for member in tar.getmembers():
                member_path = os.path.join(path, member.name)
                if not is_within_directory(path, member_path):
                    raise Exception("Attempted Path Traversal in Tar File")
        
            tar.extractall(path, members, numeric_owner=numeric_owner) 
            
        
        safe_extract(tar)

    # extract the database
    dbPath = os.path.join(
        os.getcwd(),
        "deepin-software-center-data-" +
        deepinSCVersion)
    dbPath = os.path.join(os.path.join(dbPath, "data"), "origin")

    with tarfile.open(os.path.join(dbPath, "dsc-software-data.tar.gz")) as tar:
        tar.extract("software/software.db", "db/")

    with tarfile.open(os.path.join(dbPath, "dsc-desktop-data.tar.gz")) as tar:
        tar.extract("desktop/desktop2014.db", "db/")

def getLatestPackageUrl():

    packagesFileUrl = "http://packages.linuxdeepin.com/deepin/dists/trusty/main/binary-amd64/Packages"
    with request.urlopen(packagesFileUrl) as resp:
        data = resp.read()

    content = data.decode("utf-8")

    meet = False
    fileName = ""
    version = ""
    for line in content.split("\n"):
        if line.strip() == "Package: deepin-software-center-data":
            meet = True

        if meet and line.startswith("Version:"):
            version = line.split("Version:")[1].strip()

        if meet and line.startswith("Filename:"):
            fileName = line.split("Filename: ")[1]
            break

    debUrl = "%s%s" % ("http://packages.linuxdeepin.com/deepin/", fileName)
    return debUrl, version

if __name__ == "__main__" :
    readyDatabase()
