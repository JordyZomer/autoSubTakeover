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

# Load argument parsing
parser = argparse.ArgumentParser(description='Welcome to AutoSubTakeover by  Oblivion, Mantis, Zoidberg')
parser.add_argument('--target-file', type=str, help='The file that contains the hosts')
args = parser.parse_args()

# The file with the targets we want is behind the parameter --target-file
target_file = args.target_file

# Open the target file (Read-Only) as targets  and read em :D 
with open(target_file, 'r') as targets:
  target_list = targets.read()
  
# Initialize Resolver and use Google DNS servers
dnsResolver = dns.resolver.Resolver()
dnsResolver.nameservers = ['8.8.8.8', '8.8.4.4']
# For every domain in target_file do
for domain in target_list:
  domain = "{:s}".format(domain)
# For every entry in Subbrute's output check if it's a CNAME and if it resolves to scope
  for entry in subbrute.run(domain):
    	try:
        # Query the DNS resolver to check if subdomain is a CNAME
   	     answers = dnsResolver.query(entry[0], 'CNAME')
 	     for rdata in answers:
             	output = '{:s}'.format(rdata.target)
   	      	  # If scope is/not in output splash some crap out
              	if domain in output:
   	          	  print "CNAME: %s resolves to scope" % (output)
   	        else:
    			  print "CNAME %s does not resolve to scope" % (output)
   	 	# To solve those "BLAH SUBDOMAIN IS NO CNAME" errors
	except dns.resolver.NoAnswer:
   	     pass

