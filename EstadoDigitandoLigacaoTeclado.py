from EstadoTeclado import EstadoTeclado
import UtilitarioTeclado
import _thread

# esta classe define o estado para fazer uma ligacao a partir do teclado
class EstadoDigitandoLigacaoTeclado(EstadoTeclado):

    def match(self, conteudoDigitado):
        return (len(conteudoDigitado) == UtilitarioTeclado.TAMANHO_ID)

    def executa(self, conteudoDigitado, conteudoAnterior):
        if (UtilitarioTeclado.existeId(conteudoDigitado)):
            UtilitarioTeclado.beepInicioChamada()
            UtilitarioTeclado.log("Serah feita chamada para %s" % conteudoDigitado)
            _thread.start_new_thread(self.solicitaChamadaTelefone, (conteudoDigitado, ))
            return UtilitarioTeclado.ESTADO_DIGITANDO_SENHA
        else:
            UtilitarioTeclado.log("Nao existe o ID!")
            return None

    def solicitaChamadaTelefone(self, id):
        UtilitarioTeclado.solicitaChamadaTelefone(id)

    def getNomeEstado(self):
        return "Fazendo Ligacao"

    def isDefault(self):
        return False
