import subprocess, sys

def checkfile():
    for arg in sys.argv:
        src_host = "cron-master.%s.ostk.com" % (arg) 

    done_file = "/opt/SiteMapping/logs/sitemapping.done"
    check_exists = "ssh %s ls %s" % (src_host, done_file)

    status, output = subprocess.getstatusoutput(check_exists)

    if output != done_file:
        print ('The file is not there.')
    else:
        print ('The file is there.')

checkfile()
