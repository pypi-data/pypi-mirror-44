git-word-blame
-------

Show word-by-word authors of a file

<!--
# Demo

[![screenshot](link-to-screenshot)](link_to_demo.html)
-->

## Installation

```
pip install git-word-blame
```


## Usage

```
git word-blame <path/to/my/file>
```

It will produce the following files:

```
- authors_stats.tsv         # top authors by number of characters attributed to them
- commit_stats.tsv          # same for commits
- word-blame-by-commit.html # hover on some text to see wich commit created it
- word-blame-by-author.html # same for authors
```


## Authorship algorithms

Two algorithms are available:

  - `wikiwho` (**default**): coarse but more robust
  - `mwpersistence`: precise but with more false-positives

To change the engine used by `git word-blame`:

```
git config --global word-blame.engine mwpersistence
```


## Themes

You can choose between 3 themes for the HTML output: `black-and-white`, `solarized-dark`, `solarized-light`.

```
git config --global word-blame.theme solarized-dark
```

<!-- screenshots/themes.png -->


## Limits

`git-word-blame` doesn't support **renames** for now and is only tested on files with a linear history.

There's also a default maxmum of `2000` commits processed. This can be removed with this command: `git config --global word-blame.limit 0`.


## See also

 - https://github.com/wikiwho/WikiWho/ and https://github.com/wikiwho/WhoColor
   A word-by-word blame for Wikipedia with a well tested algorithm for prose (default algorithm)
   The HTML vizualisation of this project is heavily inspired by WhoColor

 - https://github.com/mediawiki-utilities/python-mwpersistence/
   An alternative authorship algorithm detection made also for Wikipedia

 - https://github.com/d33tah/wordblame
   Export Wikipedia articles to git to perform a word-by-word blame, it does that by
   putting each word in a separate line for each file in the history

 - https://github.com/lucadealfaro/authorship-tracking
   Another altenative not yet integrated
