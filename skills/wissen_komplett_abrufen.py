import sys, os
sys.path.insert(0, '/ilija')
os.chdir('/ilija')
import chromadb
from chromadb.utils import embedding_functions

def wissen_komplett_abrufen():
    try:
        ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name='all-MiniLM-L6-v2')
        client = chromadb.PersistentClient(path='./memory/ilija_db')
        col = client.get_or_create_collection('globales_wissen', embedding_function=ef)
        count = col.count()
        if count == 0:
            return 'Gedaechtnis leer.'
        result = col.get()
        docs = result.get('documents', [])
        out = str(count) + ' Eintraege:\n'
        for i, d in enumerate(docs[:80]):
            out += '[' + str(i+1) + '] ' + d + '\n'
        return out
    except Exception as e:
        return 'Fehler: ' + str(e)

AVAILABLE_SKILLS = [wissen_komplett_abrufen]
