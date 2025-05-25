🧱 blockMeshDict GUI Generator for OpenFOAM

🚀 A lightweight Python GUI to generate blockMeshDict files quickly and accurately for OpenFOAM users.


🧐 What is this?

This is a Tkinter-based GUI tool that helps CFD engineers and OpenFOAM users generate the blockMeshDict file interactively — no more manual editing or syntax errors! It's designed for beginners and pros alike who want a fast, clean, and customizable mesh setup.


🎯 Key Features

✅ Unit Selection: Supports m, cm, and mm — scales your geometry effortlessly.
✅ Geometry Inputs: Enter domain bounds and mesh lengths along X, Y, and Z directions.
✅ Cell Resolution: Define how many cells you want in each direction.
✅ Patch Configuration UI: Fully customizable patch names (inlet, outlet, wall, or even custom).
✅ Cell Analysis: Automatically checks if your mesh cells are cubic or non-cubic, and displays it with color-coded hints.
✅ Live Feedback: See errors or confirmation messages instantly.
✅ Clean Output: A properly formatted blockMeshDict is written directly to your project directory.


📐 Why is it useful?

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
