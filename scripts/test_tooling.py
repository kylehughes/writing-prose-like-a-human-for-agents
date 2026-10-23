"""Exercise distributable contents and release safeguards in disposable repositories."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest
import zipfile
from check import ROOT, PLUGIN, SKILL, check
from package import package


class ToolingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        for path in ('scripts', 'skills', 'agents', '.claude-plugin', '.codex-plugin', '.agents'):
            shutil.copytree(ROOT / path, self.root / path, ignore=shutil.ignore_patterns('__pycache__'))
        for path in ('plugin.json', 'LICENSE', 'release.sh', '.gitignore'):
            shutil.copy2(ROOT / path, self.root / path)

    def git(self, *args):
        return subprocess.check_output(['git', '-c', 'core.fsmonitor=false', '-c', 'commit.gpgsign=false', '-C', str(self.root), *args], text=True, stderr=subprocess.DEVNULL).strip()

    def initialize(self):
        self.git('init', '-b', 'main')
        self.git('config', 'user.name', 'Release Test')
        self.git('config', 'user.email', 'test@example.invalid')
        self.git('config', 'core.hooksPath', '/dev/null')
        self.git('config', 'core.fsmonitor', 'false')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('add', '.')
        self.git('commit', '-m', 'Fixture')

    def release(self, *args):
        return subprocess.run(['bash', str(self.root / 'release.sh'), *args], cwd='/', text=True, capture_output=True)

    def test_archive_membership_and_license(self):
        skill_zip, plugin_zip = package(self.root)
        with zipfile.ZipFile(skill_zip) as archive:
            names = set(archive.namelist())
            self.assertIn('SKILL.md', names)
            self.assertIn('LICENSE', names)
            self.assertIn('ATTRIBUTION.md', names)
            self.assertNotIn('plugin.json', names)
        with zipfile.ZipFile(plugin_zip) as archive:
            names = set(archive.namelist())
            for member in ('plugin.json', '.claude-plugin/plugin.json', '.codex-plugin/plugin.json', 'LICENSE', f'skills/{SKILL}/SKILL.md', f'skills/{SKILL}/ATTRIBUTION.md', 'agents/prose-humanizer.md'):
                self.assertIn(f'{PLUGIN}/{member}', names)
            self.assertTrue(all(name.startswith(PLUGIN + '/') for name in names))
            self.assertFalse(any('/scripts/' in name or '/.github/' in name or '/AGENTS.md' in name for name in names))

    def test_mismatched_version_and_broken_link_rejected(self):
        data = json.loads((self.root / 'plugin.json').read_text())
        data['version'] = '999.0.0'
        (self.root / 'plugin.json').write_text(json.dumps(data))
        with self.assertRaisesRegex(ValueError, 'versions differ'):
            check(self.root)
        data['version'] = json.loads((self.root / '.claude-plugin/plugin.json').read_text())['version']
        (self.root / 'plugin.json').write_text(json.dumps(data))
        with (self.root / f'skills/{SKILL}/SKILL.md').open('a') as file:
            file.write('\n[Missing](missing.md)\n')
        with self.assertRaisesRegex(ValueError, 'broken or escaping link'):
            package(self.root)

    def test_release_syncs_versions_and_pushes_only_release_tag(self):
        self.initialize()
        remote = self.root / 'remote.git'
        subprocess.run(['git', 'init', '--bare', str(remote)], check=True, capture_output=True)
        # Keep the local remote outside the checkout so it does not dirty it.
        remote_outside = self.root.parent / (self.root.name + '-remote.git')
        shutil.move(remote, remote_outside)
        self.addCleanup(shutil.rmtree, remote_outside)
        self.git('remote', 'add', 'origin', str(remote_outside))
        self.git('tag', 'unrelated')
        result = self.release('999.0.0')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(check(self.root), '999.0.0')
        self.assertEqual(self.git('log', '-1', '--format=%s'), 'Release 999.0.0')
        remote_tags = self.git('ls-remote', '--tags', 'origin')
        self.assertIn('refs/tags/999.0.0', remote_tags)
        self.assertNotIn('unrelated', remote_tags)
        self.assertEqual(self.git('status', '--porcelain'), '')

    def test_dry_run_and_rejections(self):
        self.initialize()
        before = self.git('rev-parse', 'HEAD')
        manifests = {path: path.read_bytes() for path in self.root.rglob('*.json')}
        result = self.release('999.0.0', '--dry-run')
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('both archives built', result.stdout)
        self.assertEqual(self.git('rev-parse', 'HEAD'), before)
        self.assertEqual(self.git('status', '--porcelain'), '')
        self.assertEqual(self.git('tag', '--list'), '')
        self.assertFalse((self.root / 'dist').exists())
        for path, contents in manifests.items():
            self.assertEqual(path.read_bytes(), contents)
        for version in ('01.2.3', '1.2.3-beta', '0.0.0'):
            self.assertNotEqual(self.release(version, '--dry-run').returncode, 0)
        self.git('tag', '999.0.0')
        self.assertIn('already exists', self.release('999.0.0', '--dry-run').stderr)
        self.git('switch', '-c', 'feature')
        self.assertIn('main branch', self.release('998.0.0', '--dry-run').stderr)
        self.git('switch', 'main')
        (self.root / 'untracked').write_text('dirty')
        self.assertIn('clean checkout', self.release('998.0.0', '--dry-run').stderr)
        (self.root / 'untracked').unlink()
        with (self.root / 'LICENSE').open('a') as file:
            file.write('\ndirty\n')
        self.assertIn('clean checkout', self.release('998.0.0', '--dry-run').stderr)

if __name__ == '__main__':
    unittest.main()
