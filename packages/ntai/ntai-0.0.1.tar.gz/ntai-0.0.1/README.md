# ntai
ntai stands for nucleotide (nt) artificial intelligence (A.I.). ntai is a small
python library for using fasta sequences with artificial intelligence (A.I.).

Currently there are two main modules that will be of use

1. `Codex`, and
2. `bedtools`

## Codex
`Codex` is a class for hot-encoding fasta sequences into channels and back.
`Codex` is useful because a character in a fasta sequences can encode multiple
nucleotides or even random repeats.

## bedtools

`bedtools` is a function exposing the `bedtools` library to python. This allows
users to extract fasta sequences from a reference genome with writing to /
reading from files.


[bedtools]: https://bedtools.readthedocs.io/en/latest/
