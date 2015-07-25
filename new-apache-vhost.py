#!/usr/bin/python

import argparse

try:
    input = raw_input

except Exception as e:
    pass

parser = argparse.ArgumentParser(description="Create apache site config file")
parser.add_argument("--outputPath", metavar='N', type=str, nargs=1,
                   help="path to save output")

args = parser.parse_args()

def readData(text, default):
	strPrompt  = text + "["+ str(default) + "]:"


	d = input(strPrompt)

	if ("" == d):
		d = default
	return d


apacheConfPath="/etc/apache2/sites-enabled/"

hostname = input("hostname: ")
if ("" == hostname):
	raise Exception("hostname must not be empty")


port = str(readData("post", 80))
serverName = readData("server name", hostname)
defPath="/var/www/" + hostname
documentRoot = readData("document root", defPath)
logPath = documentRoot + "/log"
directoryIndex = readData("directory index", "index.php")
publicDir = documentRoot + readData("public dir sub path", "/public")


output = """<VirtualHost *:""" + port + """>
	ServerName """ + serverName + """
	ServerAdmin webmaster@localhost
	DocumentRoot """ + documentRoot + """
	DirectoryIndex """ + directoryIndex

overRide = readData("Allow override public directory by .htacces (None, All)", 'None')
print(overRide)
if (overRide == "None"):
    overRide = "None"
else:
    overRide = All



output += """
    <Directory """ + publicDir + """>
       AllowOverride """ + overRide + """
       Order allow,deny
       allow from all
     </Directory>
"""


while True:
    directory = readData("Add new Directory section? (n,y)","n")
    if 'n' == directory:
        break


    path = input("directory path")
    overRide = readData('Allow override public directory by .htacces (None, All)', 'None')

    if (overRide == 'None'):
        overRide = 'None'
    else:
        overRide = All


    access = readData('deny or allow from all (deny/allow)', deny)


    output += """
        <Directory """ + path + """>
            AllowOverride overRide
            Order allow,deny
            """ + access + """ from all
        </Directory>"""

projectType = readData('project specific conf (phalcon, none)', 'none')
#redirection directives for phalcon
if ("phalcon" == projectType):

	output += """
	<IfModule mod_rewrite.c>

	    <Directory """ + documentRoot + """>
	        RewriteEngine on
	        RewriteRule  ^$ public/    [L]
	        RewriteRule  (.*) public/$1 [L]
	    </Directory>

	    <Directory """ + publicDir + """>
	        RewriteEngine On
	        RewriteCond %{REQUEST_FILENAME} !-d
	        RewriteCond %{REQUEST_FILENAME} !-f
	        RewriteRule ^(.*)$ index.php?_url=/$1 [QSA,L]
	    </Directory>

	</IfModule>"""

output += """
	ErrorLog """ + logPath + """/error.log

	# Possible values include: debug, info, notice, warn, error, crit,
	# alert, emerg.
	LogLevel warn
	CustomLog """ + logPath + """/access.log combined

</VirtualHost>
"""
f = open(serverName + '.vhost', 'w')
print """the following configuration will be writen in the servername + '.vhost' file"""
print output
f.write(output)
f.close
