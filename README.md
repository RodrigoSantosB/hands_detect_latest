# Hands detection using openCv and MediaPipe
[![NPM](https://img.shields.io/npm/l/react)](https://github.com/RodrigoSantosB/hands_detect_latest/blob/master/LICENSE) 


# About The Project 

Hands detection é uma aplicação desenvolvida usando a biblioteca MediaPipe de detecção de movimento, ela executa algumas ações baseadas em gestos capturados através da câmera. De maneira interativa é possível, abrir alguns programas mapeados no código que correspondam a disposição dos dedos (quantidade de dedos levantados), nos sistemas `linux` e `windows`; além disso, é possível desenhar em um quadro branco gestilculando para a câmera de maneira que ela capture o gesto realizado e o reproduza no quadro.


# RoadMap: #
* Hand right is up:
  - Open and Close aplications of the sistems with: calculator, notepad, ... , etc.
  - Look in the code for the corresponding fingers raised to open each application

* Hand lefth is up:
  -  An index finger with a distance less than 85 pixels "precise" the letter, in addition, it makes the letters on the keyboard lowercase.
  - Two or more fingers raised: capital letters
  - Little finger erases written letter (make a movement of quickly raising and lowering the finger)



## FOR TO RUN THIS SCRIPT, FOLLOW THE FOLLOWING STEPS:
* 1 Have sure you have python version 3.10.0 installed
* 2 Run the requirements.txt file whith pip install
* 3 Select the camera optition in script file for your camera (values possibles: -1, 0, 1)
