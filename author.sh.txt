#!/bin/bash
HOME_LOC=/public/ntungare2/python
	
THEANO_FLAGS=mode=FAST_RUN,device=gpu,floatX=float32 python word2vecAuthorLarge.py
