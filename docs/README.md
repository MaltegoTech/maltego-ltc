# Maltego Web2Screenshot Transforms

The Maltego Web2Screenshot Transforms allow you to capture screenshots from both websites and URLs 
in a secure and anonymous manner. 

I developed these transforms to enhance my operational security 
(OPSEC) by avoiding exposing my public or VPN's IP address. With these Transforms, you can generate high-quality 
screenshots while keeping your identity and location hidden. 

To use the Maltego Web2Screenshot Transforms, simply obtain an API Key from API Flash's Free tier, which provides 100 
credits per month (1 credit per screenshot). 

Experience the power and convenience of the Web2Screenshot Transforms for your investigative needs.

## The Transforms

There are 8 available Transforms (4 per input type)

- **To Screenshot - Cache [API Flash]** : Retrieve a cached screenshot of a URL or Website, will consume 1 credit if not 
available in cache.
- **To Screenshot - Live [API Flash]** : Take a live screenshot from a URL or Website, will consume 1 credit.
- **To Screenshot XL - Cache [API Flash]** : Retrieve a cached full page screenshot from a URL or Website, will consume 1 
credit if not available in cache.
- **To Screenshot XL - Live [API Flash]** : Take a live full page screenshot from a URL or Website, will consume 1 credit.

## Capture Type

There are 2 capture types available.

1. **Live**: This will request a live screenshot from API Flash which will consume 1 credit.
2. **Cache**: This will check first if you have taken the screenshot for the specific input before, if available it will 
retrieve that copy without consuming credits, if not available, a live screenshot will be taken consuming 1 credit.

![credits.png](imgs%2Fcredits.png)

After a screenshot is retrieved, you can visually distinguish between the live and cached captures by the overlay colors 

- **Green:** Live capture
- **Yellow:** Cache capture

## Capture Size

There are 2 capture sizes available, both cost 1 credit each.

1. **Standard**: This will take a screenshot of the target without scrolling down the page.
2. **XL**: This is a full page screenshot, API Flash will attempt to scroll down the page before saving the image.

Both Transforms will give you the option to open the image on your Browser, which can be found in the Detail View

![open_browser.png](imgs%2Fopen_browser.png)

This would be specially useful for the XL screenshots.

![fullsite_browser.png](imgs%2Ffullsite_browser.png)

Zooming in will allow you to view the capture as if it was the original site's size.

## Installation

Install the required libraries by running

`pip install -r requirements.txt`

A Maltego configuration file **Web2ScreenshotTransforms.mtz** has been included under the misc folder, you can simply 
import the file into your client by going to Import | Export > Import Config > Select mtz file.

![import.png](imgs%2Fimport.png)

Finally, you will need to add your API Key for the Transforms. Simply locate the .env file in the root directory (Enable 
show Hidden files if using your OS explorer) and add your key next to the API_KEY without spaces.

![api_keys.png](imgs%2Fapi_keys.png)

The configuration file includes a Transform set called "Web2Screenshot" which will arrange your new Transforms into a 
submenu, making them easier to find and use.

**Note:** At the time of writing the Transforms I noticed the URL Entity's property that hold the url has changed it's 
unique name from url to theurl, if you don't get any results when running the URL to Screenshot Transforms could be due 
that change.

To fix this issue you can try refreshing your client or simply change the property name called **input_url** inside the 
Transforms (it's below the line where you added your API Key)

Happy OSINTing!