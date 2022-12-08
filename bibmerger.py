import sys
import json

import bibtexparser
from bibtexparser.bwriter import BibTexWriter
from bibtexparser.bparser import BibTexParser

UserInput = True

if len(sys.argv) <= 1:
    print('Provide bib file as argument')
    sys.exit(0)

bibfile = sys.argv[1]
bibfile_out = 'new-'+bibfile

print('Merging references in:', bibfile)
print('Output bib:', bibfile_out)

parser = BibTexParser()
parser.ignore_nonstandard_types = False

with open(bibfile) as bibtex_file:
    bib_database = bibtexparser.load(bibtex_file, parser)

#print(bib_database.entries)

def title_strip(t):
    t = t.replace('{', '')
    t = t.replace('}', '')
    t = t.replace('\\', '')
    t = t.replace(',', '')
    t = t.replace('.', '')
    t = t.replace(' ', '')

    return t

def compare(entry_a, entry_b):
    try:
        title_entry_a = entry_a['title']
    except:
        print('Entry does not have a title:', entry_a)
        sys.exit(0)

    try:
        title_entry_b = entry_b['title']
    except:
        print('Entry does not have a title:', entry_b)
        sys.exit(0)


    # Strip the titles
    return title_strip(title_entry_a) == title_strip(title_entry_b)

def print_entry(entry):
    print('ID:', entry['ID'], 'Title:', entry['title'])

def print_entry_long(entry):
    print(json.dumps(entry, indent=2, default=str))


# Remove duplicates with the same ID
Duplicates = []
print('')
print('Searching for duplicate IDs')
ids = set()
for entry in bib_database.entries:
    e_id = entry['ID']
    if e_id in ids:
        print('##################################')
        print('Duplicate entry ID:', e_id)
        print_entry(entry)
        Duplicates.append(entry)

    ids.add(entry['ID'])

print('')
print('=================================')
print('Duplicate IDs:')
for dup in Duplicates:
    print_entry(dup)

# Remove the duplicate IDs
for dup in Duplicates:
    bib_database.entries.remove(dup)


# Remove duplicates with another ID
Duplicates = []
print('')
print('Searching for duplicate entries')
for entry in bib_database.entries:
    for entry_b in bib_database.entries:
        if entry_b in Duplicates:
            continue
        if entry in Duplicates:
            continue
        if entry['ID'] == entry_b['ID']:
            continue

        if compare(entry, entry_b) == True:
            print('##################################')
            print('')
            print('=> A')
            print_entry_long(entry)

            print('')
            print('=> B')
            print_entry_long(entry_b)

            if UserInput == True:
                while True:
                    print('')
                    keep = input('Select the entry to keep, A or B or S (skip)\n')
                    if keep == 'A' or keep == 'a':
                        dupe_entry = entry_b
                        break
                    elif keep == 'B' or keep == 'b':
                        dupe_entry = entry
                        break
                    elif keep == 'S' or keep == 's':
                        dupe_entry = None
                        break
                    else:
                        print('Invalid choice:', keep)

            else:
                dupe_entry = entry_b

            # Mark the duplicate
            if dupe_entry != None:
                Duplicates.append(dupe_entry)

# Print the duplicates
print('')
print('=================================')
print('Duplicate entries:')
for dup in Duplicates:
    print_entry(dup)

# Remove the duplicate entries
for dup in Duplicates:
    bib_database.entries.remove(dup)

# Save the new bibfile
writer = BibTexWriter()
writer.indent = '    '
with open(bibfile_out, 'w') as bibtex_out:
    bibtexparser.dump(bib_database, bibtex_out, writer=writer)


