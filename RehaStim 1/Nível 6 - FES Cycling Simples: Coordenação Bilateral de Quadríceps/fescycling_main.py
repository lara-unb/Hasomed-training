import utils.imu_yostlabs_lara as imu_yostlabs_lara
import utils.quaternion_operations as quaternion_operations
import time
import keyboard
from math import pi
from stim_node import StimNode

# ──────────────────────────────────────────
#  CONFIGURACOES
# ──────────────────────────────────────────

PORT       = "COM5"
FREQ       = 50
N_FACTOR   = 0
GROUP_TIME = 0
STIM_MODE  = 0
CHANNEL_LF = []

# Canais 1 (Direita) e 2 (Esquerda)
CHANNELS = [1, 2]

# Listas [Canal 1, Canal 2]
PULSE_WIDTH_OFF   = [0, 0]
PULSE_CURRENT_OFF = [0, 0]

PULSE_WIDTH_ON    = [100, 100]
PULSE_CURRENT_ON  = [30, 30]

# ──────────────────────────────────────────
#  ESTADOS
# ──────────────────────────────────────────

STATE_WAITING = "waiting"
STATE_RUNNING = "running"
STATE_EXIT    = "exit"

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
    
    print("-" * 45)
    print(" [SISTEMA DE CICLISMO FES - EMA] ")
    print(" ESPACO -> Iniciar/Pausar estimulacao")
    print(" ESC    -> Encerrar programa")
    print("-" * 45)

    state = STATE_WAITING

    # Configuração IMU
    imus = [9]
    input("[IMU] Pressione Enter para configurar...")
    serial_port = imu_yostlabs_lara.initialize_dongle(imus)
    imu_yostlabs_lara.configure_imu(serial_port, imus)

    input("[IMU] Pressione Enter para iniciar streaming...")
    imu_yostlabs_lara.start_streaming(serial_port, imu_ids=imus, frequency=100, timestamp=True)

    current_quaternion1 = None
    y_deg = 0.0

    serial_port.reset_input_buffer()

    while state != STATE_EXIT:
        # 1. Captura e Processamento do Ângulo
        data = imu_yostlabs_lara.read_data(serial_port)
        if data is not None:
            quaternion1 = imu_yostlabs_lara.extract_data(data, type_of_data=0, imu_id=imus[0])
            if quaternion1 is not None:
                current_quaternion1 = quaternion1
            
        if current_quaternion1 is not None:            
            euler_angle = quaternion_operations.euler_from_quaternion(current_quaternion1)
            x_deg = euler_angle[0]
            y_raw = euler_angle[1]

            # Normalização para 0-360 graus
            # if abs(x_rad) > (pi * 0.5):
            if abs(x_deg) > 90:
                y_deg = 180 - y_raw
            else:
                y_deg = y_raw if y_raw >= 0 else 360 + y_raw
            
            #print(y_deg)
            current_quaternion1 = None  

        # 2. Máquina de Estados e Comando de Hardware
        if keyboard.is_pressed("esc"):
            state = STATE_EXIT

        if state == STATE_WAITING:
            print("Pressione Espaço para iniciar a estimulação")
            while True:
                if keyboard.is_pressed("space"):
                    state = STATE_RUNNING
                    print("\n[INFO] Estimulacao ATIVADA.")
                    time.sleep(0.3)
                    break

        elif state == STATE_RUNNING:
            if keyboard.is_pressed("space"):
                state = STATE_WAITING
                stim.update_ccl(PULSE_WIDTH_OFF, PULSE_CURRENT_OFF)
                print("\n[INFO] Estimulacao PAUSADA.")
                time.sleep(0.3)
                continue

            # Lógica de Controle: Exclusividade e Intervalos
            # current = [Canal 1, Canal 2]
            c_width = [0, 0]
            c_curr  = [0, 0]

            # Janela Perna Direita (120° a 235°)
            if 120 <= y_deg <= 235:
                c_width = [PULSE_WIDTH_ON[0], 0]
                c_curr  = [PULSE_CURRENT_ON[0], 0]
                print(f"Angulo: {y_deg:5.1f} | PERNA DIREITA (CH1) ", end="\r")

            # Janela Perna Esquerda (300° a 55°)
            elif y_deg >= 300 or y_deg <= 55:
                c_width = [0, PULSE_WIDTH_ON[1]]
                c_curr  = [0, PULSE_CURRENT_ON[1]]
                print(f"Angulo: {y_deg:5.1f} | PERNA ESQUERDA (CH2)", end="\r")
            
            # Zonas Mortas (55-120 e 235-300)
            else:
                c_width = [0, 0]
                c_curr  = [0, 0]
                print(f"Angulo: {y_deg:5.1f} | --- INTERVALO ---  ", end="\r")

            # Atualiza o estimulador com o estado atual
            stim.update_ccl(c_width, c_curr)

        time.sleep(0.01) 

    # 3. Finalização Segura
    print("\n[INFO] Encerrando...")
    stim.update_ccl(PULSE_WIDTH_OFF, PULSE_CURRENT_OFF)
    stim.stop_ccl()
    imu_yostlabs_lara.stop_streaming(serial_port, imus)
    print("[OK] Sistema desligado.")

if __name__ == "__main__":
    main()