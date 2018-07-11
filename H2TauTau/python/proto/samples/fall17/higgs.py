import copy
import re 
from CMGTools.RootTools.yellowreport.YRParser import yrparser13TeV
from CMGTools.RootTools.samples.ComponentCreator import ComponentCreator

creator = ComponentCreator()

HiggsGGH125 = creator.makeMCComponent('HiggsGGH125', '/GluGluHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
HiggsVBF125 = creator.makeMCComponent('HiggsVBF125', '/VBFHToTauTau_M125_13TeV_powheg_pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 'CMS', '.*root', 1.0)
HiggsTTH125 = creator.makeMCComponent('HiggsTTH125', '/ttHToNonbb_M125_TuneCP5_13TeV-powheg-pythia8/RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1/MINIAODSIM', 'CMS', '.*root', 1.0)


#############

mc_higgs = [
    HiggsVBF125,
    HiggsGGH125,
    HiggsTTH125
]

# Signals
sm_signals = [
    HiggsVBF125
]

# original sync list
sync_list = [
    HiggsVBF125
]

pattern = re.compile('Higgs(\D+)(\d+)')
for h in mc_higgs:
    m = pattern.match( h.name )
    process = m.group(1)
    
    isToWW = False 
    isInclusive = False
    if 'toWW' in process :
        process = process.replace('toWW', '')
        isToWW = True
    if 'Inclusive' in process:
        process = process.replace('Inclusive', '')
        isInclusive = True
          
    mass = float(m.group(2))
    xSection = 0.
    try:
        if process == 'VH':
            xSection += yrparser13TeV.get(mass)['WH']['sigma']
            xSection += yrparser13TeV.get(mass)['ZH']['sigma']
        else:
            xSection += yrparser13TeV.get(mass)[process]['sigma']
    except KeyError:
        print 'Higgs mass', mass, 'not found in cross section tables. Interpolating linearly at +- 1 GeV...'
        if process=='VH':
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)['WH']['sigma'] + xSection + yrparser13TeV.get(mass+1.)['WH']['sigma'])
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)['ZH']['sigma'] + yrparser13TeV.get(mass+1.)['ZH']['sigma'])
        else:
            xSection += 0.5 * (yrparser13TeV.get(mass-1.)[process]['sigma'] + yrparser13TeV.get(mass+1.)[process]['sigma'])

    if isToWW :
        br = yrparser13TeV.get(mass)['H2B']['WW']
    elif isInclusive:
        br = 1.
    else :
        br = yrparser13TeV.get(mass)['H2F']['tautau']
      
    h.xSection = xSection*br
    h.branchingRatio = br
    print h.name, 'sigma*br =', h.xSection, 'sigma =', xSection, 'br =', h.branchingRatio

