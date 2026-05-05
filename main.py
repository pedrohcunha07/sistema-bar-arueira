from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select
from typing import List, Optional

#Tabela_Cerveja

class Cerveja(SQLModel, table = True):
    id_bebida: Optional[int] = Field(primary_key = True, default = None)
    nome: str = Field(index = True, unique = True)
    preco: float
    categoria: str
    
sqlite_file_name = 'sistema_bar.db'
sqlite_url = f'sqlite:///{sqlite_file_name}'
engine = create_engine(sqlite_url, echo=True)


def create_db_tables():
    SQLModel.metadata.create_all(engine)
    
    
def get_session():
    with Session(engine) as session:
        yield session
        
app = FastAPI(title = 'Bar dos Cuiudo')

@app.on_event('startup')
def on_startup():
    create_db_tables()
    pop_banco_se_vazio()
    
def pop_banco_se_vazio():
    with Session(engine) as session:
        if session.exec(select(Cerveja)).first() is None:
            TABELA_CERVEJA = {
                'Skol': {'preço': 2.99, 'categoria': 'Cerveja'},
                'Antártica': {'preço': 2.99, 'categoria': 'Cerveja'},
                'Ice': {'preço': 4.50, 'categoria': 'Cerveja'},
                'Skol Beats': {'preço': 4.50, 'categoria': 'Cerveja'},
                'Amstel': {'preço': 3.99, 'categoria': 'Cerveja'},
                'Brahma': {'preço': 3.99, 'categoria': 'Cerveja'},
                'Corona 600ml': {'preço': 5.99, 'categoria': 'Cerveja'},
                'Shot - Velho Barreiro': {'preço': 5.49, 'categoria': 'Cachaça'},
                'Shot - São Fransisco': {'preço': 5.79, 'categoria': 'Cachaça'},
                'Shot - Pitú': {'preço': 6.49, 'categoria': 'Aguardente'}
            }
            for nome, info in TABELA_CERVEJA.items():
                cerveja = Cerveja(nome = nome, preco = info['preço'], categoria = info['categoria'])
                session.add(cerveja)
            session.commit()

@app.get('/cardapio', response_model = List[Cerveja])
def lista_cardapio(session: Session = Depends(get_session)):
    cervejas = session.exec(select(Cerveja)).all()
    return cervejas


@app.post('/cardapio', response_model = Cerveja)
def busca_cardapio(cerveja: Cerveja, session: Session = Depends(get_session)):
    session.add(cerveja)
    session.commit()
    session.refresh(cerveja)
    return cerveja

@app.get("/")
def home():
    return {"mensagem": "Bar do Arueira está aberto"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port = 8000)