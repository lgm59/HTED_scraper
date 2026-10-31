# FlyBase High-Throughput Expression Scraper

A Python command-line tool that collects high-throughput gene expression data from [FlyBase](https://flybase.org) for a list of *Drosophila melanogaster* genes in one run, replacing manual lookups gene by gene.

Written as a solo project to support a research lab's gene expression analysis.

**Demo video:** [https://www.loom.com/share/31d5d38dd60f4f238de9568e028c74f7](https://drive.google.com/file/d/1R3vptTJy8CDo1YTsUECgQntzTkGDegva/view?usp=sharing)

## What it does

For each gene in a CSV list, the program:

1. Opens FlyBase in a Firefox browser controlled by Selenium and searches for the gene.
2. Opens the page's **Expression** section and expands the collapsed high-throughput data panels, which the site loads dynamically.
3. Reads four RNA-seq datasets:
   - FlyAtlas2 Anatomy RNA-Seq
   - modENCODE Anatomy RNA-Seq
   - modENCODE Development RNA-Seq
   - modENCODE Treatments RNA-Seq
4. Ranks the entries in each dataset by expression value and keeps the **top three**.
5. Records `No Entry` for any dataset a gene doesn't have.

Results are collected in a pandas table (one row per gene, one column per dataset) that you can copy to the clipboard and paste into a spreadsheet.

## Requirements

- Python 3.8+
- [Firefox](https://www.mozilla.org/firefox/)
- Python packages:

```
pip install selenium pandas webdriver-manager
```

`webdriver-manager` downloads the correct Firefox driver (geckodriver) automatically. Copying results to the clipboard uses `pandas.DataFrame.to_clipboard`, which works out of the box


## Input format

A `.csv` file where:

- Cell **A1 is blank** and row 1 contains text.
- Cell **A2** contains the header `GeneFamMems`.
- Gene names (FlyBase gene symbols) are listed below it in column A.

## Usage

```
python main.py
```

1. Paste the file path of your gene list when prompted.
2. Firefox opens and the program works through the list, printing progress after each gene.
3. When it finishes, type `c` to copy the results table to your clipboard, or `r` to restart with another list.

## Output

One row per gene, in the same order as the input list, with four columns (one per dataset). Each cell holds the top three entries and their values, in the form `Tissue: value, Tissue: value, Tissue: value`. See the demo video for a real run.

The table does not include a gene-name column, so keep your input list alongside the results to match rows to genes.

## Limitations

- It depends on FlyBase's current page layout. Some elements are located by position, so a redesign of the site can break it.
- It runs one gene at a time through a visible browser window, so large lists take time.
- Results are copied to the clipboard, not saved to a file.
- It is intended for small, polite request volumes. Please follow FlyBase's terms of use and consider their bulk data downloads for very large queries.

## Files

- `main.py`: the scraper
