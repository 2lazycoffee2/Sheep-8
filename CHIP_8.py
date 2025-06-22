#coding:utf-8

import pygame as ga
import display as disp
import core as co
import input as controller
import sys

def run(rom_path, stop_event=None, framerate=-30, fullscreen=False, monitor_factory=None, fullscreen_toggle_event=None):
    """
    Fonction principale pour lancer l'émulateur CHIP-8.
    """

    ga.init()
    ga.display.set_caption("Sheep 8")
    ga.display.set_icon(ga.image.load("assets/icon/sheep-256.png"))
    ga.mixer.init()

    input0 = controller.Input()
    coreprocess = co.CPU(rom_path, input0.keypad)

    coreprocess.load_font()
    coreprocess.load_rom()

    monitor = monitor_factory() if monitor_factory else disp.Display()
    if fullscreen:
        monitor.set_fullscreen(True)
    beep = ga.mixer.Sound('sound/beep.wav')
    beep_channel = ga.mixer.Channel(0)

    # LOOP :

    running = True
    while running:
        if stop_event is not None and stop_event.is_set():
            running = False
        if fullscreen_toggle_event is not None and fullscreen_toggle_event.is_set():
            monitor.set_fullscreen(not getattr(monitor, 'fullscreen', False))
            fullscreen_toggle_event.clear()
        events = ga.event.get()
        for event in events:
            if event.type == ga.QUIT:
                running = False
            elif event.type == ga.KEYDOWN:
                if event.key == ga.K_F6:  # Arrêter
                    if stop_event is not None:
                        stop_event.set()
                elif event.key == ga.K_F7:  # Reset
                    if stop_event is not None:
                        stop_event.set()
                elif event.key == ga.K_F11:
                    monitor.set_fullscreen(not getattr(monitor, 'fullscreen', False))

        input0.update(events)

        coreprocess.decode()                                                       
        coreprocess.pipeline()                                                     
        if coreprocess.delay_timer > 0:
            coreprocess.delay_timer -=1
        if coreprocess.delay_sound > 0:
            if not beep_channel.get_busy():
                beep_channel.play(beep)
            coreprocess.delay_sound -= 1
        else:
            beep_channel.stop()
        monitor.Draw_pixel(coreprocess.Win_buffer)
        ga.time.Clock().tick(framerate)
    
    ga.quit()
    return

def toggle_fullscreen(monitor):
    monitor.set_fullscreen(not getattr(monitor, 'fullscreen', False))

