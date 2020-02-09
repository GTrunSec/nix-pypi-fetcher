## Scripts for updating the pypi sources nix expresison

### Step 1: Crawl Pypi metadata
```bash
python3 crawl_pypi
```
This will create and populate `pypi.db`

### Step 2: Generate Nix Expresison from `pypi.db`
(WARNING: This will demand aroung 5GB of RAM)
```bash
python3 gen_nix_expr.py > pypi.nix
```
This will dump the nix expression containing all pypi sources into `pypi.nix`