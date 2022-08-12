#from mutagen import File as get_tags
#from mutagen.easyid3 import EasyID3 as get_tags_mp3
from tinytag import TinyTag as tags
from operator import itemgetter as get
import archery
from os import walk, path, makedirs
from sys import stderr
from sanitize_filename import sanitize
import os
from sys import argv
from json import dumps
import sqlite3
import re
ms = re.compile(r'''\s+''')
clean_string=lambda s: ms.sub(' ', s)
DB="music.db"
db_exists= path.exists(DB)
db = sqlite3.connect(DB)
dbc = db.cursor()
if not db_exists:
    dbc.execute("""
        CREATE TABLE music(
            source TEXT PRIMARY KEY NOT NULL,
            dest TEXT NOT NULL,
            metadata TEXT NOT NULL)""")
    db.commit()
pd = lambda d: print(dumps(d, indent=4) + "\n")
SANDBOX_DIR=path.join(path.expanduser("~"), "todel_mp3_test")


wanted=[
        lambda fn : fn.lower()[-3:] in {"mp3", "mp4"} and open(fn, "rb").read(3) ==b'\x49\x44\x33',
        lambda fn : fn.lower()[-4:] in {"flac", ".wma", ".aac", ".wav"},
        ]
def is_wanted(file):
    for test in wanted:
        try:
            if test(file):
                return True
        except:
            pass



def tag_to_dict(tag,**extra):
    cleaned = { k:v and  v.strip() if hasattr(v, "strip") else v or ""  for k, v in tag.as_dict().items() }
    assert not cleaned.keys() & extra.keys(), "keys in extra conflict"
    for k, v in extra.items():
        cleaned[k] = v.strip() if hasattr(v, "strip") else v
    return cleaned
start = "."
try:
    print(argv)
    start = argv[1]
    print(start)
except:
    pass
if not path.exists(start):
    raise Exception("%s not a valid directory to look for")

with \
    open("music_found.txt", "w", encoding='utf-8') as list_of_music_found, \
    open("cant_parse.txt", "w", encoding='utf-8')  as list_of_music_wo_tags, \
    open("collision.txt", "w", encoding='utf-8')  as list_of_collision:
    n_found,n_errors, n_ignored, n_collisions = 0, 0, 0, 0
    for root, dirs, names in os.walk(start):
        fp_to_files = { path.join(root, name): sanitize(name) for name in names } 
        files = fp_to_files.keys()
        found = list(filter(is_wanted,files))
        n_found += len(found)
        for music in found:
            try:
                res=tag_to_dict(tags.get(music), dir=root, filename=music)

                if res.get("duration",1) < 1:
                    pd(res)
                    print(f'{music} is fishy not added to music')
                    n_ignored+=1
                else:
                    list_of_music_found.write(f'{music}\n')
                    album = clean_string(res.get("album", "unknown").title())
                    artist = clean_string(res.get("artist", "unknown").title())
                    name = fp_to_files[music]
                    dest_dir = path.join(SANDBOX_DIR, sanitize(artist), sanitize(album))
                    dest = path.join(dest_dir, sanitize(clean_string(name)))
                    dbc.execute("INSERT INTO music VALUES (?, ?, ?)", (music, dest, dumps(res, indent=4)))
                    try:
                        makedirs(dest_dir, exist_ok=True)
                        if path.exists(dest):
                            print(f"collision on {dest}")
                            n_collisions+=1
                            list_of_collision.write(f"{name} -> {dest}\n")
                        else:
                            with open(dest, "a") as f:
                                print(f'creating {name} -> \n   {dest}')
                    except Exception as e:
                        print(e)
                        pd(res)
                        from pdb import set_trace; set_trace()
                        n_errors+=1
                        stderr.write(f"failed wrintg {music} to {dest}\n")
            except Exception as e:
                print(e)
                list_of_music_wo_tags.write(f"{music}\n")
                from pdb import set_trace; set_trace()
                n_errors+=1
                print(f"couldn't parse {music}")
    print(f"found {n_found} items, {n_errors} errors seen, {n_ignored} ignored, {n_collisions} collisions")

        #print(sum(path.getsize(path.join(root, name)) for name in files if name.endswith("mp3")),
                #end=" ")

db.commit()





