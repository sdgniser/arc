**What is this?**

This folder contains lists of adjectives and nouns to be used for generating filenames for the uploaded files.

**How are the file names generated?**

The file names have the following pattern: &lt;adjective&gt;&lt;adjective&gt;&lt;noun&gt;.
`genURL` randomly selects two adjective and a noun from the _listed_ files, and returns the file name. It performs no checks as to whether the file already exists.

**What are these files?**

These files contain the adjectives and the nouns.

 * `3la` : list of 3-letter adjectives taken from [wordmom.com](https://www.wordmom.com/).
 * `3ln` : list of 3-letter nouns taken from wordmom.com.
 * `4la` : list of 4-letter adjectives taken from wordmom.com.
 * `4ln` : list of 4-letter nouns taken from wordmom.com.
 * `ma34` : list of 3- and 4-letter adjectives extracted from the monsterurl project
 * `mm34` : list of 3- and 4-letter names of monsters extracted from the the monsterurl project
 * `wiki-animals-34` : list of names of animals extracted from ["List of Animal Names" - Wikipedia](https://en.wikipedia.org/wiki/List_of_animal_names)
 * `simple-adj` : a list _commonly used_ 3- and 4-letter adjectives extracted from [https://gist.github.com/ijmacdowell/8325491#file-adjectives-js](https://gist.github.com/ijmacdowell/8325491#file-adjectives-js)
