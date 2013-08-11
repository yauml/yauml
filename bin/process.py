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

import yaml, sys

# Retrieve arguments
yaml_filename = sys.argv[1]

# Retrieve template
template_file = open('../template/template.dot', 'r')
template = template_file.read()
template_file.close()

# Retrieve yaml data
with open(yaml_filename) as yaml_file: data = yaml.load(yaml_file.read())

# Retrieves classes
CLASS_FORMAT = """  %s [
    label = "{%s
    |%s|%s}"
  ]

"""

def make_raw(s):
    t = ''
    for c in s:
        if c == '<':
            t += '\<'
        elif c == '>':
            t += '\>'
        else:
            t += c
    return t

class_string = ''
for entity in data:
    if 'class' in entity:
        class_name = entity['class']
    else:
        raise ValueError, 'Class name is mandatory'
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
    class_string += CLASS_FORMAT % (class_name, class_name, attributes, methods)

# Retrieves relations
RELATION_FORMAT = "  %s -> %s;\n"
# Inheritance
inheritances = ''
for entity in data:
    if 'inherits' in entity:
        for parent in entity['inherits']:
            inheritances += RELATION_FORMAT % (parent, entity['class'])
# Is-part-of
ispartofs = ''
for entity in data:
    if 'ispartof' in entity:
        for parent in entity['ispartof']:
            ispartofs += RELATION_FORMAT % (parent, entity['class'])
# Uses
uses = ''
for entity in data:
    if 'uses' in entity:
        for parent in entity['uses']:
            uses += RELATION_FORMAT % (parent, entity['class'])

print template % (class_string, inheritances, ispartofs, uses)
