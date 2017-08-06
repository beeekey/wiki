# wiki
In this repo, I'm publishing all my scripts, I use to work with my MediaWiki Installation

So far, there is only one here:

## html2wiki.py
This script is not a beauty yet, but I don't have more time right now to invest in it.

Basically, this converts a given html-page, which has to be saved as "source.html" direct in the main directory to a HTML, which my Wiki can read.

It replaces all links with tags, that the wiki can read an display right.

It also downloads all files, which are linked to (all images and pdfs) and sets a link to the wiki. After you uploaded all these files, you can directly access them from your wiki.
The original links will remain in the code, the internal are only added.

The converted HTML is then saved as "source_edited.html" in the main directory, as all downloaded files (chaotic, sorry)

### Prerequisitions
* BeautifulSoup
* lxml
* urllib