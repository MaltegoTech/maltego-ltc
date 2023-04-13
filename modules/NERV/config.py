import os

# Folder to download the image
TMP_IMG_FOLDER = os.path.join(os.path.dirname(__file__), "tmp_img")

# Maximum length a filename can reach (used to store an image)
MAX_LENGHT_FNAME_IMG = 60

# Size of the hashes, according to the Github repo of the library used for these hashes
# (https://github.com/JohannesBuchner/imagehash)
# "Each algorithm can also have its hash size adjusted (or in the case of colorhash, its binbits). Increasing the hash
# size allows an algorithm to store more detail in its hash, increasing its sensitivity to changes in detail."
AVERAGE_HASH_LENGTH = 8
P_HASH_LENGTH = 8
D_HASH_LENGTH = 8
W_HASH_LENGTH = 8
COLOR_HASH_BINBITS = 3

# Max hemming distance threshold to consider 2 images are the same or created from modified the other
# 10 as a default value comes from
MAX_HEMMING = 10

# The driver for the web browser Selenium will be using
# GET THE CORRECT DRIVE HERE IF DRIVER IS OUTDATED: https://chromedriver.chromium.org/downloads
DRIVER_PATH = ""
# if you are using OS X, you can remove the file by running the following command line: sudo xattr -c "filename"
