# Resume

LaTeX source for my resume.

## Versions

- `Israel_Alcantara_Resume_Master.tex` is my full master resume. It holds every role, project, course, honor, and organization, and runs four pages. The other versions are cut down from it.
- `Israel_Alcantara_Resume_PM.tex` is aimed at associate project manager and project coordinator roles.
- `Israel_Alcantara_Resume_IT_Analyst.tex` is aimed at IT analyst and technology analyst roles.
- `Israel_Alcantara_Resume_Cloud_Support.tex` is aimed at cloud support associate roles.
- `Israel_Alcantara_Resume_Software_Engineer.tex` is aimed at software engineering roles.
- `Israel_Alcantara_Resume_Retail.tex` is aimed at retail sales roles.

Each `.tex` file builds to the `.pdf` with the same name. The role versions are one page each.

`main.tex` and `resume-pm-it.tex` are older versions.

## How to build

The template uses pdfLaTeX. With a TeX distribution such as MiKTeX or TeX Live installed:

```sh
latexmk -pdf Israel_Alcantara_Resume_PM.tex
```

You can also upload a `.tex` file to Overleaf and compile it there with pdfLaTeX.

The `.tex` files are generated. `preamble.tex` holds the shared layout, `build.py` writes the five role versions, and `master_full.py` writes the master. To rebuild all six from Python 3:

```sh
python3 build.py
python3 master_full.py
```

The phone number is left out of public builds. If a `phone.tex` file sits next to the `.tex` files, the header prints its contents. `phone.tex` is in `.gitignore`.
