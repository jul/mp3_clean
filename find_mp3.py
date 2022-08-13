#from mutagen import File as get_tags
#from mutagen.easyid3 import EasyID3 as get_tags_mp3
from tinytag import TinyTag as tags
from operator import itemgetter as get
from archery import mdict
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
os.unlink(DB)
db_exists= path.exists(DB)
db = sqlite3.connect(DB)
dbc = db.cursor()
dbc.execute("""
    CREATE TABLE music(
        source TEXT PRIMARY KEY NOT NULL,
        dest TEXT NOT NULL,
        metadata TEXT,
        filename TEXT NOT NULL,
        sdir TEXT NOT NULL,
        artist TEXT,
        album TEXT,
        title TEXT,
        duration FLOAT,
        bitrate FLOAT,
        extension TEXT
        )""")
db.commit()
pd = lambda d: print(dumps(d, indent=4) + "\n")
SANDBOX_DIR=path.join(path.expanduser("~"), "todel_mp3_test")


def is_wanted(filename):
    return filename.lower()[-4:] in { ".mp3", "flac",".ogg", ".wma", ".aac", ".wav"}

start = "."
try:
    start = argv[1]
except:
    pass

if not path.exists(start):
    raise Exception("%s not a valid directory to look for")

score = mdict(keys=mdict(), artist=mdict())
with open("cant_parse.txt", "w", encoding='utf-8')  as list_of_music_wo_tags:
    n_found,n_errors, n_ignored, n_collisions = 0, 0, 0, 0
    for root, dirs, names in os.walk(start):
        fp_to_fn = { path.join(root, name): sanitize(name) for name in names } 
        files = fp_to_fn.keys()
        found = list(filter(is_wanted,files))
        n_found += len(found)
        for music in found:
            try:
                res=mdict({k:v and v.strip() if hasattr(v, "strip") else v for k, v in tags.get(music).as_dict().items()})
                score["keys"] += mdict({ k : 1 for k in res.keys()})
                res+=mdict(_dir=root, _src=music, _fname=fp_to_fn[music])
                extension = fp_to_fn[music].split(".")[-1]
                album = clean_string((res.get("album", "unknown") or "").title()) or "unkown"
                res["album"] = album
                artist = clean_string((res.get("artist", "unknown") or "").title()) or "unknown"
                res["artist"] = artist
                dest_dir = path.join(SANDBOX_DIR, sanitize(artist), sanitize(album))
                dest = path.join(dest_dir, sanitize(clean_string(fp_to_fn[music])))

                if artist == "unknown":
                    if "-" in (res.get("title","") or ""):
                        artist = (res.get("title") or "").split('-')[0].strip()
                        print(f"r <{res['title']}> give artist <{artist}>")
                    elif "-" in res["_fname"]:
                        r = res["_fname"].split("-")[-2].strip()
                        if not r.isdigit() or r == "311":
                            artist = r
                            print(f"r <{res['_fname']}> give artist <{artist}>")
                        else:
                            print(f'artist is not in {res["_fname"]}')

                score["artist"] += mdict({res.get("artist","unknown"):1})
                dbc.execute(
                    "INSERT INTO music VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    (music, dest, dumps(res, indent=4)) + \
                    tuple(map(
                        res.get,
                        ("_fname", "_dir", "artist", "album", "title", "duration", "bitrate", "extension" )))
                )
                makedirs(dest_dir, exist_ok=True)
                if path.exists(dest):
                    print(f"c", end="")
                    n_collisions+=1
                else:
                    with open(dest, "a") as f:
                        print(".", end="")
            except Exception as e:
                print(e)
                from pdb import set_trace; set_trace()
                list_of_music_wo_tags.write(f"{music}\n")
                n_errors+=1
                print(f"couldn't parse {music}")
    print(f"found {n_found} items, {n_errors} errors seen, {n_ignored} ignored, {n_collisions} collisions")
db.commit()

print("keys seens for all metadata")
pd(score["keys"])
print("artist most seen")
pd(dict(sorted(score["artist"].items(), key=get(1), reverse=True)[:30]))


