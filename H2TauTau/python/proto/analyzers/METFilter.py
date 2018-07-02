from PhysicsTools.Heppy.analyzers.core.Analyzer import Analyzer
from PhysicsTools.Heppy.analyzers.core.AutoHandle import AutoHandle

class METFilter(Analyzer):

    def __init__(self, cfg_ana, cfg_comp, looperName):
        super(METFilter, self).__init__(cfg_ana, cfg_comp, looperName)
        self.processName = getattr(self.cfg_ana, "processName", "HLT")
        self.triggers = cfg_ana.triggers
        self.autoAccept = True if len(self.triggers) == 0 else False

    def declareHandles(self):
        super(METFilter, self).declareHandles()
        self.handles['TriggerResults'] = AutoHandle(('TriggerResults', '', self.processName), 'edm::TriggerResults', fallbackLabel=('TriggerResults', '', 'RECO')) # fallback for data

    def beginLoop(self, setup):
        super(METFilter, self).beginLoop(setup)
        self.counters.addCounter('events')
        self.count = self.counters.counter('events')
        self.count.register('all events')
        for trigger in self.triggers:
            self.count.register('pass {t}'.format(t=trigger))


    def process(self, event):
        if self.autoAccept:
            return True

        self.readCollections(event.input)
        self.count.inc('all events')

        triggerBits = self.handles['TriggerResults'].product()
        names = event.input.object().triggerNames(triggerBits)

        for trigger_name in self.triggers:
            index = names.triggerIndex(trigger_name)

            if index == len(triggerBits):
                setattr(event, trigger_name, False)
                print 'WARNING, MET filter', trigger_name, 'not found in TriggerResults for processing step', self.processName 
                continue

            fired = triggerBits.accept(index)
            if fired:
                setattr(event, trigger_name, True)
                self.count.inc('pass {t}'.format(t=trigger_name))
            else:
                setattr(event, trigger_name, False)
    
        self.handles['badGlobalMuonTagger'].ReallyLoad(self.handles['badGlobalMuonTagger'].event)
        self.handles['cloneGlobalMuonTagger'].ReallyLoad(self.handles['cloneGlobalMuonTagger'].event)

        if not self.handles['badGlobalMuonTagger'].isValid() or not self.handles['cloneGlobalMuonTagger'].isValid():
            print 'WARNING: Bad global muon filter and clone global muon filters only work with CMSSW pre-sequence'
            event.passBadGlobalMuonFilter = True
            event.passcloneGlobalMuonFilter = True
            return True

        event.passBadGlobalMuonFilter = not self.handles['badGlobalMuonTagger'].product()[0]
        event.passcloneGlobalMuonFilter = not self.handles['cloneGlobalMuonTagger'].product()[0]
        if event.passBadGlobalMuonFilter:
            self.count.inc('bad global muon')
        if event.passcloneGlobalMuonFilter:
            self.count.inc('clone global muon')
        
        return True
