# fraise

A Python module for generating `correct horse battery staple` like random passphrases.

## Installation

```bash
pip install fraise
```

## Usage

### As an application

```bash
$ fraise --help
```

```
usage: fraise [-h] [--max-word-length MAX_WORD_LENGTH]
              [--minimum-length MINIMUM_LENGTH] [--separator SEPARATOR]
              [--word-count WORD_COUNT]

Generate memorable passphrases

optional arguments:
  -h, --help            show this help message and exit
  --max-word-length MAX_WORD_LENGTH
                        The maximum length of each word (default 8)
  --minimum-length MINIMUM_LENGTH
                        Minimum length of the phrase (default 16)
  --separator SEPARATOR
                        What to put inbetween the words (default space)
  --word-count WORD_COUNT
                        How many words to include in the phrase (default 4)

```

### As a library

```python
>>> import fraise

# By default, generate will return four lowercase words
>>> fraise.generate()
'luck unrewarded ghosts accumulation'

# Set the number of words
>>> fraise.generate(word_count=8)
'broadband hansom heaving inroad flyweight shopping abets realty'

# Require a passphrase of at least n character
>>> fraise.generate(minimum_length=32)
'virile pullets resuming worst unengaged phosphates'

# Change the separation character
>>> fraise.generate(separator='-')
'readers-reapply-bossiest-bylaw'

# Only use words of n characters or less
>>> fraise.generate(max_word_length=4)
'duct pond anon four'
```

## Contributing

Please fork the repository and raise a pull request (PR). PRs require one approval in order to be merged into the master branch.

Issue tracking is maintained on a public [Trello board](https://trello.com/b/ZiTGwaif/fraise). Please contact the repo owner if you would like access to the board. Commits should be prefixed with the Trello card ref, for example "FR-100 Did the thing". A link to the PR should be added to the card.

### Initial setup

```bash
make init
```

### Testing

```bash
make test
```

### Building

```bash
make build
```

_Tests will be run first and the directory cleaned._

### Releasing

```bash
make release
```
