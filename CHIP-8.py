#coding:utf-8

#import display as disp

import core as co
import input as controller
import pygame as ga



input0 = controller.Input()
file = input("path of your file (don't forgot the .ch8 at the end ! ) : ")
file = str(file)
coreprocess = co.CPU("rom/IBM.ch8", "font/chip48font.txt", input0.keypad)

coreprocess.load_font()
coreprocess.load_rom()

#monitor = disp.Display()
beep = ga.mixer.Sound('sound/beep.wav')
beep_channel = ga.mixer.Channel(0)

# LOOP :

while True:
    events = ga.event.get()


    input0.update(events)

    coreprocess.decode()                                                       #decode fonctionnelle
    coreprocess.pipeline()                                                     #pipeline fonctionnelle
    if coreprocess.delay_timer > 0:
        coreprocess.delay_timer -=1
    if coreprocess.sound_timer > 0:
        if not beep_channel.get_busy():
            beep_channel.play(beep)
        coreprocess.sound_timer -= 1
    else:
        beep_channel.stop()
    #monitor.Draw_pixel(coreprocess.Win_buffer)
    ga.time.Clock().tick(-30)
