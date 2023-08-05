# pycsoap

## example

```
from ase.io import read
from pycsoap.soaplite import SOAP

gb1 =read('/Users/andrewhuynguyen/Desktop/gb0011039001.xyz')
soap_desc = SOAP(atomic_numbers=[26], rcut=5, nmax=9, lmax=9)
input_soap=soap_desc.create(gb1)
input_soap
```


`input_soap` will return a matrix MxN (M is the number of atoms in the cell and N is based on rcut, nmax, and lmax).

