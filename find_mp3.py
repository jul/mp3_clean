#from mutagen import File as get_tags
#from mutagen.easyid3 import EasyID3 as get_tags_mp3
from tinytag import TinyTag as tags
import archery
from os import walk, path
from sys import stderr
import os
from sys import argv
from json import dumps
pd = lambda d: print(dumps(d, indent=4) + "\n")

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
    cleaned = { k:v for k,v in tag.as_dict().items() if v }
    assert not cleaned.keys() & extra.keys(), "keys in extra conflict"
    for k, v in extra.items():
        cleaned[k] = v
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

with open("music_found.txt", "w", encoding='utf-8') as list_of_music_found:
    n_found = 0
    for root, dirs, names in os.walk(start):
        fp_to_files = { path.join(root, name): name for name in names } 
        files = fp_to_files.keys()
        found = list(filter(is_wanted,files))
        n_found += len(found)
        if len(found):
            #print(root)
            for music in found:
                try:

                    res=tag_to_dict(tags.get(music), dir=root, filename=music)
                    if not res.keys() & { "title", "artist", "track" } or  res.get("duration",1) < 1:
                        print(f'{music} is fishy')
                        #pd(res)
                    else:
                        list_of_music_found.write(f'{music}\n')
                        artist = res.get("artist", "unknown").title()
                        album = res.get("album", "unknown").title()
                        name = fp_to_files[music]
                        print(f'{name} -> \n   {artist}/{album}/{name}')
                except:
                    from pdb import set_trace; set_trace()
                    stderr.write(f"failed reading {music}\n")
    print(f"found {n_found} items")

        #print(sum(path.getsize(path.join(root, name)) for name in files if name.endswith("mp3")),
                #end=" ")






