"""Collect the generated tree and static website, without toolchains or caches."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]


def export_build(destination):
    target = Path(destination).resolve()
    if target == ROOT or (ROOT / 'generated') == target or (ROOT / 'generated') in target.parents:
        raise ValueError('Export outside the generated tree, for example exports/docker.')
    target.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT / 'web/dist/client', target / 'site', dirs_exist_ok=True)
    shutil.copytree(ROOT / 'generated', target / 'generated', dirs_exist_ok=True)
    shutil.make_archive(str(target / 'maniac-mansion-static'), 'zip', target / 'site')
