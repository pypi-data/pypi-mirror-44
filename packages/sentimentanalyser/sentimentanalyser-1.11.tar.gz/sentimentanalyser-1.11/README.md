# sentiment-analyser-lib


To run the package from commandline

pip install sentimentanalyser

from sentimentanalyser import train
do mention your own paths to the datasets instead of the paths mentioned below

filePath="/Users/amirulislam/Desktop/training_datasets/twitter_train.csv"

outputDir="/Users/amirulislam/Desktop/outputs"

trainObj=train.Train()

trainObj.train_file_model(filePath,outputDir)

from sentimentanalyser import train

filePath="/Users/amirulislam/Desktop/training_datasets/bbc_train.csv"

outputDir="/Users/amirulislam/Desktop/outputs"

trainObj=train.Train()

trainObj.train_file_model(filePath,outputDir)

from sentimentanalyser import test

testText=""

test_file_name="/Users/amirulislam/Desktop/testing_datasets/twitter_test.csv"

test_reference_file="twitter_train"

outputDir="/Users/amirulislam/Desktop/outputs"

testObj=test.TestData()

testedDataFrame=testObj.test_model(testText,test_file_name,test_reference_file,outputDir)

from sentimentanalyser import test

testText=""

test_file_name="/Users/amirulislam/Desktop/testing_datasets/bbc_test.csv"

test_reference_file="bbc_train"

outputDir="/Users/amirulislam/Desktop/outputs"

testObj=test.TestData()

testedDataFrame=testObj.test_model(testText,test_file_name,test_reference_file,outputDir)
Utilization of package in Django application

Go to project feedprocessor

Run: python manage.py runserver

Upload training dataset at

http://localhost:8000/sentiment/models/train/

Then test with your dataset at

http://localhost:8000/sentiment/models/test/
