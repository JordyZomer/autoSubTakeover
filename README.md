# autoSubTakeover
A tool used to check if a CNAME resolves to the scope address. If the CNAME resolves to a non-scope address it might be worth checking out if subdomain takeover is possible. Also checks when a domain-name expires.

# Requirements
- argparse
- subbrute
- dnspython
- datetime
- whois


# Usage?

python main.py --target-file $FILE_WITH_TARGETS --output-file $OUTPUT_FILE

