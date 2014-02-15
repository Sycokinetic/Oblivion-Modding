'''
    File: compose.py
    Date: 15 February 2014
    Author: Sycokinetic

    Purpose and Behavior:
        This script is a personal one that composes optimized and unoptimized
        .bsa subfiles for future compression into a .bsa archive. It does this
        by first copying the unoptomized files into a target directory. Then
        it overwrites specific files with optimized copies.

        Note that files ending in _far.nif are ignored because these particular
        files were making my game crash if they were optimized. You can turn
        off this behavior by removing "ignoreFiles=ignorePatternList" from the
        last line in this script.

        The following list of optimized mesh files are copied:
            architecture\
            battlehorncastle\
            *clutter\
            dungeons\
            furniture\
            landscape\
            oblivion\architecture\
            oblivion\caves\
            oblivion\plants\
            orrery\
            plants\
            rocks\
            trees\

            *Note that clutter\magesguild\ is ignored.

    Usage:
        To use my script without editing, you must organize your files a particular way.
        It is currently written to work with the following folder structure:

            base_dir\
                composed\
                extracted\
                    DLCBattlehornCastle.bsa\
                    DLCFrostcrag.bsa\
                    DLCOrrery.bsa\
                    DLCShiveringIsles - Meshes.bsa\
                    DLCThievesDen.bsa\
                    Knights.bsa\
                    Oblivion - Meshes.bsa\
                optimized\
                    DLCBattlehornCastle.bsa\
                    DLCFrostcrag.bsa\
                    DLCOrrery.bsa\
                    DLCShiveringIsles - Meshes.bsa\
                    DLCThievesDen.bsa\
                    Knights.bsa\
                    Oblivion - Meshes.bsa\
                compose.py

        Note that items ending in "\" are folders, not files.

        extracted\ contains all unoptimized files. They have been extracted direction from
        their respective .bsa files.

        optimized\ contains all PyFFI-optimized files. I myself just lump the entire .bsa's
        contents into the optimizer and run it on each file indiscriminantly. This script
        then filters out those files that should not be optimized.

        composed\ contains the final mixture of optimized and unoptimized files. The folders
        in it are ready to be compressed into .bsa format. Optimized files have overwritten
        their respective unoptimized copies.
        
        If you wish to use different file paths, edit the extracted_dir,
        optimized_dir, target_dir, and archiveList variables accordingly.

        Note that you must have some equivalent of composed\, extracted\, and optimized\
        in the same folder as compose.py because of the script's searching algorithm.

        Running this script on all seven .bsa files can take about 15 minutes, so be
        patient.
'''

import os
import re
import shutil

def copyCleanTree(src_root, dst_root, **args):
    acceptedKeys = set(['ignoreFiles'])

    if args and not set(args.keys()).issubset(acceptedKeys):
        raise TypeError("Unrecognized key given. copyCleanTree() accepts optional key 'ignoreFiles' with value of type 'str'.")
    
    if (os.path.exists(dst_root)):
        shutil.rmtree(dst_root)

    try:
        shutil.copytree(src_root, dst_root, ignore=shutil.ignore_patterns(args['ignore']))
    except KeyError:
        shutil.copytree(src_root, dst_root)

def copyOverTree(src_root, dst_root, **args):
    acceptedKeys = set(['acceptDirs', 'ignoreDirs', 'ignoreFiles'])
    
    if args and not set(args.keys()).issubset(acceptedKeys):
        raise TypeError("""Unrecognized key given. copyCleanTree() accepts optional keys:
             \t'acceptDirs' with value of list type 'str'
             \t'ignoreDirs' with value of list type 'str'
             \t'ignoreFiles' with value of list type '_sre.SRE_Pattern'""")

    for key in acceptedKeys:
        try:
            args[key]
        except KeyError:
            args[key] = None

    for src_dir, subDirs, files in os.walk(src_root):
        for dir_ in args['ignoreDirs']:
            if dir_ in subDirs:
                subDirs.remove(dir_)
        else:
            for dir_ in args['acceptDirs']:
                if dir_ in src_dir:
                    dst_dir = src_dir.replace(src_root, dst_root)
                    if not os.path.exists(dst_dir):
                        os.makedirs(dst_dir)
                    for file in files:
                        src_file = os.path.join(src_dir, file)
                        dst_file = os.path.join(dst_dir, file)
                        try:
                            ignoredFile = [pattern.search(file) for pattern in args['ignoreFiles']]
                        except TypeError:
                            ignoredFile = [False]
                        if not ignoredFile[0] and os.path.exists(dst_file):
                            os.remove(dst_file)
                        if not ignoredFile[0]:
                            shutil.copy(src_file, dst_file)

# Store key locations
extracted_dir = 'extracted\\'
optimized_dir = 'optimized\\'
target_dir = 'composed\\'

# Store locations to ignore and accept when overwriting
ignoreString = '*_far.nif'
ignorePatternList = [re.compile(r'_far\.nif')]
archiveList = ['DLCBattlehornCastle.bsa\\',
               'DLCFrostcrag.bsa\\',
               'DLCOrrery.bsa\\',
               'DLCShiveringIsles - Meshes.bsa\\',
               'DLCThievesDen.bsa\\',
               'Knights.bsa\\',
               'Oblivion - Meshes.bsa\\']

acceptList = ['meshes\\architecture',
              'meshes\\battlehorncastle',
              'meshes\\clutter',
              'meshes\\dungeons',
              'meshes\\furniture',
              'meshes\\landscape',
              'meshes\\oblivion\\architecture',
              'meshes\\oblivion\\caves',
              'meshes\\oblivion\\plants',
              'meshes\\orrery',
              'meshes\\plants',
              'meshes\\rocks',
              'meshes\\trees']

ignoreList = ['clutter\\magesguild']     #ignores subdirectories of acceptList. directories not in acceptList are already ignored.

# Copy original meshes to target_dir. Delete previously existing directory.
copyCleanTree(extracted_dir, target_dir)

# Copy optimized meshes to target. Overwrite previously existing files.
for archive in archiveList:
    target = os.path.join(target_dir, archive)
    archive = os.path.join(optimized_dir, archive)
    copyOverTree(archive, target, acceptDirs=acceptList, ignoreDirs=ignoreList, ignoreFiles=ignorePatternList)

