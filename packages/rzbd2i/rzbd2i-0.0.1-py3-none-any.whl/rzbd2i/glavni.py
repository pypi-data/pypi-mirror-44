import xlwings as xw

# from mymodule import myfunctions as mf

from .mymodule import myfunctions as mf

def probaNEW():		
	"""Retourne Bonjour nom """
	#~app1 = xw.App()	
	return mf.proba();
	# return 'Bonjour svi !'

@xw.func
@xw.arg('nom', doc="Nom de la personne")
def hello1(nom):		
	"""Retourne Bonjour nom """
	#~app1 = xw.App()
	m = 1
	return 'Dobar dan {1}  {0}'.format(nom,m)
	



@xw.func
def hello2():		
	"""Retourne Bonjour nom """
	#~app1 = xw.App()	
	#return 'Bonjour {1}  {0}'.format(nom,m)
	return mf.proba()

# print(probag())
# print(mf.proba())

# print(probaNEW())