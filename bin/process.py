#!/usr/bin/env python3
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

import sys, yaml, getopt, re, subprocess

template_filename = '../templates/default.dot'
out_file = None
out_type = None

# CONSTANTS
VERSION='0.1'
VERSION_INFO='yauml v%s -- A script for generating UML diagrams from YAML file' % VERSION
HELP='yauml [OPTIONS] file\n\
\tfile: The YAML file to convert.\n\
OPTIONS:\n\
\t-o|--out out_file\n\
\t\tSpecifies the file to send output to (default: stdout)\n\
\t-T|--Type format\n\
\t\tThe type of file to generate (see dot(1)). Specifying this\n\
\t\twill automatically pass the output of yauml to dot. This option\n \
\t\thas to be used with -o.\n\
\t-t|--template template\n\
\t\tSepcifies the template file (default: %s).\n\
\t-h|--help\n\
\t\tDisplays this help text.' % template_filename
PROGRAM='yauml'


class DotStringBuilder(object):
    r"""
    """
    # Retrieves relations
    RELATION_FORMAT = '  edge [\n\ttaillabel = "%s"\n\theadlabel = "%s"\n  ]\n  node%s -> node%s;\n'
    CLASS_FORMAT = '  node%s [ label = "{%s | %s | %s}" ];\n\n'
    INTERFACE_FORMAT = '  node%s [ label = "{\<\<interface\>\>\\n%s | \\l | %s}" ];\n\n'

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

    def build_relation(self, relation):
        r"""
        Builds the appropriate relation string.

        INPUT:

            - ``relation`` -- The relation to look for in the data buffer.
        """
        relations = ''
        for entity in self._data:
            if relation in entity:
                for parent_string in entity[relation]:
                    parent = parent_multiplicity = child_multiplicity =  ''
                    for i,word in enumerate(parent_string.split()):
                        if i == 0:
                            parent = word
                        elif i == 1:
                            child_multiplicity = word.strip("[]")
                        elif i == 2:
                            parent_multiplicity = word.strip("[]")
                    relations += self.RELATION_FORMAT % (parent_multiplicity,child_multiplicity,\
                                                                    parent, entity['class'].split()[0])
        return relations


def build_out(template, builder):
    r"""
    Builds the apporpriate text output from the 
    YAML file.

    OUTPUT:

        A string.
    """
    out = ''
    done = {}
    done['CLASSES'] = done['INTERFACES'] = \
    done['USE RELATIONS'] = done['INHERIT RELATIONS'] = \
    done['ISPARTOF RELATIONS'] = done['IMPLEMENT RELATIONS'] = \
    done['SIMPLE RELATIONS'] = done['ISCONTAINEDBY RELATIONS'] = False
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
            out += builder.build_relation('uses')
            done['USE RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'INHERIT RELATIONS', line) and not done['INHERIT RELATIONS']:
            out += builder.build_relation('inherits')
            done['INHERIT RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'ISPARTOF RELATIONS', line) and not done['ISPARTOF RELATIONS']:
            out += builder.build_relation('ispartof')
            done['ISPARTOF RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'ISCONTAINEDBY RELATIONS', line) and not done['ISCONTAINEDBY RELATIONS']:
            out += builder.build_relation('iscontainedby')
            done['COMPOSITE RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'IMPLEMENT RELATIONS', line) and not done['IMPLEMENT RELATIONS']:
            out += builder.build_relation('implements')
            done['IMPLEMENT RELATIONS'] = True
        elif re.search(COMMENTED_RE % 'SIMPLE RELATIONS', line) and not done['SIMPLE RELATIONS']:
            out += builder.build_relation('associatedto')
            done['SIMPLE RELATIONS'] = True
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
    global yaml_filename, template, template_filename, out_file, out_type

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvt:o:T:", ["help","version","template=","out=","Type="])
    except getopt.GetoptError as err:
        print(str(err))
        print(HELP)
        sys.exit(1)

    for o,a in opts:
        if o in ("-v","--version"):
            print(VERSION_INFO)
            sys.exit(0)
        elif o in ("-T", "--type"):
            out_type = a
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

    if out_type and not out_file:
        print(PROGRAM+': -T option has to be used with -o')
        sys.exit(1)
    
    with open(template_filename, 'r') as template_file: 
        template = template_file.read()
    yaml_filename = args[0]

def main():
    getOptions()

    # Retrieve yaml data
    with open(yaml_filename) as yaml_file: 
        data = yaml.load(yaml_file.read())
    
    out_data = build_out(template, DotStringBuilder(data))
    f = sys.stdout
    #print output to stdout / file
    if out_file:
        try:
            f = open(out_file, 'w')
        except FileNotFoundError as e:
            print('%s: %s' % (PROGRAM, e), file=sys.stderr)

        #using dot directly
        if out_type:
            proc = subprocess.Popen(['dot','-T%s' % out_type,'-o%s' % out_file], stdin=subprocess.PIPE)
            proc.communicate(input=bytes(out_data, 'UTF-8'))
            sys.exit(0)

    print(out_data, file=f)

if __name__ == "__main__":
    main()
