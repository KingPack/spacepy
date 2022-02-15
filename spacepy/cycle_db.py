import schedule
import time
from datetime import datetime

from insert_data import create_data_loop, initialize_database


initialize_database()


def create_data_loop_schedule(horario_init:str):

    print('Iniciando o loop de criação de artigos...')
    
    schedule.every().day.at(horario_init).do(create_data_loop)

    contador = 0

    while True:
        schedule.run_pending()
        time.sleep(10)
        horario_atual = datetime.now().strftime('%H:%M:%S')

        print('--------------------------------------------------------------------------------\n')
        print(f'Verificando tarefas contador : {contador}')
        print('Tafera agendada para as ', horario_init)
        print(f'Horario atual: {horario_atual}')

        contador += 1


horario_init = input('\n Qual horario de inicio ? exemplo (HH:MM) 10:00 :  ')

create_data_loop_schedule(horario_init)
