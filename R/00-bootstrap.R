# Run once, in the project root, to install what the site needs to render:
#   Rscript R/00-bootstrap.R

# Rscript starts with no CRAN mirror set, so install.packages() fails with
# "trying to use CRAN without setting a mirror". Set one for this session.
repos <- getOption("repos")
if (is.null(repos[["CRAN"]]) || repos[["CRAN"]] %in% c("", "@CRAN@")) {
  options(repos = c(CRAN = "https://cloud.r-project.org"))
}

cran_pkgs <- c(
  # site + reporting
  "quarto", "rmarkdown", "knitr", "downlit", "xml2", "sessioninfo",
  # data
  "dplyr", "tidyr", "tibble", "readr", "purrr", "stringr", "lubridate", "glue",
  # graphics + interactivity
  "ggplot2", "plotly", "leaflet", "DT", "htmlwidgets", "htmltools"
)

# Only needed if you add analyses that use them; they pull heavy system
# dependencies, so they are not installed by default.
# sf só é necessário se você puser um shapefile de bacia em data/gis/
optional_pkgs <- c("seacarb", "terra", "sf")

missing <- setdiff(cran_pkgs, rownames(installed.packages()))
if (length(missing)) install.packages(missing)

# streamMetabolizer is not on CRAN:
# install.packages("remotes")
# remotes::install_github("DOI-USGS/streamMetabolizer")

still_missing <- setdiff(cran_pkgs, rownames(installed.packages()))
if (length(still_missing)) {
  stop("failed to install: ", paste(still_missing, collapse = ", "))
}
cat("All", length(cran_pkgs), "packages available.\n")

# renv is optional and NOT run here: renv::init() restarts the R session and
# starts an empty project library, which makes previously installed packages
# look missing. Run it by hand, in an interactive session, only when you want
# a locked environment:
#   if (!requireNamespace("renv", quietly = TRUE)) install.packages("renv")
#   renv::init()      # then renv::snapshot() whenever you add a package
