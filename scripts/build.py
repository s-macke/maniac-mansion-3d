#!/usr/bin/env python3
"""One build entry point for local Python, Docker and Compose."""
import argparse
import os
from pathlib import Path
import subprocess
import sys

from rooms import ROOT, catalog, sync
from room_config import load_config


def run(*args, cwd=ROOT):
    print('+', ' '.join(map(str, args)), flush=True)
    subprocess.run(args, cwd=cwd, check=True)


def blender_path():
    return os.environ.get('BLENDER_BIN', str(ROOT / 'blender-4.2.3-linux-x64/blender'))


def blend(script, *args):
    run(blender_path(), '-b', '-t', '8', '--python-exit-code', '1', '--python', str(script), *args)


def doors(force=False):
    inputs = [ROOT / p for p in ['shared/doors/build.py', 'shared/doors/designs.py',
              'scripts/blender_shared/geometry.py', 'scripts/finalize_baked_glb.py', 'source/room 011.png', 'source/room 027.png']]
    outputs = [ROOT / p for p in ['generated/blender/shared/doors/standard_doors_v1.blend',
                                  'generated/models/doors/standard_doors_v1.glb']]
    if force or any(not p.exists() for p in outputs) or max(p.stat().st_mtime for p in inputs) > min(p.stat().st_mtime for p in outputs):
        blend('shared/doors/build.py')


def ladders():
    inputs = [ROOT / p for p in ['shared/ladders/build.py', 'scripts/blender_shared/geometry.py', 'scripts/blender_shared/shell.py', 'scripts/finalize_baked_glb.py']]
    outputs = [ROOT / p for p in ['generated/blender/shared/ladders/ladder_v1.blend', 'generated/models/ladders/ladder_v1.glb']]
    if any(not p.exists() for p in outputs) or max(p.stat().st_mtime for p in inputs) > min(p.stat().st_mtime for p in outputs):
        blend('shared/ladders/build.py')


def room(room_id):
    layout, definitions = catalog(require_outputs=False)
    config = definitions[room_id]
    config_path = next(r['definition'] for r in layout['rooms'] if load_config(ROOT / r['definition'])['id'] == room_id)
    doors()
    if config['geometry'].get('ladders'):
        ladders()
    blend(config['build'])
    blend('scripts/blender_shared/bake.py', '--', '--room-config', str(ROOT / config_path))
    for source in [ROOT / config['asset'], ROOT / 'generated/models/doors/standard_doors_v1.glb']:
        run(sys.executable, 'scripts/optimize_baked_glb.py', str(source), str(source.with_name(source.stem + '_compact.glb')))


def website():
    # Fail before installing dependencies if the room build is incomplete.
    catalog()
    run('npm', 'ci', cwd=ROOT / 'web')
    run('npm', 'run', 'build', cwd=ROOT / 'web')
    run('npm', 'run', 'typecheck', cwd=ROOT / 'web')


def all_assets():
    _, definitions = catalog(require_outputs=False)
    run(sys.executable, 'scripts/build_inventory.py')
    doors(force=True)
    for room_id in definitions:
        room(room_id)
    catalog()
    for script in sorted((ROOT / 'scripts').glob('preview_*.py')):
        blend(script)
    print('All asset generation completed successfully.', flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name in ['list', 'check', 'sync', 'site', 'doors']:
        commands.add_parser(name)
    full = commands.add_parser('all')
    full.add_argument('--assets-only', action='store_true', help='Generate assets and previews without npm compilation')
    single = commands.add_parser('room')
    single.add_argument('room_id')
    single.add_argument('--site', action='store_true')
    export = commands.add_parser('export')
    export.add_argument('destination', type=Path)
    args = parser.parse_args()
    if args.command == 'room':
        _, definitions = catalog(require_outputs=False)
        if args.room_id not in definitions:
            parser.error('Unknown room. Choose: ' + ', '.join(definitions))
        room(args.room_id)
        if args.site:
            website()
    elif args.command == 'all':
        all_assets()
        if not args.assets_only:
            website()
    elif args.command == 'list':
        for key, config in catalog(require_outputs=False)[1].items():
            print(f"{key} — {config['label']}")
    elif args.command == 'site':
        website()
    elif args.command == 'doors':
        doors(force=True)
    elif args.command == 'sync':
        sync(*catalog())
    elif args.command == 'export':
        from export_build import export_build
        export_build(args.destination)
    else:
        catalog()
        print('House definitions, assets, navigation and connections valid.')


if __name__ == '__main__':
    main()
