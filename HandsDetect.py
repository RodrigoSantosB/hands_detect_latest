import cv2
import mediapipe as mp
import os
from time import sleep
from pynput.keyboard import Controller
 
WHITE       = (255,     255,    255)
BLACK       = (  0,       0,      0)
AZUL        = (255,       0,      0)
VERDE       = (0,       255,      0)
RED         = (0,         0,    255)
LIGHT_BLUE  = (255,     255,      0)



# Inicializar o detector de mãos
mp_hands = mp.solutions.hands
mp_drawn = mp.solutions.drawing_utils

# guarda os modelos para detecção das mãos
hands = mp_hands.Hands()

# seleciona a câmero do host
select_cam = 0

width = 1280
height = 720
# captura a câmera
camera = cv2.VideoCapture(select_cam)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, width)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

bloco_notas = False
chrome      = False
calculadora = False

# TECLADO
keys = [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'],
            ['A','S','D','F','G','H','J','K','L'],
            ['Z','X','C','V','B','N','M', ',','.',' ']]

offset = 50
count = 0
texto = '>'
keyboard = Controller()
 
def findHandsCoord(img, invert_side = False):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)
    all_hands = []
    if result.multi_hand_landmarks:
        for hand_side, marking_hands in zip(result.multi_handedness, result.multi_hand_landmarks):
            info_hand = {}
            coords = []
            for marking in marking_hands.landmark:
                coord_x, coord_y, coord_z = int(marking.x * width), int(marking.y * height), int(marking.z * width)
                coords.append((coord_x, coord_y, coord_z))
 
            info_hand['coords'] = coords
            if invert_side:
                if hand_side.classification[0].label == 'Left':
                    info_hand['side'] = 'Right'
                else:
                    info_hand['side'] = 'Left'
            else:
                info_hand['side'] = hand_side.classification[0].label
 
            all_hands.append(info_hand)
            mp_drawn.draw_landmarks(img,
                                    marking_hands,
                                    mp_hands.HAND_CONNECTIONS)
 
    return img, all_hands
 
 
def figerUp(hand):
    fingers = []
    for ponta_dedo in [8,12,16,20]:
        if hand['coords'][ponta_dedo][1] < hand['coords'][ponta_dedo-2][1]:
            fingers.append(True)
        else:
            fingers.append(False)
    return fingers
 
# imprime botões:
def printButtons(img, position, letter, size_letter = 50, cor_retangulo = WHITE):
    cv2.rectangle(img, position, (position[0]+size_letter, position[1]+size_letter), cor_retangulo,cv2.FILLED)
    cv2.rectangle(img, position, (position[0]+size_letter, position[1]+size_letter), LIGHT_BLUE, 1)
    cv2.putText(img, letter, (position[0]+15,position[1]+30), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 2)
    return img
    
def main():

    global offset 
    global count 
    global texto 
    global keyboard 
        
    global bloco_notas 
    global chrome      
    global calculadora 

    while True:
        sucesso, img = camera.read()
        img = cv2.flip(img, 1)
    
        img, all_hands = findHandsCoord(img)
    
        if len(all_hands) == 1:
            info_finger_hand_1 = figerUp(all_hands[0])
            if all_hands[0]['side'] == 'Left':
                indicador_x, indicador_y, indicador_z = all_hands[0]['coords'][8]
                cv2.putText(img, f'Camera distance: {indicador_z}', (850, 50), cv2.FONT_HERSHEY_COMPLEX, 1, WHITE, 2)
                for indice_linha, linha_keyboard in enumerate(keys):
                    for indice, letra in enumerate(linha_keyboard):
                        if sum(info_finger_hand_1) <= 1:
                            letra = letra.lower()
                        img = printButtons(img, (offset+indice*80, offset+indice_linha*80),letra)
                        if offset+indice*80 < indicador_x < 100+indice*80 and offset+indice_linha*80<indicador_y<100+indice_linha*80:
                            img = printButtons(img, (offset+indice*80, offset+indice_linha*80),letra, cor_retangulo=VERDE)
                            if indicador_z < -85:
                                count = 1
                                escreve = letra
                                img = printButtons(img, (offset+indice*80, offset+indice_linha*80),letra, cor_retangulo=LIGHT_BLUE)
                if count:
                    count += 1
                    if count == 3:
                        texto+= escreve
                        count = 0
                        keyboard.press(escreve)
    
                if info_finger_hand_1 == [False, False, False, True] and len(texto)>1:
                    texto = texto[:-1]
                    sleep(0.15)
    
                cv2.rectangle(img, (offset, 450), (830, 500), WHITE, cv2.FILLED)
                cv2.rectangle(img, (offset, 450), (830, 500), AZUL, 1)
                cv2.putText(img, texto[-40:], (offset, 480), cv2.FONT_HERSHEY_COMPLEX, 1, BLACK, 2)
                cv2.circle(img, (indicador_x, indicador_y), 7, AZUL, cv2.FILLED)
    
            if all_hands[0]['side'] == 'Right':
                if info_finger_hand_1 == [True, False, False, False] and bloco_notas == False:
                    bloco_notas = True
                    os.startfile(r'C:\Windows\system32\notepad.exe')
                if info_finger_hand_1 == [True, True, False, False] and chrome == False:
                    chrome = True
                    os.startfile(r'C:\Program Files\Google\Chrome\Application\chrome.exe')
                if info_finger_hand_1 == [True, True, True, False] and calculadora == False:
                    calculadora = True
                    os.startfile(r'C:\Windows\system32\calc.exe')
                if info_finger_hand_1 == [False, False, False, False] and bloco_notas == True:
                    bloco_notas = False
                    os.system('TASKKILL /IM notepad.exe')
                if info_finger_hand_1 == [True, False, False, True]:
                    break
        
        cv2.imshow("Imagem", img)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
    
    with open('texto.txt', 'w') as arquivo:
        arquivo.write(texto)

if __name__ == "__main__":
    main()