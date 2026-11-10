#!/usr/bin/env python3
"""Show the demo findings through the Lookyloo API, using pylookyloo."""
import argparse
import hashlib
import os
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import urllib3
from pylookyloo import Lookyloo

LOOKYLOO_URL = os.environ.get("LOOKYLOO_URL", "https://lookyloo.demo.cudeso.be")
SITES_DIR = Path(__file__).resolve().parent / "sites"


def capture_uuid(value):
    """Accept a capture UUID or a tree link such as https://lookyloo.example/tree/<uuid>."""
    match = re.search(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", value.lower())
    if match is None:
        raise argparse.ArgumentTypeError(f"no capture UUID in {value!r}")
    return match.group(0)


def capture(lookyloo, args):
    uuid = lookyloo.submit(url=args.url, locale=args.locale, timezone_id=args.timezone, listing=True, quiet=True)
    print(f"Submitted {args.url}, capture {uuid}")
    for _ in range(40):
        if lookyloo.get_status(uuid)["status_code"] == 1:
            break
        time.sleep(3)
    else:
        sys.exit(f"Capture {uuid} is not ready after two minutes.")
    print(f"{LOOKYLOO_URL}/tree/{uuid}\n")
    report(lookyloo, uuid)


def report(lookyloo, uuid):
    info = lookyloo.get_info(uuid)
    stats = lookyloo.get_capture_stats(uuid)
    print(f"{info['title']}\n  {info['url']}, captured {info['capture_time']}")
    print(f"  {stats['total_urls']} requests to {stats['total_unique_hostnames']} hostnames")
    print("Redirects:")
    for url in lookyloo.get_redirects(uuid)["response"]["redirects"]:
        print(f"  {url}")
    print("Hostnames:")
    for hostname in sorted(lookyloo.get_hostnames(uuid)["response"]["hostnames"]):
        print(f"  {hostname}")
    print("Cookies:")
    cookies = lookyloo.get_cookies(uuid)
    # Lookyloo returns {"error": "No cookies"} instead of an empty list.
    for cookie in cookies if isinstance(cookies, list) else []:
        print(f"  {cookie['name']}={cookie['value']} on {cookie['domain']}")


def local_files_by_hash():
    files = defaultdict(list)
    for path in sorted(SITES_DIR.rglob("*")):
        if path.is_file():
            files[hashlib.sha512(path.read_bytes()).hexdigest()].append(str(path.relative_to(SITES_DIR)))
    return files


def related(lookyloo, args):
    # Lookyloo indexes response bodies by SHA-512, and the API does not say which URL each hash belongs to.
    # Hashing the demo sites' own files names most of them; anything else is a third-party or generated response.
    local_files = local_files_by_hash()
    print("Content in this capture that also appears in other captures (SHA-512):")
    for sha512 in lookyloo.get_hashes(args.uuid)["response"]["hashes"]:
        others = Counter(occurrence["title"] for occurrence in lookyloo.get_hash_occurrences(sha512)["response"]
                         if occurrence["capture_uuid"] != args.uuid)
        if others:
            print(f"  {sha512[:16]}...  {', '.join(local_files.get(sha512, ['third-party, or changed since the capture']))}")
            for title, count in others.most_common():
                print(f"    {title} ({count} capture{'s' if count > 1 else ''})")


def compare(lookyloo, args):
    result = lookyloo.compare_captures(args.left, args.right)
    if "error" in result:
        sys.exit(result["error"])
    for key in ("final_url", "final_hostname", "final_status_code"):
        print(result[key]["message"])
    resources = result["ressources"]
    print(f"Only left: {len(resources['left'])} URLs, only right: {len(resources['right'])} URLs")
    print("Same URL in both captures:")
    for url in resources["both"]:
        print(f"  {url}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-k", "--insecure", action="store_true", help="accept a self-signed certificate on the Lookyloo instance")
    commands = parser.add_subparsers(dest="command", required=True)

    command = commands.add_parser("capture", help="submit a URL, wait for the capture and print a report")
    command.add_argument("url")
    command.add_argument("--locale", help="browser language, for example be-BY")
    command.add_argument("--timezone", help="browser time zone, for example Europe/Minsk")
    command.set_defaults(handler=capture)

    command = commands.add_parser("report", help="redirects, hostnames and cookies of a capture")
    command.add_argument("uuid", type=capture_uuid)
    command.set_defaults(handler=lambda lookyloo, args: report(lookyloo, args.uuid))

    command = commands.add_parser("related", help="other captures that received the same file content")
    command.add_argument("uuid", type=capture_uuid)
    command.set_defaults(handler=related)

    command = commands.add_parser("compare", help="compare two captures with Lookyloo's capture comparison")
    command.add_argument("left", type=capture_uuid)
    command.add_argument("right", type=capture_uuid)
    command.set_defaults(handler=compare)

    args = parser.parse_args()
    if args.insecure:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    lookyloo = Lookyloo(LOOKYLOO_URL, verify=not args.insecure)
    if not lookyloo.is_up:
        sys.exit(f"Lookyloo at {LOOKYLOO_URL} is not reachable. Use -k if it has a self-signed certificate.")
    args.handler(lookyloo, args)


if __name__ == "__main__":
    main()
