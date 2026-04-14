import time
from stim_node import StimNode
# from outro_modulo import OutraClasse  ← importe futuros módulos aqui


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
PULSE_WIDTH    = [100]  # µs
PULSE_CURRENT  = [4]   # mA

STIM_DURATION  = 5     # segundos de estimulação

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
    stim.update_ccl(PULSE_WIDTH, PULSE_CURRENT)

    time.sleep(STIM_DURATION)

    stim.stop_ccl()


if __name__ == '__main__':
    main()