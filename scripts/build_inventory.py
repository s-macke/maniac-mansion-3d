#!/usr/bin/env python3
"""Rebuild the step-1 asset inventory and lossless inspection contact sheets.
Requires Pillow. Run from any working directory. Original assets are read only.
"""
from pathlib import Path
from collections import Counter
from hashlib import sha256
import csv
import json
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated/reference'
REF = OUT / 'images'
# Descriptive working names, not assertions about internal game room names.
# id | name | cutaway position | match confidence | visible exit cues / caveats
ROWS = '''001|Front porch and grounds|Front facade, bottom of house|high|Central double entrance; porch steps; grounds extend sideways
002|Pool interior, drained|Below pool, right underground|high|Ladder to pool deck; pipes are not walking routes
003|Living room|Ground band, center|high|Door left; double door right
004|Dungeon|Upper underground band, left|medium|Two reinforced doors; artwork uses different wall treatment
005|Library|Ground band, right|high|Double door left; spiral stair, upper destination unclear
006|Pool deck|Right of house, beside garage|high|Door left; pool ladder; deck continues toward garage
007|Kitchen|Band above ground, left-center|high|Door at each end
008|Reactor / machinery room|Upper underground band, center|high|Door left; stairs right
009|Boarded telescope-view room|Projecting gray room, middle-right tower|low|Window left; boarded rear opening; no clear doorway; placement tentative
010|Entrance hall|Ground band, left of living room|high|Double entrance left; two rear single doors; right side door; central stairs
011|Entrance stair landing|Above entrance, left|medium|Side doors; central reinforced door; stair arrival in foreground
012|Windowed stair hall|Middle tower, left, below green stair flight|high|Left stairs; rear door; railed landing right
013|Security stair hall|Lowest tower band, blue corridor with stairs right|medium|Reinforced door left; two regular doors; stairs right
014|Plant / storage room|Left wing above ground, far left|high|Rear door; no clear upper exit in supplied background
015|Damaged attic|Upper-right gable|high|Floor hatch; boarded window
016|Garage|Separate structure at far right|high|Wide opening left to outdoors; rear shelving is not a ladder
017|Piano / music room|Left wing above ground, right of landing|high|Door left; piano and gramophone identify room
018|Arcade|Lower tower, right of medical room|high|Door left; rectangular floor panel near door is ambiguous
019|Heart-wallpaper bedroom (Edna candidate)|Upper bedroom band, center-left|high|Door left; ladder at far right
020|Speaker / record room|Upper-left roof room|high|No clear door or ladder shown in background
021|Radio bedroom (tentacle candidate)|Upper bedroom band, center-right|high|Ladder left; door right
022|Medical / examination room|Lower tower, left of arcade|high|Rear door; tall cabinet is a prop
023|Photo darkroom|Upper roof band, center|high|Door right to windowed stair hall (012); enlarger and print trays are fixtures, not a hatch
024|Bathroom|Below damaged attic, right|high|Rear door; no explicit ceiling hatch visible
025|Mummy / sarcophagus room|Upper bedroom band, far right|high|Door at each end
026|Green bedroom (Ed candidate)|Upper bedroom band, far left|high|Rear door; window right
027|Typewriter / fireplace room|Right end of long upper corridor band|high|Door left; fireplace not confirmed as a passage
028|Observatory|Top dome|high|No clear walking entrance in background
029|Under-house pipe corridor|Directly below porch|high|Passage extends to both image edges
030|Laboratory, control chairs|Deepest underground band, center-left|high|Door at each end; radiation-marked cabinet/compartment at right
031|Meteor / machine chamber|Deepest underground band, far left|high|Vault-like door left; regular door right
032|Moon landing / ending scene|Moon vignette, upper left|medium|Off-site scene; not a house room
033|Distant house panorama|Exterior mood reference|not mapped|Related composition to 047; not a separate interior
034|Telescope view panels A|Not mapped|not mapped|Three circular close-up views; not rooms
035|Telescope view panels B|Not mapped|not mapped|Three circular close-up views; not rooms
036|Pantry / storage vestibule|Right end of kitchen/dining band|high|Door left; blue mesh door rear
037|Dining room|Band above ground, center-right|high|Door at each end
038|Long four-door corridor|Upper tower, below bedroom band|high|Four rear doors plus side opening/door at each end
040|Television advertisement close-up|Not mapped|not mapped|Screen graphic; optional texture reference only
041|Office / ending scene|Not mapped|not mapped|Off-site-looking office; retain outside house scope
042|Television studio / ending scene|Not mapped|not mapped|Stage set; retain outside house scope
043|Keypad close-ups|Not mapped|not mapped|Interface/prop detail only
044|Gate and moon close view|Exterior mood reference|not mapped|Ground-level approach candidate; giant moon is background art
045|Title / character selection|Not mapped|not mapped|UI only
046|Roof close view|Roof reference|not mapped|Exterior silhouette reference; not a separate room
047|Distant house and moon|Exterior mood reference|not mapped|Establishing view; not a separate interior
048|Flying car / ending scene|Not mapped|not mapped|Ending illustration
049|Title logo|Not mapped|not mapped|UI only
050|Save / load menu|Not mapped|not mapped|UI only
051|Laboratory, operating apparatus|Deepest underground band, right|high|Door at each end
052|Damaged exterior fence / opening|Pool/garage exterior candidate|low|Possible altered exterior state; exact relation to 006/016 unresolved'''


def main():
    REF.mkdir(parents=True, exist_ok=True)
    metadata = {r.split('|')[0]:r.split('|')[1:] for r in ROWS.splitlines()}
    files = sorted((ROOT/'source').rglob('room *.png'), key=lambda p:p.name)
    assert len(files) == len(metadata) == 51
    palette = Counter()
    inventory = []
    for p in files:
        rid = p.stem.split()[-1]
        name, location, confidence, exits = metadata[rid]
        with Image.open(p) as im:
            rgb = im.convert('RGB')
            counts = rgb.getcolors(rgb.width * rgb.height)
            palette.update({color: count for count, color in counts})
            w,h = im.size
        scope = ('reference only' if p.parent.name == 'not_important' or rid in ('044','047') else 'walkable area')
        inventory.append(dict(id=rid,name=name,file=p.relative_to(ROOT).as_posix(),width=w,height=h,
            scope=scope,cutaway_location=location,match_confidence=confidence,exit_cues=exits,
            sha256=sha256(p.read_bytes()).hexdigest()))
    with (OUT/'room_inventory.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=inventory[0].keys());writer.writeheader();writer.writerows(inventory)
    (OUT/'palette.json').write_text(json.dumps({'source':'All 51 supplied background PNGs; RGB bytes preserved exactly',
        'colors':[{'hex':'#%02X%02X%02X'%c,'rgb':list(c),'pixel_count':palette[c]} for c in sorted(palette)]},indent=2)+'\n')
    font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',16)
    small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',13)
    for group,items in [('main',[r for r in inventory if '/not_important/' not in r['file']]),
                        ('extra',[r for r in inventory if '/not_important/' in r['file']])]:
        for start in range(0,len(items),10):
            page=items[start:start+10]
            canvas=Image.new('RGB',(1024,64+len(page)*180),'#20242b');d=ImageDraw.Draw(canvas)
            d.text((16,10),f'Maniac Mansion - {group} references - page {start//10+1}',font=font,fill='white')
            d.text((16,35),'Original pixels at 1:1. Raw aspect; no smoothing, recoloring, or panorama squeezing.',font=small,fill='#c0c8d0')
            for i,r in enumerate(page):
                y=64+i*180
                d.text((16,y),f"{r['id']}  {r['name']}  [{r['width']} x {r['height']}]",font=font,fill='white')
                with Image.open(ROOT/r['file']) as im:canvas.paste(im.convert('RGB'),(16,y+27))
            canvas.save(REF/f'contact-{group}-{start//10+1:02}.png')
    # Side-by-side aspect comparison at integer pixel scales, with no interpolated colors.
    src=Image.open(ROOT/'source/room 010.png').convert('RGB')
    canvas=Image.new('RGB',(3240,1520),'#20242b');d=ImageDraw.Draw(canvas)
    d.text((20,15),'Entrance hall: raw pixels (5x horizontal, 5x vertical)',font=font,fill='white')
    canvas.paste(src.resize((3200,640),Image.Resampling.NEAREST),(20,45))
    d.text((20,710),'Provisional DOS display aspect (5x horizontal, 6x vertical = 1.2x relative height)',font=font,fill='white')
    canvas.paste(src.resize((3200,768),Image.Resampling.NEAREST),(20,740))
    canvas.save(REF/'entrance-aspect-comparison.png')
    md=['# Room inventory','',
        'All 51 PNGs were inspected. Working names describe the visible artwork; character ownership in parentheses is tentative. IDs are filename IDs, not a verified engine resource mapping.', '',
        '35 top-level images represent candidate walkable areas; 044 and 047 are exterior establishing references. The 14 images in `not_important` are retained as supplemental references, not added as house rooms. No file numbered 039 was supplied.','',
        'Match confidence describes matching a background to the cutaway, **not** proof of any door destination. Left/right below refer to the image, not compass directions.','',
        '| ID | Working name / source | Size | Scope | Cutaway location | Match | Visible exits / caveats |',
        '|---|---|---|---|---|---|---|']
    for r in inventory:
        link='../'+r['file'].replace(' ','%20')
        md.append(f"| {r['id']} | [{r['name']}]({link}) | {r['width']}×{r['height']} | {r['scope']} | {r['cutaway_location']} | {r['match_confidence']} | {r['exit_cues']} |")
    md += ['', '## Alternate views and states','',
        '- 006 and 002 depict the pool deck and drained pool interior. They belong to one spatial structure. The walkthrough starts filled; E/tap toggles a drained exploration state and enables the same-room ladder into the basin. There are no draining puzzles, timers or swimming mechanics.',
        '- 033 and 047 are related distant-house compositions, not two separate locations to model.',
        '- 034 and 035 contain multiple telescope close-ups; 043 contains keypad close-ups.',
        '- 052 may show an altered pool/garage boundary. Keep it as a state reference until the location is verified; do not create an additional room.',
        '- 032 and 048 are ending imagery; 041 and 042 are office/studio scenes outside the initial house scope.',
        '- Static images do not enumerate all door-open, lighting, object, or destruction states. Do not infer that absent states do not exist.',
        '', '## Rebuild and audit','',
        'Run `python scripts/build_inventory.py` (requires Pillow). It rebuilds this inventory, CSV, sampled palette, contact sheets, and aspect comparison. The CSV records source SHA-256 hashes. Original files are read only. Connection and scale documents are manually reviewed interpretations.','']
    (OUT/'room_inventory.md').write_text('\n'.join(md))
    print(f'Inventoried {len(inventory)} PNGs; {len(palette)} exact RGB colors; generated 6 contact sheets.')

if __name__=='__main__':main()
