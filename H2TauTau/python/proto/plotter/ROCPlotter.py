import ROOT

from CMGTools.H2TauTau.proto.plotter.officialStyle import setTDRStyle
setTDRStyle()

colours = [1, 1, 2, 4, 4, 6, 7, 8, 9, 47, 46, 44, 43, 42, 41, 40]
linestyles = [1, 2, 1, 1, 5, 6, 7, 8]
markers = [20, 21, 22, 23, 24, 25, 26, 27]

def histsToRoc(hsig, hbg):
    '''Produce ROC curve from 2 input histograms.
    Partly adapted from Giovanni's ttH code.
    '''
    nbins = hsig.GetNbinsX()+2 # include under/overflow
    si = [hsig.GetBinContent(i) for i in xrange(nbins)]
    bi = [hbg.GetBinContent(i) for i in xrange(nbins)]

    if hsig.GetMean() > hbg.GetMean():
        si.reverse()
        bi.reverse()

    sums, sumb = sum(si), sum(bi)
    if sums == 0 or sumb == 0:
        print 'WARNING: Either signal or background histogram empty', sums, sumb
        return None

    for i in xrange(1, nbins):
        si[i] += si[i-1]
        bi[i] += bi[i-1]
    fullsi, fullbi = si[:], bi[:]
    si, bi = [], []
    for i in xrange(1, nbins):
        # skip negative weights
        if len(si) > 0 and (fullsi[i] < si[-1] or fullbi[i] < bi[-1]):
            continue
        # skip repetitions
        if fullsi[i] != fullsi[i-1] or fullbi[i] != fullbi[i-1]:
            si.append(fullsi[i])
            bi.append(fullbi[i])

    if len(si) == 2: 
        si = [si[0]]
        bi = [bi[0]]

    bins = len(si)
    roc = ROOT.TGraph(bins)
    for i in xrange(bins):
        roc.SetPoint(i, si[i]/sums, bi[i]/sumb)

    return roc


def makeLegend(rocs, textSize=0.05, title=''):
    (x1, y1, x2, y2) = (.18, .76 - textSize*max(len(rocs)*1.6-3, 0), .5, .88)
    leg = ROOT.TLegend(x1, y1, x2, y2)
    leg.SetFillColor(0)
    leg.SetShadowColor(0)
    leg.SetLineColor(0)
    leg.SetLineWidth(0)
    leg.SetTextFont(42)
    leg.SetTextSize(textSize)
    if title:
        leg.AddEntry(None, title, '')
        leg.AddEntry(None, '', '')
    for key, roc in rocs:
        leg.AddEntry(roc, key, 'lp')
    leg.Draw()

    return leg

def makeROCPlot(rocs, set_name, ymin=0., ymax=1., xmin=0., xmax=1., logy=False,
                outdir='rocplots/', title=''):

    allrocs = ROOT.TMultiGraph(set_name, '')
    point_graphs = []
    i_marker = 0
    for i_col, (name, graph) in enumerate(zip([r.name for r in rocs], rocs)):
        col = colours[i_col]
        graph.SetLineColor(col)
        graph.SetMarkerColor(col)
        graph.SetLineWidth(4)
        graph.SetLineStyle(linestyles[i_col])
        graph.SetMarkerStyle(0)
        if graph.GetN() > 0:
            allrocs.Add(graph)
        else:
            graph.SetMarkerStyle(markers[i_marker])
            i_marker += 1
            graph.SetMarkerSize(1)
            point_graphs.append(graph)

    c = ROOT.TCanvas()
    if rocs[0].GetN()<5:
        allrocs.Draw('AP')
    else:
        allrocs.Draw('APL')

    allrocs.GetXaxis().SetTitle('#varepsilon_{s}')
    allrocs.GetYaxis().SetTitle('#varepsilon_{b}')
    allrocs.GetYaxis().SetDecimals(True)

    allrocs.GetYaxis().SetRangeUser(ymin, ymax)
    allrocs.GetXaxis().SetRangeUser(xmin, xmax)
    if ymin > 0. and logy:
        c.SetLogy()

    if rocs[0].GetN()<5:
        allrocs.Draw('AP')
    else:
        allrocs.Draw('APL')

    for graph in point_graphs:
        graph.Draw('P')

    allrocs.leg = makeLegend(zip([r.title for r in rocs], rocs), title=title)

    c.Print(outdir + set_name+'.pdf')

    return allrocs
