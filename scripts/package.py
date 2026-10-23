#!/usr/bin/env python3
"""Build the standalone skill and dual-runtime plugin release archives."""
import argparse
from pathlib import Path
import zipfile
from check import ROOT, PLUGIN, SKILL, check


def package(root=ROOT, output=None):
    check(root)
    output = output or root / 'dist'
    output.mkdir(parents=True, exist_ok=True)
    skill = root / 'skills' / SKILL
    archives = []
    for name, sources, prefix in [
        (f'{SKILL}-skill.zip', [skill, root / 'LICENSE'], ''),
        (f'{SKILL}-plugin.zip', [root / 'plugin.json', root / '.claude-plugin/plugin.json', root / '.codex-plugin/plugin.json', root / 'skills', root / 'agents', root / 'LICENSE'], PLUGIN + '/'),
    ]:
        destination = output / name
        with zipfile.ZipFile(destination, 'w', zipfile.ZIP_DEFLATED) as archive:
            for source in sources:
                files = sorted(source.rglob('*')) if source.is_dir() else [source]
                for file in files:
                    if not file.is_file() or any(part.startswith('.') or part == '__pycache__' for part in file.relative_to(source if source.is_dir() else source.parent).parts):
                        continue
                    relative = file.relative_to(skill) if not prefix and file != root / 'LICENSE' else file.relative_to(root)
                    archive.write(file, prefix + relative.as_posix())
        archives.append(destination)
    return archives

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='output directory (default: repository dist/)')
    args = parser.parse_args()
    for path in package(output=args.output):
        print(path)
