# fraise

A Python module for generating `correct horse battery staple` like random pass phrases.

## Installation

```bash
pip install fraise
```

## Usage
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
