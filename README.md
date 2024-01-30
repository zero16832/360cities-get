Call this with 360cities.net URLs `https://www.360cities.net/image/...` as command line arguments or via stdin.

Creates a directory for each panorama and subdirectories for tile sizes, avoids downloading duplicate files, so if some downloads fail, there's no need to manually filter the job, just try again.

`pano-get.py` is a Python 3 script, and is the reccommended version.
`pano-get.py.old` is the old Python 2 script, and it hasn't been updated since April 2nd, 2011.