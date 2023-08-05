# vasptools
tools for vasp

[![Build Status](https://travis-ci.org/atomse/vasptools.svg?branch=master)](https://travis-ci.org/atomse/vasptools)
[![PyPI](https://img.shields.io/pypi/v/vasptools.svg?color=blue&label=vasptools)](https://pypi.org/project/vasptools)

## Installation
```python
pip install vasptools
```

## CLI mode
```bash
$ vasptools -h
usage: vasptools [-h] [-p] [-ppath PATH] [-t] [-td PATH] [-s] [-D] [-V]
                 subcommand ...

VASPTOOLS

positional arguments:
  subcommand
    potcar              POTCAR
    incar               INCAR
    LISTSUBCOMMAND      list all sub commands, just for test

optional arguments:
  -h, --help            show this help message and exit
  -p, --preview         preview
  -ppath PATH, --potpath PATH
                        set vasppot_path, you could also set env VASPPOT
  -t, --test            run test
  -td PATH, --test_dir PATH
                        test_dir
  -s, --shell           shell mode, exec shell script
  -D, --DEBUG           debug
  -V                    show program's version number and exit
$ vasptools potcar -h
usage: vasptools potcar [-h] [-i PATH] [-d PATH] [-p PTYPE] [-l]
                        [pp_names [pp_names ...]]

positional arguments:
  pp_names

optional arguments:
  -h, --help            show this help message and exit
  -i PATH, --input PATH
                        Generate POTCAR with POSCAR
  -d PATH, --dirname PATH
                        directory to generate file
  -p PTYPE, --ptype PTYPE
                        potcar type, avail: ['potcar', 'potcarGGA', 'potpaw',
                        'potpaw_GGA', 'potpaw_PBE']
  -l, --list            list available potcar

```

## POSCAR
```python
>>> from vasptools import potcar
>>> potcar.get_potcar_content(pp_names=['H', 'He', 'Li', pp_type='potpaw_PBE')
' PAW_PBE H 15Jun2001\n 1.00000000000000000\n parameters from PSCTR are:\n   VRHFIN =H: ultrasoft test\n '
>>> potcar.gen_potcar(pp_names=['H'], pp_type='potpaw_PBE')

```

## INCAR
```python
>>> from vasptools import incar
>>> incar_dict = incar.parse_incar(incarfile)
>>> print(incar_dict)
OrderedDict([('system', 'si series'), ('prec', 'accurate'), ('encut', '245.345'), ('ibrion', '-1'), ('nsw', '0'), ('nelmin', '2'), ('ediff', '1.0e-05'), ('ediffg', '-0.02'), ('voskown', '1'), ('nblock', '1'), ('lvtot', '.true.'), ('nelm', '60'), ('algo', 'fast   (blocked davidson)'), ('gga', 'pe'), ('ispin', '1'), ('iniwav', '1'), ('istart', '0'), ('icharg', '2'), ('lwave', '.false.'), ('lcharg', '.true.'), ('addgrid', '.false.'), ('lhyperfine', '.false.'), ('ismear', '0'), ('sigma', '0.2'), ('rwigs', '1.11')])
>>> print(output_incar(incar_dict))
system = si series
prec = accurate
encut = 245.345
ibrion = -1
nsw = 0
nelmin = 2
```



## TODO
- [x] INCAR
- [ ] POSCAR
- [ ] KPOINTS
- [ ] OUTCAR
- [ ] DOSCAR
- [ ] CHGCAR
- [ ] CHG
- [ ] WAVECAR

...

