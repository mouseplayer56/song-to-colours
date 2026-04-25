# version 4.1

import pydub
import vlc
import pygame
# import datetime
import time
import os
import random
import json

# pygame.init()
pygame.font.init()


# essentially, my program uses the pydub import to take the samples produced by a given song in a specific timeframe.
# a modulus of %256 from the samples is taken to generate a 'random' (based on song) number.
# the random import then generates a number from 0 -> 2 (inclusive) that determines selection of the R, G or B channel.
# the random sample number is applied to that channel every 'global_ht["gui"]["internal"]["trans_time_float"]', and the program changes colours every-
# 'global_ht["gui"]["internal"]["change_time_float"]' (modifiable here).


def get_next_song(param_list, dir_str):
    temp_list = [-1] + param_list
    num = -1
    # print(f"test: {dir_str}")
    size = len(os.listdir(dir_str))
    v = None
    while num in temp_list:
        num = random.randrange(0, size)
        # print(f"prev: {prev}; curr: {cur}; num: {num}")
        try:
            v = vlc.MediaPlayer(os.path.join(dir_str, os.listdir(dir_str)[num]))  # try to play the file
            if v.get_length() == -1:
                raise Exception("File cannot be interpreted as song!")
            elif size < len(temp_list - 1):
                break
        except Exception as ex:
            print(f"File error: {ex} (File {num})")
            v = None
        finally:
            if v is not None and size < len(temp_list - 1):
                break
            elif v is None:
                exit(-1)
            else:
                pass
    return num


def change_mode(current_int, desired_int, modes_list):
    print(f"Changing colour Mode.")
    if desired_int < 0:
        if current_int < len(modes_list) - 1:
            current_int += 1
            print(f"Changed Mode: {modes_list[current_int]}.")
        else:
            current_int = 0
            print(f"Mode reset: {modes_list[current_int]}.")
    else:
        pass
    return current_int


main_dir = os.path.dirname(os.path.abspath(__file__))
global_ht = {
    "gui": {
        "width_int": int(1280),
        "height_int": int(720),
        "fps_int": int(120),
        "caption_str": "stream screensaver",
        "internal": {
            "trans_time_float": float(0.4),
            "change_time_float": float(0.8)
        },
        "cols": {
            "bg_list": [0, 0, 0],
            "float_list": [0.0, 0.0, 0.0],
            "newbg_list": [255, 255, 255],
            # "change_list": [0, 0, 0],
            "sys_list": [0, 0, 0],
            "new_int": int(-1),
            "speed_int": -1,
            "stop_bool": False
        },
        "font": {
            "text_size": int(64),
            "sys_size": int(38),
            "time_size": int(38),
            "text_str": "Calibri",
            "sys_str": "Calibri",
            "time_str": "Calibri"
        }
    }, "system": {
        "song_vol_int": int(33),
        "song_storage_int": int(3),
        "by_percent_bool": False,
        "count_time_bool": True,
        "show_mode_bool": True,
        "disable_mouse_bool": False,
        "experiment_bool": True,
        "song_full_path_bool": False,
        # "config_str": "config.json",
        "modif_str": "modif.txt",
        "song_folder_str": "songs",
        "mode": {
            "list": ["normal", "smooth", "pause"],
            "disabled_list": [],
            "select_int": int(0)
        }
    }
}

if os.path.exists(os.path.join(main_dir, "config.json")):
    with open("config.json", "r") as config:
        global_ht = json.loads(config.read())
        # print(global_ht)
else:
    with open("config.json", "xt+") as config:
        config.write(json.dumps(global_ht))

for disabled in global_ht["system"]["mode"]["disabled_list"]:
    if disabled in global_ht["system"]["mode"]["list"]:
        global_ht["system"]["mode"]["list"].pop(global_ht["system"]["mode"]["list"].index(disabled))

if os.path.exists(os.path.join(main_dir, global_ht["system"]["modif_str"])):
    pass
else:
    try:
        with open(global_ht["system"]["modif_str"], "xt+"):
            pass
    except Exception as e:
        print(e)


if global_ht["system"]["song_full_path_bool"]:
    directory = global_ht["system"]["song_folder_str"]
else:
    directory = os.path.join(main_dir, global_ht["system"]["song_folder_str"])

screen = pygame.display.set_mode((global_ht["gui"]["width_int"], global_ht["gui"]["height_int"]))
pygame.display.set_caption(global_ht["gui"]["caption_str"])
clock = pygame.time.Clock()
dt = clock.tick(global_ht["gui"]["fps_int"]) / 1000
running = True
song_vlc = None
song_pydub = None
song_filename_str = None
song_time_initial = 0  # internal checks by vlc for pydub to take samples
mouse_two_clicked_bool = False

song_buffer_list = [-1 for k in range(global_ht["system"]["song_storage_int"])]
print(len(os.listdir(directory)))
if len(os.listdir(directory)) == 0:
    running = False
    raise Exception(f"File error: There are no songs in the {"full" if global_ht["system"]["song_full_path_bool"] else "nested"} path '{global_ht["system"]["song_folder_str"]}'")
else:
    song_buffer_list[len(song_buffer_list)-1] = get_next_song(song_buffer_list, directory)

program_halt_bool = False
space_pressed_bool = False
col_gen_bool = False

# sys_t["experiment_bool"] = False

# colours["speed_int"] = -1

# -- Main Loop --
while running:
    with open("config.json", "r+") as config:
        global_ht = json.loads(config.read())

    gui = global_ht["gui"]
    internal = gui["internal"]
    colours = gui["cols"]
    fonts = gui["font"]
    
    sys_t = global_ht["system"]
    mode = sys_t["mode"]

    while global_ht["system"]["song_storage_int"] > len(song_buffer_list):
        song_buffer_list.insert(0, -1)
    while global_ht["system"]["song_storage_int"] < len(song_buffer_list):
        song_buffer_list.pop(0)

    # bg
    screen.fill((colours["bg_list"][0], colours["bg_list"][1], colours["bg_list"][2]))

    # manual user input

    if (pygame.key.get_pressed()[pygame.K_LSHIFT]
            and pygame.key.get_pressed()[pygame.K_LCTRL]
            and pygame.mouse.get_pressed(3)[2]
            and not mouse_two_clicked_bool):  # left_shift & left ctrl & right mouse
        mode["select_int"] = len(mode["list"]) - 1
        mouse_two_clicked_bool = True
    elif (pygame.key.get_pressed()[pygame.K_LSHIFT]
            and pygame.mouse.get_pressed(3)[2]
            and not mouse_two_clicked_bool):  # left_shift & right mouse
        mode["select_int"] = change_mode(mode["select_int"], -1, mode["list"])
        mouse_two_clicked_bool = True

    if not sys_t["disable_mouse_bool"]:
        if pygame.mouse.get_pressed(3)[2] and song_vlc is not None and not mouse_two_clicked_bool:  # right click
            if not song_vlc.is_playing():  # if not playing, play it.
                song_vlc.play()
            else:  # if playing, set the position forward by 5%.
                song_vlc.set_position(float(song_vlc.get_position()) + 0.05)
            # print(f"PLAY THAT AT {song_vlc.get_position()}")
            mouse_two_clicked_bool = True

    # if pygame.mouse.get_pressed(3)[2] and pygame.key.get_pressed()[pygame.K_q] and not mouse_two_clicked_bool:
    #     sys_t["experiment_bool"] = not sys_t["experiment_bool"]
    #     print("EXPERIMENTAL MODE" + ("ACTIVATED" if sys_t["experiment_bool"] else "DEACTIVATED"))
    #     mouse_two_clicked_bool = True

    if pygame.mouse.get_pressed(3)[2]:
        pass
    else:
        mouse_two_clicked_bool = False

    if pygame.key.get_pressed()[pygame.K_SPACE]:
        if not space_pressed_bool:
            program_halt_bool = not program_halt_bool
            space_pressed_bool = True
            print(f"Program {"has been" if program_halt_bool else "is no longer"} halted.")
        else:
            pass
    else:
        space_pressed_bool = False

    if song_vlc is None or (song_vlc.get_position() >= 1 or not song_vlc.is_playing()) or (pygame.mouse.get_pressed(3)[0] and not sys_t["disable_mouse_bool"]):
        # print(f"PRE: {song_buffer_list}")
        if song_vlc is not None:
            time.sleep(1)
            song_vlc.pause()
            song_time_initial = 0

        for vol in range(0, len(song_buffer_list) - 1):
            # print(vol - 1)
            # song_buffer_list[len(song_buffer_list) - vol - 1] = song_buffer_list[len(song_buffer_list) - vol]
            song_buffer_list[vol] = song_buffer_list[vol + 1]

        song_buffer_list[len(song_buffer_list)-1] = get_next_song(song_buffer_list, directory)

        song_filename_str = os.listdir(directory)[song_buffer_list[len(song_buffer_list)-2]]
        song_dir = os.path.join(directory, song_filename_str)
        print(f"Playing: {song_filename_str} from {song_dir}")

        song_pydub = pydub.AudioSegment.from_file(song_dir)
        song_vlc = vlc.MediaPlayer(song_dir)
        song_vlc.audio_set_volume(sys_t["song_vol_int"])
        song_vlc.play()
        # print(f"POST: {song_buffer_list}")
    else:
        if song_vlc.get_time() - song_time_initial >= 1000 * internal["change_time_float"] and not colours["stop_bool"]:
            if sys_t["experiment_bool"]:
                sos_a = int(
                    (sum((song_pydub[song_vlc.get_time() - (1000 * internal["change_time_float"]): song_vlc.get_time()])
                         .get_array_of_samples())))
                sos_b = sos_a // 3
                sos_c = sos_a // (2**8)
                colours["newbg_list"] = [sos_a % 256, sos_b % 256, sos_c % 256]
                col_gen_bool = True
            else:
                colours["new_int"] = random.randrange(0, 3)
                colours["newbg_list"][colours["new_int"]] = int(
                    (
                        sum(
                            (song_pydub[song_vlc.get_time() - (1000 * internal["change_time_float"]): song_vlc.get_time()])
                            .get_array_of_samples()
                        )
                    ) % 256
                )
            song_time_initial = song_vlc.get_time()
            print(f"{colours["bg_list"]} -> TO -> {colours["newbg_list"]}") #  -- CHANGE: {colours["change_list"]}")

    for colour in range(3):
        def cols_bg_adjust(colours_list, colours_new_list, colours_change):
            if colours_list[colour] < colours_new_list[colour] <= 255 and int(colours_list[colour] + colours_change) <= 255:  # print("increasing")
                colours_list[colour] += colours_change
            if colours_list[colour] > colours_new_list[colour] > -1 and int(colours_list[colour] - colours_change >= 0):  # print("decreasing")
                colours_list[colour] -= colours_change
            else:
                pass
            return colours_list[colour]


        match mode["list"][mode["select_int"]]:
            case "normal":
                # colours["change_list"] = [0, 0, 0]
                # colours["float_list"][colour] = cols_bg_adjust(colours["float_list"], colours["newbg_list"], (abs(colours["float_list"][colour] - colours["newbg_list"][colour]) * dt) / internal["trans_time_float"])
                if colours["speed_int"] < 0 or col_gen_bool:
                    colours["speed_int"] = abs(colours["float_list"][colour] - colours["newbg_list"][colour]) * dt / internal["trans_time_float"]
                colours["float_list"][colour] = cols_bg_adjust(colours["float_list"], colours["newbg_list"], colours["speed_int"])
            case "smooth":
                # colours["change_list"][colour] = [0, 0, 0]
                colours["float_list"][colour] = cols_bg_adjust(colours["float_list"], colours["newbg_list"], (abs(colours["float_list"][colour] - colours["newbg_list"][colour]) * dt) / internal["trans_time_float"])
            case "pause":
                colours["speed_int"] = -1
        colours["bg_list"][colour] = round(colours["float_list"][colour])

    text_obj = pygame.font.SysFont(None, 64).render("'modif.txt' not found/not readable", True, (0, 0, 0))
    try:
        with open(global_ht["system"]["modif_str"], "r") as f:
            text_str = str(f.read())
        text_obj = pygame.font.SysFont(fonts["text_str"], fonts["text_size"], True).render(text_str, True, [255 - colours["bg_list"][0], 255 - colours["bg_list"][1], 255 - colours["bg_list"][2]])
    except Exception as e:
        print(e)
    finally:
        text_rect = text_obj.get_rect(center=(gui["width_int"] // 2, gui["height_int"] // 2))
        screen.blit(text_obj, text_rect)

    song_obj = pygame.font.SysFont(None, 48).render(f"""No Songname Detected""", True, (0, 0, 0))
    try:
        song_vlc.get_media().parse()
        song_obj = pygame.font.SysFont(fonts["sys_str"], fonts["sys_size"], True).render(
            f"""{song_filename_str[:-4]}""", True, colours["sys_list"]
        )
        song_obj = pygame.font.SysFont(fonts["sys_str"], fonts["sys_size"], True).render(
            f"""{song_vlc.get_media().get_meta(vlc.Meta.Title)}""", True, colours["sys_list"]
        )
    except Exception as e:
        print(e)
    finally:
        song_rect = song_obj.get_rect(center=(gui["width_int"] // 2, (gui["height_int"] // 2) + fonts["text_size"]))
        screen.blit(song_obj, song_rect)

    author_obj = pygame.font.SysFont(None, 48).render(f"""No Author Detected""", True, (0, 0, 0))
    try:
        song_vlc.get_media().parse()
        author_obj = pygame.font.SysFont(fonts["sys_str"], fonts["sys_size"], True).render(
            f"""by {song_vlc.get_media().get_meta(vlc.Meta.Artist)}""", True, colours["sys_list"]
        )
    except Exception as e:
        print(e)
    finally:
        author_rect = author_obj.get_rect(center=(gui["width_int"] // 2, (gui["height_int"] // 2) + fonts["text_size"] + fonts["sys_size"]))
        screen.blit(author_obj, author_rect)

    if sys_t["count_time_bool"]:
        song_scan_obj = pygame.font.SysFont(None, 48).render(f"""Nothing is Playing!""", True, (0, 0, 0))
        try:
            if sys_t["by_percent_bool"]:
                song_scan_obj = pygame.font.SysFont(fonts["time_str"], fonts["time_size"], True).render(f"""{song_vlc.get_position()*100:.2f}%""", True, colours["sys_list"])
            else:
                song_scan_obj = pygame.font.SysFont(fonts["time_str"], fonts["time_size"], True).render(f"""{song_vlc.get_time()/1000:.0f}s / {song_vlc.get_length()/1000:.0f}s""", True, colours["sys_list"])
        except Exception as e:
            print(e)
        finally:
            song_scan_rect = song_scan_obj.get_rect(center=(gui["width_int"] // 2, (gui["height_int"] // 2) + fonts["text_size"] + (2 * fonts["sys_size"])))
            screen.blit(song_scan_obj, song_scan_rect)

    if program_halt_bool:
        program_halt_obj = pygame.font.SysFont(None, 20).render(f"""PROGRAM HALTED -- SAFE TO MODIFY {"config.json"}""", False, (255, 0, 0))
        program_halt_rect = program_halt_obj.get_rect(top=0, left=0)
        screen.blit(program_halt_obj, program_halt_rect)

    # print(colours["bg_list"])
    if sys_t["show_mode_bool"]:
        program_mode_obj = pygame.font.SysFont(None, 24).render(f"""Mode: {mode["list"][mode["select_int"]]}""", True, [255 - colours["bg_list"][0], 255 - colours["bg_list"][1], 255 - colours["bg_list"][2]])
        program_mode_rect = program_mode_obj.get_rect(top=5, right=gui["width_int"] - 5)
        screen.blit(program_mode_obj, program_mode_rect)

    if not program_halt_bool:
        with open("config.json", "w+") as config:
            config.write(json.dumps(global_ht))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if song_vlc is not None and song_vlc.is_playing():
                song_vlc.pause()
                song_vlc.release()
                song_vlc = None
                song_pydub = None
            pygame.quit()
            exit(0)

    pygame.display.flip()
    clock.tick(gui["fps_int"])
    col_gen_bool = False

    # print(f"mode: {mode["list"][mode["select_int"]]}, song: {song_filename_str[:-4]}\nR -- {colours["bg_list"][0]} ({colours["float_list"][0]:.2f}) : {colours["newbg_list"][0]} : {colours["change_list"][0]}\n" +
    #       f"G -- {colours["bg_list"][1]} ({colours["float_list"][1]:.2f}) : {colours["newbg_list"][1]} : {colours["change_list"][1]}\n" +
    #       f"B -- {colours["bg_list"][2]} ({colours["float_list"][2]:.2f}) : {colours["newbg_list"][2]} : {colours["change_list"][2]}")
