from bs4 import BeautifulSoup, NavigableString
import lxml
import urllib
import random

def read_html_from_locfile(filename):
    """ reads in a local html file"""
    file_to_read = open(filename, 'r')
    content = file_to_read.read()
    return content


def local_txt_to_soup(content):
    """ converts txt-html to bs4"""
    soup = BeautifulSoup(content, 'html.parser')
    soup = soup.find('body')

    # extracting scripts and styles
    for elem in soup.findAll(['script', 'style', 'noscript']):
        elem.extract()


    return soup


def handle_links(soup):
    """ extracts all links and converts them to wiki tags
    does this with images also, to link to these external sources """

    file_extensions_to_download = ['.jpg', '.jpeg', '.gif', '.png', '.bmp', '.pdf']

    links = soup.findAll('a')
    for link in links:
        # soup.find('a', text=link.text).replaceWith('[' + link['href'] + ' ' + link.text + ']')

        has_ext = False
        for ext in file_extensions_to_download:
            if ext in link['href']:
                filename = download_all_files(link['href'])
                has_ext = True

        if has_ext:
            soup.find('a', text=link.text).replaceWith('[' + link['href'] + ' ' + link.text + '] [[File:' + filename + ']]')
        else:
            soup.find('a', text=link.text).replaceWith('[' + link['href'] + ' ' + link.text + ']')



    images = soup.findAll('img')
    print(len(images))
    for img in images:
        has_ext = False
        print(img)
        image = soup.find('img')
        try:
            for ext in file_extensions_to_download:
                if ext in img['src']:
                    filename = download_all_files(img['src'])
                    has_ext = True

            if has_ext:
                image.replaceWith(img['src'] + ' ' + '[[Image:' + filename + ']]')
            else:
                image.replaceWith(img['src'])

        except:
            for ext in file_extensions_to_download:
                if ext in img['data-src']:
                    filename = download_all_files(img['data-src'])
                    has_ext = True

            if has_ext:
                image.replaceWith(img['data-src'] + ' ' + '[[Image:' + filename + ']]')
            else:
                image.replaceWith(img['data-src'])

    return soup


def download_all_files(file_url):
    """ downloads all external files, like images and pdfs """

    print('downloading: {}'.format(file_url))

    myrndm = random.randint(0, 10000)


    if '?' in file_url:
        extension = file_url[file_url.rfind('.'):file_url.find('?')]
        fname = file_url[file_url.rfind('/') + 1: file_url.rfind('.')] + '_' + str(myrndm)
        local_file_url = fname + extension
    else:
        extension = file_url[file_url.rfind('.'):]
        fname = file_url[file_url.rfind('/') + 1: file_url.rfind('.')] + '_' +  str(myrndm)
        local_file_url = fname + extension

    if '*' in local_file_url:
        local_file_url = local_file_url.replace('*','_')

    print(local_file_url)
    # urllib.urlretrieve(file_url, local_file_url)
    return local_file_url


def strip_tags(soup):
    ### https://stackoverflow.com/questions/1765848/remove-a-tag-using-beautifulsoup-but-keep-its-contents
    invalid_tags = ['div', 'canvas', 'span']
    # soup = BeautifulSoup(html)

    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()

    return soup


def dirty_replace_tags(html):
    print('start replacing html the dirty way')
    replace_tags = [{'h1','=='},{'h2','==='},{'h3','===='},{'h4','====='},{'h5','======'}]

    html_list = list(html)
    replace_index = []

    for rep, tag in replace_tags:
        if tag in html:
            html = html.replace('</' + tag + '>', '')


            for i in range(html.count(tag)):
                start_starttag = html.find('<' + tag)
                end_starttag = html.find('>', start_starttag+1)
                # html = html[:start_starttag] + rep + html[end_starttag+1:]
                replace_index.append({'start_starttag':start_starttag, 'end_starttag':end_starttag})


    print(replace_index)
    cleaned_html = []
    i = 0
    last_endtag = 0
    for i in replace_index:

        if i == 0:
            cleaned_html += html_list[:i['start_starttag']]
            i = 1
        else:
            cleaned_html += html_list[last_endtag:i['start_starttag']]
        last_endtag = i['end_starttag']


    html = ''.join(cleaned_html)

    print('end replacing html the dirty way')
    return html



def save_to_local(soup, filename):
    """ saves th soup back"""

    # for elem in soup.findAll('div'):
    #     elem.replaceWith(elem.contents + ' xxx')

    soup = strip_tags(soup)
    html = str(soup.prettify().encode('utf-8'))
    # html = dirty_replace_tags(html)

    with open(filename, 'w') as f:
        # f.write(str(soup.prettify().encode('utf-8')).replace('<body', '<div').replace('</body>', '</div>'))
        f.write(html)







if __name__ == '__main__':
    ctc = read_html_from_locfile('source.html')
    # print(type(ctc))
    # print(ctc)

    soup = local_txt_to_soup(ctc)
    # print(soup)

    soup = handle_links(soup)
    print(soup)

    save_to_local(soup, 'source_edited.html')


