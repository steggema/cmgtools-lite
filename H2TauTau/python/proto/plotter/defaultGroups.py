def createDefaultGroups(plot):
    plot.Group('VV', ['VVTo2L2Nu', 'WWTo2L2Nu', 'ZZTo2L2Nu', 'ZZTo2L2Q', 'WWTo1L1Nu2Q', 'WZTo1L3Nu', 'ZZTo4L', 'WZTo3L', 'WZTo2L2Q', 'WZTo1L1Nu2Q', 'T_tWch_noFullyHad', 'TBar_tWch_noFullyHad', 'TToLeptons_tch_powheg', 'TBarToLeptons_tch_powheg'], silent=True)
    plot.Group('TT', ['TTLep_pow', 'TTHad_pow', 'TTSemi_pow'])
    plot.Group('ZTT', ['ZTT', 'ZTT1Jets', 'ZTT2Jets', 'ZTT3Jets', 'ZTT4Jets', 'ZTTM150', 'ZTTM10'], silent=True)
    plot.Group('ZJ', ['ZJ', 'ZJ1Jets', 'ZJ2Jets', 'ZJ3Jets', 'ZJ4Jets', 'ZJM150', 'ZJM10'], silent=True)
    plot.Group('ZL', ['ZL', 'ZL1Jets', 'ZL2Jets', 'ZL3Jets', 'ZL4Jets', 'ZLM150', 'ZLM10'], silent=True)
