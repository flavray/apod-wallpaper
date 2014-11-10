import os.path
import re
import subprocess
import sys
import urllib2


APOD = 'http://apod.nasa.gov/apod'
APOD_URL = APOD + '/astropix.html'


def treat(path):
    '''
    Adds APOD prefix if the given url is relative
    '''

    if '://' not in path:
        return os.path.join(APOD, path)

    return path


def get_image_path(html):
    '''
    Finds the url of the APOD within the page
    '''

    image_re = re.search('href="(image.*?)">', html, re.IGNORECASE)

    return treat(image_re.group(1))


def save_apod(destination):
    '''
    Saves the APOD into the destination directory
    '''

    try:
        response = urllib2.urlopen(APOD_URL, timeout=2)
        html = response.read()
        response.close()

        image_path = get_image_path(html)
        image_name = image_path.split('/')[-1]

        image_destination = os.path.join(destination, image_name)

        # The image has not already been fetched
        if not os.path.isfile(image_destination):
            with open(image_destination, 'w') as f:
                image = urllib2.urlopen(image_path)
                f.write(image.read())
                image.close()

        subprocess.call(['feh', '--bg-scale', image_destination])

    # No internet connection?
    except urllib2.URLError:
        return


if __name__ == '__main__':
    # sys.argv[1] = directory to save the picture to
    image_path = save_apod(sys.argv[1])
