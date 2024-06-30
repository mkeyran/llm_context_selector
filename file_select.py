#! /bin/python
import curses
import os
import sys
import subprocess

def sort_files(files):
    directories = [f for f in files if os.path.isdir(f)]
    regular_files = [f for f in files if os.path.isfile(f)]
    directories.sort(key=str.lower)
    regular_files.sort(key=str.lower)
    return directories + regular_files

def main(stdscr):
    curses.curs_set(0)
    stdscr.clear()
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    
    start_dir = os.getcwd()
    current_dir = start_dir
    selected_files = []
    current_index = 0
    scroll_offset = 0
    
    while True:
        stdscr.clear()
        height, width = stdscr.getmaxyx()
        
        files = [os.path.join(current_dir, f) for f in os.listdir(current_dir)]
        sorted_files = sort_files(files)
        display_files = [os.pardir] + [os.path.basename(f) for f in sorted_files]
        
        if current_index - scroll_offset >= height - 1:
            scroll_offset = current_index - height + 2
        elif current_index < scroll_offset:
            scroll_offset = current_index

        # Left panel: file list
        for i in range(height - 1):
            file_index = i + scroll_offset
            if file_index >= len(display_files):
                break
            file = display_files[file_index]
            full_path = os.path.join(current_dir, file) if file != os.pardir else os.path.dirname(current_dir)
            is_dir = file == os.pardir or os.path.isdir(full_path)
            is_selected = full_path in selected_files
            
            if file_index == current_index:
                stdscr.attron(curses.A_REVERSE)
            if is_dir:
                stdscr.attron(curses.color_pair(1))
            elif is_selected:
                stdscr.attron(curses.color_pair(2))
            
            display_name = ".." if file == os.pardir else file
            stdscr.addstr(i, 0, display_name[:width//2-1])
            
            if is_dir:
                stdscr.attroff(curses.color_pair(1))
            elif is_selected:
                stdscr.attroff(curses.color_pair(2))
            if file_index == current_index:
                stdscr.attroff(curses.A_REVERSE)
        
        # Right panel: selected files
        for i, file in enumerate(selected_files):
            if i >= height - 1:
                break
            rel_path = os.path.relpath(file, start_dir)
            stdscr.addstr(i, width//2, rel_path[:width//2-1])
        
        stdscr.refresh()
        
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == curses.KEY_UP and current_index > 0:
            current_index -= 1
        elif key == curses.KEY_DOWN and current_index < len(display_files) - 1:
            current_index += 1
        elif key == curses.KEY_PPAGE:  # Page Up
            current_index = max(0, current_index - (height - 1))
        elif key == curses.KEY_NPAGE:  # Page Down
            current_index = min(len(display_files) - 1, current_index + (height - 1))
        elif key == ord('\n'):  # Enter key
            if display_files[current_index] == os.pardir:
                current_dir = os.path.dirname(current_dir)
                current_index = 0
                scroll_offset = 0
            else:
                full_path = os.path.join(current_dir, display_files[current_index])
                if os.path.isdir(full_path):
                    current_dir = full_path
                    current_index = 0
                    scroll_offset = 0
                else:
                    if full_path in selected_files:
                        selected_files.remove(full_path)
                    else:
                        selected_files.append(full_path)
        elif key == ord('g'):
            generate_output(selected_files, start_dir)
            stdscr.addstr(height-1, 0, "Output generated. Press any key to continue.")
            stdscr.getch()
        elif key == ord('c'):
            copy_to_clipboard(selected_files, start_dir)
            stdscr.addstr(height-1, 0, "Copied to clipboard. Press any key to continue.")
            stdscr.getch()

def generate_output(selected_files, start_dir):
    with open('output.txt', 'w') as outfile:
        for file_path in selected_files:
            rel_path = os.path.relpath(file_path, start_dir)
            outfile.write(f"#{rel_path}\n")
            with open(file_path, 'r') as infile:
                outfile.write(infile.read())
            outfile.write("\n---\n")

def copy_to_clipboard(selected_files, start_dir):
    output = ""
    for file_path in selected_files:
        rel_path = os.path.relpath(file_path, start_dir)
        output += f"#{rel_path}\n"
        with open(file_path, 'r') as infile:
            output += infile.read()
        output += "\n---\n"
    
    process = subprocess.Popen(['xclip', '-selection', 'clipboard'], stdin=subprocess.PIPE)
    process.communicate(output.encode())

if __name__ == "__main__":
    curses.wrapper(main)