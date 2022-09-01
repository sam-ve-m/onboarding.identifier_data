#!/bin/bash
fission spec init
fission env create --spec --name identifier-data-env --image nexus.sigame.com.br/fission-async:0.1.6 --builder nexus.sigame.com.br/fission-builder-3.8:0.0.1
fission fn create --spec --name identifier-data-fn --env identifier-data-env --src "./func/*" --entrypoint main.user_identifier_data --executortype newdeploy --maxscale 1
fission route create --spec --name identifier-data-rt --method PUT --url /onboarding/identifier_data --function identifier-data-fn
