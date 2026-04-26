# song-to-colours
Uses PyDub to collect samples from a song, and uses PyGame to output a window that changes colour according to the samples from said songs. Plays the song using VLC.
Essentially, just a collaborative mish-mash of external libraries to create this script.

## the GUI
The GUI can be directly interacted with, using the mouse and some keyboard modifiers.

Left Click = if "disable_mouse_bool" is false, will play the current song if it isn't playing OR play the next song if it is.

Right Click = skips the current song ahead by 5% (or by +0.05 out of 1 within vlc).

L. SHIFT + Right Click = changes the mode, which determines how the colour transitions are displayed.

L. CTRL + L. SHIFT + Right Click = sets the mode to 'pause' (or, the last mode).


## modif.txt
This file can be edited to display text in the GUI. Any text inside the file will be displayed.

## config.json
The program (creates if non-existant, and) uses the 'config.json' file to deduce what it should do. Every frame, it loads the file, processes the data, and then uploads the file.
Editing the config while the program has been deployed is risky. Hence to counteract this, pressing 'SPACE' on your keyboard while tabbed into the program will halt the file upload process.
This way, you can modify the file and gain direct visual feedback on the changes without the potential for memory access errors.

## Configurations (Variables you can modify)
-- GUI

"width_int" = width of the window created.

"height_int" = height of the window created.

"fps_int" = maximum framerate of the window.

"caption_str" = name the window will be given.

"internal": {
  "trans_time_float": time taken for a colour transition to occur.
  
  "change_time_float": time taken for a new colour to be picked (to transition to).
  
},

"cols": {
 "bg_list" = changes the colour of the background directly, must be int.
 
 "float_list" = mathematical colour of the background, for advanced changes.
 
 "newbg_list" = the new background colour to be changed into.
 
 "sys_list" = colour of the fonts displaying file information.
 
 "new_int" = [OUTDATED], used as the selector for a colour from newbg_list to be changed randomly (when experimental_bool is false).
 
 "speed_int" = used for the 'normal' mode, which defines a fixed speed for bg_list to transition into newbg_list with.
 
 "stop_bool" = ceases colour changing entirely.
 
},

"font": {
 "text_size" = size of the text displayed from modif.txt.
 
 "sys_size" = ~ displaying file information.
 
 "time_size" = ~ displaying the runtime of the song.
 
 "text_str" = name of the font to be used for the text displayed from modif.txt.
 
 "sys_str" = ~ for file information.
 
 "time_str" = ~ for runtime.
 
}


-- SYSTEM

 "song_vol_int" = volume of the song playing.
 
 "song_storage_int" = the program retains a memory of the songs it has played, to prevent looping over the same song. this changes the size of that memory.
 
 "by_percent_bool" = should time be counted as a percentage?
 
 "count_time_bool" = should time be counted at all?
 
 "show_mode_bool" = should the mode be shown in the GUI (top right)?
 
 "disable_mouse_bool" = disables the left click functionality of the program (which changes the song).
 
 "experiment_bool" = uses a sampling-based system to determine colours. false defaults to a random pattern.
 
 "song_full_path_bool" = for 'song_folder_str', defines if the provided path is the full path or a nested path.
 
 "modif_str" = the nested file the program looks for to change the text in the GUI.
 
 "song_folder_str": the nested directory the program looks for to pick songs from.
 
 "mode": {
  "list" = all the available modes.
  
  "disabled_list" = any mode in here will be disabled in the 'list'.
  
  "select_int" = the selected mode.
  
  }


### REQUIRES PyDub: https://github.com/jiaaro/pydub
### - Python 3.13+ requires Audioop-lts: https://github.com/AbstractUmbra/audioop
### REQUIRES PyGame: https://github.com/pygame/pygame
### REQUIRES Python-VLC: https://github.com/oaubert/python-vlc/tree/master/examples
