#!/usr/bin/env python3
"""Derive the hardware-only config.yaml (for devices.esphome.io) from a full MTH config.

The full configs in Configs/ are ready to flash: they contain Wi-Fi credentials
(!secret), api, ota, web_server, captive_portal and dashboard_import. The
devices.esphome.io site accepts only the hardware part, so this script cuts the
rest out and changes nothing else:

  * removed top-level blocks: api, ota, web_server, captive_portal, dashboard_import
  * wifi: credentials are removed, only an empty "ap:" is kept
  * lines longer than 120 characters (the yamllint limit of devices.esphome.io)
    get their trailing "# comment" moved to a comment line above

Usage:
  make_hardware_config.py FULL.yaml [-o config.yaml] [--source-url URL]
      write the hardware-only config (stdout if -o is omitted)
  make_hardware_config.py --check FULL.yaml config.yaml
      exit 0 if config.yaml is exactly what FULL.yaml produces, 1 otherwise
"""
import argparse
import re
import sys

MAX_LEN = 120
DROP = {"api", "ota", "web_server", "captive_portal", "dashboard_import"}
HEADER_PREFIX = "# Hardware-only copy"
TOP_KEY = re.compile(r"^([A-Za-z_][\w-]*):")


def derive(text, source_url=None):
    out = []
    mode = "keep"  # keep | drop | wifi
    for line in text.splitlines():
        m = TOP_KEY.match(line)
        if m:
            key = m.group(1)
            if key in DROP:
                mode = "drop"
                continue
            if key == "wifi":
                mode = "wifi"
                out.append("wifi:")
                out.append("  ap: {}")
                continue
            mode = "keep"
        elif mode in ("drop", "wifi"):
            # inside a removed block: indented lines and blank lines belong to it,
            # a column-0 comment ends it
            if line.startswith((" ", "\t")) or not line.strip():
                continue
            mode = "keep"
            if out and out[-1].strip():
                out.append("")  # keep a blank line where a removed block ended
        if mode == "keep":
            out.append(line)
    # collapse blank-line runs, trim edges
    cleaned = []
    for line in out:
        if not line.strip() and cleaned and not cleaned[-1].strip():
            continue
        cleaned.append(line.rstrip())
    while cleaned and not cleaned[0].strip():
        cleaned.pop(0)
    while cleaned and not cleaned[-1].strip():
        cleaned.pop()
    cleaned = fit_width(cleaned)
    body = "\n".join(cleaned) + "\n"
    if source_url:
        head = (f"{HEADER_PREFIX}. Full configuration (Wi-Fi, API, OTA, web server):\n"
                f"# {source_url}\n")
        body = head + body
    return body


def fit_width(lines):
    """Move a trailing comment above its line when the line is longer than MAX_LEN."""
    out = []
    for line in lines:
        if len(line) > MAX_LEN and not line.lstrip().startswith("#"):
            m = re.match(r"^(.*?\S)\s+(#.*)$", line)
            if m and "#" not in m.group(1).split('"')[0]:
                indent = line[: len(line) - len(line.lstrip())]
                out.append(f"{indent}{m.group(2)}")
                out.append(m.group(1))
                continue
        out.append(line)
    return out


def strip_header(text):
    lines = text.splitlines(keepends=True)
    if lines and lines[0].startswith(HEADER_PREFIX):
        lines = lines[1:]
        if lines and lines[0].startswith("# http"):
            lines = lines[1:]
    return "".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("full")
    ap.add_argument("config", nargs="?", help="with --check: the config.yaml to compare")
    ap.add_argument("-o", "--output")
    ap.add_argument("--source-url")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    with open(a.full, encoding="utf-8") as f:
        derived = derive(f.read())
    if a.check:
        if not a.config:
            ap.error("--check needs FULL.yaml and config.yaml")
        with open(a.config, encoding="utf-8") as f:
            have = strip_header(f.read())
        if have == derived:
            print(f"OK: {a.config} matches {a.full}")
            return 0
        print(f"MISMATCH: {a.config} differs from what {a.full} produces", file=sys.stderr)
        return 1
    if a.source_url:
        derived = derive(open(a.full, encoding="utf-8").read(), a.source_url)
    if a.output:
        with open(a.output, "w", encoding="utf-8", newline="\n") as f:
            f.write(derived)
    else:
        sys.stdout.write(derived)
    return 0


if __name__ == "__main__":
    sys.exit(main())
