## Settings Variables

In `'settings.py'` the following variables are defined:


### `REPEAT_CHAR`
Because repeated masked regions are indicated by lower case nucleotides, to know what channel to encode repeats in the unique character `REPEAT_CHAR` is used.

`REPEAT_CHAR` defaults to `'.'`


### `FASTA_CHARS`
The set of valid fasta characters which can be used for sequence validation. Only lowercase letters are used. So make sure to test via:

`char.lower() in FASTA_CHARS`

### `ENCODE_ORDER`
The channel order used in the encoding.
Defaults to `['a', 'c', 't', 'g', 'u']`

### `INCLUDE_URACIL`
Whether or not uracil should be included in the encoding.
Defaults to `False`

### `INCLUDE_REPEAT`
Whether or not repeated masked regions should be included in the encoding. If `True` it is expected that `REPEAT_CHAR` appears in the `ENCODE_ORDER`.
Defaults to `False`

### `FASTA_ENCODEX`
The dictionary mapping a fasta character to its corresponding nucleotide(s).

`FASTA_ENCODEX` takes a fasta character and returns all the nucleotides it indicates as the FASTA format is defined. Repeated masked regions (lower case) are treated the same as normal nucleotides, as repeats are handled as their own
channel (see `INCLUDE_REPEAT`)

### `FASTA_DECODEX`
The dictionary mapping (a) nucleotide(s) to its/their
corresponding fasta character.
