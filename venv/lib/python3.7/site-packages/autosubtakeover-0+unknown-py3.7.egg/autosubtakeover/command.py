"""Collection of autosubtakeover's command line entry points that allow you to start
the program from the command-line"""
import logging
import asyncio
import socket

from typing import Tuple, Union
from datetime import datetime
from contextlib import closing

import click
import aiodns
import tldextract
import tornado.iostream

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


async def check_expiry(domain: str, subdomain: str, server: str) -> None:
    """This function queries a whois database to check if a domain name is expired or not"""
    whois_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        with closing(tornado.iostream.IOStream(whois_socket)) as stream:
            await stream.connect((server, 43))
            await stream.write((f"{domain}\r\n").encode("utf8"))
            await stream.read_until(b"Expiry Date: ")
            date = await stream.read_until(b"\n")
            date = date.decode("utf8").rstrip()
            date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
            if date <= datetime.now():
                log.debug(
                    "%s points to %s which was expired on %s",
                    subdomain,
                    domain,
                    date,
                )
    except tornado.iostream.StreamClosedError:
        pass


async def check_takeover(
        subdomain: str, resolver: aiodns.DNSResolver
) -> Tuple[str, Union[str, None]]:
    """This function asynchronously resolves a domain name"""
    try:
        result = await resolver.query(subdomain, "CNAME")
        domain = tldextract.extract(subdomain)
        domain = f"{domain.domain}.{domain.suffix}"
        result_domain = tldextract.extract(result.cname)
        result_domain = f"{result_domain.domain}.{result_domain.suffix}"
        await check_expiry(result_domain, subdomain, "whois.verisign-grs.com")

        if domain not in result_domain:
            log.debug(
                "%s points to an external domain %s", subdomain, result_domain
            )

        return (subdomain, result.cname, result_domain)
    except aiodns.error.DNSError:
        return (subdomain, None, None)


async def parse_data(
        wordlist: str, domainlist: str, nameservers: Union[str, None]
) -> None:
    """This function loads the specified worlist and domainlist and runs the resolve function"""
    with open(wordlist, "r") as file_handler:
        word_list = file_handler.read().splitlines()
    with open(domainlist, "r") as file_handler:
        domain_list = file_handler.read().splitlines()
    if nameservers is None:
        name_servers = None
    else:
        with open(nameservers, "r") as file_handler:
            name_servers = file_handler.read().splitlines()

    resolver = aiodns.DNSResolver(nameservers=name_servers)

    tasks = [
        check_takeover(f"{subdomain}.{domain}", resolver)
        for subdomain in word_list
        for domain in domain_list
    ]

    resolved = await asyncio.gather(*tasks)
    resolved = [x for x in resolved if x[1] is not None]
    log.debug("Domains resolved: %d", len(resolved))


@click.command()
@click.option("--domains", default="./domains.txt", help="Domains to brute.")
@click.option("--nameservers", default=None, help="Nameservers to use.")
@click.option(
    "--wordlist", default="./wordlist.txt", help="Wordlist of subdomains"
)
def main(domains: str, wordlist: str, nameservers: Union[str, None]) -> None:
    """AutoSubTakeover by Oblivion, Mantis and Zoidberg"""
    print("AutoSubTakeover by Oblivion, Mantis and Zoidberg")
    asyncio.run(parse_data(wordlist, domains, nameservers))
