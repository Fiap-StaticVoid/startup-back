from bcrypt import checkpw, gensalt, hashpw


def gerar_senha(senha: str) -> str:
    return hashpw(senha.encode(), gensalt()).decode()


def verificar_senha(senha: str, hash_senha: str) -> bool:
    return checkpw(senha.encode(), hash_senha.encode())
