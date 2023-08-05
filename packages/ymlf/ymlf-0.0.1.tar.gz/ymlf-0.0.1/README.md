# ymlf

Command-line tool that parses **YAML** from `stdin` and writes the parsed
**YAML**, or a subset thereof, to `stdout`.

## Install

Install `ymlf` system-wide via the pip:

```bash
sudo pip install ymlf
```

Or install it at user-level via the pip:

```bash
pip install ymlf
```

**NOTE:** When doing user-level install, then include the `pip` binary install
path in your `PATH` definition. For example `PATH="$PATH:$HOME/.local/bin"`

## Usage

Pipe a **YAML** file to `ymlf` and it will echo it back without comments, e.g.:

```bash
ymlf < samples/nvm_dev_info.yml
```

Yields:

```bash
dev_attr:
  bbts_cached: 0
  be_id: 1
  be_name: NVM_BE_IOCTL
  fd: 3
  mccap: '00000000000000000000000000000001'
  name: nvme0n1
  path: /dev/nvme0n1
  quirks: '00000101'
  ssw: 12
  verid: 2
dev_cmd_opts:
  addr: VECTOR
  iomd: SYNC
  mask: '00000000000000000000000110010000'
  plod: PRP
dev_geo:
  nbytes: 4096
  nbytes_oob: 16
  nchunk: 1474
  npugrp: 8
  npunit: 4
  nsectr: 6144
  tbytes: 1187021586432
  tmbytes: 1132032
  verid: 2
dev_lbaf:
  chunk: 11
  pugrp: 3
  punit: 2
  sectr: 13
dev_lbam:
  chunk: '0000000000000000000000000000000000000000111111111110000000000000'
  pugrp: '0000000000000000000000000000000000011100000000000000000000000000'
  punit: '0000000000000000000000000000000000000011000000000000000000000000'
  sectr: '0000000000000000000000000000000000000000000000000001111111111111'
dev_lbaz:
  chunk: 13
  pugrp: 26
  punit: 24
  sectr: 0
dev_ppaf: null
dev_ppaf_mask: null
dev_vblk_opts:
  erase_naddrs_max: 64
  meta_mode: 0
  pmode: SNGL
  read_naddrs_max: 64
  write_naddrs_max: 64
```

Pipe a **YAML** file to `ymlf` and provide an attribute filter, and it will echo
only a subset of the parsed **YAML** back, e.g.:

```bash
ymlf dev_geo < samples/nvm_dev_info.yml
```

Yields:

```yaml
nbytes: 4096
nbytes_oob: 16
nchunk: 1474
npugrp: 8
npunit: 4
nsectr: 6144
tbytes: 1187021586432
tmbytes: 1132032
verid: 2
```

So, if you are looking for that one specific attribute, e.g. `dev_geo.npugrp`,
then you can filter it by invoking:

```bash
ymlf dev_geo.npugrp < samples/nvm_dev_info.yml
```

Yielding:

```yaml
8
```

## Error Handling

When **YAML** is parsed and filtered successfully then `ymlf` has exit code 0.
On error, exit-code is non-zero and a **YAML** comment is output. For example,
when attempting to get non-existing attribute `dev_geo.foo`:

```bash
ymlf < samples/nvm_dev_info.yml dev_geo.foo
```

Then exit code is 1, and the following will be written to `stdout`:

```yaml
# invalid attr: 'dev_geo.foo'
```
