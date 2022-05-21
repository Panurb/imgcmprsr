# imgcmprsr

Image compression tool.

## Algorithm

The compression uses a recursive algorithm. The input is an RGB-image so an 8-bit integer array. We shall denote it by:
$$
A \in \mathbb{Z}_{256}^{h \times w \times 3}
$$
where w and h are the image width and height in pixels, respectively.
The region of interest at the start is the whole image, so
$$
(x_1, y_1, x_2, y_2) = (0, 0, w, h)
$$

If the area of the region of interest is zero, we have reached the base case. Do nothing.

Otherwise, calculate detail level in region of interest. For this the following formula is used:
$$
\mathrm{detail}(A) = \sum_k \max_{i,j}(A_{ijk}) - \min_{i,j}(A_{ijk})
$$

If this detail level in below a threshold value, defined as
$$
\mathrm{threshold} = 1000 \times \mathrm{compression level}
$$
the region is filled with the average value of all the pixels within it. 
The average value of the region is calculated as simply the mean of each individual color channel:
$$
\mathrm{average}(A)_k = \frac{1}{hw}\sum_{i,j} A_{ijk}
$$

If the detail level is above the threshold, the region is divided into 4 subregions and the function is called recursively for each subregion.
The subregions are given by
$$
(x_1, y_1, x, y), \;
(x, y_1, x_2, y), \;
(x_1, y, x, y_2), \;
(x, y, x_2, y_2)
$$
where
$$
    x = \frac{x_1 + x_2}{2}, \; y = \frac{y_1 + y_2}{2}.
$$

## Coordinate system

Since the image is repeatedly divided into smaller subregions, we can keep track where we are in the image by labelling
each subregion from 0 to 3 and keeping track of the chain of subregions. The subregions are labeled in the following way:

\begin{center}
\begin{tabular}{|c|c|}
\hline
0 & 1 \\ \hline
2 & 3 \\ \hline
\end{tabular}
\end{center}

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
