# Heavyweight Translator

The heavyweight translator is a tool used to translate extremely large Microsoft Word documents. Word documents that are too large to process for either DeepL, ChatGPT, or another online translation tool are considered to be "extremely large". For example, an 800-page user manual containing hundreds of figures with an overall size of 70MB was the document which inspired this project in the first place. In late 2023, no online translation tool would even allow uploading a document of such size.

The heavyweight translator aims to circumvent such size limitations by extracting the plain text from the Word document, having it translated by the user (or later, via an API), and then swapping in the translated text at the correct locations. The user may use their online translator of choice, but DeepL is the translator that was used during development of this project.

The python docx library is used extensively to convert a Microsoft Word document into a mutable object which contains other mutable objects. Specifically, the docx library is used to access each paragraph and its runs for manipulation.


## Key features list
 - Enables translation without size limitations
 - Retains all paragraph-styled formatting that was present prior to translation
 - Consolidates broken runs (explained below)
 - Extracts paragraph-level text to get the best translations and re-applies run-level character formatting to the correct text regardless of word ordering


## Complications

Microsoft Word uses Open Office XML (OOXML) as a base markup language. Roughly speaking, a document contains pargraphs which contain runs, any present tables also contain pargraphs. Paragraphs are broken into runs which host plain text, applied character styling, and other attributes.

Word dictates the breaking of paragraphs into runs. Often this is done in a seemingly intuitive manner, but just as often the run breaks interrupt sentences or words in ways that make extraction of text at run level for the purposes of translation difficult. For example, Word breaks runs of German sentences on either side of special characters such as ä, ö, ü, and ß, often placing these characters in their own run. 

Extraction of text on a paragraph level is possible using the python docx library, but all character-level formatting will be lost after the translated text is swapped back into the paragraph. That is a current limitation of online translators in general: sometimes formatting is incompletely kept or lost altogether.
