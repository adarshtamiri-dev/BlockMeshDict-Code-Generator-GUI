# blockMeshDict (box) GUI Generator

## A lightweight Python GUI to generate blockMeshDict files quickly and accurately for OpenFOAM users.

This is a GUI tool that helps beginners and those who want a fast and clean code. 

- Perfect for academic projects, tutorials, and small-scale industrial setups  

## Example Output Preview

Vertices, blocks, boundaries and more are all auto-calculated.  
Saves the file as `blockMeshDict` — ready to plug into your `constant/polyMesh` folder.

## Requirements

- Python 3.x
- Tkinter Library

## Contribution

Feel free to fork, star, and contribute.  
Found a bug or have a feature idea? Open an issue.

### Step-by-Step Instructions

#### 1. Download or Clone the Repository

Option 1: Click the green Code button on this GitHub page, then Download ZIP.

Option 2: Use Git:

```bash
git clone https://github.com/aerxstxck/BlockMeshDict-Code-Generator-GUI.git
cd BlockMeshDict-Code-Generator-GUI
```

2. Run the Application

Once you're in the repository's directory, execute the Python script using your terminal or command prompt:
```bash
python3 bmg-v3.py
```

3. Fill in Your Mesh Details

Inside the GUI, provide the required mesh parameters. This includes defining your coordinate origin, the overall dimensions of your domain, and the number of cells along each axis. You'll also specify the unit scale for your mesh.

Use the "Configure Patch Names" button to customize your boundary patches. Optionally, you can check the "Cell Stats" for insights into mesh quality, such as cubicity.
4. Generate the blockMeshDict File

After inputting all the details, click the "Generate blockMeshDict" button. The blockMeshDict file will then be created and saved in the current directory from which you launched the script.
5. Use in OpenFOAM

To integrate this mesh into your OpenFOAM case, place the generated blockMeshDict file inside the system/ folder of your OpenFOAM case directory. Afterward, execute the blockMesh utility in your OpenFOAM terminal to generate the mesh:
```bash
blockMesh
```
