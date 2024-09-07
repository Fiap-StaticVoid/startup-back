from bcrypt import checkpw, gensalt, hashpw


class CheckSenhaForte:
    @staticmethod
    def possui_no_minimo_8_caracteres(senha: str) -> str | None:
        return None if len(senha) > 8 else "Precisa ter no mínimo 8 caracteres"

    @staticmethod
    def possui_letras_minusculas(senha: str) -> str | None:
        return (
            None
            if any(letra.islower() for letra in senha)
            else "Precisa ter letras minúsculas"
        )

    @staticmethod
    def possui_letras_maiusculas(senha: str) -> str | None:
        return (
            None
            if any(letra.isupper() for letra in senha)
            else "Precisa ter letras maiúsculas"
        )

    @staticmethod
    def possui_numeros(senha: str) -> str | None:
        return (
            None if any(letra.isdigit() for letra in senha) else "Precisa ter números"
        )

    @staticmethod
    def possui_simbolos(senha: str) -> str | None:
        return (
            None
            if any(not letra.isalnum() for letra in senha)
            else "Precisa ter símbolos"
        )

    @staticmethod
    def senha_eh_forte(senha: str) -> tuple[bool, list[str]]:
        possui_no_minimo_8_caracteres = CheckSenhaForte.possui_no_minimo_8_caracteres(
            senha
        )
        possui_letras_minusculas = CheckSenhaForte.possui_letras_minusculas(senha)
        possui_letras_maiusculas = CheckSenhaForte.possui_letras_maiusculas(senha)
        possui_numeros = CheckSenhaForte.possui_numeros(senha)
        possui_simbolos = CheckSenhaForte.possui_simbolos(senha)
        erros = list(
            filter(
                None,
                [
                    possui_no_minimo_8_caracteres,
                    possui_letras_minusculas,
                    possui_letras_maiusculas,
                    possui_numeros,
                    possui_simbolos,
                ],
            )
        )
        return not erros, erros


def gerar_senha(senha: str) -> str:
    return hashpw(senha.encode(), gensalt()).decode()


def verificar_senha(senha: str, hash_senha: str) -> bool:
    return checkpw(senha.encode(), hash_senha.encode())
