import cPickle as pickle
from os.path import exists
from models import ListaPrendas, ListaClientes, Configuracion

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

def backup(self, f): # f es la ruta donde se va a guardar el backup.
    """crear un archivo de back up"""
    bf = open(f, 'w')
    bp = pickle.Pickler(bf)
    bp.dump(self.objects)
    bf.close()





# En caso de no existir el archivo de datos, se crea un nuevo archivo
# con las colecciones de datos vacias

if not exists(DATA_FILE):
    
    objects = {
        'clientes': ListaClientes(),
        'prendas': ListaPrendas(),
        'configuracion': Configuracion()
    }

    save(objects)

