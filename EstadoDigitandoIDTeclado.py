from EstadoTeclado import EstadoTeclado as EstTeclado
import UtilitarioTeclado

# O usuario entra neste estado quando digita a senha para cadastrar novas senhas.
# O primeiro passo (este estado aqui) eh digitar o ID.
# Depois de atingir o tamanha do ID (definido no metodo match), o sistema emite um beep para cadastrar a senha (proximo estado).
class EstadoDigitandoIDTeclado(EstTeclado):

    def match(self, conteudoDigitado):
        return (len(conteudoDigitado) == UtilitarioTeclado.TAMANHO_ID)

    # apenas passa para o proximo estado, para cadastrar nova senha
    def executa(self, conteudoDigitado, conteudoAnterior):
        UtilitarioTeclado.beepEntrarDados()
        return UtilitarioTeclado.ESTADO_DIGITANDO_SENHA_CADASTRO

    def getNomeEstado(self):
        return "Digitando ID"

    def isDefault(self):
        return False

