# hashget

*You do not need to bear the cost to store files which you can download*

Hashget is network deduplication tool developed mainly for archiving (backup) debian virtual machines (mostly), but 
could be used for other backups too. For example, it's very useful for backup LXC containers 
before uploading to Amazon Glacier. 

Upon compressing, hashget replaces *indexed static files* (which could be downloaded by static URL) 
to it's hashes and URLs. This can compress 600Mb debian root filesystem with mysql, apache and other software to just 4Mb !

Upon decompressing, hashget downloads these files, verifies hashsum and places it on target system with same 
permissions, ownership, atime and mtime.

Hashget archive (in contrast to incremental and differential archive) is 'self-sufficient in same world' 
(where Debian or Linux kernel projects are still alive). 

## Installation

Pip (recommended):
~~~
pip3 install hashget[plugins]
~~~

or clone from git:
~~~
git clone https://gitlab.com/yaroslaff/hashget.git
~~~


## QuickStart

### Compressing

Compressing [test machine](https://gitlab.com/yaroslaff/hashget/wikis/Test-machine): 

~~~
# hashget -zf /tmp/mydebian.tar.gz --pack /var/lib/lxc/mydebvm/rootfs/ --exclude var/cache/apt var/lib/apt/lists
STEP 1/3 Indexing debian packages...
Total: 222 packages
Indexing done in 0.02s. 222 local + 0 pulled + 0 new = 222 total.
STEP 2/3 prepare exclude list for packing...
saved: 8515 files, 216 pkgs, size: 445.8M. Download: 98.7M
STEP 3/3 tarring...
/var/lib/lxc/mydebvm/rootfs/ (687.2M) packed into /tmp/mydebian.tar.gz (4.0M)
~~~

`--exclude` directive tells hashget and tar to skip some directories which are not necessary in backup. 
(You can omit it, backup will be larger)

Now lets compare results with usual tarring
~~~
# du -sh --apparent-size /var/lib/lxc/mydebvm/rootfs/
693M	/var/lib/lxc/mydebvm/rootfs/

# tar -czf /tmp/mydebvm-orig.tar.gz  --exclude=var/cache/apt --exclude=var/lib/apt/lists -C /var/lib/lxc/mydebvm/rootfs/ .

# ls -lh mydebvm*
-rw-r--r-- 1 root root 165M Mar 29 00:27 mydebvm-orig.tar.gz
-rw-r--r-- 1 root root 4.1M Mar 29 00:24 mydebvm.tar.gz
~~~
Optimized backup is 40 times smaller!

### Decompressing

Untarring:
~~~
# mkdir rootfs
# tar -xzf mydebvm.tar.gz -C rootfs
# du -sh --apparent-size rootfs/
130M	rootfs/
~~~

After untarring, we have just 130 Mb. Now, get all the missing files with hashget:
~~~
# hashget -u rootfs/
Recovered 8534/8534 files 450.0M bytes (49.9M downloaded, 49.1M cached) in 242.68s
~~~
(you can run with -v for verbosity)

Now we have fully working debian system. Some files are still missing (e.g. APT list files in /var/lib/apt/lists, 
which we **explicitly** --exclude'd. Hashget didn't misses anything on it's own) but can be created with 'apt update' command.

## Heuristics
Heuristics is small plugins (installed when you did `pip3 install hashget[plugins]`, or can be installed separately)
which can auto-detect some non-indexed files which could be indexed.

Now, lets add some files to our test machine:
~~~
mydebvm# wget -q https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.4.tar.xz
mydebvm# tar -xf linux-5.0.4.tar.xz 
mydebvm# du -sh --apparent-size .
893M	.
~~~

If we will pack this machine same way as before we will see this:
~~~
# hashget -zf /tmp/mydebian.tar.gz --pack /var/lib/lxc/mydebvm/rootfs/ --exclude var/cache/apt var/lib/apt/lists
STEP 1/3 Indexing debian packages...
Total: 222 packages
Indexing done in 0.03s. 222 local + 0 pulled + 0 new = 222 total.
submitting https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.5.tar.xz
STEP 2/3 prepare exclude list for packing...
saved: 59095 files, 217 pkgs, size: 1.3G. Download: 199.1M
STEP 3/3 tarring...
/var/lib/lxc/mydebvm/rootfs/ (1.5G) packed into /tmp/mydebian.tar.gz (8.7M)
~~~

One very interesting line here is:
~~~
submitting https://cdn.kernel.org/pub/linux/kernel/v5.x/linux-5.0.5.tar.xz
~~~

Hashget detected linux kernel sources package, downloaded and indexed it. And we got fantastic result again: 1.5G 
packed into just 8.7M!

Hashget packs this into 8 Mb in 28 seconds (on my Core i5 computer) vs 426Mb in 48 seconds with plain tar -czf. 
(And 3 minutes with hashget/tar/gz vs 4 minutes with tar on slower notebook). Hashget packs faster and often 
much more effective.


If you will make `hashget-admin --status` you will see kernel.org project. `hashget-admin --list -p PROJECT` will 
show content of project:
~~~
# hashget-admin --list -p kernel.org
linux-5.0.5.tar.xz (767/50579)
~~~

Even when new kernel package will be released (and it's not indexed anywhere), hashget will detect it and 
automatically index (at least while new linux kernels will match same 'template' as it matches now for kernels 
1.0 to 5.0.5).

Users and developers of large packages can write their own hashget plugins using [Linux kernel hashget plugin](https://gitlab.com/yaroslaff/hashget-kernel_org/)
as example.

## Manually indexing files to local HashDB
Now lets make test directory for packing.
~~~
# mkdir /tmp/test
# cd /tmp/test/
# wget -q https://ru.wordpress.org/wordpress-5.1.1-ru_RU.zip
# unzip wordpress-5.1.1-ru_RU.zip 
Archive:  wordpress-5.1.1-ru_RU.zip
   creating: wordpress/
  inflating: wordpress/wp-login.php  
  inflating: wordpress/wp-cron.php   
....
# du -sh --apparent-size .
54M	.
~~~

and now we will pack it:
~~~
# hashget -zf /tmp/test.tar.gz --pack /tmp/test/
STEP 1/3 Indexing...
STEP 2/3 prepare exclude list for packing...
saved: 4 files, 3 pkgs, size: 104.6K. Download: 3.8M
STEP 3/3 tarring...
/tmp/test/ (52.3M) packed into /tmp/test.tar.gz (22.1M)
~~~

Thats same result as usual tar would do. Only ~100K saved (you can see it in .hashget-restore.json file, there are
usual license files). Still ok, but not as impressive as before. Lets fix miracle and make it impressive again!

~~~
# hashget --project my --submit https://ru.wordpress.org/wordpress-5.1.1-ru_RU.zip
# hashget -zf /tmp/test.tar.gz --pack /tmp/test/
STEP 1/3 Indexing...
STEP 2/3 prepare exclude list for packing...
saved: 1396 files, 1 pkgs, size: 52.2M. Download: 11.7M
STEP 3/3 tarring...
/tmp/test/ (52.3M) packed into /tmp/test.tar.gz (157.9K)
~~~  
50M packed into 150K. Very good! What other archiver can make such great compression? (300+ times smaller!)

We can look our project details:
~~~
# hashget-admin --status -p my
my DirHashDB(path:/var/cache/hashget/hashdb/my stor:basename pkgtype:generic packages:0)
  size: 119.4K
  packages: 1
  first crawled: 2019-04-01 01:45:45
  last_crawled: 2019-04-01 01:45:45
  files: 1395
  anchors: 72
  packages size: 11.7M
  files size: 40.7M
  indexed size: 40.5M (99.61%)
  noanchor packages: 0
  noanchor size: 0
  no anchor link: 0
  bad anchor link: 0

~~~
It takes just 100K on disk, has 1 package indexed (11.7M), over 1395 total files. You can clean HashDB, but usually 
it's not needed, because HashDB is very small. 

And one important thing - hashget archiving keeps all your changes! If you will make any changes in data, e.g.:
~~~
# echo zzz >> wordpress/index.php
~~~
and --pack it, it will be just little bigger (158K for me instead of 157.9) but will keep your changed file as-is.
This file has different hashsum, so it will be .tar.gz'ipped and not recovered from wordpress archive as other 
wordpress files.

# Hint files
If our package is indexed (like we just did with wordpress) it will be very effectively deduplicated on packing.
But what if it's not indexed? For example, if you cleaned hashdb cache or if you will restored this backup on other 
machine and pack it again. It will take it's full space again. 

We will delete index for this file:
~~~
# hashget-admin --purge wordpress-5.1.1-ru_RU.zip
~~~
Now, if you will make hashget --pack it it will make huge 22M archive again, our magic is lost...

Now, create special *hint* file hashget-hint.json (or .hashget-hint.json , 
if you want it to be hidden) in /tmp/test with this content:
~~~
{
	"project": "wordpress.org",
	"url": "https://ru.wordpress.org/wordpress-5.1.1-ru_RU.zip"
}
~~~

And now try compress it again:
~~~
# hashget -zf /tmp/test.tar.gz --pack /tmp/test
STEP 1/3 Indexing...
submitting https://ru.wordpress.org/wordpress-5.1.1-ru_RU.zip
STEP 2/3 prepare exclude list for packing...
saved: 1396 files, 1 pkgs, size: 52.2M. Download: 11.7M
STEP 3/3 tarring...
/tmp/test (52.3M) packed into /tmp/test.tar.gz (157.9K)
~~~

Great! Hashget used hint file and automatically indexed file, so we got our fantastic compression rate again.

## What you should NOT index
You should index ONLY static and permanent files, which will be available on same URL with same content.
Not all projects provides such files. Usual linux package repositories has only latest files so it's not good for this
purpose, but debian has great [snapshot.debian.org](https://snapshot.debian.org/) repository, which makes Debian great 
for hashget compression.

Do not index *latest* files, because content will change    later (it's not _static_). E.g. you may index 
https://wordpress.org/wordpress-5.1.1.zip but you should not index https://wordpress.org/latest.zip 

## Documentation
For more detailed documentation see [Wiki](https://gitlab.com/yaroslaff/hashget/wikis/home).



