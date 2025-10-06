# Heavyweight Translator

The heavyweight translator is a tool used to translate extremely large Microsoft Word documents. Word documents that are too large to process for either DeepL, ChatGPT, or another online translation tool are considered to be "extremely large". For example, an 800-page user manual containing hundreds of figures with an overall size of 70MB was the document which inspired this project. In late 2023, no online translation tool would allow uploading a document of such size for processing.

The heavyweight translator aims to circumvent such size limitations by extracting the plain text from the Word document, having it translated by the user (or later, via an API), and then swapping in the translated text at the correct locations. The user may use their online translator of choice, but DeepL is the translator that was used during development of this project.

The python docx library is used extensively to convert a Microsoft Word document into a mutable object which contains other mutable objects. Specifically, the docx library is used to access each paragraph and its runs for manipulation. This includes paragraphs inside of tables.


## Key features list
 - Enables translation without size limitations
 - Retains all paragraph-styled formatting that was present prior to translation
 - Consolidates broken runs (explained below)
 - Extracts paragraph-level text to get the best translations and re-applies run-level character formatting to the correct text regardless of word ordering


## Complications

Microsoft Word uses Open Office XML (OOXML) as a base markup language. Roughly speaking, a document contains pargraphs, and any present tables also contain pargraphs. Paragraphs are broken into runs which host plain text, applied character styling, and other attributes.

Word dictates the breaking of paragraphs into runs. Often this is done in a seemingly intuitive manner, but just as often the run breaks interrupt sentences or words in ways that make extraction of text at run level for the purposes of translation difficult. For example, Word breaks runs of German sentences on either side of special characters such as ä, ö, ü, and ß, often placing these characters in their own run. 

Extraction of text on a paragraph level is possible using the `python-docx` library, but all directly-applied character-level formatting will be lost after the translated text is swapped back into the paragraph. That is a current limitation of online translators in general: sometimes formatting is incompletely kept or lost altogether.

## How it works

The heavyweight translator is essentially a pre- and post-processor for the real work of translating sentences and sentence fragments in one or more batches. There are three major steps to translate a large document using the heavyweight translator:
1. Extract text
2. Translate text
3. Swap in translations

The heavyweight translator only performs the extraction and swapping steps. 

## Instructions

To translate a document using the heavyweight translator:
### Extract text
1. Clone the latest version of the repository to your local drive.
2. Set the initial parameters:
    * Save a copy of your .docx file in the `./private` folder.
    * Copy the name of the .docx file to the clipboard (without the file extension).
    * Open `input_parameters.py`.
    * Assign the file name to `source_document_file_name_without_extension`.
    * Set the creation date to today's date. For now, setting this manually is preferred.
    * Set the `target_language` and `target_culture` parameters. These can be freely named, but using ISO2 codes is advisable. In this example, `de-DE` will be translated to `en-UK`.
    * Save the changes to the `input_parameters.py` file.
3. Set the mode of execution to `EXTRACT`:
    * Open `main.py`.
    * Comment out the line containing `SWAP`.
    * Save the changes to the `main.py` file.
4. Run `main.py` to perform the extraction step.

### Translate text
1. Locate the results of the extraction and open the files.
    * Switch to the directory `./private/<today's date>__<source_document_file_name_without_extension>`.
    * Open `01__extracted_source_text_elements_de-DE.csv`, e.g. in Notepad++.
    * Open `02__translated_text_elements_en-UK.csv`.
2. Translate the text.
    * Copy the contents of `01__extracted_source_text_elements_de-DE.csv` and paste them into an online translator. Note that some online translators place limits on how much text can be translated. If the use case justifies it, consider purchasing a subscription.
    * Paste the resulting translations into `02__translated_text_elements_en-UK.csv`.
    * Check that the counts of lines in both .csv files match. If not, ensure that line feed characters or carriage return characters are not interfering. Sometimes the online translators can introduce unwanted extra lines or even unhandled characters.
    * Compare the source text to the translations by making spot checks. For example, pick certain line numbers to compare and make sure that the text of the line in the source file and translation file really correspond to each other. Often the online translator will cause some source-translation pairs to become offset from one another, and (for now) this has to be corrected manually. For this reason, it is advisible to translate only about 1000 lines at a time before comparing and correcting.
    * Save the changes to the `02__translated_text_elements_en-UK.py` file.

### Swap in translations
1. Set the mode of execution to `SWAP`:
    * Open `main.py`.
    * Uncomment the line containing `SWAP`.
    * Save the changes to the `main.py` file.
2. Run `main.py` to perform the swapping step for the first time.
3. Open the `./private/<today's date>__<source_document_file_name_without_extension>` directory.
4. Open the `./unparseables` folder. Here a collection of unparseable xml files can be found. During the translation step, the online translator introduced characters that broke the xml tagging that was applied to the paragraphs runs. Then heavyweight translator failed to parse the translations because they are no longer in valid xml format. If there are unparseable translations found, there are two options to repair them:
    * Extend the regex statements at the beginning of `preprocessing_operations.py` so that they repair any broken tags. This step is performed prior to xml-parsing of the translations, so the translations will first be repaired and then parsed.
    * Note that some dropped closing run tags may not be repairable using regex during the preprocessing step. This is because restoring missing closing tags via regex often adds superflous closing tags to markup that was already working, causing it to break. Rather, such repairs may be attempted just prior to parsing but only after a first attempt at parsing has failed.
    * Manually correct the individual broken tags in the `02__translated_text_elements_en-UK.py` file. The unparseable files should aid with this find-and-replace process. While these corrections may be tedious, the occurrence rate of the failures that lead to such corrections is currently less than 0.15%.
5. Run `main.py` to perform another interation of the swapping step. Repeat steps 3-5 until a satisfactory level of completion is reached.
6. Open the new Word document in `./private/<today's date>__<source_document_file_name_without_extension>`.
7. The language of the document must be set manually to the target larguage (for now). Be sure to select the option which applies the language to the whole document.
8. Update the table of contents and any other dynamically generated collections of fields (if applicable). For now, the header, footer, and cover page will have to be translated manually during this step.
9. Save the Word document and optionally rename it so the file name is in the target language.