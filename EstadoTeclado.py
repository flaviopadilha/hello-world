from abc import ABC, abstractmethod
import UtilitarioTeclado

# Classe abstrata. Todos os estados devem estender esta classe, que eh o nucleo da aplicacao. Todos os comandos/funcionalidades sao executados aqui.
class EstadoTeclado(ABC):
    teclasPressionadasAteAgora = "" # concatenacao dos digitos
    conteudoAnterior="" # informacao que pode ser passado de um estado para o outro
    executando=False # veja o metodo abaixo "isExecutando"

    # se o estado concreto quiser um beep diferente para SUCESSO, basta sobrescrever este metodo
    def beepSucesso(self):
        UtilitarioTeclado.beepSucesso()

    # se o estado concreto quiser um beep diferente para FALHA, basta sobrescrever este metodo
    def beepFalha(self):
        UtilitarioTeclado.beepFalha()

    # retorna True se o metodo abstrato "executa" estah executando nas classes que estenderam esta classe
    def isExecutando(self):
        return self.executando

    def reset(self):
        self.teclasPressionadasAteAgora = ""
        self.conteudoAnterior=""
        self.executando=False

    def isInicio(self):
        return self.teclasPressionadasAteAgora == ""

    # Retorna o estado atual depois de ler o digito.
    def leDigito(self, digito):
        self.teclasPressionadasAteAgora+=digito
        UtilitarioTeclado.beepTeclando()

        if (self.teclasPressionadasAteAgora == UtilitarioTeclado.CHARACTER_ID_LIGACAO):
            self.reset()
            UtilitarioTeclado.log("ESTADO PARA FAZER LIGACAO")
            UtilitarioTeclado.beepInicioChamada()
            return UtilitarioTeclado.ESTADO_DIGITANDO_LIGACAO

        elif (UtilitarioTeclado.ESTADO_DIGITANDO_DESLIGA.match(self.teclasPressionadasAteAgora)):
            return UtilitarioTeclado.ESTADO_DIGITANDO_DESLIGA.executa(None, None)

        elif (self.match(self.teclasPressionadasAteAgora)):
            # ATENCAO: a execucao abaixo nao pode demorar... ou vai esgotar o tempo para digitar...
            # .. idealmente, jogar a execucao para uma thread separada...
            # De qualquer forma, serah verificado se ainda estah executando com a variavel "executando"
            self.executando=True
            novoEstado = self.executa(self.teclasPressionadasAteAgora, self.conteudoAnterior)
            if (novoEstado is not None):
                novoEstado.reset()
                novoEstado.conteudoAnterior=self.teclasPressionadasAteAgora
                self.beepSucesso()
                UtilitarioTeclado.log("SUCESSO!! INDO PARA O ESTADO: %s" % novoEstado.getNomeEstado())
            else:
                self.beepFalha()
                UtilitarioTeclado.log("FALHA!!")

            self.reset()
            return novoEstado

        else:
            return self

    # returna True se o padrao de digitos esperado para este estado foi atingido
    @abstractmethod
    def match(self, conteudoDigitado):
        pass

    # retorna o proximo estado, se executar com sucesso. Se houver falha, retorna None
    @abstractmethod
    def executa(self, conteudoDigitado):
        pass

    @abstractmethod
    def getNomeEstado(self):
        pass

    # em principio, apenas o estado inicial eh o default. Eh o estado para digitar a senha.
    @abstractmethod
    def isDefault(self):
        pass

