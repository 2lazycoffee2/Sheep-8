#coding:utf-8

import pygame as ga
import display as disp
import core as co
import input as controller
import sys

def run(rom_path, stop_event=None):
    """
    Fonction principale pour lancer l'émulateur CHIP-8.
    """
    ga.init()
    ga.display.set_caption("Sheep 8")
    ga.display.set_icon(ga.image.load("assets/icon/sheep-256.png"))
    ga.mixer.init()

    input0 = controller.Input()
    coreprocess = co.CPU(rom_path, "font/chip48font.txt", input0.keypad)

    coreprocess.load_font()
    coreprocess.load_rom()

    monitor = disp.Display()
    beep = ga.mixer.Sound('sound/beep.wav')
    beep_channel = ga.mixer.Channel(0)

    # LOOP :

    running = True
    while running:
        if stop_event is not None and stop_event.is_set():
            running = False
        events = ga.event.get()
        for event in events:
            if event.type == ga.QUIT:
                running = False

        input0.update(events)

        coreprocess.decode()                                                       #decode fonctionnelle
        coreprocess.pipeline()                                                     #pipeline fonctionnelle
        if coreprocess.delay_timer > 0:
            coreprocess.delay_timer -=1
        if coreprocess.delay_sound > 0:
            if not beep_channel.get_busy():
                beep_channel.play(beep)
            coreprocess.delay_sound -= 1
        else:
            beep_channel.stop()
        monitor.Draw_pixel(coreprocess.Win_buffer)
        ga.time.Clock().tick(-30)
    
    ga.quit()
    return

