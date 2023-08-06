<!--
https://pypi.org/project/readme-generator/
https://pypi.org/project/python-readme-generator/
-->

[![](https://img.shields.io/badge/OS-MacOS-blue.svg?longCache=True)]()
[![](https://img.shields.io/badge/language-AppleScript,%20Bash-blue.svg?longCache=True)]()

#### Installation
```bash
$ [sudo] pip install itunes-cli
```

#### Scripts usage
```bash
usage: itunes command [args]

Available commands:

    play        play current track
    pause       pause current track
    next        next track
    prev        previous track
    stop        stop play

    playlists   playlists names

    volume      get/set iTunes volume
    mute        mute sound
    unmute      unmute sound
    muted       true/false if muted

    kill        kill iTunes.app
    pid         iTunes.app pid

run `itunes COMMAND --help` for more infos
```

#### Examples
```bash
$ itunes play
$ itunes pause
$ itunes stop
$ itunes next
$ itunes previous
```

volume
```bash
$ itunes volume 50
$ itunes volume
50
```

mute
```bash
$ itunes mute
$ itunes muted
true
$ itunes unmute
```

process
```bash
$ itunes pid
42
$ itunes kill
```

<p align="center">
    <a href="https://pypi.org/project/python-readme-generator/">python-readme-generator</a>
</p>