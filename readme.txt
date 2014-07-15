Master In Computer Science at University of Yaounde 1.

	Extraction des données : 
 
		      
			$ python -u buildInitialData.py data_folder brown NB_DATA TEST_PERCENTAGE VALIDATION_PERCENTAGE k
		  
			- python	:	nom de la commande python.
			- u	:	option python qui permet de ne pas conserver dans le cache les sorties du fichier exécuté.
			- buildInitialData.py	:	nom du fichier python qui permet d'exécuter le générateur de résultats.
			- data\_folder	:	dossier dans lequel se trouve le jeu de données.
			- brown	:	 indique que les tests doivent avoir lieu sur le Brown corpus.
			- NB\_DATA	:	 nombre de phrase à considérer pour ce jeu de données.
			- TEST\_PERCENTAGE	:	 pourcentage du jeu de données de test.
			- VALIDATION\_PERCENTAGE	:	 pourcentage du jeu de données de validation pour l'apprentissage avec le réseau de neurones élastique.
			- k	:	 nombre de dossiers pour un k-cross test.
		  
			
		  D'où les commandes ci-après ont été utilisées pour le cross test et le test simple respectivement : 
			
			  $ python -u buildInitialData.py ../data brown 8000 25 25 0  | tee ../data/brown/logs/build/build_8000.log
			
			
		  et
			
			
			  $ python -u buildInitialData.py ../data brown 500 25 25 0 tee ../data/brown/logs/build/build_8000.log
			
			
			
		  Où $NB\_DATA$ prend tour à tour les valeurs : 500, 1000, 2000, 4000, 8000, 16000, 32000, 56000 (ces différents jeux de données ont été utilisés pour les tests de la section \ref{subsect:evolutiveTest).
		 
 
	Exécution du test simple : 
		  
		      
			$ python -u fichier.py data_folder brown TRAIN [BATCH]
		  
  
		  
			- python	: nom de la commande python.
			- u		:	option python qui permet de ne pas conserver dans le cache les sorties du fichier exécuté.
			- fichier.py	: 	nom du fichier python qui permet d'exécuter un test simple de l'étiqueteur concerné (executeBLMRandTesting.py, executeENNRandTesting.py, executeHMMRandTesting.py, executeSECOHMMRandTesting.py).
			- data\_folder	: dossier dans lequel se trouve le jeu de données.
			- brown : indique que les tests doivent avoir lieu sur le Brown corpus.
			- TRAIN : qui peut prendre l'une des valeurs true ou false. Une valeur false indique que le modèle sera lu dans un fichier tandis que true indique que le modèle sera construit à partir du jeux de données et ensuite sera sauvegardé dans un fichier.
			- BATCH : qui peut prendre l'une des valeurs true ou false (dans le cas spécifique du réseau de neurones élastique). Une valeur true indique que l'apprentissage en mode batch sera appliqué tandis que false indique que l'apprentissage en mode séquentiel sera appliqué.
		  
			
		  D'où les commandes ci après ont été utilisées : 
		  
				$ python -u executeBLMRandTesting.py ../data/500 brown true | tee ../data/500/brown/logs/blm/blmRand.log
				$ python -u executeENNRandTesting.py ../data/500 brown true	true | tee ../data/500/brown/logs/enn/ennRand.log
				$ python -u executeSECOHMMRandTesting.py ../data/500 brown true  tee ../data/500/brown/logs/secohmm/secohmmRand.log
				$ python -u executeHMMRandTesting.py ../data/500 brown true | tee ../data/500/brown/logs/hmm/hmmRand.log
			
			
		  Pour chaque jeu de données le $data\_folder$ est remplacé par le dossier approprié : ../data/500, ../data/1000, ../data/2000, ../data/4000, ../data/8000, ../data/16000 (ces différents jeux de données ont été utilisés pour les tests de la section \ref{subsect:evolutiveTest).
		  
  
	Exécution du k-cross test : 
		  
		      
			$ python -u fichier.py data_folder brown k TRAIN [BATCH]
		  
		  
		  
			- python	:	nom de la commande python.
			- u		:	option python qui permet de ne pas conserver dans le cache les sorties du fichier exécuté.
			- fichier.py	: 	nom du fichier python qui permet d'exécuter un cross test de l'étiqueteur concerné (executeBLMCrossTesting.py, executeENNCrossTesting.py, executeHMMCrossTesting.py, executeSECOHMMCrossTesting.py).
			- data\_folder	: dossier dans lequel se trouve le jeu de données.
			- brown : indique que les tests doivent avoir lieu sur le Brown corpus
			- k : nombre de dossiers pour un k-cross test.
			- TRAIN : qui peut prendre l'une des valeurs true ou false. Une valeur false indique que le modèle sera lu dans un fichier tandis que true indique que le modèle sera construit à partir du jeu de données et ensuite sera sauvegardé dans un fichier.
			- BATCH : qui peut prendre l'une des valeurs true ou false (dans le cas spécifique du réseau de neurones élastique). Une valeur true indique que l'apprentissage en mode batch sera appliqué tandis que false indique que l'apprentissage en mode séquentiel sera appliqué.
			
			D'où les commandes ci après ont été utilisées pour le cross test : 
			 
			  python -u executeBLMCrossTesting.py ../data brown 4 true | tee ../data/brown/logs/blm/cross.log
			  python -u executeENNCrossTesting.py ../data brown 4 true true | tee ../data/brown/logs/enn/cross.log
			  python -u executeHMMCrossTesting.py ../data brown 4 true | tee ../data/brown/logs/hmm/cross.log
			  python -u executeSECOHMMCrossTesting.py ../data brown 4 true | tee ../data/brown/logs/secohmm/cross.log
						
		  

	Analyse des résultats :  
		  
		      
			$ python -u resultAnalyser.py data_folder brown k NBMOSTPOS MODEL TYPE	  
		  
		  
		  
			- python	:	nom de la commande python.
			- u		:	option python qui permet de ne pas conserver dans le cache les sorties du fichier exécuté.
			- resultAnalyser.py	: 	nom du fichier python qui permet d'exécuter la génération des résultats.
			- data\_folder	: dossier dans lequel se trouve le jeu de données.
			- brown : indique que les tests doivent avoir lieu sur le Brown corpus.
			- k : nombre de dossier disponible pour le k-cross test. Dans le cas où le paramètre $TYPE$ prend la valeur ONECROSS, il représente le numéro du dossier cross à évaluer.
			- NBMOSTPOS : nombre d'étiquettes à considérer pour le cas des étiquettes les plus fréquentes.
			- MODEL : qui peut prendre l'une des valeurs BLM, ENN, HMM, SECHMM en fonction de l'étiqueteur visé.
			- TYPE : qui peut prendre l'une des valeurs ALLCROSS (évaluer tout le k-cross test), ONECROSS (évaluer le dossier cross k), RAND (évaluer un test simple).
		  
			
		  D'où les commandes ci après ont été utilisées pour l'analyse des résultats du k-cross test : 
			 
			  python -u resultAnalyser.py ../data brown 4 5 BLM ALLCROSS | tee ../data/brown/testResult/resCross_BLM.log
			  python -u resultAnalyser.py ../data brown 4 5 ENN ALLCROSS | tee ../data/brown/testResult/resCross_ENN.log
			  python -u resultAnalyser.py ../data brown 4 5 HMM ALLCROSS | tee ../data/brown/testResult/resCross_HMM.log
			  python -u resultAnalyser.py ../data brown 4 5 SECHMM ALLCROSS | tee ../data/brown/testResult/resCross_SECHMM.log
			
			
		  et pour l'analyse des résultats d'un test simple
			
			
			  python -u resultAnalyser.py ../data/500 brown 4 5 BLM RAND | tee ../data/500/brown/testResult/resRand_BLM.log
			  python -u resultAnalyser.py ../data/500 brown 4 5 ENN RAND | tee ../data/500/brown/testResult/resRand_ENN.log
			  python -u resultAnalyser.py ../data/500 brown 4 5 HMM RAND | tee ../data/500/brown/testResult/resRand_HMM.log
			  python -u resultAnalyser.py ../data/500 brown 4 5 SECHMM RAND | tee ../data/500/brown/testResult/resRand_SECHMM.log
			
			
		  Pour chaque jeu de données le $data\_folder$ est remplacé par le dossier approprié : ../data/500, ../data/1000, ../data/2000, ../data/4000, ../data/8000, ../data/16000 (ces différents jeux de données ont été utilisés pour les tests de la section \ref{subsect:evolutiveTest).
	  
