# autoSubTakeover
A tool used to check if a CNAME resolves to the scope adress. If the CNAME resolves to a non-scope adress it might be worth checking out if subdomain takeover is possible.

# Requirements
- argparse
- subbrute
- dnspython
# Usage?

python main.py --target-file $FILE_WITH_TARGETS
