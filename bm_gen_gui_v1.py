import tkinter as tk
from tkinter import ttk

patch_faces = ["bottom (zmin)", "top (zmax)", "front (ymax)", "back (ymin)", "left (xmin)", "right (xmax)"]

# Default patch types
default_patch_types = ["inlet", "outlet", "wall", "custom"]

# This dict will hold patch names keyed by face
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

    entries = {}

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

    patch_vars = {}
    custom_entries = {}

    for face in patch_faces:
        frame = tk.Frame(config_win)
        frame.pack(pady=8, padx=10, fill='x')

        tk.Label(frame, text=face+":", width=15, anchor='w').pack(side=tk.LEFT)

        patch_var = tk.StringVar(value=patch_names.get(face, "walls"))
        patch_vars[face] = patch_var

        combo = ttk.Combobox(frame, values=default_patch_types, textvariable=patch_var, width=10, state="readonly")
        combo.pack(side=tk.LEFT, padx=5)
        combo.bind("<<ComboboxSelected>>", lambda e, f=face: on_patch_type_change(e, f))

        custom_entry = tk.Entry(frame, width=15, state="disabled")
        custom_entry.pack(side=tk.LEFT, padx=5)
        custom_entries[face] = custom_entry

        # If currently custom, enable entry and fill value
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
    # Validate inputs
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

    # Compose boundary section from patch_names
    face_vertex_map = {
        "bottom (zmin)": "(0 1 2 3)",
        "top (zmax)": "(4 5 6 7)",
        "front (ymax)": "(2 3 7 6)",
        "back (ymin)": "(0 1 5 4)",
        "left (xmin)": "(0 3 7 4)",
        "right (xmax)": "(1 2 6 5)"
    }

    boundary_str = "boundary\n(\n"
    for face, name in patch_names.items():
        boundary_str += f"    {name}{{ type patch; faces ( {face_vertex_map[face]} ); }}\n"
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

xmin {xmin};
ymin {ymin};
zmin {zmin};

dx {length_x};
dy {length_y};
dz {length_z};

xmax {xmax};
ymax {ymax};
zmax {zmax};

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

blocks (hex (0 1 2 3 4 5 6 7) ({cells_x} {cells_y} {cells_z}) simpleGrading (1 1 1));

edges();

{boundary_str}
// ************************************************************************* //
"""

    with open("blockMeshDict", "w") as f:
        f.write(blockMeshDict)

    status_label.config(text="blockMeshDict generated successfully!", fg="green")


root = tk.Tk()
root.title("blockMeshDict Generator")
root.geometry("370x550")
root.resizable(False, False)

# Scale unit selection
scale_unit_var = tk.StringVar(value="m")
tk.Label(root, text="Select Scale Unit:", font=("Arial", 10, "bold")).pack(pady=5)
units_frame = tk.Frame(root)
units_frame.pack()
for unit in ["m", "cm", "mm"]:
    rb = tk.Radiobutton(units_frame, text=unit, variable=scale_unit_var, value=unit)
    rb.pack(side=tk.LEFT, padx=10)

# Input fields function
def make_labeled_entry(parent, label_text, var):
    frame = tk.Frame(parent)
    frame.pack(pady=5, fill='x', padx=15)
    label = tk.Label(frame, text=label_text, anchor='w', width=18)
    label.pack(side=tk.LEFT)
    entry = tk.Entry(frame, textvariable=var, width=12)
    entry.pack(side=tk.LEFT)

xmin_var = tk.StringVar(value="-2")
ymin_var = tk.StringVar(value="-2")
zmin_var = tk.StringVar(value="-1")

length_x_var = tk.StringVar(value="2")
length_y_var = tk.StringVar(value="2")
length_z_var = tk.StringVar(value="20")

cells_x_var = tk.StringVar(value="20")
cells_y_var = tk.StringVar(value="20")
cells_z_var = tk.StringVar(value="20")

make_labeled_entry(root, "X min coordinate:", xmin_var)
make_labeled_entry(root, "Y min coordinate:", ymin_var)
make_labeled_entry(root, "Z min coordinate:", zmin_var)

make_labeled_entry(root, "Length in X:", length_x_var)
make_labeled_entry(root, "Length in Y:", length_y_var)
make_labeled_entry(root, "Length in Z:", length_z_var)

make_labeled_entry(root, "Cells in X dir:", cells_x_var)
make_labeled_entry(root, "Cells in Y dir:", cells_y_var)
make_labeled_entry(root, "Cells in Z dir:", cells_z_var)

tk.Button(root, text="Configure Patch Names", command=open_patch_config, bg="#2196F3", fg="white", font=("Arial", 11)).pack(pady=10)

tk.Button(root, text="Show Cell Stats", command=show_cell_stats, bg="#FF9800", fg="white", font=("Arial", 11, "bold")).pack(pady=5)


tk.Button(root, text="Generate blockMeshDict", command=generate_dict, bg="#4CAF50", fg="white", font=("Arial", 11, "bold")).pack(pady=10)

status_label = tk.Label(root, text="", font=("Arial", 9), fg="green")
status_label.pack()

root.mainloop()
