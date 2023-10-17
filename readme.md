# Pokemon Ruby AI

## Install instructions

1. Install conda (brew for mac, chocolatey could work on Windows. Or 
just download it from the official website 
https://docs.conda.io/projects/conda/en/23.1.x/user-guide/install/download.html)).

2. Check conda install status running conda --version on your local 
terminal

3. create a virtual env with

```
conda create --name pokemon_ai python=3.10
```

4. activate the environment with

```
conda activate pokemon_ai
```

(if you are running a older version of conda you will need to run `source 
activate pokemon_ai` instead on mac)

for windows:

```
activate pokemon_ai
```

5. Install require packages with:

```
conda install --file requirements.txt -c conda-forge 
```

6. Download VisualBoyAdvance from https://sourceforge.net/projects/vba/
