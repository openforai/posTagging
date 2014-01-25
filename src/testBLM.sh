python -u executeBLMRandTesting.py ../data brown | tee ../data/brown/logs/blm/rand24jan2014.log
python -u executeBLMCrossTesting.py ../data brown 10 | tee ../data/brown/logs/blm/cross24jan2014.log
