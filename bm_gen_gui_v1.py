import tkinter as tk
from tkinter import ttk

patch_faces = ["bottom (zmin)", "top (zmax)", "front (ymax)", "back (ymin)", "left (xmin)", "right (xmax)"]
default_patch_types = ["inlet", "outlet", "wall", "custom"]

patch_names = {
    "bottom (zmin)": "walls",
    "top (zmax)": "walls",
    "front (ymax)": "walls",
    "back (ymin)": "walls",
    "left (xmin)": "inlet",
    "right (xmax)": "outlet"
}

def open_patch_config():
    config_win = tk.Toplevel(root)
    config_win.title("Configure Patch Names")
    config_win.geometry("350x350")
    config_win.resizable(False, False)

    patch_vars = {}
    custom_entries = {}

    def on_patch_type_change(event, face):
        sel = patch_vars[face].get()
        if sel == "custom":
            custom_entries[face].config(state="normal")
        else:
            custom_entries[face].delete(0, tk.END)
            custom_entries[face].insert(0, "")
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

    for face in patch_faces:
        frame = tk.Frame(config_win)
        frame.pack(pady=8, padx=10, fill='x')
        tk.Label(frame, text=face + ":", width=15, anchor='w').pack(side=tk.LEFT)

        patch_var = tk.StringVar(value=patch_names.get(face, "walls"))
        patch_vars[face] = patch_var

        combo = ttk.Combobox(frame, values=default_patch_types, textvariable=patch_var, width=10, state="readonly")
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e, f=face: on_patch_type_change(e, f))

        custom_entry = tk.Entry(frame, width=15, state="disabled")
        custom_entry.pack(side=tk.LEFT, padx=5)
        custom_entries[face] = custom_entry

        if patch_var.get() == "custom":
            custom_entry.config(state="normal")
            custom_entry.insert(0, patch_names.get(face, ""))

    tk.Button(config_win, text="Save & Close", command=save_and_close, bg="#4CAF50", fg="white").pack(pady=15)

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
        patch = patch_names.get(face, "walls")
        if patch not in grouped_faces:
            grouped_faces[patch] = []
        grouped_faces[patch].append(face_vertex_map[face])

    # Build boundary string by grouping faces under one patch entry each
    boundary_str = "boundary\n(\n"
    for patch, faces in grouped_faces.items():
        # Decide patch type, default to 'wall' if unknown
        patch_type = patch if patch in ["inlet", "outlet", "wall"] else "wall"
        boundary_str += f"    {patch}\n    {{\n        type {patch_type};\n        faces\n        (\n"
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

    status_label.config(text="blockMeshDict generated with grouped patch faces!", fg="green")

root = tk.Tk()
root.title("blockMeshDict Generator")
root.geometry("370x550")
root.resizable(False, False)

scale_unit_var = tk.StringVar(value="m")
tk.Label(root, text="Select Scale Unit:", font=("Arial", 10, "bold")).pack(pady=5)
units_frame = tk.Frame(root)
units_frame.pack()
for unit in ["m", "cm", "mm"]:
    tk.Radiobutton(units_frame, text=unit, variable=scale_unit_var, value=unit).pack(side=tk.LEFT, padx=10)

def make_labeled_entry(parent, label_text, var):
    frame = tk.Frame(parent)
    frame.pack(pady=5, fill='x', padx=15)
    tk.Label(frame, text=label_text, anchor='w', width=18).pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=var, width=12)
    entry.pack(side=tk.LEFT)
    return entry

xmin_var = tk.StringVar()
ymin_var = tk.StringVar()
zmin_var = tk.StringVar()
length_x_var = tk.StringVar()
length_y_var = tk.StringVar()
length_z_var = tk.StringVar()
cells_x_var = tk.StringVar()
cells_y_var = tk.StringVar()
cells_z_var = tk.StringVar()

make_labeled_entry(root, "X min:", xmin_var)
make_labeled_entry(root, "Y min:", ymin_var)
make_labeled_entry(root, "Z min:", zmin_var)
make_labeled_entry(root, "Length X:", length_x_var)
make_labeled_entry(root, "Length Y:", length_y_var)
make_labeled_entry(root, "Length Z:", length_z_var)
make_labeled_entry(root, "Cells X:", cells_x_var)
make_labeled_entry(root, "Cells Y:", cells_y_var)
make_labeled_entry(root, "Cells Z:", cells_z_var)

tk.Button(root, text="Show Cell Stats", command=show_cell_stats, bg="#2196F3", fg="white").pack(pady=10)
tk.Button(root, text="Configure Patch Names", command=open_patch_config, bg="#FF5722", fg="white").pack(pady=10)
tk.Button(root, text="Generate blockMeshDict", command=generate_dict, bg="#4CAF50", fg="white").pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 10))
status_label.pack(pady=5)

root.mainloop()
