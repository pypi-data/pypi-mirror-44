from requests.auth import HTTPBasicAuth
import requests

import pandas as pd
from .settings import URL_API

def carregar_dados(entityIdentifier, token, date=None, offset=None, limit=None):
    '''
    Carrega os dados de uma entidade que está no QuarkSmart, 
    para isso utiliza os dados do token para realizar a autenticacao
    e saber em qual base de dados pegar as informações.

    Parameters
    ----------
    entityIdentifier : str
        Identificador da entidade que o torna um componente unico 
        no sistema. Normalmente um slug que pode ser encontrado na
        lista das entidades.
    token : str
        Token responsável pela autenticação do usuário no sistema,
        um md5 gerado para identificar cada instituição. Pode ser 
        encontrado na página de API REST do sistema.
    date: str, default None
        Data que pode ser utilizada para fazer um screenshot do DW
        em uma data específica. O formato pode ser 'dd/MM/yyyy'.

    Examples
    --------
    >>> import quarksmart as qs
    >>> entidade = qs.carregar_dados("pessoa", \
                    token="b40734876aeea537ec0dce2e371da4a1")
    >>> type(entidade)
    pandas.core.frame.DataFrame
    '''

    try:
        url = URL_API + '/' + entityIdentifier + '?'

        if (date):
            url += 'date=' + date + '&'
        if (offset):
            url += 'offset=' + str(offset) + '&'
        if (limit):
            url += 'limit=' + str(limit)

        headers = {'content-type': 'application/json', 
                    'TOKEN': token}

        dados = requests.get(url, headers=headers)

        if (dados.status_code == 200):
            return pd.DataFrame(dados.json()['rows'])
        elif (dados.status_code == 401):
            return "Falha de Autenticação."
        else:
            return "Falha ao carregar os dados."
    except Exception as e:
        return "Falha ao carregar os dados. Erro: " + str(e)

def authentication(user, password):
    '''
    Utiliza os dados de login e senha para autenticar 
    um usuário no quarkbi, o retorno desse método é 
    um token que deve ser utilizado para importar os dados.  

    Examples
    --------
    >>> import quarksmart as qs
    >>> token = qs.authentication("usuario", "senha")
    >>> print(token)
    b40734876aeea537ec0dce2e371da4a1

    >>> token2 = qs.authentication("user", "incorreta")
    >>> print(token2)
    Falha na autenticação.
    '''
    url = URL_API + "/authentication"

    auth = HTTPBasicAuth(user, password)
    req = requests.get(url, auth=auth)

    if req.status_code == "200":
        json = req.json()
        token = json.token
        return token
    
    return "Falha na autenticação."

def teste():
    '''
    Método de Teste.
    '''
    print("Esse é um método de testes.")
