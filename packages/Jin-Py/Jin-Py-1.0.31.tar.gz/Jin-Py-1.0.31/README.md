# Jin

Jin is a Git/Mercurial flavored Rsync wrapper, making it easy to:
  * manage projects like you would with Git/Mercurial
  * push and pull from remote "repositories" or machines
  * quickly backup files without hassle or knowing how to use Rsync

Jin, however, is not:
  * a direct replacement for Git, Mercurial, or any other version control system
  * able to use every feature of Rsync (as of now)

### Requirements

* `Rsync (tested 3.1.2)`
* `Watchdog >= 0.9.0` - `pip install watchdog==0.9.0`

### Installation

Jin can be installed with pip:
* `pip install jin-py==1.0.3`

It can also be installed manually:
  * `git clone https://github.com/kyoto-shift/jin && cd jin/`
  * `python setup.py install`
  * *Note: Jin has only been tested on Python 3.7.3*

### Basic Guide

To get started, simply enter a directory you'd like to work with and run `jin init`. This command will create a file and a folder:
  * `.jinconfig` - your project's configuration file
  * `.jin/` - where information about your project lives *(you shouldn't have to go in here)*

  `.jinconfig` files follow a simple format. A rule ending in a `:` character, followed by the values *(separated by spaces)* (e.g. `rule: value1 value2`). The default configuration created has every rule present, but commented out using the `#` character. Uncomment these lines to activate them.
  * `host_address` - The hostname of the machine you'd like to track changes from. If working locally *(i.e. pushing from your machine to a remote machine/local directory)*, this can be commented out.
  * `host_location` - The location on the host machine to track from. Most times this will be set to `./` *(the Jin project's directory)*.
  * `remote_address` - The hostname of the machine you'd like to push to. Once again, leave this commented out if working locally.
  * `remote_location` - The directory on the remote machine to push to. If `remote_address` is commented out, this can be another location on the same machine *(e.g. pushing to an external hard drive)*.
  * `watch_min_updated` - If the `watch` flag has been set, this is the minimum number of changes that will need to occur in the project's directory before Jin pushes the changes automatically.
  * `ignore_specific` - Specific files or folders Jin should ignore. *(e.g.* `ignore_specific: __pycache__/ notes.txt`*)*
  * `ignore_filetype` - Generic file types Jin should ignore *(e.g.* `ignore_filetype: *.o *.swp`*)*

An example Jin configuration where files are sent to an external backup server could look like this:
```
  host_location: ./

  remote_address: backups@server.ip.address
  remote_location: /2019/samples/library/

  ignore_specific: .jinconfig soundfonts/ wavetables/
  ignore_filetype: *.jin *.asd *.reapeaks
```

My actual configuration while working on Jin looked like this:
```
  host_location: ./jin

  remote_address: citadel@192.168.1.85
  remote_location: /home/citadel/test_enviroments/python37/jin

  ignore_specific: .jinconfig __pycache__/
  ignore_filetype: *.jin *.pyc *.swp
```

The above configuration allowed me to work comfortably on my Windows machine while being able to run test builds of Jin on a headless Linux machine on my network.


### Why I Made This

For me, working on Windows is nice since I do some game development work and I have a workflow I'm comfortable with. However, I also enjoy programming in languages like C, Crystal, Scheme, etc, which Windows *(8.1, sorry)* doesn't usually play well with. I wrote Jin so that I could write my programs using a workflow I actually like, while testing and executing on a platform that actually works well with any toolchains I throw at it *(thank you Linux)*.
