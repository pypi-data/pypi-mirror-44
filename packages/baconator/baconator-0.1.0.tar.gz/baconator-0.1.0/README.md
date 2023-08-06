# Baconator - Hollywood-themed random name generator

Baconator is like [Haikunator](https://github.com/Atrox/haikunatorpy)
(and [many other versions](https://www.google.com/search?q=haikunator)).
It generates easy to quote random names for stuff - files, jobs, servers - you name it 😉

### Why another Haikunator version?
To make this fun. Baconator random-pairs the first and last names of famous actors.
"Benicio Del Neeson" or "Keanu Ford" are more memorable and way cooler than "delicate haze".

### "Baconator"??
The name is a reference to the
[Six Degrees of Kevin Bacon](https://en.wikipedia.org/wiki/Six_Degrees_of_Kevin_Bacon)
game.
See if you can find the shortest path between the first and last name that Baconator generates 🤓

## Installation
```
pip install baconator
```

## Usage

```python
import baconator

baconator.generate()  # => Jake-Gooding-Jr-6425
baconator.generate('😀')  # => 'Harrison😀Brando😀9054'
baconator.generate(delimiter='+', token_len=2)  # => 'Patricia+Crystal+68'
```

It also installs a console script:
```bash
$ baconator
Charlize-Whitaker-7743
```
