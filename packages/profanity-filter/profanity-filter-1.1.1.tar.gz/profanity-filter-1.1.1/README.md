# profanity-filter: A Python library for detecting and filtering profanity
[![License](https://img.shields.io/pypi/l/profanity-filter.svg)](https://www.gnu.org/licenses/gpl-3.0.en.html)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/profanity-filter.svg)
[![PyPI](https://img.shields.io/pypi/v/profanity-filter.svg)](https://pypi.org/project/profanity-filter/)

## Table of contents
<!--ts-->
   * [profanity-filter: A Python library for detecting and filtering profanity](#profanity-filter-a-python-library-for-detecting-and-filtering-profanity)
      * [Table of contents](#table-of-contents)
      * [Installation](#installation)
      * [Usage](#usage)
      * [Deep analysis](#deep-analysis)
      * [Multilingual support](#multilingual-support)
         * [Add language](#add-language)
            * [Russian language support](#russian-language-support)
               * [Pymorphy2](#pymorphy2)
         * [Usage](#usage-1)
      * [Using as a part of Spacy pipeline](#using-as-a-part-of-spacy-pipeline)
      * [Console Executable](#console-executable)
      * [Troubleshooting](#troubleshooting)
      * [Credits](#credits)

<!-- Added by: rominf, at: Ср мар 27 10:10:32 MSK 2019 -->

<!--te-->

## Installation
`profanity-filter` library is universal, it can detect and filter profanity in any language.
To accomplish this task it needs profane word dictionaries and language tools with models installed.
`profanity-filter` is already packaged with English and Russian profane word dictionaries.

For minimal setup for English you need to install `profanity-filter` with is bundled with `spacy` and download `spacy`
model for tokenization and lemmatization:
```
$ pip install profanity-filter
$ python -m spacy download en
```

For more info about `spacy` models read: https://spacy.io/usage/models/.

## Usage

```python
from profanity_filter import ProfanityFilter

pf = ProfanityFilter()

pf.censor("That's bullshit!")
# "That's ********!"

pf.censor_char = '@'
pf.censor("That's bullshit!")
# "That's @@@@@@@@!"

pf.censor_char = '*'
pf.custom_profane_word_dictionaries = {'en': {'love', 'dog'}}
pf.censor("I love dogs and penguins!")
# "I **** **** and penguins"

pf.restore_profane_word_dictionaries()
pf.is_clean("That's awesome!")
# True

pf.is_clean("That's bullshit!")
# False

pf.is_profane("That's bullshit!")
# True

pf.extra_profane_word_dictionaries = {'en': {'chocolate', 'orange'}}
pf.censor("Fuck orange chocolates")
# "**** ****** **********"
```

## Deep analysis
Deep analysis detects profane words that are inflected from profane words in profane word dictionary.

To get deep analysis functionality install additional libraries and dictionary for your language.

Firstly, install `hunspell` and `hunspell-devel` packages with your system package manager.

For Amazon Linux AMI run:
```shell
$ sudo yum install hunspell
```

For openSUSE run:
```shell
$ sudo zypper install hunspell hunspell-devel
```

Then run (for English):
```shell
$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-deep-analysis.txt
$ cd profanity_filter/data
$ wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.aff
$ wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/en/en_US.dic
$ mv en_US.aff en.aff
$ mv en_US.dic en.dic
```

Then use profanity filter as usual:
```python
from profanity_filter import ProfanityFilter

pf = ProfanityFilter()

pf.censor("fuckfuck")
# "********"

pf.censor_whole_words = False
pf.censor("oofucksoo")
# "oo*****oo"
```

## Multilingual support
This library comes with multilingual support, which is enabled automatically after installing `polyglot` package and 
it's requirements for language detection. See https://polyglot.readthedocs.io/en/latest/Installation.html for 
instructions.

For Amazon Linux AMI run:
```shell
$ sudo yum install libicu-devel
```

For openSUSE run:
```shell
$ sudo zypper install libicu-devel
```

Then run:
```shell
$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-multilingual.txt
```

### Add language
Let's take Russian language for example, to show how to add language support.

#### Russian language support
Firstly, we need to provide file `profanity_filter/data/ru_badwords.txt` which contains newline separated list of profane
words. For Russian language it's already present, so we skip file generation.

Next, we need to download appropriate Spacy model. Unfortunately, Spacy model for Russian is not yet ready, 
so we will use English model for tokenization and `hunspell` and `pymorphy2` for lemmatization.

Next, we download dictionaries for deep analysis:
```shell
> cd profanity_filter/data
> wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/ru_RU/ru_RU.aff
> wget https://cgit.freedesktop.org/libreoffice/dictionaries/plain/ru_RU/ru_RU.dic
> mv ru_RU.aff ru.aff
> mv ru_RU.dic ru.dic
```

##### Pymorphy2
For Russian and Ukrainian languages to achieve better results we suggest you to install `pymorphy2`.
To install `pymorphy2` with Russian dictionary run:
```shell
$ pip install -U -r https://raw.githubusercontent.com/rominf/profanity-filter/master/requirements-pymorphy2-ru.txt
```

### Usage
Let's create `ProfanityFilter` to filter Russian and English profanity. 
```python
from profanity_filter import ProfanityFilter

pf = ProfanityFilter(languages=['ru', 'en'])

pf.censor("Да бля, это просто shit какой-то!")
# "Да ***, это просто **** какой-то!"
```

Note, that order of languages in `languages` argument does matter. If a language tool (profane words list, Spacy model, 
HunSpell dictionary or pymorphy2 dictionary) is not found for a language that was detected for part of text, 
`profanity-filter` library automatically fallbacks to the first suitable language in `languages`.

As a consequence, if you want to filter just Russian profanity, you still need to specify some other language in 
`languages` argument to fallback on for loading Spacy model to perform tokenization, because, as noted before, there is 
no Spacy model for Russian.

## Using as a part of Spacy pipeline
You can use `profanity-filter` library as a part of Spacy pipeline. Here is the example:
```python
import spacy
from profanity_filter import ProfanityFilter

nlp = spacy.load('en')
profanity_filter = ProfanityFilter(nlps={'en': nlp})  # reuse spacy Language (optional)
nlp.add_pipe(profanity_filter.spacy_component, last=True)

doc = nlp('This is shiiit!')

doc._.is_profane
# True

doc[:2]._.is_profane
# False

for token in doc:
    print(f'{token}: '
          f'censored={token._.censored}, '
          f'is_profane={token._.is_profane}, '
          f'original_profane_word={token._.original_profane_word}'
    )
# This: censored=This, is_profane=False, original_profane_word=None
# is: censored=is, is_profane=False, original_profane_word=None
# shiiit: censored=******, is_profane=True, original_profane_word=shit
# !: censored=!, is_profane=False, original_profane_word=None
```

## Console Executable

```bash
$ profanity_filter -h
usage: profanity_filter [-h] [-t TEXT | -f PATH] [-l LANGUAGES] [-o OUTPUT_FILE] [--show]

Profanity filter console utility

optional arguments:
  -h, --help            show this help message and exit
  -t TEXT, --text TEXT  Test the given text for profanity
  -f PATH, --file PATH  Test the given file for profanity
  -l LANGUAGES, --languages LANGUAGES
                        Test for profanity using specified languages (comma
                        separated)
  -o OUTPUT_FILE, --output OUTPUT_FILE
                        Write the censored output to a file
  --show                Print the censored text
```

## Troubleshooting
You can always check will deep, morphological, and multilingual analyses work by inspecting the value of corresponding
variables. If everything is set up correctly you will see following:
```python
from profanity_filter import DEEP_ANALYSIS_AVAILABLE, MORPHOLOGICAL_ANALYSIS_AVAILABLE, MULTILINGUAL_ANALYSIS_AVAILABLE

print(DEEP_ANALYSIS_AVAILABLE)
# True

print(MORPHOLOGICAL_ANALYSIS_AVAILABLE)
# True

print(MULTILINGUAL_ANALYSIS_AVAILABLE)
# True
```

If some of variables are not `True`, you can import dependencies yourself to see the import exceptions:
```python
from profanity_filter.analysis.deep import *
from profanity_filter.analysis.morphological import *
from profanity_filter.analysis.multilingual import *
```

## Credits
English profane word dictionary: https://github.com/areebbeigh/profanityfilter/ (author Areeb Beigh).

Russian profane word dictionary: https://github.com/PixxxeL/djantimat (author Ivan Sergeev).
