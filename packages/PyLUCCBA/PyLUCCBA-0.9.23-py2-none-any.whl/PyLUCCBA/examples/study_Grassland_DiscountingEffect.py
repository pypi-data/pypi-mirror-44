# -*- coding: utf8 -*-
from __future__ import print_function
from PyLUCCBA.examples import studies_constant_settings as cs
import PyLUCCBA as cc


scenarizer = lambda rate : cc.CBACalculator(
    run_name               = 'Grassland-Cropland_DR=%s_CP=O'%rate,
    project_horizon        = 20,
    T_so                   = 20,
    T_vg_diff              = 1,
    T_vg_unif              = 20,
    discount_rate          = rate,
    co2_prices_scenario    = 'O',
    initial_landuse        = 'improved grassland',
    final_landuse          = 'wheat',
    input_flows_scenario   = 'IFP',
    **cs.other_parameters
)

discount_rates = [.0, .03, .045]

objects = {}
for d_rate in discount_rates:    
    cba = scenarizer(d_rate)
    objects[cba.run_name] = {'summary':cba.summary_args,'object':cba}



print(u"""
*******************************************************************************
            ╔═╗┬ ┬┌┬┐┌┬┐┌─┐┬─┐┬┌─┐┌─┐                                         *
            ╚═╗│ │││││││├─┤├┬┘│├┤ └─┐                                         *
            ╚═╝└─┘┴ ┴┴ ┴┴ ┴┴└─┴└─┘└─┘                                         *
*******************************************************************************""")
for run_name, dico in objects.items():
    print(dico['summary'])
    dico['object'].all_XLSXed
