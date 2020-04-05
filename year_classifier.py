from exif import Image
import os
import sys
import re
import time

t1 = time.time()
pattern = '(20[0-9]{2})'

def extractdate(name):
    p = re.compile(pattern)
    result = p.search(name)
    if result:
        year = result[1]
    else:
        year = None
    return year

try:
    directory = sys.argv[1]
    files = os.listdir(directory)
except IndexError:
    print('IndexError: you either forgot to give a source directory or gave more than one (use " ")')
    sys.exit()
except FileNotFoundError:
    print('FileNotFoundError: path not found')
    sys.exit()
except NotADirectoryError:
    print('NotADirectoryError: The source is a file. Please give a directory')
    sys.exit()

for count, f in enumerate(files, start = 1):
    pathimg = os.path.join(directory, f)

    if os.path.isdir(pathimg):
        continue
    else:
        with open(pathimg, 'rb') as i:
            try:
                img = Image(i)

                if hasattr(img, 'datetime_digitized'):
                    year = img.datetime_digitized.split(':')[0]
                if hasattr(img, 'datetime'):    
                    year = img.datetime.split(':')[0]
                if hasattr(img, 'datetime_original'):
                    year = img.datetime_original.split(':')[0]
                else:
                    year = extractdate(f)
                    print('No attribute, trying to extract date with regex')

            except KeyError:
                print('KeyError, trying to extract date with regex')
                year = extractdate(f)
            except:
                year = extractdate(f)
                print('Error')
        
        if year is not None:
            yeardir = os.path.join(directory, year)
            newpath = os.path.join(yeardir, f)

            if os.path.exists(yeardir):
                os.rename(pathimg, newpath)
            else:
                os.mkdir(yeardir)
                os.rename(pathimg, newpath)

        print(f'{count}/{len(files)}')

elapsed = time.time() - t1        
print(f'Done in {elapsed} s or {elapsed /60} min')