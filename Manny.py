import subprocess

dim = str(subprocess.check_output("xrandr  | grep \* | cut -d' ' -f4", shell = True)).split("\\n")[0].split("\'")[1].split("x")

#Center a Tkinter window 
def center_window(widget):
        mid_width = int(int(dim[0])/2)
        mid_height = int(int(dim[1])/2)
        w_width = widget.winfo_width()
        w_height = widget.winfo_height()

        widget.geometry(f"{w_width}x{w_height}+{int(mid_width-w_width/2)}+{int(mid_height-w_height/2)}")