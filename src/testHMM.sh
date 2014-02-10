#python -u executeHMMRandTesting.py ../data/brown/1000 brown | tee ../data/brown/1000/brown/logs/hmm/rand09fev-1000.log
#python -u executeHMMCrossTesting.py ../data/brown/1000 brown 10 | tee ../data/brown/1000/brown/logs/hmm/cross09fev-1000.log

#python -u executeHMMRandTesting.py ../data/brown/2000 brown | tee ../data/brown/2000/brown/logs/hmm/rand09fev-2000.log
#python -u executeHMMCrossTesting.py ../data/brown/2000 brown 10 | tee ../data/brown/2000/brown/logs/hmm/cross09fev-2000.log

#python -u executeHMMRandTesting.py ../data/brown/4000 brown | tee ../data/brown/4000/brown/logs/hmm/rand09fev-4000.log
#python -u executeHMMCrossTesting.py ../data/brown/4000 brown 10 | tee ../data/brown/4000/brown/logs/hmm/cross09fev-4000.log

#python -u executeHMMRandTesting.py ../data/brown/8000 brown | tee ../data/brown/8000/brown/logs/hmm/rand09fev-8000.log
#python -u executeHMMCrossTesting.py ../data/brown/8000 brown 10 | tee ../data/brown/8000/brown/logs/hmm/cross09fev-8000.log

#python -u executeHMMRandTesting.py ../data/brown/16000 brown | tee ../data/brown/16000/brown/logs/hmm/rand09fev-16000.log
#python -u executeHMMCrossTesting.py ../data/brown/16000 brown 10 | tee ../data/brown/16000/brown/logs/hmm/cross09fev-16000.log

#python -u executeHMMRandTesting.py ../data/brown/32000 brown | tee ../data/brown/32000/brown/logs/hmm/rand09fev-32000.log
#python -u executeHMMCrossTesting.py ../data/brown/32000 brown 10 | tee ../data/brown/32000/brown/logs/hmm/cross09fev-32000.log

#python -u executeHMMRandTesting.py ../data/brown/60000 brown | tee ../data/brown/60000/brown/logs/hmm/rand09fev-60000.log
#python -u executeHMMCrossTesting.py ../data/brown/60000 brown 10 | tee ../data/brown/60000/brown/logs/hmm/cross09fev-60000.log

python -u executeHMMCrossTesting.py ../data/ brown 4 | tee ../data/brown/logs/hmm/cross09fev-8000.log

