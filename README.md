# autoSubTakeover
A tool used to check if a CNAME resolves to the scope adress. If the CNAME resolves to a non-scope adress it might be worth checking out if subdomain takeover is possible. Also checks when a domain-name expires.

# Requirements
- argparse
- subbrute
- dnspython
- datetime
- whois


# Usage?

python main.py --target-file $FILE_WITH_TARGETS --output-file $OUTPUT_FILE

