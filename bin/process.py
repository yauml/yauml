#!/usr/bin/env python
# coding=utf-8
r"""
Creating UML diagrams from YAML files.

AUTHORS:

- Alexandre Blondin Massé
- Simon Désaulniers
"""
#************************************************************************************
#  Copyright (C) 2013 Alexandre Blondin Massé <alexandre.blondin.masse@gmail.com    *
#                     Simon Désaulniers <rostydela@gmail.com>                       *
#                                                                                   *
#  Distributed under the terms of the GNU General Public License version 2 (GPLv2)  *
#                                                                                   *
#  The full text of the GPLv2 is available at:                                      *
#                                                                                   *
#                  http://www.gnu.org/licenses/                                     *
#************************************************************************************

import yaml, sys, getopt, re

template_filename = '../template/template.dot'
out_file = None

# CONSTANTS
VERSION='0.1'
VERSION_INFO='yauml v%s -- A script for generating UML diagrams from YAML file' % VERSION
HELP='yauml [OPTIONS] file\n\
\tfile: The YAML file to convert.\n\
OPTIONS:\n\
\t-o|--out out_file\n\
\t\tSpecifies the file to send output to (default: stdout)\n\
\t-t|--template template\n\
\t\tSepcifies the template file (default: %s).\n\
\t-h|--help\n\
\t\tDisplays this help text.' % template_filename
PROGRAM='yauml'


class DotStringBuilder(object):
    r"""
    """
    # Retrieves relations
    RELATION_FORMAT = "  node%s -> node%s;\n"
    CLASS_FORMAT = '  node%s [\n\tlabel = "{%s\n\t|%s|%s}"\n  \n  ]\n\n'
    INTERFACE_FORMAT = '  node%s [\n\tlabel = "{\<\<interface\>\>\\n%s\n\t|\\l|%s}"\n  ]\n\n'

    def __init__(self, data):
        self._data = data

    def build_classes(self):
        r"""
        Builds the class ndoes string.
        """
        class_string = ''
        for entity in self._data:
            if 'class' in entity:
                class_name = make_raw(entity['class'])
        
                attributes = ''
                if 'attributes' in entity:
                    for attribute in entity['attributes']:
                        attributes += '%s\\l' % make_raw(attribute)
                else:
                    attributes += '\\l'
                methods = ''
                if 'methods' in entity:
                    for method in entity['methods']:
                        methods += '%s\\l' % make_raw(method)
                else:
                    methods += '\\l'
                class_string += self.CLASS_FORMAT % (class_name.split()[0], class_name, attributes, methods)

        return class_string

    def build_interfaces(self):
        """
        Builds the interface nodes string.
        """
        interface_string = ''
        for entity in self._data:
            if 'interface' in entity:
               interface_name = entity['interface']
               
               methods = ''
               if 'methods' in entity:
                   for method in entity['methods']:
                       methods += '%s\\l' % make_raw(method)
               else:
                   methods += '\\l'

               interface_string += self.INTERFACE_FORMAT % (interface_name, interface_name, methods)

        return interface_string

    def build_uses(self):
        r"""
        Builds the "uses" nodes string.
        """
        # Uses
        uses = ''
        for entity in self._data:
            if 'uses' in entity:
                for parent in entity['uses']:
                    uses += self.RELATION_FORMAT % (parent, entity['class'].split()[0])
        return uses

    def build_inherits(self):
        r"""
        Builds the "inherits" nodes string.
        """
        # Inheritance
        inheritances = ''
        for entity in self._data:
            if 'inherits' in entity:
                for parent in entity['inherits']:
                    inheritances += self.RELATION_FORMAT % (parent, entity['class'].split()[0])
        return inheritances

    def build_is_part_of(self):
        r"""
        Builds the "is part of"  nodes string.
        """
        # Is-part-of
        ispartofs = ''
        for entity in self._data:
            if 'ispartof' in entity:
                for parent in entity['ispartof']:
                    ispartofs += self.RELATION_FORMAT % (parent, entity['class'].split()[0])
        return ispartofs

    def build_implements(self):
        r"""
        Builds the "implements" nodes string.
        """
        # Implements
        implements = ''
        for entity in self._data:
            if 'implements' in entity:
                for parent in entity['implements']:
                    implements += self.RELATION_FORMAT % (parent, entity['class'].split()[0])
        return implements

def build_out(template, builder):
    r"""
    Builds the apporpriate text output from the 
    YAML file.

    OUTPUT:

        A string.
    """
    out = ''
    done = {}
    done['CLASSES'], done['INTERFACES'], \
    done['USE RELATIONS'], done['INHERIT RELATIONS'], \
    done['ISPARTOF RELATIONS'], done['IMPLEMENT RELATIONS'] = False,False,False,False,False,False
    COMMENTED_RE = '//.*%s'

    for line in template.split(sep='\n'):
        out += line + '\n'
        if re.search(COMMENTED_RE % 'CLASSES',line) and not done['CLASSES']:
            out += builder.build_classes()
            done['CLASSES'] = True
        elif re.search(COMMENTED_RE % 'INTERFACES',line) and not done['INTERFACES']:
            out += builder.build_interfaces()
            done['INTERFACES'] = True
        elif re.search(COMMENTED_RE % 'USE RELATIONS',line) and not done['USE RELATIONS']:
            out += builder.build_uses()
            done['USE RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'INHERIT RELATIONS', line) and not done['INHERIT RELATIONS']:
            out += builder.build_inherits()
            done['INHERIT RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'ISPARTOF RELATIONS', line) and not done['ISPARTOF RELATIONS']:
            out += builder.build_is_part_of()
            done['ISPARTOF RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'IMPLEMENT RELATIONS', line) and not done['IMPLEMENT RELATIONS']:
            out += builder.build_implements()
            done['IMPLEMENT RELATIONS'] = True
    return out

def make_raw(s):
    special_dictionnary = {'<','>','{','}','[',']'}
    t = ''
    for c in s:
        if c in special_dictionnary:
            t += '\\'+c
        else:
            t+=c
    return t
   
def getOptions():
    r"""
    Gets all options at command line.
    """
    global yaml_filename, template, template_filename, out_file

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvt:o:", ["help","version","template=","out="])
    except getopt.GetoptError as err:
        print(str(err))
        print(HELP)
        sys.exit(1)

    for o,a in opts:
        if o in ("-v","--version"):
            print(VERSION_INFO)
            sys.exit(0)
        elif o in ("-o","--out"):
            out_file = a
        elif o in ("-h","--help"):
            print(HELP)
            sys.exit(0)
        elif o in ("-t","--template"):
            template_filename = a
        else:
            assert False
            
    if len(args) < 1:
        print(PROGRAM+': an argument is missing.')
        sys.exit(1)
    
    with open(template_filename, 'r') as template_file: 
        template = template_file.read()
    yaml_filename = args[0]

def main():
    getOptions()

    # Retrieve yaml data
    with open(yaml_filename) as yaml_file: 
        data = yaml.load(yaml_file.read())

    f = sys.stdout
    #print output to stdout / file
    if out_file:
        try:
            f = open(out_file, 'w')
        except FileNotFoundError as e:
            print('%s: %s' % (PROGRAM, e), file=sys.stderr)
    print(build_out(template, DotStringBuilder(data)), file=f)

if __name__ == "__main__":
    main()
