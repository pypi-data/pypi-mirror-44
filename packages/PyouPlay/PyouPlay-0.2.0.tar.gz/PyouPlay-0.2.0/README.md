[![Build Status](https://travis-ci.com/omi10859/PyouPlay.svg?branch=master)](https://travis-ci.com/omi10859/PyouPlay)
# PyouPlay
python Package to get links to videos from youtube when you pass search argument


# How to use?

## Dowload using pip 
```pip install pyouplay```

### Import 
```from PyouPlay import get ```

# Pass seach argument 
```get.toplink("Pass a string you want to seach")``` [toplink will return a string containing link to the youtube video]
#### OR
```get.toplinks("Pass a string you want to seach")``` [toplinks will return a list of top 20 videos links from youtube] 
 
# Optional Argument - Open video in browser
#### Pass 1 for the second positional argument
```get.toplink("Pass a string you want to seach", 1)``` [toplink will open the youtube video in the web browser]


