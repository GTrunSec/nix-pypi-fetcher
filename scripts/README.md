## Scripts for updating the pypi sources nix expresison

### Step 1: Crawl Pypi metadata
```bash
python3 crawl_pypi
```
This will create and populate `pypi.db`

### Step 2: Generate Nix Expresison from `pypi.db`
(WARNING: This will demand aroung 5GB of RAM)
```bash
python3 gen_nix_expr.py
```
This will dump the nix expressions containing all pypi sources into `./pypi/`.
To use the new sources, replace the `pypi` directory of the project root with the one you just generated.
