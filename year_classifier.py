from exif import Image
import argparse
import os
import sys
import re
import time

t1 = time.time()

class YearClassifier:
    PATTERN = '(20[0-9]{2})'
    RECUR = False
    VERBOSE = False
    initial_directory = None
    initial_contains = None
    count = 0
    total = 0

    def __init__(self, path, recursive=False, verbose=False, pattern=None):
        if path is None:
            raise(Exception("Path missing"))
        else:
            self.setInitialDirectory(path)

        self.RECUR = recursive
        self.VERBOSE = verbose

        if pattern is not None:
            self.PATTERN = pattern

        try:        
            self.classifyDir(self.initial_directory)
        except Exception as e:
            self.print_v(e)

    def print_v(self, msg):
        if self.VERBOSE:
            print(msg)

    def isValidDir(self, directory):
        try:
            os.listdir(directory)
            return True
        except FileNotFoundError:
            self.print_v('FileNotFoundError: Path not found')
        except NotADirectoryError:
            self.print_v('NotADirectoryError: The source is a file. Please give a directory')
        except Exception:
            self.print_v('ExceptionError: Something went wrong')
    
    def setInitialDirectory(self, directory_path):
        if self.isValidDir(directory_path):
            self.initial_directory = directory_path

    def extract_year(self, name):
        p = re.compile(self.PATTERN)
        result = p.search(name)
        if result:
            year = result[1]
        else:
            year = None
        return year
    
    def counterUpdater(self):
        print(f"{self.count} / {self.total}", end="\r") 

    def classifyDir(self, directory):
        if not self.isValidDir(directory):
            self.print_v('Not a valid dir')

        contains = os.listdir(directory)
        self.total += len(contains)

        for elem in contains:
            self.counterUpdater()
            
            f = os.path.join(directory, elem)

            if self.RECUR and os.path.isdir(f):
                self.classifyDir(f)
            if os.path.isdir(f):
                continue
            else:
                self.count += 1
                with open(f, 'rb') as i:
                    try:
                        img = Image(i)
                        if hasattr(img, 'datetime_digitized'):
                            year = img.datetime_digitized.split(':')[0]
                        elif hasattr(img, 'datetime'):    
                            year = img.datetime.split(':')[0]
                        elif hasattr(img, 'datetime_original'):
                            year = img.datetime_original.split(':')[0]
                        else:
                            year = self.extract_year(elem)
                            self.print_v('No attribute, trying to extract date with regex')

                    except KeyError:
                        year = self.extract_year(elem)
                        self.print_v('KeyError, trying to extract date with regex')
                    except:
                        year = self.extract_year(elem)
                        self.print_v('Error')
                
                if year is not None:
                    directory_name = directory.split('\\')[-1]
                    yeardir = directory if directory_name == year else os.path.join(directory, year)
                    newpath = os.path.join(yeardir, elem)

                    if os.path.exists(yeardir):
                        os.rename(f, newpath)
                    else:
                        os.mkdir(yeardir)
                        os.rename(f, newpath)

        print(f"{self.count} / {self.total}")


parser = argparse.ArgumentParser(description='Classify your pictures.')
parser.add_argument('path', type=str, help='(str) The path of the directory containing your pictures.')
parser.add_argument('-r', action='store_true', help='--recursive, classify recursively every pictures contained in that directory.')
parser.add_argument('-v', action='store_true', help='--verbose, print out errors. ')
args = parser.parse_args()

classifier = YearClassifier(args.path, args.r, args.v)

elapsed = time.time() - t1   
if elapsed/60 < 1:
    print(f'Done in {round(elapsed, 2)} s')
else:
    print(f'Done in {round(elapsed / 60, 2)} min')