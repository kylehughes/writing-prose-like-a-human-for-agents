#!/usr/bin/env python3
"""Prepare and atomically push one numeric release from a clean main checkout."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
from check import ROOT, SEMVER, check
from package import package


def git(*args):
    return subprocess.check_output(['git', '-C', str(ROOT), *args], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('version')
    parser.add_argument('--dry-run', action='store_true', help='check release eligibility and build temporary archives without modifying the repository')
    args = parser.parse_args()
    try:
        if not SEMVER.fullmatch(args.version):
            raise ValueError('version must be numeric X.Y.Z without leading zeros')
        if git('branch', '--show-current') != 'main':
            raise ValueError('releases require the main branch')
        if git('status', '--porcelain', '--untracked-files=all'):
            raise ValueError('releases require a clean checkout, including untracked files')
        if args.version in git('tag', '--list').splitlines():
            raise ValueError(f'tag {args.version} already exists')
        current = check()
        if tuple(map(int, args.version.split('.'))) <= tuple(map(int, current.split('.'))):
            raise ValueError(f'version must increase from {current}')
        with tempfile.TemporaryDirectory(prefix='prose-release-') as temporary:
            package(output=Path(temporary))
        paths = ['plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json', '.claude-plugin/marketplace.json']
        if args.dry_run:
            print(f'Dry run validated: {current} -> {args.version}; both archives built successfully.')
            print(f'Would synchronize five version fields, validate, commit "Release {args.version}", tag {args.version}, and atomically push main and only that tag.')
            return
        originals = {path: (ROOT / path).read_bytes() for path in paths}
        try:
            for path in paths:
                file = ROOT / path
                data = json.loads(originals[path])
                if path.endswith('marketplace.json'):
                    data['metadata']['version'] = args.version
                    data['plugins'][0]['version'] = args.version
                else:
                    data['version'] = args.version
                file.write_text(json.dumps(data, indent=2) + '\n')
            check(expected_version=args.version)
            with tempfile.TemporaryDirectory(prefix='prose-release-') as temporary:
                package(output=Path(temporary))
        except Exception:
            for path, contents in originals.items():
                (ROOT / path).write_bytes(contents)
            raise
        subprocess.run(['git', '-C', str(ROOT), 'add', '--', *paths], check=True)
        subprocess.run(['git', '-C', str(ROOT), 'commit', '-m', f'Release {args.version}'], check=True)
        subprocess.run(['git', '-C', str(ROOT), 'tag', args.version], check=True)
        subprocess.run(['git', '-C', str(ROOT), 'push', '--atomic', 'origin', 'refs/heads/main:refs/heads/main', f'refs/tags/{args.version}:refs/tags/{args.version}'], check=True)
        print(f'Released {args.version}')
    except (ValueError, OSError, subprocess.CalledProcessError, KeyError, IndexError, TypeError) as error:
        parser.exit(1, f'Release rejected: {error}\n')

if __name__ == '__main__':
    main()
