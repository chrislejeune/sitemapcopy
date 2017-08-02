import os, commands, sys

## Data related to Bing sitemap files has been commented out per request of Rinkesh for dogfood test.

# Server variables
for arg in sys.argv:
	src_host = "cron-master.%s.ostk.com" % (arg) 
	jweb1 = "jweb01.%s.ostk.com" % (arg)
	jweb2 = "jweb02.%s.ostk.com" % (arg)

# Path variables
src_path = "/opt/SiteMapping/pages/*"
local_path = "/opt/dops/SiteMapping/pages/"
done_file = "/opt/SiteMapping/logs/sitemapping.done"
pages = "/www/pages/"
#bing_dir = "bing-sitemap"
local_pages = "/dops/www/pages/"
#bing_pages = "/www/pages/bing-sitemap/"

# Methods
check_exists = "ssh root@%s ls %s" % (src_host, done_file)
#check_bing1 = "ssh root@%s ls %s | grep bing" % (jweb1, pages) 
#check_bing2 = "ssh root@%s ls %s | grep bing" % (jweb2, pages) 
source_key = "ssh-keyscan %s >> /root/.ssh/known_hosts" % (src_host)
jweb1_key = "ssh-keyscan %s >> /root/.ssh/known_hosts" % (jweb1)
jweb2_key = "ssh-keyscan %s >> /root/.ssh/known_hosts" % (jweb2)
get_files = "rsync -avp root@%s:%s %s" % (src_host, src_path, local_path)
jweb1_copy = "rsync -avp %s* root@%s:%s" % (local_path, jweb1, pages)
jweb2_copy = "rsync -avp %s* root@%s:%s" % (local_path, jweb2, pages)
#jweb1_bing = "rsync -avp %s* root@%s:%s" % (local_pages, jweb1, bing_pages)
#jweb2_bing = "rsync -avp %s* root@%s:%s" % (local_pages, jweb2, bing_pages)
cleanup_file = "ssh %s rm -f %s" % (src_host, done_file)
cleanup_pages = "rm -rf %s*" % (local_pages)
#create_dir1 = "ssh root@%s mkdir %s" % (jweb1, bing_pages)
#create_dir2 = "ssh root@%s mkdir %s" % (jweb2, bing_pages)
local_copy = "rsync -avp %s* %s" % (local_path, local_pages)

# Setup keys
os.system(source_key)
os.system(jweb1_key)
os.system(jweb2_key)

# Check to see if sitemapping.done file is present
status, output = commands.getstatusoutput(check_exists)

if output != done_file:
	sys.exit(0)
else:

# Get the files from cronmaster
	os.system(get_files)

# Push the files from here to the jwebs
        os.system(jweb1_copy)
        os.system(jweb2_copy)

# Check to see if bing directory is present and create it if not
'''
status, output = commands.getstatusoutput(check_bing1)

if output != bing_dir:
	os.system(create_dir1)

status, output = commands.getstatusoutput(check_bing2)

if output != bing_dir:
        os.system(create_dir2)

# Copy sitemap info to local directory and bingify
os.system(local_copy)
os.system("find /dops/www/pages/googlebase/ -name *.gz -type f -exec gunzip '{}' \;")

# Copy the uncompressed files to the jwebs under the bing-sitemap directory
os.system(jweb1_bing)
os.system(jweb2_bing)
'''
# Cleanup the sitemapping.done file so it can be generated again
os.system(cleanup_file)
os.system(cleanup_pages)
