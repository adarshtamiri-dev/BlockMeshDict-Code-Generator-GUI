import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import re

patch_faces = ["bottom (zmin)", "top (zmax)", "front (ymax)", "back (ymin)", "left (xmin)", "right (xmax)"]
patch_types = ["patch", "wall", "symmetryPlane", "empty", "wedge", "cyclic"]
patch_role_types = ["inlet", "outlet", "custom"]

# Initialize with blank patch names
patch_names = {
    "bottom (zmin)": {"type": "patch", "name": ""},
    "top (zmax)": {"type": "patch", "name": ""},
    "front (ymax)": {"type": "patch", "name": ""},
    "back (ymin)": {"type": "patch", "name": ""},
    "left (xmin)": {"type": "patch", "name": ""},
    "right (xmax)": {"type": "patch", "name": ""}
}

SAVE_FILE = "responses.json"

def load_saved_data():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, "r") as f:
                data = json.load(f)
            return data
        except Exception:
            return {}
    return {}

def save_data():
    data = {
        "xmin": xmin_var.get(),
        "ymin": ymin_var.get(),
        "zmin": zmin_var.get(),
        "length_x": length_x_var.get(),
        "length_y": length_y_var.get(),
        "length_z": length_z_var.get(),
        "cells_x": cells_x_var.get(),
        "cells_y": cells_y_var.get(),
        "cells_z": cells_z_var.get(),
        "scale_unit": scale_unit_var.get(),
        "custom_sign": custom_sign_var.get(),
        "custom_exp": custom_exp_var.get(),
        "patch_names": patch_names,
        "save_responses": save_responses_var.get()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

def open_patch_config():
    config_win = tk.Toplevel(root)
    config_win.title("Configure Boundaries")
    
    # Set the size and center the window
    window_width = 600
    window_height = 400
    center_window(config_win, window_width, window_height)

    config_win.resizable(False, False)

    patch_type_vars = {}
    patch_name_vars = {}
    validation_label = tk.Label(config_win, text="", fg="red")
    validation_label.pack(pady=(0, 5))

    # Function to validate boundary names
    def validate_boundary_name(name):
        if not name:
            return False, "Boundary name cannot be empty."
        if name[0].isdigit():
            return False, "Boundary name cannot start with a number."
        if re.search(r'[#/]', name):
            return False, "Boundary name cannot contain '#' or '/'."
        if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', name):
            return False, "Boundary name can only contain alphanumeric characters and underscores."
        return True, ""

    def on_type_change(event, face):
        validation_label.config(text="") # Clear validation message on type change

    # Table header
    header = tk.Frame(config_win)
    header.pack(pady=(10, 0), padx=10, fill='x')
    tk.Label(header, text="Face", width=15, anchor='w', font=("Arial", 10, "bold")).pack(side=tk.LEFT)
    tk.Label(header, text="Type", width=14, anchor='w', font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=(0, 10))
    tk.Label(header, text="Boundary Name", width=18, anchor='w', font=("Arial", 10, "bold")).pack(side=tk.LEFT)

    for face in patch_faces:
        frame = tk.Frame(config_win)
        frame.pack(pady=5, padx=10, fill='x')
        tk.Label(frame, text=face + ":", width=15, anchor='w').pack(side=tk.LEFT)

        type_val = patch_names[face]["type"]
        name_val = patch_names[face]["name"]

        patch_type_var = tk.StringVar(value=type_val)
        patch_type_vars[face] = patch_type_var
        combo = ttk.Combobox(frame, values=patch_types, textvariable=patch_type_var, width=14, state="readonly")
        combo.pack(side=tk.LEFT, padx=(0, 10))
        combo.bind("<<ComboboxSelected>>", lambda event, f=face: on_type_change(event, f))

        patch_name_var = tk.StringVar(value=name_val)
        patch_name_vars[face] = patch_name_var
        entry = tk.Entry(frame, textvariable=patch_name_var, width=18)
        entry.pack(side=tk.LEFT)
        entry.bind("<KeyRelease>", lambda event: validation_label.config(text="")) # Clear on key release

    def reset_window_fields():
        validation_label.config(text="")
        for face in patch_faces:
            patch_type_vars[face].set("patch")
            patch_name_vars[face].set("")

    def save_and_close_patch_config():
        validation_label.config(text="") # Clear previous warning

        # Validate boundary names first
        for face in patch_faces:
            name = patch_name_vars[face].get().strip()
            is_valid, message = validate_boundary_name(name)
            if not is_valid:
                validation_label.config(text=f"Error for '{face}': {message}")
                return

        # Check for same name, different type conflict
        name_type_map = {}
        for face in patch_faces:
            name = patch_name_vars[face].get().strip()
            p_type = patch_type_vars[face].get()
            if name in name_type_map:
                if name_type_map[name] != p_type:
                    validation_label.config(text=f"Same boundary name '{name}' has different types!")
                    return
            else:
                name_type_map[name] = p_type

        # If all validations pass, save and close
        for face in patch_faces:
            t = patch_type_vars[face].get()
            n = patch_name_vars[face].get().strip()
            patch_names[face] = {"type": t, "name": n}
        config_win.destroy()
        status_label.config(text="Boundary types/names updated.")
        if save_responses_var.get():
            save_data()
        update_patch_btn_color()

    btn_frame = tk.Frame(config_win)
    btn_frame.pack(pady=15)
    tk.Button(btn_frame, text="Save and Close", command=save_and_close_patch_config, bg="#4CAF50", fg="white", width=18).pack(side=tk.LEFT, padx=10)
    tk.Button(btn_frame, text="Reset", command=reset_window_fields, bg="#F44336", fg="white", width=12).pack(side=tk.LEFT, padx=10)

def patch_names_complete():
    # Returns True if all patch names are non-empty
    for face in patch_faces:
        name_data = patch_names.get(face)
        if not name_data or not name_data.get("name", "").strip():
            return False
    return True

def update_patch_btn_color():
    if patch_names_complete():
        patch_btn.config(bg="#2196F3")  # blue
    else:
        patch_btn.config(bg="#FF9800")  # orange

def show_cell_stats():
    stats_window = tk.Toplevel(root)
    stats_window.title("Cell Stats")
    
    # Set the size and center the window
    window_width = 350
    window_height = 200
    center_window(stats_window, window_width, window_height)

    try:
        length_x = float(length_x_var.get())
        length_y = float(length_y_var.get())
        length_z = float(length_z_var.get())
        cells_x = int(cells_x_var.get())
        cells_y = int(cells_y_var.get())
        cells_z = int(cells_z_var.get())
    except ValueError:
        tk.Label(stats_window, text="Invalid input values.", fg="red").pack(pady=20)
        return

    dx = length_x / cells_x
    dy = length_y / cells_y
    dz = length_z / cells_z

    cell_dimensions = f"{dx:.3f} x {dy:.3f} x {dz:.3f} ({scale_unit_var.get()})"
    if abs(dx - dy) < 1e-6 and abs(dy - dz) < 1e-6:
        nature = "Cubic."
        color = "green"
        message = "This is Optimal"
    else:
        nature = "Non-Cubic."
        color = "orange"
        message = "Proceed with precaution."

    tk.Label(stats_window, text=f"Cell Dimensions: {cell_dimensions}", font=('Arial', 12)).pack(pady=5)
    tk.Label(stats_window, text=f"Geometry form: {nature}", bg=color, fg="white", font=('Arial', 12)).pack(pady=5)
    tk.Label(stats_window, text=message, fg=color, font=('Arial', 10, 'italic')).pack(pady=5)
    tk.Button(stats_window, text="Close", command=stats_window.destroy).pack(pady=10)

def generate_dict():
    all_fields = [
        xmin_var.get(), ymin_var.get(), zmin_var.get(),
        length_x_var.get(), length_y_var.get(), length_z_var.get(),
        cells_x_var.get(), cells_y_var.get(), cells_z_var.get()
    ]
    if not all(all_fields):
        status_label.config(text="One or more field(s) were not entered.", fg="red")
        return

    try:
        xmin = float(xmin_var.get())
        ymin = float(ymin_var.get())
        zmin = float(zmin_var.get())
        length_x = float(length_x_var.get())
        length_y = float(length_y_var.get())
        length_z = float(length_z_var.get())
        cells_x = int(cells_x_var.get())
        cells_y = int(cells_y_var.get())
        cells_z = int(cells_z_var.get())
    except ValueError:
        status_label.config(text="Please enter valid numbers.", fg="red")
        return

    # Determine scale
    if scale_unit_var.get() == "custom..":
        try:
            sign = custom_sign_var.get()
            exp = int(custom_exp_var.get())
            if not (1 <= exp <= 10):
                raise ValueError
            exponent = exp if sign == "+" else -exp
            scale = 10 ** exponent
        except Exception:
            scale = 1  # fallback
    else:
        unit_scale = {'m': 1, 'cm': 0.01, 'mm': 0.001}
        scale = unit_scale.get(scale_unit_var.get(), 1)
    xmax = xmin + length_x
    ymax = ymin + length_y
    zmax = zmin + length_z

    face_vertex_map = {
        "bottom (zmin)": "(0 1 2 3)",
        "top (zmax)": "(4 5 6 7)",
        "front (ymax)": "(2 3 7 6)",
        "back (ymin)": "(0 1 5 4)",
        "left (xmin)": "(0 3 7 4)",
        "right (xmax)": "(1 2 6 5)"
    }

    # Group faces by patch names and types
    grouped_faces = {}
    patch_types_map = {}
    for face in patch_faces:
        val = patch_names.get(face, "")
        if isinstance(val, dict):
            patch_type = val.get("type", "patch")
            name = val.get("name", "").strip() or patch_type
        else: # Handle legacy saved data where patch_names might just store the name
            patch_type = "patch" # Default type for legacy data
            name = val.strip() or patch_type
        if name not in grouped_faces:
            grouped_faces[name] = []
            patch_types_map[name] = patch_type
        grouped_faces[name].append(face_vertex_map[face])

    boundary_str = "boundary\n(\n"
    for patch_name, faces in grouped_faces.items():
        patch_type = patch_types_map.get(patch_name, "patch")
        boundary_str += f"    {patch_name}\n    {{\n        type {patch_type};\n        faces\n        (\n"
        for face_vertices in faces:
            boundary_str += f"            {face_vertices}\n"
        boundary_str += "        );\n    }\n"
    boundary_str += ");\n"

    blockMeshDict = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                               |                                 |
| \\\\      /  F ield        | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration    | Version:  v2312                                 |
|   \\\\  /    A nd          | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation |                                                 |
\\*---------------------------------------------------------------------------*/
FoamFile
{{
    version     2.0;
    format      ascii;
    class       dictionary;
    object      blockMeshDict;
}}

scale   {scale};

vertices
(
    ({xmin} {ymin} {zmin})
    ({xmax} {ymin} {zmin})
    ({xmax} {ymax} {zmin})
    ({xmin} {ymax} {zmin})
    ({xmin} {ymin} {zmax})
    ({xmax} {ymin} {zmax})
    ({xmax} {ymax} {zmax})
    ({xmin} {ymax} {zmax})
);

blocks
(
    hex (0 1 2 3 4 5 6 7) ({cells_x} {cells_y} {cells_z}) simpleGrading (1 1 1)
);

edges();

{boundary_str}
// ************************************************************************* //
"""
    with open("blockMeshDict", "w") as f:
        f.write(blockMeshDict)

    status_label.config(text="blockMeshDict has been generated!", fg="green")

    if save_responses_var.get():
        save_data()

def all_fields_reset():
    # Check if all input fields and patch names are empty/default
    if any([
        xmin_var.get(), ymin_var.get(), zmin_var.get(),
        length_x_var.get(), length_y_var.get(), length_z_var.get(),
        cells_x_var.get(), cells_y_var.get(), cells_z_var.get(),
        scale_unit_var.get() != "m", # Check if not default "m"
        custom_sign_var.get() != "+", # Check if not default "+"
        custom_exp_var.get() != "1"   # Check if not default "1"
    ]):
        return False
    for face in patch_faces:
        val = patch_names.get(face)
        if val and (val.get("type", "patch") != "patch" or val.get("name", "").strip() != ""):
            return False
    return True

def update_reset_btn_color():
    if all_fields_reset():
        reset_btn.config(bg="#2196F3")  # blue
    else:
        reset_btn.config(bg="#F44336")  # red

def reset_all_fields():
    if all_fields_reset():
        # Already reset, show info popup
        popup = tk.Toplevel(root)
        popup.title("Already Reset")
        window_width = 300
        window_height = 100
        center_window(popup, window_width, window_height)
        popup.configure(bg="#2196F3")
        tk.Label(popup, text="All fields are already reset.", bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=20)
        tk.Button(popup, text="OK", command=popup.destroy, bg="white", fg="#2196F3", width=10).pack()
        return

    def do_reset():
        xmin_var.set("")
        ymin_var.set("")
        zmin_var.set("")
        length_x_var.set("")
        length_y_var.set("")
        length_z_var.set("")
        cells_x_var.set("")
        cells_y_var.set("")
        cells_z_var.set("")
        scale_unit_var.set("m") # Reset to default
        custom_sign_var.set("+") # Reset to default
        custom_exp_var.set("1")  # Reset to default
        hide_custom_scale_entry_in_inputs() # Hide custom scale entry
        for face in patch_faces:
            patch_names[face] = {"type": "patch", "name": ""} # Reset to default dict structure
        save_responses_var.set(False)
        update_patch_btn_color()
        update_reset_btn_color()
        status_label.config(text="All responses have been cleared.", fg="blue")
        confirm.destroy()

    confirm = tk.Toplevel(root)
    confirm.title("Confirm Reset")
    window_width = 400
    window_height = 120
    center_window(confirm, window_width, window_height)
    #confirm.configure(bg="#F44336") # Commented out this line as per your original code
    tk.Label(confirm, text="Are you sure you want to delete all your responses?", fg="black", font=("Arial", 10)).pack(pady=15)
    btns = tk.Frame(confirm)
    btns.pack()
    tk.Button(btns, text="Yes, Reset", command=do_reset, fg="white", bg="red", width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(btns, text="Cancel", command=confirm.destroy, bg="white", width=12).pack(side=tk.LEFT, padx=10)

root = tk.Tk()
root.title("blockMeshDict Generator")
# Center the main window as well
root_width = 500
root_height = 600
center_window(root, root_width, root_height)
root.resizable(False, False)

scale_unit_var = tk.StringVar(value="m")
custom_sign_var = tk.StringVar(value="+")
custom_exp_var = tk.StringVar(value="1")
custom_scale_frame = None

def show_custom_scale_entry_in_inputs(parent):
    global custom_scale_frame
    if custom_scale_frame is not None:
        custom_scale_frame.destroy()
    custom_scale_frame = tk.Frame(parent)
    custom_scale_frame.pack(pady=3)
    tk.Label(custom_scale_frame, text="Custom scale: 1e", font=("Arial", 10)).pack(side=tk.LEFT)
    sign_menu = ttk.Combobox(custom_scale_frame, values=["+", "-"], width=2, state="readonly", textvariable=custom_sign_var)
    sign_menu.pack(side=tk.LEFT, padx=2)
    if custom_sign_var.get() in ["+", "-"]:
        sign_menu.set(custom_sign_var.get())
    else:
        sign_menu.set("+")
    exp_entry = tk.Entry(custom_scale_frame, textvariable=custom_exp_var, width=2)
    exp_entry.pack(side=tk.LEFT, padx=2)
    tk.Label(custom_scale_frame, text=" * m", font=("Arial", 10)).pack(side=tk.LEFT)

def hide_custom_scale_entry_in_inputs():
    global custom_scale_frame
    if custom_scale_frame is not None:
        custom_scale_frame.destroy()
        custom_scale_frame = None

def on_scale_select(event):
    if scale_unit_var.get() == "custom..":
        show_custom_scale_entry_in_inputs(input_frame)
    else:
        hide_custom_scale_entry_in_inputs()

tk.Label(root, text="Select Scale:", font=("Arial", 10, "bold")).pack(pady=5)
units_frame = tk.Frame(root)
units_frame.pack()

scale_options = ["m", "cm", "mm", "custom.."]
scale_map = {
    "m": "m",
    "cm": "cm",
    "mm": "mm",
    "custom..": "custom.."
}
scale_dropdown = ttk.Combobox(units_frame, values=scale_options, state="readonly", textvariable=scale_unit_var)
scale_dropdown.current(0)
scale_dropdown.pack(anchor="w")
def scale_dropdown_callback(event):
    on_scale_select(event)
scale_dropdown.bind("<<ComboboxSelected>>", scale_dropdown_callback)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

xmin_var = tk.StringVar()
ymin_var = tk.StringVar()
zmin_var = tk.StringVar()
length_x_var = tk.StringVar()
length_y_var = tk.StringVar()
length_z_var = tk.StringVar()
cells_x_var = tk.StringVar()
cells_y_var = tk.StringVar()
cells_z_var = tk.StringVar()

def make_labeled_entry(parent, label_text, var):
    frame = tk.Frame(parent)
    frame.pack(pady=3)
    tk.Label(frame, text=label_text + ":", width=15, anchor="w").pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=var, width=12)
    entry.pack(side=tk.LEFT)
    return entry

make_labeled_entry(input_frame, "Xmin", xmin_var)
make_labeled_entry(input_frame, "Ymin", ymin_var)
make_labeled_entry(input_frame, "Zmin", zmin_var)
make_labeled_entry(input_frame, "Length in X", length_x_var)
make_labeled_entry(input_frame, "Length in Y", length_y_var)
make_labeled_entry(input_frame, "Length in Z", length_z_var)
make_labeled_entry(input_frame, "Cells in X direction", cells_x_var)
make_labeled_entry(input_frame, "Cells in Y direction", cells_y_var)
make_labeled_entry(input_frame, "Cells in Z direction", cells_z_var)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

patch_btn = tk.Button(btn_frame, text="Configure Boundaries", command=open_patch_config, bg="#2196F3", fg="white", width=20)
patch_btn.grid(row=0, column=0, padx=5, pady=5)

stats_btn = tk.Button(btn_frame, text="Show Cell Stats", command=show_cell_stats, bg="#2196F3", fg="white", width=20)
stats_btn.grid(row=0, column=1, padx=5, pady=5)

generate_btn = tk.Button(root, text="Generate blockMeshDict", command=generate_dict, bg="#4CAF50", fg="white", width=25)
generate_btn.pack(pady=10)

save_responses_var = tk.BooleanVar(value=False)
save_radio_frame = tk.Frame(root)
save_radio_frame.pack(pady=10)
save_checkbox = tk.Checkbutton(save_radio_frame, text="Save responses before generating.", variable=save_responses_var)
save_checkbox.pack(anchor="w")

btns_below = tk.Frame(root)
btns_below.pack(pady=10)
reset_btn = tk.Button(btns_below, text="Reset", command=reset_all_fields, bg="#F44336", fg="white", width=12)
reset_btn.pack(side=tk.LEFT, padx=10)
exit_btn = tk.Button(btns_below, text="Exit", command=root.destroy, bg="#F44336", fg="white", width=12)
exit_btn.pack(side=tk.LEFT, padx=10)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=10)

# Load saved data if exists
saved = load_saved_data()
if saved:
    xmin_var.set(saved.get("xmin", ""))
    ymin_var.set(saved.get("ymin", ""))
    zmin_var.set(saved.get("zmin", ""))
    length_x_var.set(saved.get("length_x", ""))
    length_y_var.set(saved.get("length_y", ""))
    length_z_var.set(saved.get("length_z", ""))
    cells_x_var.set(saved.get("cells_x", ""))
    cells_y_var.set(saved.get("cells_y", ""))
    cells_z_var.set(saved.get("cells_z", ""))
    scale_unit_var.set(saved.get("scale_unit", "m"))
    custom_sign_var.set(saved.get("custom_sign", "+"))
    custom_exp_var.set(saved.get("custom_exp", "1"))

    if scale_unit_var.get() in scale_options:
        scale_dropdown.set(scale_unit_var.get())
    else:
        scale_dropdown.set("custom..")

    # Update patch_names from saved data, handling old format
    saved_patch_names = saved.get("patch_names", {})
    for face in patch_faces:
        if face in saved_patch_names:
            val = saved_patch_names[face]
            if isinstance(val, dict):
                patch_names[face] = val
            else: # Convert old string format to new dictionary format
                patch_names[face] = {"type": "patch", "name": val}
        else: # Ensure all patch_faces are initialized
            patch_names[face] = {"type": "patch", "name": ""}

    save_responses_var.set(saved.get("save_responses", False))
    status_label.config(text="Loaded previous responses.", fg="green")

if scale_unit_var.get() == "custom..":
    show_custom_scale_entry_in_inputs(input_frame)
else:
    hide_custom_scale_entry_in_inputs()

update_patch_btn_color()
update_reset_btn_color()

root.mainloop()
