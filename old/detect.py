import cv2
import mediapipe as mp
import os
from time import sleep 
from pynput.keyboard import Key

#CORES
WHITE      = ( 255, 255, 255)
BLACK      = ( 0,     0,   0)
BLUE       = ( 255,   0,   0)
GREEN      = ( 0,   255,   0)
RED        = ( 0,   0,   255)
LIGHT_BLUE = ( 255, 255,   0) 


# Inicializar o detector de mãos
mp_hands = mp.solutions.hands
mp_drawn = mp.solutions.drawing_utils

# guarda os modelos para detecção das mãos
hand = mp_hands.Hands()
# seleciona a câmero do host
select_cam = 0

# captura a câmera
cam = cv2.VideoCapture(select_cam)

# define a resolução da tela 
screen_x = 1920
screen_y = 1080
cam.set(cv2.CAP_PROP_FRAME_WIDTH, screen_x)
cam.set(cv2.CAP_PROP_FRAME_WIDTH, screen_y)

chrome      = False
notepad     = False
calculadora = False

# TECLADO
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
        ['A','S','D','F','G','H','J','K','L'],
        ['Z','X','C','V','B','N','M', ',','.',' ']]

# offset em px
offset = 50 
count = 0
text = '>'


# calcula as coords dos dedos nas mãos
def findHandsCoord(img, invert_side=False):
    # Converte uma imagem BGR para RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # instancia modelo
    result = hand.process(img_rgb)
    
    # pontos das mãos (21pontos)
    hand_points = result.multi_hand_landmarks
    hands_side = result.multi_handedness
    # armazena os todos os pontos de ambas as mãos
    all_hands = []
    if hand_points:
        for hand_side, marking_hands in zip(hands_side, hand_points):
            info_hand = {}
            coords = []
            for mark in marking_hands.landmark:
                coord_x = int(mark.x * screen_x) 
                coord_y = int(mark.y * screen_y)
                coord_z = int(mark.z * screen_x)
                coords.append((coord_x, coord_y, coord_z))
                
            info_hand['coords'] = coords
            if invert_side:
                if hand_side.classification[0].label == 'Left':
                    info_hand['side'] = 'Right'
                else:
                    info_hand['side'] = 'Left'
            else:
                info_hand['side'] = hand_side.classification[0].label
                
            # print(info_hand['side'])
            
            all_hands.append(info_hand)
            mp_drawn.draw_landmarks(img,
                                    marking_hands,
                                    mp_hands.HAND_CONNECTIONS
                                                            )
    return img, all_hands

# verifica se há dedos levantados
def fingerUp(hand):
    fingers = []
    
    # if hand['side'] == 'Right': 
    #     if hand['coords'][4][0] < hand['coords'][3][0]:
    #         fingers.append(True)
    #     else:
    #         fingers.append(False)
    # else:
    #     if hand['coords'][4][0] > hand['coords'][3][0]:
    #         fingers.append(True)
    #     else:
    #         fingers.append(False)
            
    # pontas dos dedos
    for fingertip in [8, 12, 16, 20]:
        if hand['coords'][fingertip][1] < hand['coords'][fingertip-2][1]:
            fingers.append(True)
        else:
            fingers.append(False)
    return fingers
     
     
def openProgram(info_finger_hand, finger_list, program_name):
    global chrome
    global calculadora
    global notepad
    
    if info_finger_hand == finger_list and  chrome == False:
        chrome = True
        # Windows
        # os.startfile(r'C:\Windows\system32\notepad.exe')
        # Linux
        os.system('google-chrome')
        
    if info_finger_hand == finger_list and  notepad == False:
        notepad = True
        # Windows
        os.startfile(r'C:\Windows\system32\notepad.exe')
        # Linux
        # os.system('gnome-calculator')
    
    # fechar um programa em específico
    if info_finger_hand == [False, False, False, False] and chrome:
        notepad = False
        os.system('TASKKILL /IM notepad.exe')
        # Linux:
        # os.system(f'pkill {program_name}')

# imprime botões:
def print_buttons(img, position, letter, size=50, collor_rectangle=WHITE): 
    cv2.rectangle(img, position, (position[0]+size, position[1]+size), collor_rectangle, cv2.FILLED)
    cv2.rectangle(img, position, (position[0]+size, position[1]+size), BLUE, 1)
    cv2.putText(img, letter, (position[0]+15,position[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 2)
    return img


def main():
    global keys
    global count
    global text
    # captura frames da camera em real time
    while True:
        success, frame = cam.read()
        
        frame = cv2.flip(frame, 1)
        frame, all_hands = findHandsCoord(frame)   
        
    
    
        if len(all_hands) == 1:
            info_finger_hand_1 = fingerUp(all_hands[0])
            if all_hands[0]['side'] == 'Left':
                indicator_x, indicator_y, indicator_z = all_hands[0]['coords'][8]
                cv2.putText(frame, f'Distance of camera: {indicator_z}', (850, 50), cv2.FONT_HERSHEY_COMPLEX, 1, WHITE, 2)
                for index_line, linha_teclado in enumerate(keys):
                    for index, letter in enumerate(linha_teclado):
                        if sum(info_finger_hand_1) <= 1:
                            letter = letter.lower()
                        frame = print_buttons(frame, (offset+index*80, offset+index_line*80),letter)
                        if offset+index*80 < indicator_x < 100+index*80 and offset+index_line*80<indicator_y<100+index_line*80:
                            frame = print_buttons(frame, (offset+index*80, offset+index_line*80),letter, collor_rectangle=GREEN)
                            if indicator_z < -85:
                                count = 1
                                write = letter
                                frame = print_buttons(frame, (offset+index*80, offset+index_line*80),letter, collor_rectangle=LIGHT_BLUE)
                if count:
                    count += 1
                    if count == 3:
                        text+= write
                        count = 0
                        keys.press(write)
    
                if info_finger_hand_1 == [False, False, False, True] and len(text)>1:
                    text = text[:-1]
                    sleep(0.15)
    
                cv2.rectangle(frame, (offset, 450), (830, 500), WHITE, cv2.FILLED)
                cv2.rectangle(frame, (offset, 450), (830, 500), BLUE, 1)
                cv2.putText(frame, text[-40:], (offset, 480), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 2)
                cv2.circle(frame, (indicator_x, indicator_y), 7, BLUE, cv2.FILLED)

                # se levantar a mão direita
                if all_hands[0]['side'] == 'Right':
                    openProgram(info_finger_hand_1, [True, False, False, False], 'google-chrome')
                    
                    # fechar camera com dedos abaixados:
                    if info_finger_hand_1 == [True, False, False, True]:
                        break
                
                
        cv2.imshow('IMAGE', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
            
    cv2.imshow('CAM', frame)
    cam.release()
    cv2.destroyAllWindows()
    

if __name__ == "__main__":
    main()