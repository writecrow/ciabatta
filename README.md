# ciabatta
Corpus In A Box: Automated Tools, Tutorials, &amp; Advising

## Download the latest release
Download the latest release at https://github.com/writecrow/corpus_text_processor/releases
The tool does not come with an installer. Instead, just save the .exe file to your Desktop. You can run it from there. 

## Create a new top level folder
Before running the tool, it is recommended that you create a new top level folder to save your processed files to. You can create that folder at the same level of the top level parent directory for the files you wish to process. You don’t need to recreate the subdirectory structure because the Crow corpus processing tool will do this for you. 

## Run the tool
To run the tool, choose the folder that you want to process (below, “Original”) and your output folder to save the processed data to (below, “Converted”). You can only process a folder, not individual files. If you have multiple subdirectories to convert, just choose the parent directory. The Crow corpus processing tool will process all the subdirectories and recreate the directory structure in the output folder. DO NOT select the same folder to read and write the files. 

File types that are supported include .pdf, .doc, .docx., .html, and .pptx.

IMAGE TO BE INSERTED

## Process folders

Run each processor separately, and create a new folder for each process (converted, standardized, normalized, for example). We recommend running the processes in the order in which they are listed (Convert to plaintext, Standardize to UTF-8 encoding, Normalize characters). In fact, it should be noted that the "Normalize characters" process is designed only to work with files already in UTF-8 format. The only exception to this is that you do not generally need to run the “remove PDF metadata” process. We use this for de-identifying files that will go into the repository as PDFs as well as plain text.


