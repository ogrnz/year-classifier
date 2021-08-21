# Year classifier script

The script classifies pictures (or any given file actually) in a given directory.
It uses the exif (https://pypi.org/project/exif/) lib to extract metadata. When no metadata is found, 
the script looks for a simple `20[0-9]{2}` regex pattern (adapt it if you have old pics) in the file name. 

### How to use:
After downloading the script and setting up the environment, 
just call the python script with the source directory as the first and only argument : `python year_classifier.py "G:/path/to/pictures"`
```bash
# Initialize virtual environment
virtualenv venv
venv\Scripts\activate

# Pip install
pip install -r requirements.txt

# Use the script and voilà!
python year_classifier.py "G:/path/to/pictures"
1/1505
2/1505
...
1505/1505
Done in 27.016995668411255 s
````
### TODO
- Add recursivity via `-r` flag

### Notes
- It works on unix systems as well as on Windows
- It is *not* recursive yet
