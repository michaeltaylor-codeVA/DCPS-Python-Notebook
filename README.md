# DCPS Data Science: JupyterLite Site

This repository builds the browser-based Jupyter Notebook site that DCPS students use for the Python lessons in Introduction to Data Science (Unit 2 onward). It is maintained by CodeVA.

Students open the site in a web browser. Nothing is installed on their computers, no accounts are needed, and no student work is sent anywhere: notebooks are saved in each student's own browser. Python and every library the course uses are bundled into the site itself, so it does not depend on any outside download service that a school web filter might block.

## What's in this repository

| Path | What it is |
|---|---|
| `content/` | Everything students see in the file browser: lesson folders, starter notebooks, datasets. **Add course files here.** |
| `content/00 Device Check.ipynb` | One-click check that a computer can run everything Unit 2 needs. |
| `scripts/prepare_site.py` | Bundles Python into the site and sets the kernel on every notebook. Runs automatically. |
| `.github/workflows/deploy.yml` | Rebuilds and republishes the site every time anything changes. |
| `jupyter-lite.json` | Site settings: opens in the Jupyter Notebook interface and names the site. |
| `requirements.txt` | Pinned build tool versions. |

**Guidelines**

* **Put each lesson's dataset in the same folder as its notebook.** Then the notebook loads it by plain filename, for example `pd.read_csv('pokemon.csv')`. Never use Colab-style paths such as `/content/pokemon.csv`.
* **Keep each file under about 50 MB.** Browsers limit storage, and larger files may fail to open. The full `DC_Properties.csv` (55 MB) is too large; use `DC_Properties_300_Student.csv`.
* **Never put teacher keys or answer files in this repository.** The site is public. Keep keys in the Drive teacher folders.
* **Clear notebook outputs before uploading** so students start from a clean notebook.

## What teachers and students should know

* **Work is saved in the browser on that computer only.** It does not follow a student to another computer, and clearing browser data deletes it. Private or incognito windows delete it when closed. Students should choose **File > Download** at the end of every class to keep a copy of their notebook.
* **The first cell takes longer.** Python loads into the browser the first time a notebook runs in a session (about 30 to 60 seconds on first visit; faster after that).
* **Saving a chart shows a pink warning.** `plt.savefig(...)` prints a *MatplotlibDeprecationWarning* in this environment. The chart still saves correctly; students can ignore it.
* **If a "Select Kernel" box appears,** choose **Python (Pyodide)**. The build sets this automatically, so this should be rare.
* **When the site is updated,** students who already opened a file keep their own saved copy. To get the new version of a file, a student can right-click it in the file browser and choose **Delete**, then reload the page; the updated original reappears.

## Adding a Python library

The site includes pandas, NumPy, Matplotlib, SciPy, scikit-learn, and their dependencies. If a lesson needs another library, add its name to the `NEEDED` list at the top of `scripts/prepare_site.py` and commit. The library must be one that Pyodide supports (see the list at pyodide.org, under "Packages built in Pyodide").

## Preview the site on your own computer (optional)

With Python 3.12 installed:

```
pip install -r requirements.txt
python scripts/prepare_site.py
jupyter lite build --contents content --output-dir dist
python -m http.server 8000 --directory dist
```

Then open `http://localhost:8000` in a browser. (Opening `dist/index.html` directly from the file system does not work; it must be served.)

## Versions

Pinned and tested together: jupyterlite-core 0.8.6, jupyterlite-pyodide-kernel 0.8.6, Pyodide 314.0.6 (Python 3.14, pandas 3.0, NumPy 2.4, Matplotlib 3.10, SciPy 1.18, scikit-learn 1.8). If you upgrade the build tools, update `PYODIDE_VERSION` in `scripts/prepare_site.py` to match and rerun the Device Check.
