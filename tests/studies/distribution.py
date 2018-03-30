#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ROOT import(s)
import ROOT

# Project import(s)
from .common import *
from adversarial.utils import mkdir, latex, wpercentile
from adversarial.profile import profile
from adversarial.constants import *

# Custom import(s)
import rootplotting as rp


@profile
def study_distribution (data, args, feat):
    """
    ...
    """

    # Define bins
    if 'knn' in feat.lower():
        xmin, xmax = -1, 2
    elif 'NN' in feat or 'tau21' in feat.lower() or 'boost' in feat.lower():
        xmin, xmax = 0., 1.
    elif feat == 'D2':
        xmin, xmax = 0, 3.5
    else:
        xmin = wpercentile (data[feat].values,  1, weights=data['weight'].values)
        xmax = wpercentile (data[feat].values, 99, weights=data['weight'].values)
        pass

    bins = np.linspace(xmin, xmax, 50 + 1, endpoint=True)

    # Canvas
    c = rp.canvas(batch=not args.show)

    # Plots
    ROOT.gStyle.SetHatchesLineWidth(3)
    c.hist(data.loc[(data['signal'] == 0), feat].values, bins=bins,
           weights=data.loc[(data['signal'] == 0), 'weight'].values,
           alpha=0.5, fillcolor=rp.colours[1], label="QCD jets", normalise=True,
           fillstyle=3445, linewidth=3, linecolor=rp.colours[1])
    c.hist(data.loc[(data['signal'] == 1), feat].values, bins=bins,
           weights=data.loc[(data['signal'] == 1), 'weight'].values,
           alpha=0.5, fillcolor=rp.colours[5], label="#it{W} jets", normalise=True,
           fillstyle=3454, linewidth=3, linecolor=rp.colours[5])

    # Decorations
    ROOT.gStyle.SetTitleOffset(1.6, 'y')
    c.xlabel("Large-#it{R} jet " + latex(feat, ROOT=True))
    c.ylabel("Fraction of jets")
    c.text(["#sqrt{s} = 13 TeV",
            "Testing dataset",
            "Baseline selection",
            ],
        qualifier=QUALIFIER)
    c.ylim(2E-03, 2E+00)
    c.logy()
    c.legend()

    # Save
    if args.save:
        mkdir('figures/')
        c.save('figures/distribution_{}.pdf'.format(standardise(feat)))
        pass

    # Show
    if args.show:
        c.show()
        pass

    return
