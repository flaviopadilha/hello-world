from EstadoTeclado import EstadoTeclado
import UtilitarioTeclado

# depois de digitar um ID para cadastro, o proximo estado (este aqui) eh cadastrar a senha
class EstadoDigitandoSenhaCadastroTeclado(EstadoTeclado):

    def match(self, conteudoDigitado):
        return (len(conteudoDigitado) == UtilitarioTeclado.TAMANHO_SENHA)

    def executa(self, conteudoDigitado, conteudoAnterior):
        UtilitarioTeclado.armazenaNovaSenha(conteudoAnterior, conteudoDigitado)
        UtilitarioTeclado.log("Senha cadastrada com sucesso para o ID %s " % conteudoAnterior)
        UtilitarioTeclado.notificaInteressados("Senha cadastrada com sucesso para o ID " + conteudoAnterior)
        return UtilitarioTeclado.ESTADO_DIGITANDO_SENHA

    def getNomeEstado(self):
        return "Cadastro Nova Senha"

    def isDefault(self):
        return False
