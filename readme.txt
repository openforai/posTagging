Master In Computer Science at University of Yaounde 1.

cmd:


python -u buildInitialData.py ../data brown 30 10 | tee ../data/brown/logs/buildInitialData24jan2014.log

python -u executeBLMRandTesting.py ../data brown | tee ../data/brown/logs/blm/rand24jan2014.log
python -u executeBLMCrossTesting.py ../data brown 10 | tee ../data/brown/logs/blm/cross24jan2014.log

python -u executeHMMRandTesting.py ../data brown | tee ../data/brown/logs/hmm/rand24jan2014.log
python -u executeHMMCrossTesting.py ../data brown 10 | tee ../data/brown/logs/hmm/cross24jan2014.log