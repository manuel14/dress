import cPickle as pickle
from os.path import exists
from models import ListaPrendas, ListaClientes

DATA_FILE = 'dress.dat'

def save(objects):
    
    dfile = open(DATA_FILE, 'w')
    pickler = pickle.Pickler(dfile)
    pickler.dump(objects)
    dfile.close()


def load():

    dfile = open(DATA_FILE, 'r')
    unpickler = pickle.Unpickler(dfile)
    data = unpickler.load() 
    dfile.close()

    return data





# En caso de no existir el archivo de datos, se crea un nuevo archivo
# con las colecciones de datos vacias

if not exists(DATA_FILE):
    
    objects = {
        'clientes': ListaClientes(),
	'prendas': ListaPrendas()
    }

    save(objects)

