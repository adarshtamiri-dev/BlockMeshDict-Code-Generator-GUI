import tkinter as tk
from tkinter import ttk
import json
import os

patch_faces = ["bottom (zmin)", "top (zmax)", "front (ymax)", "back (ymin)", "left (xmin)", "right (xmax)"]
default_patch_types = ["inlet", "outlet", "walls", "custom"]

# Initialize with blank patch names
patch_names = {
    "bottom (zmin)": "",
    "top (zmax)": "",
    "front (ymax)": "",
    "back (ymin)": "",
    "left (xmin)": "",
    "right (xmax)": ""
}

SAVE_FILE = "save_bmgp.json"

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
        "patch_names": patch_names,
        "save_responses": save_responses_var.get()
    }
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

def open_patch_config():
    config_win = tk.Toplevel(root)
    config_win.title("Configure Patch Names")
    config_win.geometry("350x400")
    config_win.resizable(False, False)

    patch_vars = {}
    custom_entries = {}

    def on_patch_type_change(event, face):
        sel = patch_vars[face].get()
        if sel == "custom":
            custom_entries[face].config(state="normal")
            if patch_names.get(face) and patch_names[face] not in default_patch_types:
                custom_entries[face].delete(0, tk.END)
                custom_entries[face].insert(0, patch_names[face])
        else:
            custom_entries[face].delete(0, tk.END)
            custom_entries[face].config(state="disabled")

    def save_and_close():
        for face in patch_faces:
            selected = patch_vars[face].get()
            if selected == "custom":
                name = custom_entries[face].get().strip()
                if not name:
                    name = "customPatch"
            else:
                name = selected
            patch_names[face] = name
        config_win.destroy()
        status_label.config(text="Patch names updated.")
        # If save responses is ON, save right away
        if save_responses_var.get():
            save_data()
        update_patch_btn_color()  # Update color after closing

    for face in patch_faces:
        frame = tk.Frame(config_win)
        frame.pack(pady=8, padx=10, fill='x')
        tk.Label(frame, text=face + ":", width=15, anchor='w').pack(side=tk.LEFT)

        # Determine starting value for combobox
        current_name = patch_names.get(face, "")
        start_value = ""
        if current_name in default_patch_types:
            start_value = current_name
        elif current_name:
            start_value = "custom"
        patch_var = tk.StringVar(value=start_value)
        patch_vars[face] = patch_var

        combo = ttk.Combobox(frame, values=default_patch_types, textvariable=patch_var, width=10, state="readonly")
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e, f=face: on_patch_type_change(e, f))

        custom_entry = tk.Entry(frame, width=15, state="disabled")
        custom_entry.pack(side=tk.LEFT, padx=5)
        custom_entries[face] = custom_entry

        if patch_var.get() == "custom":
            custom_entry.config(state="normal")
            if current_name not in default_patch_types:
                custom_entry.insert(0, current_name)

    # Save and Close button
    btn_frame = tk.Frame(config_win)
    btn_frame.pack(pady=15)
    tk.Button(btn_frame, text="Save and Close", command=save_and_close, bg="#4CAF50", fg="white", width=15).pack()

def patch_names_complete():
    # Returns True if all patch names are non-empty
    for face in patch_faces:
        name = patch_names.get(face, "").strip()
        if not name:
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
    stats_window.geometry("350x200")

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

    unit_scale = {'m': 1, 'cm': 0.01, 'mm': 0.001}
    scale = unit_scale[scale_unit_var.get()]
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

    # Group faces by patch names
    grouped_faces = {}
    for face in patch_faces:
        name = patch_names.get(face, "").strip()
        if not name:
            name = "walls"
        if name not in grouped_faces:
            grouped_faces[name] = []
        grouped_faces[name].append(face_vertex_map[face])

    boundary_str = "boundary\n(\n"
    for patch_name, faces in grouped_faces.items():
        boundary_str += f"    {patch_name}\n    {{\n        type {patch_name};\n        faces\n        (\n"
        for face_vertices in faces:
            boundary_str += f"            {face_vertices}\n"
        boundary_str += "        );\n    }\n"
    boundary_str += ");\n"

    blockMeshDict = f"""/*--------------------------------*- C++ -*----------------------------------*\\
| =========                 |                                                 |
| \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
|  \\\\    /   O peration     | Version:  v2312                                 |
|   \\\\  /    A nd           | Website:  www.openfoam.com                      |
|    \\\\/     M anipulation  |                                                 |
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
        cells_x_var.get(), cells_y_var.get(), cells_z_var.get()
    ]):
        return False
    for face in patch_faces:
        if patch_names.get(face, ""):
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
        popup.geometry("300x100")
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
        for face in patch_faces:
            patch_names[face] = ""
        save_responses_var.set(False)
        update_patch_btn_color()
        update_reset_btn_color()
        status_label.config(text="All fields have been reset.", fg="blue")
        confirm.destroy()

    confirm = tk.Toplevel(root)
    confirm.title("Confirm Reset")
    confirm.geometry("300x120")
    confirm.configure(bg="#F44336")
    tk.Label(confirm, text="Are you sure you want to reset all fields?", bg="#F44336", fg="white", font=("Arial", 11)).pack(pady=15)
    btns = tk.Frame(confirm, bg="#F44336")
    btns.pack()
    tk.Button(btns, text="Yes, Reset", command=do_reset, bg="white", fg="#F44336", width=12).pack(side=tk.LEFT, padx=10)
    tk.Button(btns, text="Cancel", command=confirm.destroy, bg="white", fg="#F44336", width=12).pack(side=tk.LEFT, padx=10)

root = tk.Tk()
root.title("blockMeshDict Generator")
root.geometry("500x600")
root.resizable(False, False)

scale_unit_var = tk.StringVar(value="m")
tk.Label(root, text="Select Scale Unit:", font=("Arial", 10, "bold")).pack(pady=5)
units_frame = tk.Frame(root)
units_frame.pack()
for unit in ["m", "cm", "mm"]:
    tk.Radiobutton(units_frame, text=unit, variable=scale_unit_var, value=unit).pack(side=tk.LEFT, padx=10)

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

patch_btn = tk.Button(btn_frame, text="Configure Patch Names", command=open_patch_config, bg="#2196F3", fg="white", width=20)
patch_btn.grid(row=0, column=0, padx=5, pady=5)

stats_btn = tk.Button(btn_frame, text="Show Cell Stats", command=show_cell_stats, bg="#2196F3", fg="white", width=20)
stats_btn.grid(row=0, column=1, padx=5, pady=5)

generate_btn = tk.Button(root, text="Generate blockMeshDict", command=generate_dict, bg="#4CAF50", fg="white", width=25)
generate_btn.pack(pady=10)

save_responses_var = tk.BooleanVar(value=False)
save_radio_frame = tk.Frame(root)
save_radio_frame.pack(pady=10)
tk.Label(save_radio_frame, text="Save Inputs and Patch Names:").pack(anchor="w")
tk.Radiobutton(save_radio_frame, text="Yes", variable=save_responses_var, value=True).pack(side=tk.LEFT, padx=15)
tk.Radiobutton(save_radio_frame, text="No", variable=save_responses_var, value=False).pack(side=tk.LEFT, padx=15)

# Add Reset and Exit buttons below save inputs radio buttons
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
    patch_names.update(saved.get("patch_names", patch_names))
    save_responses_var.set(saved.get("save_responses", False))
    status_label.config(text="Loaded previous responses.", fg="green")

update_patch_btn_color()  # Set initial color on load
update_reset_btn_color()  # Set initial color for reset button

root.mainloop()
