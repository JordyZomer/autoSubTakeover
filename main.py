#!/usr/bin/env python
# Copyright 2016-2017 Oblivion, Mantis and Zoidberg. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A tool used to check if a CNAME resolves to the scope adress.
If the CNAME resolves to a non-scope adress it might be worth checking out if subdomain takeover is possibru
"""

# Normal imports
import inspect, os
import argparse
import dns.resolver

# External imports 
from subbrute import subbrute
from whois import whois
from datetime import datetime

# Function to grab expiry date from the domain
# and return whether it is expired or not
def w(domain):
	try:
		info = whois(domain)
		now = datetime.now()
		if info.expiration_date[0] < now:
			return "\033[91mYES (%s)\033[0m" % info.expiration_date[0]
		else:
			return "\033[93mNO (%s)\033[0m" % info.expiration_date[0]	
	except:
		return "\033[93mNo whois data\033[0m"

		

# Load argument parsing
parser = argparse.ArgumentParser(description='Welcome to AutoSubTakeover by  Oblivion, Mantis, Zoidberg')
parser.add_argument('--target-file', type=str, help='The file that contains the hosts')
parser.add_argument('--output-file', type=str, help='The file that will contain the output')
args = parser.parse_args()

# The file with the targets we want is behind the parameter --target-file
target_file = args.target_file
output_file = args.output_file

# Open the target file (Read-Only) as targets  and read em :D 
domains = open(target_file).read().split('\n')
# Initialize Resolver and use Google DNS servers
dnsResolver = dns.resolver.Resolver()
dnsResolver.nameservers = ['8.8.8.8', '8.8.4.4']

output_file_handle = open(output_file, 'w', 0)

# For every domain in target_file do
for domain in domains:
  domain = "{:s}".format(domain)
# For every entry in Subbrute's output check if it's a CNAME and if it resolves to scope
  for entry in subbrute.run(domain):
    	try:
        # Query the DNS resolver to check if subdomain is a CNAME
   	     answers = dnsResolver.query(entry[0], 'CNAME')
	# Query whois
 	     for rdata in answers:
             	output = '{:s}'.format(rdata.target)
		expired = w(output)
   	      	  # If scope is/not in output splash some crap out
                if domain in output:
                    output_text = "[%s] - Expired: [%s] - CNAME: %s \033[93mresolves\033[0m to scope" % (entry[0], expired, output)
                    output_file_handle.write(output_text + "\n")
                    print output_text
                else:
                    output_text = "[%s] - Expired: [%s] - CNAME %s \033[91mdoes not\033[0m resolve to scope" % (entry[0], expired, output)
                    output_file_handle.write(output_text + "\n")
                    print output_text
	# To solve those "BLAH SUBDOMAIN IS NO CNAME" errors
	except dns.resolver.NoAnswer:
   	     pass

output_file_handle.close()
