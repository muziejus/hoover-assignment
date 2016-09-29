# What I did

## Moacir P. de Sá Pereira

The assignment:

> Download Henry James’s “Four Meetings” from these two sources:

> Gutenberg: http://www.gutenberg.org/files/21773/21773-0.txt

> SUNY New Palz: http://www2.newpaltz.edu/~hathawar/fourmeetings.html

> Evaluate the texts and edit them in any way that seems appropriate. Record briefly what you did to prepare them, and discuss briefly any peculiarities, difficulties, questions, significant decisions, interesting characteristics, that you find. Save the texts as Plain Text files and add them to the Intelligent Archive. Now create word frequency lists for them.

* Copied (not saved as...) the texts from the browser into two text files, `four_meetings_suny.txt` and `four_meetings_gutenberg.txt`.

* In so doing, I also stripped out the metadata.

* The first peculiarity:

  ```
  > wc *.txt
  1270   10014   56496 four_meetings_gutenberg.txt
   560   11817   65863 four_meetings_suny.txt
  ```

* The gutenberg version has linebreaks, so if anything it should be “longer,”
  but the suny version is almost 10k characters longer. I look at the last
  paragraph and note that the gutenberg version begins “I detained Caroline
  Spencer as, after looking a moment in silence at the little table…” The suny
  version begins “I detained that lady as, after considering a moment in silence
  the small array…” The point is the texts are clearly different, possibly
  enough to explain the discrepancies in length.

* I feed the texts into nltk and tokenize them using `word_tokenize`, giving a
  dictionary, `c`, with a key corresponding to the version and a value of
  the tokens.

* How many tokens to we have:
    
  ```
  >>> [print("{0}: {1}".format(k, len(c[k]))) for k in c]
  suny: 14939
  gutenberg: 11852
  ```

* The suny version is longer, in that it has more tokens
  than the gutenberg version, but the comparison between nltk and wc is also
  notable. `wc` counted 84% as many words in the gutenberg version as nltk, but
  only 79% of the words found in the suny version. 

* I suspect this may be because of the underscores?
    
  ```
  >>> len([token for token in c['suny'] if "_" in token])
  54
  ```

* In a word, no. There are only 54 tokens with underscores in them (and “_” is
  not one of them)

* On the other hand, simple punctuation (.,?!) makes up about 1500 tokens in
  the suny text, which still does not account for the discrepancy. What if I
  use the WhitespaceTokenizer instead?

  ```
  >>> [print("{0}: {1}".format(k, len(ws[k]))) for k in ws]
  suny: 11817
  gutenberg: 10013
  ```

  Results in line with `wc`!

* Now to build the frequency tables. Let’s see how many unique tokens there are:

  ```
  >>> [print("{0}: {1}".format(k, len(set(c[k])))) for k in c]
  suny: 2584
  gutenberg: 2166

  >>> [print("{0}: {1}".format(k, len(set(ws[k])))) for k in ws]
  suny: 3585
  gutenberg: 2820
  ```

  Unsuprisingly, the whitespace tokenizer finds many more tokens. For example:

  ```
  >>> set([token for token in ws['suny'] if "about" in token])
  {'about', 'about,', 'about."', 'about?"', 'about:'}
  >>> set([token for token in c['suny'] if "about" in token])
  {'about'}
  ```

* Next, lets add the two versions (per tokenizer) and see how many unique tokens there are:

  ```
  >>> cs = c['suny'] + c['gutenberg']
  >>> wss = ws['suny'] + ws['gutenberg']
  >>> len(set(cs))
  3111
  >>> len(set(wss))
  4601
  ```

  This suggests that the suny and gutenberg versions are very, very different,
  with literally hundreds of words appearing in one version but not the other.

* One more addition to get the total number of distinct tokens, against which I can match each separate version’s frequency distribution:

  ```
  >>> total_tokens = set(cs + wss)
  >>> len(total_tokens)
  5331
  ```

* Create each frequency distribution:

  ```
  >>> c_suny_fd = FreqDist(c['suny'])
  >>> c_gutenberg_fd = FreqDist(c['gutenberg'])
  >>> ws_suny_fd = FreqDist(ws['suny'])
  >>> ws_gutenberg_fd = FreqDist(ws['gutenberg'])
  ```

* Look at the distributions, and a problem immediately arises:

  ```
  >>> c_suny_fd
  FreqDist({'.': 691, ',': 646, 'I': 506, 'the': 466, "''": 369, '``': 358, 'to': 317, 'of': 310, 'a': 297, 'and': 281, ...})
  >>> c_gutenberg_fd
  FreqDist({',': 726, '.': 519, 'I': 396, 'the': 371, 'a': 271, 'to': 248, 'and': 228, 'her': 219, '”': 212, 'of': 212, ...})
  ```

  The tokenizer stripped out the ” quote from the gutenberg version but not
  leading “ (there are 0 instances of such a token), meaning the tokenizer is
  not smart-quote aware. The suny version, presented without smart quotes, had
  the quotes changed to their TeX-style counterparts, but imperfectly, because
  there are 11 more close-quotes than open-quotes (it should be the other way
  around). Some testing indicates that the tokenizer is… inconsistent with
  smart quotes. This means pre-processing for the gutenberg version, to replace
  smart quotes with dumb.

  * The new list of unique tokens is 5022.

  ```
  >>> c_suny_fd
  FreqDist({'.': 691, ',': 646, 'I': 506, 'the': 466, "''": 369, '``': 358, 'to': 317, 'of': 310, 'a': 297, 'and': 281, ...})
  >>> c_gutenberg_fd
  FreqDist({',': 726, '.': 647, 'I': 468, 'the': 371, "''": 358, '``': 336, 'a': 271, 'to': 252, 'and': 228, 'her': 220, ...})
  ```

  This feels more like it, though the discrepancy between open and close quotes is still unclear.

* Dump everything to a naive csv, with “|” as the text delimiter.

  ```
  >>> f = open('word_frequencies.csv', 'w')
  >>> f.write("Word, suny_c, gutenberg_c, suny_ws, gutenberg_ws, total\n")
  >>> for token in total_tokens:
  ...    f.write("|{0}|, |{1}|, |{2}|, |{3}|, |{4}|\n".format(token, c_suny_fd[token], c_gutenberg_fd[token], ws_suny_fd[token], ws_gutenberg_fd[token]))
  >>> f.close
  ```
