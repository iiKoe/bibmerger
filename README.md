#bibmerger

Small python script to
1. remove duplicate bib entries with the same ID (automatic)
2. remove duplicate bib entries with the same title (using A, B, or Skip)

## Dependencies
[bibtexparser](https://bibtexparser.readthedocs.io/en/master/install.html#how-to-install)

## Usage
Before using the script, concatenate all your bib files into one large bib file with duplicates.
Then run:
```
python bibmerger.py <your-bib-file.bib>
```

ID-based duplicates are removed automatically, and for the title-based duplicates, you have to manually choose which one to keep (or skip the choice).
In the end, a new file originally named `new-<your-bib-file.bib>` is created that hopefully has no more duplicate entries.

## Note
I only tested this on one (rather large) bib file of my own. If I missed anything, you could create a PR to help the next pour soul merge bib files.
