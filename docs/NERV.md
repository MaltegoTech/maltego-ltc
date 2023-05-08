# NERV: Navigation and Extraction of Representations for Verification

NERV is intended to help you extract and compare images in Maltego. The comparison can be done using the hashing 
functions hosted in the [excellent GitHub repository of Johannes Buchner](https://github.com/JohannesBuchner/imagehash).
While traditional hashes (md5, SHA1, SHA256, etc.) are very useful to quickly check if 2 files are the same, they cannot
be used to check if 2 image are the same, or if one is a subtle modifications of the other.


# Why use Image hashes?
When images are uploaded online, they can undergo different transformation: rescaling, cropping, compression, etc. This 
kind of transformation make it impossible to compare images simply using traditional hashes. This is where images hashes
 come into play. See the comparison below

Here are 2 identical pictures. The only difference is that one is saved as a JPEG and the other as a PNG. The table
below shows the traditional output if we use "traditional" hashes then using image hashes. As a reference, the Hamming 
distance between both hash is provided in the 4th column. In this case, is a good indicator of how close 2 images are.
The author of the repository we use cites an author who suggest that a hamming distance equal to 0 means the images are 
the same and a distance inferior to 10 means that the image are very close.


| Hash Name |                          Original                           | Reformated | Hamming distance |
|-----------|:-----------------------------------------------------------:| :----: |:----------------:|
|           | ![A picture of a statue of a lion](./imgs/NERV/origin.jpeg) | ![A picture of a statue of a lion](./imgs/NERV/other_format.png)       |                  |
| MD5       |              b28782b47455ce323a05ed49f9d79792               | 1c463e975909486d1e2fe0c34ddf912d |       N/A        |
| pHash     |                      c205cf6d2cdaca8d                       | c205cf6d2cdaca8d |        0         |
| dHash     |                      e7ced08da6a17165                       | e7ced08da6a17165 |        0         |
| wHash     |                      21377e4000f8fdf5                       | 21377e4000f8fdf5 |        0         |
| ColorHash |                         06180000000                         | 06180001000 |        1         |


Here is the same comparison with a completely different image. As you can see, the Hamming distances are far greater.

| Hash Name | Original  |                  Different Image                   | Hamming distance |
|-----------|:----:|:--------------------------------------------------:|:----------------:|
|           | ![A picture of a statue of a lion](./imgs/NERV/origin.jpeg)     | ![A picture of a lion](./imgs/NERV/different.jpeg) |                  |
| MD5       | b28782b47455ce323a05ed49f9d79792 |          ba0a6e7a6b4d081d51242d7c8e329a4c          |       N/A        |
| pHash     | c205cf6d2cdaca8d |                  efe0d08d34366d68                  |        34        |
| dHash     | e7ced08da6a17165 |                  0c83312d336361bc                  |        29        |
| wHash     | 21377e4000f8fdf5 |                  fffd8000013919ff                  |        28        |
| ColorHash | 06180000000 |                    07c00018000                     |        7         |

# How to use the Transforms in this module?
The Transforms in this modules are intended to help you sort out a large number of images. They give you the tools to 
harvest, download and compare images. Here are possible usecases. Please notes that there likely are many others, if any come to your mind, please suggest them.
### Possible usecases
- **Compare different websites**: when listing websites belonging to different domains, you might want to know if they share
a favicon, which could indicate that they are a mirror of the same website. You could do it like so: 
  - Select the websites on your graph ▶ To Favicon ▶ To pHash ▶ Look at the different hashes and see if some of them are closes to each other.
- **Verify if several URLs are sharing the same images**: whether it is to study disinformation or the propagation of other images, 
it can be useful to check if some URLs display the same images. To avoid consulting all the URLs and comparing the images yourself
you could proceed like so:
  - Select the URLs on you graph ▶ To Images ▶ To pHash ▶ Look at the different hashes and see if some of them are closes to each other.

# What are the hashes available and which should I use?

**tl;dr: if you don't know what to use and what to check the closeness between 2 images, use To pHash.**

I have no idea what hash you should use. However, the people that produced the Image Hash library that we are using linked
some sources and articles that can help us learn about these hashes. Here is a little summary:
 
## Average Hash (aHash)
Resistant to scaling, ration changes, change in brightness, contrast and color alteration.
More info on it: https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

## Perception Hash (pHash)
Resistant to minor modifications (ex: adding text)
More info on it: https://www.hackerfactor.com/blog/index.php?/archives/432-Looks-Like-It.html

Quote from this article:
'if there are modifications -- like text was added or a head was spliced into place, then Average Hash probably
won't do the job. While pHash is slower, it is very tolerant of minor modifications (minor being less than 25%
of the picture).'

## Difference Hash (dHash)
This blog article (https://www.hackerfactor.com/blog/index.php?/archives/529-Kind-of-Like-That.html), linked by the Image Hash lib author, considers
it as a better version of average hash.

## Wavelet Hash (wHash)
According to this blog (https://fullstackml.com/wavelet-image-hash-in-python-3504fdd282b5) it is similar to
pHash in its mechanism

## Crop Resistant Hash
According to this blog https://erdogant.github.io/undouble/pages/html/hash_functions.html#crop-resistant-hash,
this algorithm is particularly resistant to cropped images. (Not implemented yet.)

Original paper: https://ieeexplore.ieee.org/document/6980335

## Color Hash

# Config
The config file (modules/NERV/config.py) contains the following variable that you can modify to suit your usage of this module:
- **TMP_IMG_FOLDER**: Whenever an image is hashed (using **To pHash** or any other hash) we download it to this folder. Please note that there is no mechanism
to clean this folder. You need to remove the images yourself. By default, the images are stored in **maltego-ltc/modules/NERV/tmp_img**.


- **MAX_LENGHT_FNAME_IMG**: When downloading an image, we save it and generate a file name by encoding the URL in base 64. This 
might generate some extra long filename, which depending on the length of the path to the folder in which we save the image, might cause issue with the 
the OS and the maximum lenght that a file path can have. You probably will not have to touch this but its there if you need it.


- **AVERAGE_HASH_LENGTH**: According to the author of the Image Hash library: "Each algorithm can also have its hash size adjusted (or in the case of colorhash, its binbits). Increasing the hash
size allows an algorithm to store more detail in its hash, increasing its sensitivity to changes in detail."


- **P_HASH_LENGTH**: See **AVERAGE_HASH_LENGTH**.


- **D_HASH_LENGTH**: See **AVERAGE_HASH_LENGTH**.


- **W_HASH_LENGTH**: See **AVERAGE_HASH_LENGTH**.


- **COLOR_HASH_BINBITS**: See **AVERAGE_HASH_LENGTH**.


- **DRIVER_PATH**: The default package used to retrieve page HTML is Selenium. This package uses a real web browser to visit the webpage. This makes the presence of a driver for your browser necessary. Please use this variable to link the path to the Chrome browser we are using. If Selenium is not configured or if there is a problem retrieving the URL with it, we will fall back on requests. To install and configure Selenium, please follow this guide: https://selenium-python.readthedocs.io/installation.html

# Next steps
- Implement Crop Resistant hash Transforms.