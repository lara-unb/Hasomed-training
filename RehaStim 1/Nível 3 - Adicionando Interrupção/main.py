import time
import threading
from stim_node import StimNode


# ──────────────────────────────────────────
#  CONFIGURAÇÕES — edite aqui
# ──────────────────────────────────────────

PORT       = "COM5"
FREQ       = 50      # Hz
N_FACTOR   = 0
GROUP_TIME = 0
STIM_MODE  = 0       # 0 = single
CHANNEL_LF = []

CHANNELS       = [1]   # canais ativos (1–8)
PULSE_WIDTH    = [100 ]  # µs
PULSE_CURRENT  = [4]   # mA

# ──────────────────────────────────────────
#  MAIN
# ──────────────────────────────────────────

stop_flag = False

def aguardar_parada():
    global stop_flag
    input("\n[INFO] Pressione ENTER a qualquer momento para parar a estimulação...\n")
    stop_flag = True

def main():
    global stop_flag

    stim = StimNode(
        port=PORT,
        freq=FREQ,
        n_factor=N_FACTOR,
        group_time=GROUP_TIME,
        stim_mode=STIM_MODE,
        channel_lf=CHANNEL_LF,
    )

    stim.initialize_ccl(CHANNELS)
    stim.update_ccl(PULSE_WIDTH, PULSE_CURRENT)

    # Inicia thread que aguarda ENTER para parar
    t = threading.Thread(target=aguardar_parada, daemon=True)
    t.start()

    print("[INFO] Estimulação em andamento...")
    while not stop_flag:
        time.sleep(0.1)  # checa a flag a cada 100 ms

    stim.stop_ccl()
    print("[INFO] Estimulação encerrada.")


if __name__ == '__main__':
    main()