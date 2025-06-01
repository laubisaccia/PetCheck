from jwt import encode,decode

#funcion que genera el token
def createToken(data:dict):
    token:str= encode (payload=data,key="misecret",algorithm="HS256")
    return token

#aca verifico que el token sea true y devuelvo la info
def validateToken(token:str) ->dict:
    data:dict=decode(token,key="misecret",algorithms="HS256")
    return data