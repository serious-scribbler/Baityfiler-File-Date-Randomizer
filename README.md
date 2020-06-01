# Baityfiler-File-Date-Randomizer
Baityfiler randomizes file creation, access and modification dates to make tech scambaiting VMs look more realistic.

# Where do I get the .exe?
You can download the .exe from the [releases tab](https://github.com/serious-scribbler/Baityfiler-File-Date-Randomizer/releases) or generate it yourself using auto-py2-exe

# How to use Baityfiler

## Changing the dates of a single file

This example sets the access, modification and creation dates of _examplefile.txt_ to random dates between June 1, 1990 and December 31, 2000.
`Baityfiler.exe 1990-06-01 2000-12-31 examplefile.txt`

## Changing the dates of all files in a directory

This example changes the dates of all files and directories in the _testdir_ directory and the dates of the directory itself. Anything contained in its subdirectories will stay unchanged.
`Baityfiler.exe 1984-06-01 2000-05-04 testdir\`

## Changing the dates of all files in a directory and it's subdirectories

This example changes the dates of all files and directories in the _testdir_ directory and its subdirectories.The dates of the directory itself will also be changed.
`Baityfiler.exe 1984-06-01 2000-05-04 testdir\ -r`

## Getting help

Any comand ending with the `-h` flag will display the help, this includes `Baityfiler.exe -h` without the normally required parameters.

# Known issues
* Directories/files in some protected directories can't be modified (Program files for example). I will try to resolve this issue in the next version of the program.

# What to do when you run into problems
If you have any issues with the program that aren't listed under known issues in this readme, please report them by creating an issue under the [Issues tab](https://github.com/serious-scribbler/Baityfiler-File-Date-Randomizer/issues).

# Where to suggest changes/improvements
Please suggest changes/improvements under the [Issues tab](https://github.com/serious-scribbler/Baityfiler-File-Date-Randomizer/issues), just name your issue appropriately.
