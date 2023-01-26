fission spec init
fission env create --spec --name onb-br-identifier-env --image nexus.sigame.com.br/fission-onboarding-br-identifier-data:0.1.1 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-identifier-fn --env onb-br-identifier-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --name onb-br-identifier-rt --method PUT --url /onboarding/identifier_data --function onb-br-identifier-fn
