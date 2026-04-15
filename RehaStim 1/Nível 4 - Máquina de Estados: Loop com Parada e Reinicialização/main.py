import time
import keyboard
from stim_node import StimNode


# ────────────────────────────────────────── plpl
#  CONFIGURACOES
# ──────────────────────────────────────────

PORT       = "COM5"
FREQ       = 50
N_FACTOR   = 0
GROUP_TIME = 0
STIM_MODE  = 0
CHANNEL_LF = []

CHANNELS = [1]

PULSE_WIDTH_OFF   = [0]
PULSE_CURRENT_OFF = [0]

PULSE_WIDTH_ON    = [100]
PULSE_CURRENT_ON  = [6]


# ──────────────────────────────────────────
#  ESTADOS
# ──────────────────────────────────────────

STATE_WAITING  = "waiting"
STATE_STIM_ON  = "stim_on"
STATE_STIM_OFF = "stim_off"
STATE_EXIT     = "exit"


# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────

def main():
    stim = StimNode(
        port=PORT,
        freq=FREQ,
        n_factor=N_FACTOR,
        group_time=GROUP_TIME,
        stim_mode=STIM_MODE,
        channel_lf=CHANNEL_LF,
    )

    stim.initialize_ccl(CHANNELS)
    stim.update_ccl(PULSE_WIDTH_OFF, PULSE_CURRENT_OFF)
    print("[INFO] Sistema inicializado com valores zerados.")
    print("-" * 45)
    print("  ESPACO -> iniciar estimulacao")
    print("  P      -> pausar (valores zerados)")
    print("  L      -> retomar estimulacao")
    print("  ESC    -> encerrar programa")
    print("-" * 45)
    print("[INFO] Aguardando ESPACO para iniciar...")

    state = STATE_WAITING

    while state != STATE_EXIT:

        match state:

            case "waiting":     # estado de espera, aperta espaço que entra no programad da estimulação
                if keyboard.is_pressed("space"):
                    state = STATE_STIM_ON
                    stim.update_ccl(PULSE_WIDTH_ON, PULSE_CURRENT_ON)
                    print("[STIM ON]  Estimulacao iniciada.")
                    time.sleep(0.3)

            case "stim_on":     # estado de estimulação, quando entra no programa de estimulação
                stim.update_ccl(PULSE_WIDTH_ON, PULSE_CURRENT_ON)

                if keyboard.is_pressed("p"):    #condição de "pausa"
                    state = STATE_STIM_OFF
                    stim.update_ccl(PULSE_WIDTH_OFF, PULSE_CURRENT_OFF)
                    print("[PAUSADO]  Valores zerados. Pressione L para retomar.")
                    time.sleep(0.3)

                elif keyboard.is_pressed("esc"):    # condição de saida e encerramento
                    state = STATE_EXIT

            case "stim_off":        #condição de pausa
                stim.update_ccl(PULSE_WIDTH_OFF, PULSE_CURRENT_OFF)

                if keyboard.is_pressed("l"):    # condição de estimulação
                    state = STATE_STIM_ON
                    stim.update_ccl(PULSE_WIDTH_ON, PULSE_CURRENT_ON)
                    print("[STIM ON]  Estimulacao retomada.")
                    time.sleep(0.3)

                elif keyboard.is_pressed("esc"):    # condição de saida e encerramento
                    state = STATE_EXIT

        time.sleep(0.05)

    stim.stop_ccl() # encerra o programa e finaliza
    print("[INFO] Estimulacao encerrada. Programa finalizado.")


if __name__ == "__main__":
    main()