python -u executeHMMRandTesting.py ../data brown | tee ../data/brown/logs/hmm/rand24jan2014.log
python -u executeHMMCrossTesting.py ../data brown 10 | tee ../data/brown/logs/hmm/cross24jan2014.log
