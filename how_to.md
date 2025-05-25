🚀 How to Use This App

Setting up and using this GUI is super simple — even if you're just getting started with Python and OpenFOAM!
✅ Step-by-Step Instructions:

🔽 Download or Clone the Repository

Option 1: Click the green Code button on this GitHub page, then Download ZIP.

Option 2: Use Git:

    git clone https://github.com/your-username/blockMeshDict-GUI.git
    cd blockMeshDict-GUI

🐍 Make Sure Python 3 is Installed

Check using:

    python3 --version

📦 No Extra Dependencies Needed!

This app uses only Tkinter, which is already included in standard Python installations. No pip install needed!

▶️ Run the App

In your terminal or command prompt:

    python3 bm_gen_gui_v1.py

🧮 Fill in Your Mesh Details

Choose your coordinate origin, dimensions, number of cells, and unit scale.

Customize patch names via the Configure Patch Names button.

Optionally check cell stats for cubicity (ideal mesh!).

📄 Click “Generate blockMeshDict”

The file blockMeshDict will be created in the current directory.

🚀 Use It in OpenFOAM

Just place the blockMeshDict file inside the system/ folder of your OpenFOAM case and run:

    blockMesh
