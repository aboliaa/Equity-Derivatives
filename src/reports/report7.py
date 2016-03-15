from math import *

def CND(X):
	(a1,a2,a3,a4,a5) = (0.31938153, -0.356563782, 1.781477937, -1.821255978, 1.330274429)
	L = abs(X)
	K = 1.0 / (1.0 + 0.2316419 * L)
	w = 1.0 - 1.0 / sqrt(2*pi)*exp(-L*L/2.) * (a1*K + a2*K*K + a3*pow(K,3) + a4*pow(K,4) + a5*pow(K,5))
	if X<0:
		w = 1.0-w
	return w

def BlackScholesImpliedVolatility(S, X, RF, T, YIELD, MPR, MAXERR, ch):
	'''
	Black-Scholes Function to calculate European option prices and Greeks
	S = stock price
	X = exercise price
	RF = risk-free rate
	T = time to expiration
	YIELD = dividend yield
	MPR = market price of option
	MAXERR = maximum acceptable difference between market price and model price
	ch = choice - see below
		 Put the choice word in quotes
		   call =   European call price
		   put =   European put price
	'''

	Diff = MAXERR + 1.0
	RF = RF / 100.0
	YIELD = YIELD / 100.0
	SIGGUESS = sqrt(abs(log(S * exp(-YIELD * T) / float(X)) + RF * T) * (2.0 / T))

	while 1:
		dsub1 = (log(S * exp(-YIELD * T) / float(X)) + (RF + pow(SIGGUESS,2) / 2.0) * T) / (SIGGUESS * sqrt(T))
		dsub2 = dsub1 - SIGGUESS * sqrt(T)
		Nd1 = CND(dsub1)
		Nd2 = CND(dsub2)

		if ch == "call":
			BSP = S * exp(-YIELD * T) * Nd1 - X * exp(-RF * T) * Nd2
		elif ch == "put":
			BSP = X * exp(-RF * T) * (1 - Nd2) - S * exp(-YIELD * T) * (1 - Nd1)

		Diff = abs(MPR - BSP)
		if Diff < MAXERR:
			break

		SIGGUESS = SIGGUESS - ((BSP - MPR) * exp(pow(-dsub1,2) / 2.0) * sqrt(2 * pi)) / (S * exp(-YIELD * T) * sqrt(T))
		
	BlackScholesImpliedVolatility = SIGGUESS
	return BlackScholesImpliedVolatility

def BlackScholesModelPrice(S, X, RF, T, SIGMA, YIELD, ch):
	'''
	Black-Scholes Function to calculate European 
	S = stock price
	X = exercise price
	RF = risk-free rate
	T = time to expiration
	YIELD = dividend yield
	SIGMA = standard deviation
	ch = choice - see below
		 Put the choice word in quotes
		   ecprice =   European call price
		   ecdelta =   European call delta
		   ecgamma =   European call gamma
		   ectheta =   European call theta
		   ecvega  =   European call vega
		   ecrho   =   European call rho
		   epprice =   European put price
		   epdelta =   European put delta
		   epgamma =   European put gamma
		   eptheta =   European put theta
		   epvega  =   European put vega
		   eprho   =   European put rho
		   eod1    =   European option d1
		   eod2    =   European option d2
		   eond1   =   European option Nd1
		   eond2   =   European option Nd2
	'''
	
	ModelPrice = 0.0

	if S == 0:
		if ch is "epprice":
			ModelPrice = X * exp(-RF * T)
		elif ch is "epdelta":
			ModelPrice = -1
		elif ch is "eptheta":
			ModelPrice = RF * X * exp(-RF * T)
		elif ch is "eprho":
			ModelPrice = -T * X * exp(-RF * T)
		elif ch is "eod1":
			ModelPrice = "- infinity"
		elif ch is "eod2":
			ModelPrice = "- infinity"

	elif T == 0:
		if ch is "ecprice":
			ModelPrice = (S-X) if S>X else 0.0
		elif ch is "ecdelta":
			ModelPrice = 1.0 if S>X else 0.0
		if ch is "epprice":
			ModelPrice = 0.0 if S>X else (X-S)
		elif ch is "epdelta":
			ModelPrice = 0.0 if S>=X else -1.0
		elif ch is "eond1":
			ModelPrice = 1.0 if S>X else 0.0
		elif ch is "eond2":
			ModelPrice = 1.0 if S>X else 0.0
		elif ch is "eod1":
			ModelPrice = "+ infinity" if S>X else "- infinity"
		elif ch is "eod2":
			ModelPrice = "+ infinity" if S>X else "- infinity"

	elif SIGMA == 0:
		e1 = (S) * exp(-YIELD * T)
		e2 = X * exp(-RF * T)
		if ch is "ecprice":
			if e1 > e2:
				ModelPrice = (S) * exp(-YIELD * T) - X * exp(-RF * T)
			else:
				ModelPrice = 0.0
		elif ch is "ecdelta":
			if e1 > e2:
				ModelPrice = exp(-YIELD * T)
			else:
				ModelPrice = 0.0
		elif ch is "ectheta":
			if e1 > e2:
				ModelPrice = -RF * X * exp(-RF * T) + YIELD * (S) * exp(-YIELD * T)
			else:
				ModelPrice = 0.0
		elif ch is "ecrho":
			if e1 > e2:
				ModelPrice = T * X * exp(-RF * T)
		elif ch is "epprice":
			if e1 > e2:
				ModelPrice = 0.0
			else:
				ModelPrice = X * exp(-RF * T) - (S) * exp(-YIELD * T)
		elif ch is "epdelta":
			if e1 >= e2:
				ModelPrice = 0.0
			else:
				ModelPrice = -exp(-YIELD * T)
		elif ch is "eptheta":
			if e1 > e2:
				ModelPrice = RF * X * exp(-RF * T) - YIELD * (S) * exp(-YIELD * T)
			else:
				ModelPrice = -exp(-YIELD * T)
		elif ch is "eprho":
			if e1 > e2:
				ModelPrice = -T * X * exp(-RF * T)
		elif ch is "eond1":
			if e1 > e2:
				ModelPrice = 1.0
			else:
				ModelPrice = 0.0
		elif ch is "eond2":
			if e1 > e2:
				ModelPrice = 1.0
			else:
				ModelPrice = 0.0
		elif ch is "eod1":
			if e1 > e2:
				ModelPrice = "+ infinity"
			else:
				ModelPrice = "- infinity"
		elif ch is "eod2":
			if e1 > e2:
				ModelPrice = "+ infinity"
			else:
				ModelPrice = "- infinity"

	else:
		dsub1 = (log((S) * exp(-YIELD * T) / float(X)) + (RF + pow(SIGMA,2) / 2.0) * T) / (SIGMA * sqrt(T))
		dsub2 = dsub1 - SIGMA * sqrt(T)
		Nd1 = CND(dsub1)
		Nd2 = CND(dsub2)

		Nprimed1 = (1.0 / sqrt(2 * pi)) * exp(pow(-dsub1,2) / 2.0)

		if ch is "ecprice":
			ModelPrice = (S) * exp(-YIELD * T) * Nd1 - X * exp(-RF * T) * Nd2
		elif ch is "epprice":
			ModelPrice = X * exp(-RF * T) * (1 - Nd2) - (S) * exp(-YIELD * T) * (1 - Nd1)
		elif ch is "ecdelta":
			ModelPrice = exp(-YIELD * T) * Nd1
		elif ch is "epdelta":
			ModelPrice = exp(-YIELD * T) * (Nd1 - 1)
		elif ch is "ecgamma":
			if S>0:
				ModelPrice = (exp(-YIELD * T) * Nprimed1) / ((S) * SIGMA * sqrt(T))
			else:
				ModelPrice = 0.0
		elif ch is "epgamma":
			if S>0:
				ModelPrice = (exp(-YIELD * T) * Nprimed1) / ((S) * SIGMA * sqrt(T))
			else:
				ModelPrice = 0.0
		elif ch is "ectheta":
			ModelPrice = -(S) * Nprimed1 * SIGMA * exp(-YIELD * T) / (2 * sqrt(T)) + YIELD * (S) * Nd1 * exp(-YIELD * T) - RF * X * exp(-RF * T) * Nd2
		elif ch is "eptheta":
			ModelPrice = -(S) * Nprimed1 * SIGMA * exp(-YIELD * T) / (2 * sqrt(T)) - YIELD * (S) * (1 - Nd1) * exp(-YIELD * T) + RF * X * exp(-RF * T) * (1 - Nd2)
		elif ch is "ecvega":
			ModelPrice = (S) * sqrt(T) * Nprimed1 * exp(-YIELD * T)
		elif ch is "epvega":
			ModelPrice = (S) * sqrt(T) * Nprimed1 * exp(-YIELD * T)
		elif ch is "ecrho":
			ModelPrice = X * T * exp(-RF * T) * Nd2
		elif ch is "eprho":
			ModelPrice = -X * T * exp(-RF * T) * (1 - Nd2)
		elif ch is "eod1":
			if S>0:
				ModelPrice = dsub1
			else:
				ModelPrice = "NA"
		elif ch is "eod2":
			if S>0:
				ModelPrice = dsub2
			else:
				ModelPrice = "NA"
		elif ch is "eond1":
			ModelPrice = Nd1
		elif ch is "eond2":
			ModelPrice = Nd2
	return ModelPrice

