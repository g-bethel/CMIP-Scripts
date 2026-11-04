#!/usr/bin/env python3

import os
os.umask(0o007)

import intake_esgf
from intake_esgf import ESGFCatalog

intake_esgf.conf.set(
    indices={
        "ESGF2-US-1.5-Catalog": False,
        "esgf.ceda.ac.uk": True,
        "esgf-data.dkrz.de": True,
        "esgf-node.ipsl.upmc.fr": True,
    },
    local_cache="/quobyte/emoniergrp/CMIP5/esgf_cache",
    confirm_download=False,
)

base_search = dict(
    project="CMIP5",
    variable="tasmin",
    experiment="rcp85",
    time_frequency="day",
    ensemble="r1i1p1",
    cmor_table="day",
)

# First catalog: only used to discover available models
cat = ESGFCatalog()
cat.search(**base_search)

print("Full search:")
print(cat)
cat.download_summary()

# Get unique model names from the search results
df = cat.df.copy()
models = sorted(df["model"].dropna().unique())

print(f"\nFound {len(models)} models:")
for model in models:
    print(" ", model)

# Download one model at a time
for i, model in enumerate(models, start=1):
    print("\n" + "=" * 80)
    print(f"Downloading model {i}/{len(models)}: {model}")
    print("=" * 80)

    model_cat = ESGFCatalog()
    model_cat.search(
        **base_search,
        model=model,
    )

    print(model_cat)
    model_cat.download_summary()

    try:
        dsets = model_cat.to_dataset_dict(
            prefer_streaming=False,
"esgf-intake.py" 73L, 1583B                                                                                                                                                             1,20          Top
