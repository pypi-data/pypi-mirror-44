Libpyn
======
> A third-party API for **libsyn**.
___

Installation
------------

In order to install _libpyn_, run this command on the terminal

``` console
foo@bar:~$ pip install libpyn
```

___

Features
--------

* ### The Podcast class <a name="podcast-class"></a>

The _Podcast class_ is the main feature of this package.

``` python
# Import statement
from libpyn.podcast import Podcast
```

In order to create an instance of the Podcast class, pass a link to a _libsyn_ channel in with the instance declaration.

``` python
channel = 'https://therabbithole.libsyn.com/'
example = Podcast(channel)
```

Once initialized, the Podcast class contains useful information about the podcast.

``` python
example.name = # Name of the podcast channel
self.mp3list = # List of episodes, each episode saved as a dictionary
self.htmllink = # Link to the podcast's website  
```

Each dictionary in _self.mp3list_ contains these key/value pairs:

``` python
podcast = {}    # Dictionary for storing podcast info
podcast['title'] = # Name of episode
podcast['date'] = # Publish date
podcast['mp3'] = # Link to mp3 file
podcast['image'] = # Channel logo
```

* ### Downloading podcasts

In order to download the mp3 files of a podcast channel, use the **download()** function.

``` python
# This will download the mp3 files in a directory named after the podcast channel
# in the Downloads directory
example.download()
```

A specific _path_ can be specified, the name of the directory (_foldername_) in which the mp3 files will be stored can also be specified. If the foldername is not specified, it will be the name of the channel. (Spaces are replaced with underscores.)

``` python
path = 'path/to/store/mp3'
directory = '/files'
example.download(path=path, foldername=directory)
```

* ### iframes

In order to get a list of HTML iframes of the latest episodes to embed on a webpage, use the **iframes()** function.

``` python
iframesList = example.iframes()
```

___

Changelog
---------

### == v1.0.1 ==
* _Fix bugs involving download function_
* _Remove HTML tags from podcast.name attribute_
* _Fix logger, log always in same directory as podcast.py_

### == v1.0.0 ==
* _Initial release_
