#!/usr/bin/env python

"""

configure.py

Sets up the Django template as a new, distinct project.

"""

import os
import sys

if len(sys.argv) <= 1:
    print "You must supply a project name."
    sys.exit(1)
    
PROJECT_NAME = sys.argv[1]

HERE = os.path.dirname(os.path.abspath(__file__))


class NoDjTemplateDir(Exception):
    def __str__(self):
        return (
            "Directory 'djangotemplate' does not exist. "
            "Are you sure this is a valid djangotemplate fork?"
        )
        
        
class NoDjSettings(Exception):
    def __str__(self):
        return (
            "Could not open {}/settings.py. "
            "Are you sure this is a valid djangotemplate fork?"
                .format(PROJECT_NAME)
        )
        
        
def rename_directory():
    """ Renames the djangotemplate directory to PROJECT_NAME. """
    
    djtemplatePath = os.path.join(HERE, 'djangotemplate')
    
    if not os.path.exists(djtemplatePath):
        raise NoDjTemplateDir()
        
    os.rename(djtemplatePath, PROJECT_NAME)
    
    
def replace_references(dir=HERE):
    """ Recursively walks through the project and replaces references to 
    'djangotemplate' with PROJECT_NAME.
    
    """
    
    for item in os.listdir(dir):
        itemPath = os.path.join(dir, item)
        
        if os.path.isdir(itemPath) and item != '.git':
            # Recursively walk directories and replace references
            replace_references(itemPath)
            
        # Replace references in all *.py files (except configure.py),
        # and also the Procfile.
        elif ((item.endswith('.py') and item != 'configure.py')
                or item == 'Procfile'):
                
            # Read the file data
            with open(itemPath, 'r') as f:
                data = f.read()
                
            # Replace all references
            newData = data.replace('djangotemplate', PROJECT_NAME)
            
            # Re-save the file
            with open(itemPath, 'w') as f:
                f.write(newData)
                
                
def generate_key():
    """ Generate a new Django secret key for use in settings.py. """
    
    settingsPath = os.path.join(HERE, PROJECT_NAME, 'settings.py')
    
    try:
        with open(settingsPath, 'r') as f:
            data = f.read()
            
    except IOError:
        raise NoDjSettings()
        
    # Generate a new secret key (consisting of 50 OS-produced random bytes)
    newKey = (
        ''.join(
                (
                    '\\x{}'.format(
                            '0' + hex(n)[2:] if n < 0x10 else hex(n)[2:]
                        )
                    for n in (ord(b) for b in os.urandom(10))
                )
            )
        for i in xrange(5)
    )
    
    # Insert the new key into settings.py
    newData = data.replace(
            '\'[[ INSERT_SECRET_KEY_HERE ]]\'',
            '(\n{})'.format(
                    ''.join(
                            (
                                '{}\'{}\'\n'.format(' ' * 4, keyPart)
                                for keyPart in newKey
                            )
                        )
                )
        )
        
    # Save the new settings.py
    with open(settingsPath, 'w') as f:
        f.write(newData)
        
        
def main():
    print "Renaming directory 'djangotemplate' to '{}'... ".format(
            PROJECT_NAME
        ),
    rename_directory()
    print "Done!"
    
    print "Replacing 'djangotemplate' references with '{}'... ".format(
            PROJECT_NAME
        ),
    replace_references()
    print "Done!"
    
    print "Generating new Django secret key... ",
    generate_key()
    print "Done!"
    
    print ""
    print "Configuration finished!"
    print "You may now remove this file (configure.py)."
    
    return 0
    
    
if __name__ == '__main__':
    sys.exit(main())
    