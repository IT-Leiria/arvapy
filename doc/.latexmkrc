@default_files = ('doc.tex');

# Run latexmk silently, not output to text
$silent     = 0;
$quiet      = 0;
# Create file containing a list of the files that these programs have read and written
# For better source file detection
$recorder   = 1;

# Generate a pdf version of the document using pdflatex
$pdf_mode   = 1;
# $pdflatex = "pdflatex -synctex=1 -interaction=nonstopmode --shell-escape";
# $pdflatex .= ' -synctex=1 -interaction=nonstopmode  -shell-escape';

$pdflatex = 'pdflatex -synctex=1 -interaction=nonstopmode %O  --shell-escape %S';

# Use bibtex if an appropriate *.bib file exists
$bibtex_use = 1;

# If nonzero, continue processing past minor latex errors including unrecognized cross references
$force_mode = 0;

# Define all output directories to be "tmp"
# All build files will now be placed in this directory
# $aux_dir = "/tmp/build_latex";
# $tmpdir  = "/tmp/build_latex";
# $out_dir = '/tmp/build_latex';

$clean_ext = "out snm acn acr aux alg bbl blg fls ist log lof lot maf out toc nav xdy";

