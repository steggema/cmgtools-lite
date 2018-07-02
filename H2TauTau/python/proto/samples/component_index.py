import imp
import pprint
import collections
import fnmatch
from types import ModuleType
import PhysicsTools.HeppyCore.framework.config as cfg
from PhysicsTools.HeppyCore.framework.config import Component

def representation(comp):
    return '{}:{}'.format(comp.name, comp.dataset)
Component.__repr__ = representation

class ComponentIndex(object):

    def __init__(self, fname):
        mod = fname
        if not isinstance(mod, ModuleType):
            with open(fname) as ifile:
                mod = imp.load_source('mod', fname, ifile)
        self.components = dict()
        self.lists = dict()
        for attr in dir(mod):
            obj = getattr(mod, attr)
            if isinstance(obj, cfg.Component):
                self.components[attr] = obj
            if isinstance(obj, list) and \
                    len(obj) and \
                    isinstance(obj[0],cfg.Component):
                for comp in obj:
                    self.components[comp.name] = comp
                self.lists[attr]=obj
    
    def glob(self, pattern):
        result = []
        for name, comp in self.components.iteritems():
            if comp in result:
                continue
            if fnmatch.fnmatch(name, pattern) or \
                    fnmatch.fnmatch(comp.dataset, pattern):
                result.append(comp)
        result.sort(key=lambda x:x.name)
        for name, lst in self.lists.iteritems():
            if fnmatch.fnmatch(name, pattern):
                result.extend(lst)
        # the following is important, as 
        # a dataset could be present in several lists.
        result = sorted(list(set(result)))
        return result

    def __str__(self):
        return pprint.pformat(self.components)


if __name__=='__main__':
    import sys

    if len(sys.argv)!=2:
        print 'usage: component_index <sample module>'
        sys.exit(1)
    fname = sys.argv[1]
    index = ComponentIndex(fname)
    print index
