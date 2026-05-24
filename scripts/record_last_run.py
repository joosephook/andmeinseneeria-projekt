#!/usr/bin/env python3
"""
Insert or update a "Viimati skripti käivitamine" section at the end of a markdown file.

Usage:
  python scripts/record_last_run.py --file path/to/file.md --label "pipeline"
"""
import argparse
from datetime import datetime, timezone
from pathlib import Path


def format_section(ts_iso: str, who: str = None):
    lines = ["## Viimati skripti käivitamine\n"]
    lines.append(f"- Aeg (UTC): {ts_iso}\n")
    if who:
        lines.append(f"- Kirjeldus: {who}\n")
    lines.append('\n')
    return ''.join(lines)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--file', required=True, help='Markdown file to update')
    p.add_argument('--label', help='Optional short description to include')
    args = p.parse_args()

    path = Path(args.file)
    if not path.exists():
        print(f"File not found: {path}")
        return 2

    text = path.read_text(encoding='utf-8')
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    new_section = format_section(now, args.label)

    # Remove existing section if present
    marker = '## Viimati skripti käivitamine'
    if marker in text:
        pre, _, _ = text.partition(marker)
        new_text = pre.rstrip() + '\n\n' + new_section
    else:
        new_text = text.rstrip() + '\n\n' + new_section

    path.write_text(new_text, encoding='utf-8')
    print(f"Updated {path} with timestamp {now}")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
