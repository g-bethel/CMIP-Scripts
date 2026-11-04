#!/usr/bin/env python3

import intake_esgf
from intake_esgf import ESGFCatalog

intake_esgf.conf.set(
    indices={
        "ESGF2-US-1.5-Catalog": False,
        "esgf.ceda.ac.uk": True,
        "esgf-data.dkrz.de": True,
        #"esgf-node.ipsl.upmc.fr": True,
    },
    local_cache="/quobyte/emoniergrp/CMIP5/esgf_cache",
    confirm_download=False,
)

base_search = dict(
    project="CMIP5",
    variable="tasmax",
    experiment="rcp45",
    time_frequency="day",
    ensemble="r1i1p1",
    cmor_table="day",
)

#model = "bcc-csm1-1-m"
institute = "BNU"

model_cat = ESGFCatalog()
model_cat.search(
    **base_search,
#    model=model,
    institute=institute,
)

print(model_cat)
model_cat.download_summary()

dsets = model_cat.to_dataset_dict(
    prefer_streaming=False,
    quiet=False,
)
