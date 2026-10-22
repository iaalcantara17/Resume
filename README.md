# Resume

LaTeX source for my resume.

## Versions

- `main.tex` is my main resume. It builds to `main.pdf`.
- `resume-pm-it.tex` has the same content in a different order, aimed at technical project management, project management, and IT roles. It builds to `resume-pm-it.pdf`.

## How to build

The template uses pdfLaTeX. With a TeX distribution such as MiKTeX or TeX Live installed:

```sh
latexmk -pdf main.tex
latexmk -pdf resume-pm-it.tex
```

You can also upload a `.tex` file to Overleaf and compile it there with pdfLaTeX.

The phone number is left out of public builds. If a `phone.tex` file sits next to the `.tex` files, the header prints its contents. `phone.tex` is in `.gitignore`.
