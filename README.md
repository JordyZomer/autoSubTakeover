# autoSubTakeover
A tool used to check if a CNAME resolves to the scope address. If the CNAME resolves to a non-scope address it might be worth checking out if subdomain takeover is possible. Also checks if the domain that a subdomain points to is expired.

# Requirements (also in requirements.txt)

```
Click==7.0
pycares==3.0.0
tornado==6.0.3
aiodns==2.0.0
asyncio==3.4.3
tldextract==2.2.2
```

# Installation

install the package through pip:

```
  pip install autosubtakeover
```

or by building it from source:

```
   git clone https://github.com/JordyZomer/autoSubTakeover
   cd autoSubTakeover
   python setup.py install
```


# Usage

This is how you can run the tool, please make sure that your arguments point to valid files that contain each entry on a new line.
```
Usage: autosubtakeover [OPTIONS]

  AutoSubTakeover by Oblivion, Mantis and Zoidberg

Options:
  --domains TEXT      Domains to brute.
  --nameservers TEXT  Nameservers to use.
  --wordlist TEXT     Wordlist of subdomains
  --help              Show this message and exit.
  
```

# Note

This project is licensed under the MIT license, even though I don't really care what you do with it I do appreciate credits!
