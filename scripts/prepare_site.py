"""Prepare the DCPS JupyterLite site before `jupyter lite build`.

1. Downloads Pyodide 314.0.6 (the Python that runs in the browser) and keeps only
   what Unit 2 needs, so the site never loads Python from an outside CDN.
2. Gives every course notebook a kernel setting so students are not asked to pick one.

Usage:  python scripts/prepare_site.py            (downloads Pyodide)
        python scripts/prepare_site.py FILE.tar.bz2 (uses a tarball you already have)
"""
import json, os, shutil, sys, tarfile, urllib.request, glob

PYODIDE_VERSION = "314.0.6"   # must match jupyterlite-pyodide-kernel 0.8.6
URL = f"https://github.com/pyodide/pyodide/releases/download/{PYODIDE_VERSION}/pyodide-{PYODIDE_VERSION}.tar.bz2"
# Libraries Unit 2 imports. Add a name here if a lesson needs another library.
NEEDED = ["numpy", "pandas", "matplotlib", "scipy", "scikit-learn",
          "micropip", "packaging", "pyodide-http", "ipython", "traitlets",
          "pygments", "jedi", "decorator", "prompt-toolkit", "wcwidth",
          "six", "python-dateutil", "pytz", "tzdata"]
OUT = os.path.join("static", "pyodide")

def fetch(src):
    if src and os.path.exists(src):
        tar = src
    else:
        tar = "pyodide.tar.bz2"
        print("Downloading", URL)
        urllib.request.urlretrieve(URL, tar)
    print("Extracting", tar)
    with tarfile.open(tar) as t:
        t.extractall("_pyodide_full", filter="data")
    return os.path.join("_pyodide_full", "pyodide")

def trim(full):
    lock = json.load(open(os.path.join(full, "pyodide-lock.json")))["packages"]
    norm = lambda s: s.lower().replace("_", "-")
    names = {norm(k): k for k in lock}
    keep = set()
    def add(n):
        k = names.get(norm(n))
        if k and k not in keep:
            keep.add(k)
            for d in lock[k].get("depends", []): add(d)
    for n in NEEDED: add(n)
    files = {lock[k]["file_name"] for k in keep}
    shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)
    for f in os.listdir(full):
        p = os.path.join(full, f)
        if os.path.isdir(p): continue
        core = not (f.endswith(".whl") or f.endswith(".zip") or f.endswith(".metadata"))
        if core or f in files or f == "python_stdlib.zip" or (f.endswith(".metadata") and f[:-9] in files):
            shutil.copy2(p, os.path.join(OUT, f))
    size = sum(os.path.getsize(os.path.join(OUT, f)) for f in os.listdir(OUT)) / 1e6
    print(f"Kept {len(keep)} packages ({size:.0f} MB): {', '.join(sorted(keep))}")
    assert os.path.exists(os.path.join(OUT, "python_stdlib.zip")), "python_stdlib.zip missing"

def stamp_kernels():
    for path in glob.glob("content/**/*.ipynb", recursive=True):
        nb = json.load(open(path, encoding="utf-8"))
        ks = nb.setdefault("metadata", {}).get("kernelspec")
        if not ks:
            nb["metadata"]["kernelspec"] = {"name": "python", "display_name": "Python (Pyodide)", "language": "python"}
            with open(path, "w", encoding="utf-8") as f: json.dump(nb, f, indent=1, ensure_ascii=False); f.write("\n")
            print("Set kernel for", path)

if __name__ == "__main__":
    trim(fetch(sys.argv[1] if len(sys.argv) > 1 else None))
    stamp_kernels()
    shutil.rmtree("_pyodide_full", ignore_errors=True)
