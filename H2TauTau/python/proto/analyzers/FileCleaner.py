import os
from shutil import copyfile

from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer


class FileCleaner(Analyzer):

    '''Gets rid of the preprocessed rootfile, or saves it somewhere if needed'''

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(FileCleaner, self).__init__(cfg_ana, cfg_comp, looperName)

    def process(self, event):
        pass

    def endLoop(self, setup):
        print self, self.__class__
        super(FileCleaner, self).endLoop(setup)
        for comp in setup.config.components:
            for f in comp.files:
                if hasattr(self.cfg_ana, 'savepreproc') and self.cfg_ana.savepreproc:
                    if not os.path.exists('preprocessed_files/'+comp.name):
                        os.makedirs('preprocessed_files/'+comp.name)
                    copyfile(f,'preprocessed_files/'+comp.name+'/cmsswPreProcessing.root')
                os.remove(f)
