all:
	python bow.py
	./svm_multiclass_learn -c 1000 feats.train model
	svm_multiclass_classify feats.test model pred.out
	python evalustion.py