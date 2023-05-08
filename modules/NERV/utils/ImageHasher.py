import io
import base64
import logging
import hashlib
import imagehash
import requests
from PIL import Image

try:
    from imghdr import what as imghdr_what  # deprecated, planning that it might get removed in next versions of Python
except:
    imghdr_what = lambda y: None
import filetype

from ..config import *

log = logging.getLogger(__name__)

def get_url_from_image_entity(request_entity):
    """Get the URL from an Image Entity, pass the request object that is passed to the create_entity method."""
    if "url" in request_entity.Properties:
        url_image = request_entity.getProperty("url")
    elif "fullImage" in request_entity.Properties:
        url_image = request_entity.getProperty("fullImage")
    else:
        raise Exception("URL could not be found in the image")
    return url_image


class ImageHasher:
    # https://github.com/JohannesBuchner/imagehash
    """
    If like me you don't  know what hash to use, use pHash by default. As this blog cited several times by the author of
    the library we are using (imagehash), considers it as "best with regards to accuracy".
    Source: https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html
    """

    def __init__(self, url):
        if os.path.exists(url):
            self.path_to_file = url
        else:
            self.path_to_file = self._download_img(url)
        with open(self.path_to_file, "rb") as f:
            self.raw_content = f.read()
        self.image = None

    def _load_as_image(self):
        if self.image is None:
            self.image = Image.open(io.BytesIO(self.raw_content))
        return self.image

    def get_average_hash(self):
        """
        Resistant to scaling, ration changes, change in brightness, contrast and color alteration.

        More info on it: https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

        Comparing pHash:If you want to compare two images, construct the hash from each image and count the number
        of bit positions that are different. (This is a Hamming distance.) A distance of zero indicates that it is
        likely a very similar picture (or a variation of the same picture). A distance of 5 means a few things may be
        different, but they are probably still close enough to be similar. But a distance of 10 or more? That's probably
         a very different picture.
         """
        return imagehash.average_hash(self._load_as_image(), hash_size=AVERAGE_HASH_LENGTH)

    def get_phash(self):
        """
        Resistant to minor modifications (ex: adding text)

        More info on it: https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

        'if there are modifications -- like text was added or a head was spliced into place, then Average Hash probably
         won't do the job. While pHash is slower, it is very tolerant of minor modifications (minor being less than 25%
         of the picture).'
        """
        return imagehash.phash(self._load_as_image(), hash_size=P_HASH_LENGTH)

    def get_dhash(self):
        """
        This blog article (https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html) considers
        it as a better version of average hash
        """
        return imagehash.dhash(self._load_as_image(), hash_size=D_HASH_LENGTH)

    def get_whash(self):
        """
        According to this blog (https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) it is similar to
        pHash in its mechanism
        """
        return imagehash.whash(self._load_as_image(), hash_size=W_HASH_LENGTH)

    def get_crop_resistant_hash(self):
        """
        According to this blog (https://erdogant.github.io/undouble/pages/html/hash_functions.html#crop-resistant-hash),
        this algorithm is particularly resistant to cropping images

        Original paper: https://ieeexplore.ieee.org/document/6980335
        """
        return imagehash.crop_resistant_hash(self._load_as_image())

    def get_colorhash(self):
        return imagehash.colorhash(self._load_as_image(), binbits=COLOR_HASH_BINBITS)

    def get_sha1(self):
        return hashlib.sha1(self.raw_content).hexdigest()

    def get_sha256(self):
        return hashlib.sha256(self.raw_content).hexdigest()

    def get_md5(self):
        return hashlib.md5(self.raw_content).hexdigest()

    @classmethod
    def _download_img(cls, url):
        r = requests.get(url)
        cont = r.content
        # filename will be the URL encoded in b64 (cut off at 60 chars max)
        fname = base64.b64encode(url.encode("utf8")).hex()[-MAX_LENGHT_FNAME_IMG:]
        os.makedirs(TMP_IMG_FOLDER, exist_ok=True)
        fpath = os.path.join(TMP_IMG_FOLDER, fname)
        with open(fpath, "wb") as f:
            f.write(cont)
        extension = cls._get_filetype(fpath)
        fpath_with_extension = fpath + "." + extension
        os.rename(fpath, fpath_with_extension)
        return fpath_with_extension

    @classmethod
    def _get_filetype(cls, fpath):
        extension_imghdr = imghdr_what(fpath)
        extension_filetype = filetype.guess_extension(fpath)
        if extension_filetype != extension_imghdr:
            log.warning(f"Filetype for {fpath} is unsure: Imghdr says {extension_imghdr} and Filetype says "
                  f"{extension_filetype}.")
        return extension_filetype
