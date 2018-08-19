from EstadoTeclado import EstadoTeclado
import UtilitarioTeclado
import _thread

# Define o estado default/inicial, ao qual o sistema sempre retorna.
# O sistema, inicialmente, sempre estah aguardando uma senha para liberar o portao.
class EstadoDigitandoSenhaTeclado(EstadoTeclado):

    def match(self, conteudoDigitado):
        return (len(conteudoDigitado) == UtilitarioTeclado.TAMANHO_SENHA)

    def executa(self, conteudoDigitado, conteudoAnterior):
        UtilitarioTeclado.log("SENHA COMPLETA.. CHECANDO ID CORRESPONDENTE...")
        id = UtilitarioTeclado.getId(conteudoDigitado)

        if (id is not None):
            if (id == UtilitarioTeclado.ID_CADASTRO_SENHA): # usuario entrou com uma senha que permite cadastrar outras senhas
                UtilitarioTeclado.beepCadastroSenha()
                return UtilitarioTeclado.ESTADO_DIGITANDO_ID # vai para o estado para entrar com novo ID
            else:
                UtilitarioTeclado.log("Senha valida! Identificado %s" % id)
                _thread.start_new_thread(self.abrePortao, (id, ))
                return UtilitarioTeclado.ESTADO_DIGITANDO_SENHA
        else:
            UtilitarioTeclado.log("Senha invalida!")
            return None

    def abrePortao(self, id):
        UtilitarioTeclado.abrePortao(id)
        UtilitarioTeclado.notificaInteressados("Entrada liberada para " + id)

    def getNomeEstado(self):
        return "Digitando Senha"

    def isDefault(self):
        return True
