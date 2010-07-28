#!/usr/bin/env python
"""

Usage:
        grammar.py file.grammar > grammar.yaml

"""
import re
import sys
from warnings import warn
import pprint

import yaml
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

def y(o):
    print yaml.dump(o, default_flow_style=False)
    return o

class GrammarModule():
    def __init__(self, input_path):
        dict = yaml.load(file(input_path))
        self.grammar = {}
        for k in dict:
            self.grammar[k] = self.transform(dict[k])

        # return   # without collapse regexps

        self.final = {}

        self.combinate_rule('document')

    def combinate_rule(self, rule):
        if rule in self.final:
            return
        object = self.final[rule] = self.grammar[rule]
        self.combinate_object(object)

    def combinate_object(self, object):
        if '+re' in object:
            self.combinate_re(object)
        elif '+rule' in object:
            rule = object['+rule']
            if rule in self.grammar:
                self.combinate_rule(rule)
        elif '+any' in object:
            for elem in object['+any']:
                self.combinate_object(elem)
        elif '+all' in object:
            for elem in object['+all']:
                self.combinate_object(elem)
        else:
            raise Exception("Can't combinate: %s" % object)

    def combinate_re(self, regexp):
        def f(m):
            n = m.groups()[0]
            if n in self.grammar:
                reo = self.grammar[n]
                if '+re' in reo:
                    return reo['+re']
            raise Exception("'%s' is not defined in the grammar" % n)

        while True:
            regexp2 = re.sub(r'<(\w+)>', f, regexp['+re'])
            if regexp2 == regexp['+re']:
                break
            regexp['+re'] = regexp2

    def transform(self, v):
        t = v.__class__.__name__
        if t == 'str':
            if v[0] == '/':
                return self.re(v)
            elif v[0] == '<':
                return self.rule(v)
            elif v[0] == '(':
                if re.search(r'[>/]\s*[</]', v):
                    return self.all_str(v)
                elif re.search(r'[>/]\s*\|\s*[</]', v):
                    return self.any_str(v)
                else:
                    raise Exception("'%s' is bad collection string" % v)
            else:
                raise Exception("'%s' is bad string" % v)
        elif t == 'list':
            return self.all(v)
        else:
            raise Exception("Unknown node: '%s'" % pprint.pformat(v, indent=2))

    def re(self, str):
        return { '+re': str[1:-1] }

    def rule(self, str):
        rule = {}
        if str[-1] in ['?', '*', '+']:
            rule['<'] = str[-1]
            str = str[0:-1]
        rule['+rule'] = str[1:-1]
        return rule

    def all_str(self, str):
        l = []
        all = {'+all': l }
        if str[-1] in ['?', '*', '+']:
            all['<'] = str[-1]
            str = str[0:-1]

        str = str[1:-1]
        m = re.match(r'\s*((?:<!?\w+>)|(?:/.*?/))\s*', str)
        while m:
            l.append(self.transform(m.groups()[0]))
            str = str[m.end():]
            m = re.match(r'\s*((?:<!?\w+>)|(?:/.*?/))\s*', str)
        return all

    def any_str(self, str):
        l = []
        any = {'+any': l }
        if str[-1] in ['?', '*', '+']:
            any['<'] = str[-1]
            str = str[0:-1]

        str = str[1:-1]
        m = re.match(r'\s*((?:<!?\w+>)|(?:/.*?/))\s*\|?\s*', str)
        while m:
            l.append(self.transform(m.groups()[0]))
            str = str[m.end():]
            m = re.match(r'\s*((?:<!?\w+>)|(?:/.*?/))\s*\|?\s*', str)
        return any

    def all(self, array):
        l = []
        all = {'+all': l}
        if array[-1] in ['?', '*', '+']:
            all['<'] = array.pop()
        for elem in array:
            l.append(self.transform(elem))
        return all

    def generate_yaml(self):
        return yaml.dump(self.final, default_flow_style=False);

if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise Exception(__doc__)
    grammar_file = sys.argv[1]
    print GrammarModule(grammar_file).generate_yaml()
