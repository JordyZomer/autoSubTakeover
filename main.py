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
import threading

# External imports
from subbrute import subbrute
import whois
from datetime import datetime

class AutoSubTakeOver:
	domains = []
	domain_resolvers = []


	# Function to grab expiry date from the domain
	# and return whether it is expired or not
	def is_expired(self, domain):
		stripdomain = domain.rstrip('.')
		fixdomain = "{:s}".format(stripdomain)
		now = datetime.now()
		info = whois.whois('{:s}'.format(fixdomain))
		if info.expiration_date[0] < now:
			return "\033[91mVULN (%s)\033[0m" % info.expiration_date[0]
		else:
			return "\033[93mNOTVULN (%s)\033[0m" % info.expiration_date[0]
		

	def check(self,output_file):
		# Initialize Resolver and use Google DNS servers
		dnsResolver = dns.resolver.Resolver()
		dnsResolver.nameservers = self.domain_resolvers
		ret_out = []
		for domain in self.domains:
			try:
				domain = "{:s}".format(domain)
				output_text = ""
				expired = self.is_expired(domain)
				for entry in subbrute.run(domain):
					try:
						# Query the DNS resolver to check if subdomain is a CNAME
						answers = dnsResolver.query(entry[0], 'CNAME')	
						for rdata in answers:
							output = '{:s}'.format(rdata.target)
							output_file_handle = open(output_file, 'w', 0)
					
							# If scope is/not in output splash some crap out
							if domain in output:
								output_text = "[%s]\t-Expired: [%s] - CNAME: %s \033[93mresolves\033[0m to scope" % (entry[0], expired, output)
								print output_text
								output_file_handle.write(output_text + "\n")
							else:
								output_text = "[%s]\t-Expired: [%s] - CNAME %s \033[91mdoes not\033[0m resolve to scope" % (entry[0], expired, output)
								# This should be returned
								print output_text
								output_file_handle.write(output_text + "\n")
							ret_out.append(output_text)
					except Exception as e:
						print str(e)
						pass
			except Exception as e:
				print str(e)
				pass
		return ret_out

def main():

	# Load argument parsing
	parser = argparse.ArgumentParser(description='Welcome to AutoSubTakeover by  Oblivion, Mantis, Zoidberg')
	parser.add_argument('--target-file', type=str, required=True, help='The file that contains the hosts')
	parser.add_argument('--output-file', type=str, required=True, help='The file that will contain the output')
	parser.add_argument('--dns', type=str, default="8.8.8.8,8.8.4.4", help='The number of threads to run on, default=1')
	args = parser.parse_args()

	# The file with the targets we want is behind the parameter --target-file
	target_file = args.target_file
	output_file = args.output_file

	ast = AutoSubTakeOver()

	# Open the target file (Read-Only) as targets  and read em :D
	ast.domains = open(target_file).read().split('\n')
	ast.domain_resolvers = args.dns.split(',')
	ast.check(output_file=args.output_file)

if __name__ == '__main__':
	main()
