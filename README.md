# imgcmprsr

Image compression tool.

## Algorithm

The compression uses a recursive algorithm. The input is an RGB-image so an 8-bit integer array. We shall denote it by:
<p align="center"><img src="svgs/2bac01daa5a1bdafb65698c8333b642e.svg?invert_in_darkmode" align=middle width=87.99479204999999pt height=19.406267099999997pt/></p>
where *w* and *h* are the image width and height in pixels, respectively.
The region of interest at the start is the whole image, so
<p align="center"><img src="svgs/37954f9daf267417ba7b05e026e07668.svg?invert_in_darkmode" align=middle width=193.85085389999998pt height=16.438356pt/></p>

If the area of the region of interest is zero, we have reached the base case. Do nothing.

Otherwise, calculate detail level in region of interest. For this the following formula is used:
<p align="center"><img src="svgs/73c1ba804c4f1224efc3738a7d7c2dbd.svg?invert_in_darkmode" align=middle width=279.69593684999995pt height=37.03214955pt/></p>

If this detail level in below a threshold value, defined as
<p align="center"><img src="svgs/9f0b9efc2356568b147eccfb22202676.svg?invert_in_darkmode" align=middle width=260.63959845pt height=14.611878599999999pt/></p>
the region is filled with the average value of all the pixels within it. 
The average value of the region is calculated as simply the mean of each individual color channel:
<p align="center"><img src="svgs/18f8fc3106ac74e5876a08ae376d25df.svg?invert_in_darkmode" align=middle width=193.7912031pt height=43.346758949999995pt/></p>

If the detail level is above the threshold, the region is divided into 4 subregions and the function is called recursively for each subregion.
The subregions are given by
<p align="center"><img src="svgs/095a2b39880680d96f57d54dc7af6be8.svg?invert_in_darkmode" align=middle width=375.4184082pt height=16.438356pt/></p>
where
<p align="center"><img src="svgs/a35cbfd030a3023cd3db68dcaf267b54.svg?invert_in_darkmode" align=middle width=190.79704214999998pt height=31.985609699999994pt/></p>

## Coordinate system

Since the image is repeatedly divided into smaller subregions, we can keep track where we are in the image by labelling
each subregion from 0 to 3 and keeping track of the chain of subregions. The subregions are labeled in the following way:

<p align="center"><img src="svgs/bcd599ca6d65aa6893090369693b210f.svg?invert_in_darkmode" align=middle width=56.548041pt height=41.42462775pt/></p>

Each subregions is further divided into four subregions recursively. Then the lowest level subregion is uniquely defined
by the chain of subregions leading up to it, represented as a chain of number, e.g. '023123'.

This chain of numbers is then interpreted as a single base 4 integer. To account for any zeros at the start of the chain,
it is first prepended with a '1'. For example '023123' becomes '1023123' becomes 4827. This operation is then fully
reversible.

## Storing

The compressed file is stored as a plain text file. The first line contains the horizontal and vertical resolution of
the output image. Each line thereafter contains four values: the coordinate of the subregion and the three RGB 
components of its color.

## Acknowledgements

This readme file was created using readme2tex, using the command:
```
python -m readme2tex --nocdn --output README.md INPUT.md
```
