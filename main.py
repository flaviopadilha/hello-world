# biblioteca do teclado
from pad4pi import rpi_gpio
# fim biblioteca do teclado

# biblioteca dos pinos I/O
import RPi.GPIO as gpio
# biblioteca dos pinos I/O

# bibliotecas gerais
import signal, os
import io
import time
from datetime import datetime
import threading
import sys
# fim de bibliotecas gerais

# repositorio das funcoes gerais usadas neste aplicativo
import UtilitarioTeclado

# nao mostra mensagens de warning quando comeca esta aplicacao
gpio.setwarnings(False)

# configuracao dos pinos do Raspberry pi3 para o teclado utilizado
KEYPAD = [
        ["1","2","3","A"],
        ["4","5","6","B"],
        ["7","8","9","C"],
        ["*","0","#","D"]
]

ROW_PINS = [4, 14, 15, 17] # numeracao BCM
COL_PINS = [18, 27, 22, 23] # numeracao BCM

factory = rpi_gpio.KeypadFactory()
keypad = factory.create_keypad(keypad=KEYPAD, row_pins=ROW_PINS, col_pins=COL_PINS)
current_milli_time = lambda: int(round(time.time()))
estadoAtual = UtilitarioTeclado.ESTADO_DIGITANDO_SENHA # setando o estado inicial desta aplicacao

# funcao que controla o tempo esperado entre digitar 2 teclas
def contaTempo(cv):
    global estadoAtual
    try:
        while (True):
            with cv:
                if (estadoAtual.isInicio() and estadoAtual.isDefault()):
                    UtilitarioTeclado.log('Aguardando...')
                    cv.wait() # todo estado tem um tempo maximo de permanencia e sempre acaba voltando pra ca
                    continue
                else:
                    segundosAntes = current_milli_time()
                    cv.wait(UtilitarioTeclado.SEGUNDOS_PARA_DIGITAR_TECLA) # neste caso, alguem estah digitando... 
                    if (estadoAtual.isExecutando()):
                        UtilitarioTeclado.log('Ainda executando... {estado}'.format(estado=estadoAtual.getNomeEstado())) # a execucao das tarefas dentro dos estados tem que rodar em thread separada

                segundosDepois = current_milli_time()

                # existe um tempo limite para digitar.. se esgotado o tempo, volta para o estado inicial
                if (segundosDepois - segundosAntes >= UtilitarioTeclado.SEGUNDOS_PARA_DIGITAR_TECLA):

                    estadoAnterior = estadoAtual
                    estadoAtual = UtilitarioTeclado.ESTADO_DIGITANDO_SENHA
                    estadoAtual.reset()

                    if (estadoAnterior.isExecutando()):
                        UtilitarioTeclado.log('Ainda executando...')
                    else:
                        UtilitarioTeclado.beepFalha()
                        UtilitarioTeclado.log("Demorou... voltando para o estado inicial.") # aqui foi o usuario que demorou para digitar

    except (KeyboardInterrupt):
        UtilitarioTeclado.log("Voce pressionou Ctrl+C para interromper.")

# funcao chamada quando o usuario aperta uma tecla
def teclaPressionada(key):
    with condition:
        global estadoAtual
        estadoAtual = estadoAtual.leDigito(key)
        if (estadoAtual is None):
            estadoAtual = UtilitarioTeclado.ESTADO_DIGITANDO_SENHA # errou a senha, por exemplo.. sempre volta para o estado inicial
        elif (estadoAtual == UtilitarioTeclado.ESTADO_DIGITANDO_DESLIGA):
            UtilitarioTeclado.log("Desligando")
            sys.exit()

        condition.notifyAll()

if __name__ == '__main__':

    #################################### CHECAGEM DE EXECUCAO DE PROCESSOS #############################################
    if (UtilitarioTeclado.checkRodando("python3", "main.py", True)):
        UtilitarioTeclado.log("Jah existe uma instancia em execucao!")
        UtilitarioTeclado.mataProcesso("python3",  "main.py")
        UtilitarioTeclado.log("Matando processo...")

    #################################### INICIALIZACAO DO TECLADO  #############################################
    keypad.registerKeyPressHandler(teclaPressionada)
    condition = threading.Condition()
    temporizador = threading.Thread(name='temporizador', target=contaTempo, args=(condition,))

    try:
        temporizador.start()
        UtilitarioTeclado.beepInicioAPP()
        UtilitarioTeclado.iniciaClienteMQTT()
    except:
        UtilitarioTeclado.log("Processo interrompido")
        keypad.cleanup()
        UtilitarioTeclado.desconectaMqtt()
