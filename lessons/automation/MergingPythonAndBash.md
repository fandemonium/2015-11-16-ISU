# Merging Python and UNIX

Adapted from UT Biocomputing course and Python Data Carpentry materials.

## Putting Python in a script

So far, we have run python from notebook. We might not want to do that for every solution. The notebook, for example, cannot be included in a pipeline.

To this end, I've included a script, wordcount.py in the code directory. 


## The python `sys` module

The `sys` module interacts with the python interpreter. This module primarily comes with certain **variables** (rather than functions) which are particularly useful, two of which are described below.

### Passing command-line arguments `sys.argv`
Often, you'll want to pass input arguments to a script. All input arguments are stored in the variable `sys.argv` (note that you must import the `sys` module!). For example, you might have a script called `wordcount.py` which performs certain calculations on a sequence data file, but each time you run the script, you might want to process a different file. One option to pass the file name as an input argument: `python wordcount.py unicorns.txt`, where `unicorns.txt` is the single command-line argument. If you've loaded the `sys` module, all command line arguments will be stored in `sys.argv`:

Assume the following code is included in the script wordcount.py. 
```python
import sys
print sys.argv
```
From the command line you run `python wordcount.py creatures/unicorn.dat unicorn_counts.txt` and get back nothing, but there should now be a file called 'unicorn_count.txt'.


Notice that the first entry in `sys.argv` is the name of the script. After this come all command line arguments! In addition, all `sys.argv` entries will be **strings**. So remember that if you want to use an input argument as a number, you must convert it to a float or integer.

Generally, you should save the input arguments to a new variable inside the script:
```python
import sys
infile = sys.argv[1]
```

Error checking is often very useful here; you might have a script which **requires** two command line arguments. For instance, let's say you have a script (which does something..) which takes a file name and a number as its two arguments. To ensure that this always happens, help yourself out with assertion statements:

```python
import sys
  input_file = sys.argv[1]
  output_file = sys.argv[2]
  min_length = 1
  if (len(sys.argv) > 3):
    min_length = int(sys.argv[3]) # remember to convert from string to int, as needed!
  word_count(input_file, output_file, min_length) 
```


### Editing the path with `sys.path`

You can view everything in python's path by printing the contents of the list `sys.path`. This variable will you tell which directories on your computer that the current python interpretter is able to access. To edit this path in place, for instance by adding a directory to the path, simply use `.append()`:
```python
import sys
sys.path.append("/path/to/directory/that/python/should/know/about/")
```

<br><br>
## The python `os` and `shutil` modules

The `os` and `shutil` modules are useful for interacting with your computer's operating system (typically UNIX). With these modules, you can run commands from your python script which are analogous to UNIX commands like `cd` and `pwd`. 
<br>Some examples:

Module | Command  |  Description | Unix equivalent | Example
-------|----------|--------------|-----------------|--------
`os` | `os.listdir`| List all items in a given directory | `ls` | `os.listdir("/directory/of/interest/")`
`os` | `os.remove` | Remove a file | `rm` | `os.remove("i_hate_this_file.txt")`
`os` | `os.rmdir` | Remove a directory | `rm -r`| `os.rmdir("/i/hate/this/directory/")`
`os` | `os.mkdir`  | Create a new directory | `mkdir` |`os.mkdir("/path/to/brand/new/directory/")`
`os` | `os.mkdirs`  | Create many new directories | `mkdir`|`os.mkdir("/path/to/a/brand/new/directory/", "/path/to/another/brand/new/directory/")`
`os` | `os.chdir`  | Change directory where python is running | `cd` | `os.chdir("/another/directory/where/i/want/to/be/")`
`shutil` | `shutil.copy` | Copy a file | `cp` | `shutil.copy("old_file.txt", "new_file.txt")`
`shutil` | `shutil.move` | Move a file | `mv` | `shutil.move("old_file.txt", "new_file.txt")`


### Running external commands with `os`

You will often want to use Python scripting to automate analyses which use external programs or softwares. You can actually call these programs directly from your python script using the function `os.system()`. This function takes a single argument: the command you want to run (as a string). Anything that you could type into the command line can be given to `os.system`!

```python
def check_against_unix(input_file, output_file, min_length=1):
	'''A function to check our file against unix wc'''
	command = "sort creatures/unicorn.dat | wc > unix_check"
	os.system(command)	
```

# Part 2: useful UNIX/Bash one-liners: `sed`  and `awk`

Bash is great for getting a quick look at your data and for simple regex replacements

<br><br>
### `sed` is useful for quick and recursive replacements using Regex

* General pseudocode: `sed [-E] command/regex/replacement/optionalflag filename > newfile`
* My favorite pseudocode: `sed -E s/OLD/NEW/`
* Mac users must include `-E` to access regular expressions
* `sed` does not understand `\t` and `\n`, see below

```bash
# replace first instance of XX with YY for each line
sed s/XX/YY/ creatures/unicorn.dat > creatures/unicorns_corrected.dat
```

```bash
# replace all instances of XX with YY 
# - `g` flag means 'global' and searches for all instances of the pattern
sed s/CC/GG/g creatures/unicorn.dat > creatures/unicorns_corrected.dat
```

```bash
# replace all instances of XX with YY and of AA with ZZ
# - `-e` flag lets you execute multiple sed commands at once
sed -e s/CC/GG/g -e s/AA/TT/g creatures/unicorn.dat > creatures/unicorns_corrected.dat
```

```bash
# keep only letter and space characters ([a-zA-Z' ']*) that come before a different type of character in each line
# - must escape all () using `\`, ie: \([regex]\)
# - must put whitespace and replacement ('\1\2') in quotes, or else it is interpreted as a separate command
sed -E s/\([a-zA-Z' ']*\)\(.*\)/'\1'/ creatures/unicorn.dat > creatures/unicorns_corrected.dat
```

* To insert tabs (`\t`) you'll have to hit `ctrl + v`, then `Tab` while in the terminal environment
* For newline characters (`\n`), you have to code it directly into the line with `\ + enter`, for example:

```
sed -E s/\([0-9]\)/'\1\
'/ creatures/unicorn.dat > creatures/unicorns_corrected.dat
```

Sed is great for doing quick replacements in your files.

Now, let's put it all together. 

```UNIX
for file in creatures/*corrected*; 
do echo $file; 
python wordcount.py $file $file.output 1; 
done
```

This is a little clunky, no? We have all this directory in which processed data and unprocessed data are being stored together - that could be confusing!

Let's add a function to our word count script that makes a directory in which to store our output:

```python
if 'processed' in os.listdir('.'):
    print 'Processed directory exists'
else:
    os.mkdir('processed')
    print 'Processed directory created'   
```

With a partner, take this code, make it into a function called make_output, and add it to externalCall.py. Now run the script. How do you have to modify the arguments you provide?


##So ... __name__ == __main__? That's weird.

This odd-looking statement tells Python that this file can be used as either a stand-alone program or as a module. This lists the actions that will occur and variables that will be defined if we execute the script.

If we want to import our script as a library, and use the functions inside of it, the main statement also allows us to do this.

Let's say we wanted to call the function you just created, make_output. In the wordcount.py script, add this import statement:

```python

import ReadOnly

```

Now, in the main statement, add a call to the make_output function. Where should it go? When do we want to create the output directory?

How could we modify our import statement to make our function call simpler?
