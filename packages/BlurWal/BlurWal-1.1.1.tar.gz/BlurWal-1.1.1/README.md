<div align="center">
  <img src="https://gitlab.com/BVollmerhaus/blurwal/raw/master/blurwal-logo.svg"
       title='"Wal" is short for "Wallpaper", but also means "Whale" in German – hence the logo.'
       alt="BlurWal Logo" width="30%" />
</div>

<div align="center">
  <p>Smoothly blurs the wallpaper when windows are opened.</p>
  <img src="https://img.shields.io/pypi/v/blurwal.svg" />
  <img src="https://img.shields.io/pypi/pyversions/blurwal.svg" />
  <img src="https://gitlab.com/BVollmerhaus/blurwal/badges/master/pipeline.svg" />
  <img src="https://img.shields.io/pypi/l/blurwal.svg" />
  <img src="https://img.shields.io/cii/percentage/2554.svg" />
</div>


# BlurWal

BlurWal smoothly blurs the wallpaper when a given number of windows is opened
on the focused workspace. This is done by first generating transition frames
from the current wallpaper, with each of them being blurred with an increasing
level. Upon opening enough windows, each frame will be set as the wallpaper in
quick succession, resulting in a transition. When the number of open windows
goes below the threshold again, the transition will run in reverse and
consequently unblur the wallpaper.


## Table of Contents

* [Installation](#installation)
  * [Dependencies](#dependencies)
  * [Supported Backends](#supported-backends)
  * [Stable Release](#stable-release)
  * [Development Version](#development-version)
* [Usage](#usage)
* [Multi-monitor Setups](#multi-monitor-setups)
* [Contributors](#contributors)
* [License](#license)


## Installation

### Dependencies

* `Python 3.6+`
* `ImageMagick` (for generating transition frames)
* A compatible backend, depending on your environment

### Supported Backends

| Name in [CLI](#cli) | Command used | Environment | Availability |
| ------------------- | ------------ | ----------- | ------------ |
| `feh`  | `feh` | **Most WMs** (i3, awesome, bspwm, Openbox, etc.) | Separate package
| `xfce` | `xfconf-query` | **Xfce** (uses xfconf to [store wallpaper configuration](https://git.xfce.org/xfce/xfdesktop/tree/doc/README.xfconf#n1)) | Part of Xfce

### Stable Release

```sh
pip install --user blurwal
```

> Also [available in the Arch User Repository](https://aur.archlinux.org/packages/blurwal/) as `blurwal`
>
> Installing from the AUR is preferred, as BlurWal will be updated together
> with the rest of your system.

### Development Version

```sh
git clone https://gitlab.com/BVollmerhaus/blurwal
cd blurwal
pip install --user .
```

> The latest changes on master, which may not be as stable.


## Usage

Simply run `blurwal` and it will regenerate its transition frames and blur
on the appropriate window events.


### CLI

This list includes only the interesting options – run `blurwal -h` for a
complete list and further information.

| Option | Description |
| ------ | ----------- |
| `-m`, `--min`    | The minimum number of windows to blur the wallpaper (default: 2)
| `-s`, `--steps`  | The number of steps in a blur transition (default: 10, minimum: 2)
| `-b`, `--blur`   | The blur strength (sigma) to use when fully blurred (default: 10)
| `-i`, `--ignore` | A space-separated list of window classes to exclude
| `--backend`      | The backend to use (one of the [compatible backends](#supported-backends))


## Multi-monitor Setups

Multi-monitor configurations are only partially supported. Depending on the
backend, BlurWal will use the wallpaper of your primary monitor (and first
workspace) and apply it to all monitors, only taking the focused workspace and
the number of windows on it into account. This also means that using different
wallpapers per individual monitor is not possible, as all will be overwritten
with the primary one.

> Changing this behavior is planned but will require some major changes.


## Contributors

### Maintainer

* [Benedikt Vollmerhaus](https://gitlab.com/BVollmerhaus)

### Others

* [Matthias Bräuer](https://gitlab.com/Braeuer) (Testing and Code Reviews)


## License

BlurWal is licensed under the MIT license. See
[LICENSE](https://gitlab.com/BVollmerhaus/blurwal/blob/master/LICENSE)
for more information.
