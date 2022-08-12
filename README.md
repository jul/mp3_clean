DAY 3
=====

I normally write the README at the beginning, but here, it is a new experiment : I code
freely.

It is a refreshing experience. Instead of planning, I code following the easy way, making
mistakes and seeing what I learned.

Problem at hand
---------------

During the last 25 years (a quarter of a century) I have made a mess of having too much mp3s
and I would like tu put them in a central place.

Yep, my collections is as old as it can be.

Other problem, my desktop have always been running linux and windows (dos2linux, dual boot,
and now WSL/qemu) because well ... Sound on linux is a major pain in the ass, so my main
collection is on windows.

I normally code only on linux, and I hate coding "the office way" on windows.

Office way is having IDE, and click a click setup, and bloatware like conda that are candy
eye stuff but are not important. I have uninstalled conda on windows after 3 years of giving
it a chance. It does not fit **me**.

And I like portable code.

So, this project began with git bash + vim + vanilla almoste last stable python. Command
line setup with minimal vimrc.


Also, having gotten riped CDs now physically too old to be used and music you cannot find
even on the dark web I also have to handle the "untagged" music files in various format
(AAC, flac, ogg, MP3, MP4 and even some wav).

Before deciding of a strategy I decided to make a minimal POC to assess current situation
with a small sample of my library (5000 files).

Well, I have 10% doublons for a start. And that is gonna be a subject. I will have to find a
way to score wich files to keep.

The good news is, you can still code as a unix coder on windows. gh+git cli (github cli) is
helping a lot.  I know github is evil. But this code is merely more about this file than the
code and cleaning the mess.

It is about getting back to minimalism and basics.

Like, you know this dest field in the database is already scratching a nerve because I know it
is uncorrectly named.  On the other hand, I am very glad I tried to tackle initial
difficulties on a large enough sample to not get mad.

For instance: correctly handling windows path name. I normally do rely on some shortcuts for
building paths like using "~".

If I have some grudges about python, like python3.10 `from collections.abc import
MutableMapping`, but  the os stdlib is not one of it. It really tackles the accidental
difficulties of constructing path names in a nice way. And in computers path names are
important.

Also I took the liberty to use a 90 column layout, because, being on windows, I feel free to
ignore the tabou of the 80 cols width. I know :set tw=90, gg (or v), gqG (vim tip)

It does feel great to be honest. I don't understand why I lost so many years not going into
my comfort zone.

PEP8 ? Well, you see, I don't care. PEP8 is rigid as typography. Especially on ponctuation,
and I am not a native english speaker.

I prefer for some things the french typography where you have a space before double
ponctuation marks. I sometimes prefer as when I was doing math at university to put useless
() and space in expression if I feel like **I** can better read, and going back on my
comfort zone on this feels great too. And sometimes I code like I write english of french.
First I make sure to lay down the ideas straight, and later, eventually I do a pass at
improving the style. But style really is a second thought when I focus, and sometimes
(often) PEP8 linter infuriates me because I LOVE multiple statements in one line. It fits my
way of thinking. I insist it is not about a TRUTH that is universal for all coders, it is MY
TRUTH. I have PEP8 compliant code somewhere on github. But, I really don't care about PEP8.

I had to reinstall git bash and gh-cli. Kind of scares me as unsecure, but, I don't care.
The security by web token has becomed prevalent, even on linux. So, why not. Of course git
bash pseudo terminal is so shitty (mintty) on some aspect like using ipython history or
sqlite3 console that I am a tad pissed to have to use the useless cmd.exe.

Having good pseudo terminal with readline (ctrl + R, history ...) is really important
whatever the environment. The problem is whatever the OS is, the console subsystem is a
bloated mess piling up decades of conservatism and huge amount of shit. Don't start me on
why I cannot plug a second keyboard on any OS with mame to play with my kid comfortably. (I
have writtend a framebuffer device driver for linux for a multihead cirrus logic 5480 in the
early days when coding in C was accessible and had to dive deep into console, and I still 
have nightmares).

mingw (the minimal cygwin subsystem used by microsoft/github) has however a lot of neatty
features including a lot that I don't care about for its tty. Like the support for emojis or
graphic in the console. On the stuff I care about is the font, the ease of resizing screen,
the shortcut for copy pasting with mouse with the button I prefer, and the fact I can use vim.

Ok, love semi transparent screen too. I don't know why, but since Eterm (amiga enlightment)
I love this stuff.

I miss a tad fluxbox. It would be nice to have as a replacement for windows GUI.

Well, you see, I learned a thing in the process. If writing code is made with tools you
don't like, you cannot write code. It is infuriating.

Comfort is important. And for the same reason we have shoes of different sizes, shape,
protections level, one size does not fit all. The tooling for WRITING, doing fast test from
environment, checking hypothesis, firing a sql console should stay at the freedom of the
user. vim IS NOT THE BEST EDITOR. I sometime use kate to be honest. But, vim is so portable
being comfortable with it gives you a huge room of comfort applying from a mainframe, a
server, a linux beefed up laptop up to an old 486. So vim is quite a good editor.

So basically, solving a problem is not only identifying what to do, but also to make
yourself comfortable at coding by removing the most frictions and complexity. Including your
workspace. I am so glad to be able to code at home and not in a fucking dysfunctionning
company right now and to enjoy my freedom to the fullest I warmly suggest you give it a try.

It is exhilarating, empowering, emancipating. You can feel what matters or not. Like since I
write in vim in a console I don't have the grammar/orthograph nazis nudge from web forms
telling me I made a mistake that piss me so much I don't dare write anymore. My text is full
of grammar and other mistakes ? Well, beat it. Live free from social pressure.


Choice of tinytag
-----------------

Doing a stackoverflow way of discovering the "right" library for accessing music files
metadata was not evident.

The web brought me a lot of outdated libraries for the problem at hand. Of course I was soon
redirected to finally mutagen which is the most precise way of handling metadata. The **BEST**
library.

However, I was not interested in the best, especially if it meant trashing precious wav
file.

Mutagen code is also the **ONE BEST WAY** to code. Seriously. Like they do for professional
project. With a lot of classes accesible, in multiple files, classes everywhere. The BEST.

However, I needed to have unified interface to info such as `artist, album, title` and to
not care about the intended encoding.

I like the code of tinytag, its API and the way it returns "usable" unified data structure.

It's a onefile code with very complete and nice collection of parsers for various formats
and it is intended for ease of modification. It uses unpack ... in a way that could be used
for a tutorial on the use of pack/unpack. I recommand it.

Choice of sqlite
----------------

Well, when you code, you really don't care for the database as long as you know it has
the minimal requirement for doing what you want : GROUP BY/PARTITION BY to find duplicates
and score them, and JSON manipulation in requests. There are stuffs for which database is
the answer. When it comes to finding duplicates and being able to manipulate lists of a lot
of stuff without having to code database are there with ALL the tutorials to help you when
you have forgotten. Postgres is installed on this computer. But seriously, I prefer when no
security is required to connect to the DB without a login/pass. Plus, sqlite as a very
impressive support of SQL and nice documentation. JSON + minimal structure (where is the
file). I could have used an array of JSON with all inside, but updates and accidents where
kind of not my cup of tea.

Maybe I'm wrong and it's overkill, but I really think sqlite is the best alternative to CSV
(knowing that exporting a table to CSV is fairly easy).

Given the number of expected rows and the memory I have, I really don't have the need for
distinct table with relationship, and json will take care of the evolutive part of the data.
Yep, at the opposite of classical tutorials on building your database for your "list of
songs" I did not give into the artist table, album table, track table. One table to rule
them all.

This "example" database is the exact example of sqlite tutorials. And I really think people
are overcomplexifying their data structure. I am not amazon, I don't need to store more data
than my 4G memory can handle.

Sanitizing filename
-------------------

Well I already hinted I did a quick live test by touching file on a directory to look at the
layout that would result. I had quite a few surprises and thought that I would not like a
vulnerability (or more probably an accident) due to someone adding a **.** at the end of a
name of an artist. It reminds me I did not cover the case the sanization of string would
return an empty string which would throw the code in an uncharted territory I don't want to
discover. You understand, accident will happen when you work with thousands of file
and creations en masse. And well, I have a new job, saved while being poor on backups, and
this project is basically a preparation for backup. If it works well, I may try to reproduce
the idea for pictures, documents, source codes if it turns well.

Backup are important. But when your main media station has a 1TB disk that is the biggest at
home, you want to put data that are important in a place easy to locate.


Future
------

The embasing code is done. It works pretty well. The torture test on the filesystem did not
ended up in a corruption or a loss of data. I am pretty relived. Having an old hard drive I
will finalize this part of the code because full intensive scan of the hard drive (>10 years
old) cringes me.

I probably will add some tools to create playlist for a cli musicplayer (ffmpeg?, vlc
nographic?) since I am not satisfied by the bloated musicplayer on windows. I want something
simple like an old mp3 player with just the name of the artist/album/track that plays in
shuffle by default and has ONE shortcut for NEXT.

I will probably put the untagged songs in the db too and think of a minimal GUI to play/tag
them. The songs being ripped from my CD before the internet era they don't match an internet
database. I think already of using python tk since I have a json editor made in python tk ;)
check there https://gist.github.com/jul/e9132abe8b5aeea573917191591fb90b which is the only
difficulty in the process.

So after having proven to myself in 3 days worth of coding and leisure it was possible, I
will proceed at my own pace. Remembering how coding is fun and useful when you focus not on
HOW TO DO IT THE ONE BEST WAY, but when you can stay focus on the task at hand and minimize
the stress of handling cases that never happens while having real life shower down your
expectations.

