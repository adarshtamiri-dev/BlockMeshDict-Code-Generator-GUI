# 🧱 blockMeshDict GUI Generator for OpenFOAM

# 🚀 A lightweight Python GUI to generate blockMeshDict files quickly and accurately for OpenFOAM users.

# For Beginners 

## This is a GUI tool that helps beginners generate the blockMeshDict file. It's designed for beginners and pros alike who want a fast, clean, and customizable mesh setup.


## 📐 Why is it useful?

🛠️ Reduces setup time for simple blockMesh domains.

🧠 Removes guesswork — helps users focus on simulation, not syntax.

🎯 Avoids mesh errors by clearly displaying dimensions and patch faces.

 📊 Educational for beginners — makes learning mesh structure more intuitive.

💼 Perfect for academic projects, tutorials, and small-scale industrial CFD setups.


🖼️ Example Output Preview

 Vertices, blocks, boundaries and more are all auto-calculated.

Saves the file as blockMeshDict — ready to plug into your constant/polyMesh folder!

🔧 Requirements

Python 3.x

Tkinter (comes pre-installed with most Python distributions)

💡 Future Ideas

Add preview rendering using matplotlib or PyOpenGL

 Export multiple mesh formats

 Add support for grading and advanced mesh setups

🙌 Contribution

Feel free to fork, star, and contribute!
Found a bug or have a feature idea? Open an issue!
🧠 Author

Created with ❤️ by an OpenFOAM enthusiast to make meshing easier for everyone.



## 🚀 How to Use This App

Setting up and using this GUI is super simple — even if you're just getting started with Python and OpenFOAM!
✅ Step-by-Step Instructions:

🔽 Download or Clone the Repository

Option 1: Click the green Code button on this GitHub page, then Download ZIP.

Option 2: Use Git:

    git clone https://github.com/aerxstxck/BlockMeshDict-Code-Generator-GUI.git
    cd BlockMeshDict-Code-Generator-GUI

🐍 Make Sure Python 3 is Installed

Check using:

    python3 --version

📦 No Extra Dependencies Needed!

This app uses only Tkinter, which is already included in standard Python installations. No pip install needed!

▶️ Run the App

In your terminal or command prompt:

    python3 bmg-v3.py

🧮 Fill in Your Mesh Details

Choose your coordinate origin, dimensions, number of cells, and unit scale.

Customize patch names via the Configure Patch Names button.

Optionally check cell stats for cubicity (ideal mesh!).

📄 Click “Generate blockMeshDict”

 The file blockMeshDict will be created in the current directory.

🚀 Use It in OpenFOAM

Just place the blockMeshDict file inside the system/ folder of your OpenFOAM case and run:
    
    blockMesh

![image](https://github.com/user-attachments/assets/64af4783-1a25-4df4-886e-2137932981cd)


