"""Authored room inputs and generated runtime metadata have separate owners."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DERIVED_GEOMETRY = ('doors', 'sharedAssets', 'doorObstacles')


def manifest_path(config):
    return ROOT / 'generated/reports/rooms' / config['id'] / 'manifest.json'


def load_config(path, *, generated=False, prepare=False):
    config = json.loads(Path(path).read_text())
    geometry = config.setdefault('geometry', {})
    for key in DERIVED_GEOMETRY:
        geometry[key] = []
    if generated:
        path = manifest_path(config)
        if not path.is_file():
            raise ValueError(f'Missing {path.relative_to(ROOT)}; build this room first.')
        metadata = json.loads(path.read_text())
        if metadata['id'] != config['id']:
            raise ValueError(f'Room manifest identity mismatch: {path}')
        geometry.update(metadata['geometry'])
        if metadata.get('sharedAssetLibraries'):
            config['sharedAssetLibraries'] = metadata['sharedAssetLibraries']
        if metadata.get('sharedAssetLibrary'):
            config['sharedAssetLibrary'] = metadata['sharedAssetLibrary']
    if prepare:
        for key in ['source', 'baked', 'asset']:
            (ROOT / config[key]).parent.mkdir(parents=True, exist_ok=True)
        manifest_path(config).parent.mkdir(parents=True, exist_ok=True)
    return config


def save_generated(config):
    """Called after construction; never write back to the authored room.json."""
    metadata = {'id': config['id'], 'geometry': {
        key: config['geometry'].get(key, []) for key in DERIVED_GEOMETRY}}
    if config.get('sharedAssetLibraries'):
        metadata['sharedAssetLibraries'] = config['sharedAssetLibraries']
    if config.get('sharedAssetLibrary'):
        metadata['sharedAssetLibrary'] = config['sharedAssetLibrary']
    path = manifest_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix('.tmp')
    temporary.write_text(json.dumps(metadata, indent=2) + '\n')
    temporary.replace(path)
