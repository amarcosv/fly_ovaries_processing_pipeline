from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "literature_review_spatial_analysis.pdf")

BLUE  = (30, 80, 160)
LINK  = (0, 100, 200)
GRAY  = (80, 80, 80)
LGRAY = (230, 230, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


class PDF(FPDF):
    def header(self):
        self.set_fill_color(*BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6, "Literature Review - Spatial Analysis of Cell Populations from Fluorescence Microscopy", new_x="RIGHT", new_y="TOP")
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6, f"Page {self.page_no()} | PubMed search - March 2026 | fly_ovaries_processing_pipeline", align="C")

    def section_title(self, title):
        self.ln(4)
        self.set_fill_color(*BLUE)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def subsection_title(self, title):
        self.ln(3)
        self.set_text_color(*BLUE)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*BLUE)
        self.line(self.get_x(), self.get_y(), self.get_x() + 190, self.get_y())
        self.ln(2)

    def paper_entry(self, title, authors_journal, pmid, doi, abstract_bullets, relevance, display, controls):
        # Title box
        self.set_fill_color(*LGRAY)
        self.set_text_color(*BLACK)
        self.set_font("Helvetica", "B", 9)
        self.multi_cell(0, 5, title, fill=True, new_x="LMARGIN")
        # Authors / journal / IDs
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.set_x(self.l_margin)
        self.write(4, f"{authors_journal}  |  PMID: {pmid}  |  DOI: ")
        self.set_text_color(*LINK)
        self.write(4, doi, link=f"https://doi.org/{doi}")
        self.set_text_color(*GRAY)
        self.ln(4)
        self.ln(1)
        # Content rows
        self._labeled_block("Summary", abstract_bullets)
        self._labeled_block("Your relevance", relevance)
        self._labeled_block("Display ideas", display)
        self._labeled_block("Controls used", controls)
        self.ln(3)

    def _labeled_block(self, label, text):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.cell(28, 4, label + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 4, text, new_x="LMARGIN")

    def table_row(self, cols, widths, header=False):
        if header:
            self.set_fill_color(*BLUE)
            self.set_text_color(*WHITE)
            self.set_font("Helvetica", "B", 8)
        else:
            self.set_fill_color(*WHITE)
            self.set_text_color(*BLACK)
            self.set_font("Helvetica", "", 8)
        x0 = self.get_x()
        y0 = self.get_y()
        max_h = 0
        # measure height
        for text, w in zip(cols, widths):
            lines = self.multi_cell(w, 4, text, dry_run=True, output="LINES")
            max_h = max(max_h, len(lines) * 4 + 2)
        # draw cells
        for text, w in zip(cols, widths):
            self.set_xy(x0, y0)
            self.multi_cell(w, 4, text, border=1, fill=header, max_line_height=4, new_x="RIGHT", new_y="TOP")
            x0 += w
        self.set_xy(self.l_margin, y0 + max_h)

    def bullet_list(self, items, indent=5):
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BLACK)
        for item in items:
            self.set_x(self.l_margin + indent)
            self.multi_cell(0, 5, f"*  {item}", new_x="LMARGIN")


pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# -- TITLE PAGE BLOCK --------------------------------------------------------
pdf.set_font("Helvetica", "B", 16)
pdf.set_text_color(*BLUE)
pdf.ln(2)
pdf.multi_cell(0, 8, "Spatial Analysis of Cell Populations from\nFluorescence Microscopy", align="C", new_x="LMARGIN")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*GRAY)
pdf.cell(0, 6, "Literature review for the fly_ovaries_processing_pipeline project", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.cell(0, 6, "PubMed search conducted March 2026", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(4)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
intro = (
    "This review covers published work most relevant to segmenting cell populations from 3D fluorescence "
    "microscopy and characterizing their spatial distribution and connectivity. The focus is on: "
    "(1) Ripley's K and related spatial statistics, (2) cell contact graph and network analysis, "
    "(3) 3D segmentation + spatial phenotyping pipelines, and (4) statistical controls to avoid "
    "false conclusions. For each paper, display ideas and controls are highlighted."
)
pdf.multi_cell(0, 5, intro, new_x="LMARGIN")

# -- SECTION 1 ---------------------------------------------------------------
pdf.section_title("SECTION 1  -  Ripley's K and Spatial Statistics Methods")

pdf.paper_entry(
    title="Spatiopath: Statistical analysis of spatial patterns in tumor microenvironment images",
    authors_journal="Benimam et al.  -  Nature Communications 2025",
    pmid="40164621",
    doi="10.1038/s41467-025-57943-y",
    abstract_bullets=(
        "Extends Ripley's K to analyze cell-cell AND cell-tumor boundary interactions in multiplexed IF images. "
        "Introduces a null-hypothesis framework (CSR permutation envelopes) to distinguish significant associations from random. "
        "Validated with synthetic simulations before application to lung tumor sections."
    ),
    relevance=(
        "You could add a cell-to-tissue-boundary or cell-to-TJ-region proximity metric using the same extension of K. "
        "Their edge correction approach handles bounded tissue regions  -  critical for whole-ovary images."
    ),
    display="K(r) curves with Monte Carlo confidence bands (ribbon). Heatmaps of significant vs. random spatial zones.",
    controls="Synthetic simulation validation before real data. CSR permutation envelope (n=1000 randomizations)."
)

pdf.paper_entry(
    title="Benchmarking Spatial Co-Localization Methods for Single-Cell Multiplex Imaging",
    authors_journal="Soupir et al.  -  Statistics and Data Science in Imaging 2025",
    pmid="40051984",
    doi="10.1080/29979676.2024.2437947",
    abstract_bullets=(
        "Head-to-head benchmarking of 6 spatial co-localization metrics across simulated and real cancer imaging data. "
        "Tests statistical power and type I error for each metric."
    ),
    relevance=(
        "Key finding: Ripley's K and pair correlation g(r) have the greatest power to detect co-localization. "
        "Other commonly used metrics have poor power. Justifies your use of K and motivates adding g(r)."
    ),
    display="Power curves vs. effect size. ROC-style comparison of metrics.",
    controls="Simulated data with known spatial structure. Type I error checked with random data."
)

pdf.paper_entry(
    title="Tumor immune cell clustering and its association with survival in ovarian cancer",
    authors_journal="Wilson et al.  -  PLoS Computational Biology 2022",
    pmid="35235563",
    doi="10.1371/journal.pcbi.1009900",
    abstract_bullets=(
        "Ripley's K + permutation-based CSR test applied to multiplex IF data from 160 ovarian cancer patients. "
        "Compares cell abundance and spatial clustering separately; shows combining both metrics discriminates survival better than either alone."
    ),
    relevance=(
        "Strong evidence that spatial clustering metrics add information beyond cell counts. "
        "The K-curve summary statistic (area between observed and CSR) converts the curve into a scalar for statistical comparison across conditions."
    ),
    display="Per-sample K summary statistic as boxplots by condition. Kaplan-Meier curves stratified by spatial clustering.",
    controls="Permutation of cell labels within each tissue section (n=1000). Separate validation cohort (TMA)."
)

pdf.paper_entry(
    title="spatialTIME and iTIME: R package for spatial analysis of immunofluorescence data",
    authors_journal="Creed et al.  -  Bioinformatics 2021",
    pmid="34734969",
    doi="10.1093/bioinformatics/btab757",
    abstract_bullets=(
        "Open-source R package implementing Ripley's K, Besag's L, Macron's M, and G-function (nearest-neighbor CDF). "
        "Includes a Shiny web app for non-programmers. Produces publication-quality spatial organization plots."
    ),
    relevance=(
        "Ready-to-use toolbox. The M function (normalized K) is scale-free and comparable across samples of different sizes. "
        "The L(r)-r plot centers CSR at zero, making deviations immediately visible."
    ),
    display="L(r)-r curves (CSR baseline at zero). Univariate and bivariate spatial plots per sample.",
    controls="CSR permutation envelopes built into the package."
)

pdf.paper_entry(
    title="Geospatial distribution of cancer-associated fibroblasts in renal cell carcinoma",
    authors_journal="Chakiryan et al.  -  Cancers 2021",
    pmid="34359645",
    doi="10.3390/cancers13153743",
    abstract_bullets=(
        "Uses normalized Ripley's K at a fixed radius (nK(25) at 25 um) as a single summary scalar per sample. "
        "Also computes median nearest-neighbor distance between two cell types (CAFs and proliferating tumor cells). "
        "Links spatial metrics to patient survival and therapy resistance."
    ),
    relevance=(
        "The 'K at fixed radius' approach converts the K curve into one number per sample  -  directly usable in boxplots, "
        "ANOVAs, or regressions comparing experimental conditions. Choose radius based on biology (e.g., expected contact distance)."
    ),
    display="Boxplots of nK(r) and NN distance by condition. Scatter of NN distance vs. cell density.",
    controls="nK=1 represents CSR; test whether observed significantly differs. Multivariable Cox regression adjusting for covariates."
)

pdf.paper_entry(
    title="Analysis of spatial structure of epidermal nerve fibre patterns from replicated data",
    authors_journal="Myllymaki et al.  -  Journal of Microscopy 2012",
    pmid="22906010",
    doi="10.1111/j.1365-2818.2012.03636.x",
    abstract_bullets=(
        "CRITICAL METHODOLOGICAL PAPER. Presents a mixed model approach for Ripley's K applied to replicated spatial data "
        "(multiple images per subject/condition). Accounts for within-group vs. between-group variability."
    ),
    relevance=(
        "When you have multiple ovary images per condition, you cannot pool K functions naively  -  images from the same "
        "condition are not fully independent. This paper shows how to correctly compare groups with replicates."
    ),
    display="Pooled K function curves per group with confidence bands derived from mixed model.",
    controls="Mixed model F-test for group differences in K(r) across a range of radii."
)

pdf.paper_entry(
    title="Pairwise interaction Markov model for 3D epidermal nerve fibre endings",
    authors_journal="Konstantinou & Sarkka  -  Journal of Microscopy 2022",
    pmid="36106649",
    doi="10.1111/jmi.13142",
    abstract_bullets=(
        "Applies anisotropic cylindrical Ripley's K for 3D confocal data where Z resolution differs from XY. "
        "Models spatial interactions in 3D with an anisotropy factor."
    ),
    relevance=(
        "Your 3D confocal data has different pixel sizes in Z (0.25 um) vs XY (0.14 um). "
        "Your current Ripley's K implementation should use the anisotropy factor (1.78)  -  this paper shows the theory."
    ),
    display="K-function in cylindrical coordinates. Comparison of healthy vs. diabetic neuropathy groups.",
    controls="Anisotropy factor validated by comparison with isotropic model on synthetic data."
)

# -- SECTION 2 ---------------------------------------------------------------
pdf.section_title("SECTION 2  -  Cell Contact Graphs and Network Analysis")

pdf.paper_entry(
    title="Geometric and network organization of visceral organ epithelium",
    authors_journal="Liu et al.  -  Frontiers in Network Physiology 2023",
    pmid="37234691",
    doi="10.3389/fnetp.2023.1144186",
    abstract_bullets=(
        "Converts cell segmentation into a cell contact network (cell = node, shared border = edge). "
        "Computes polygon distributions, graphlet (subgraph) frequencies using EpiGraph software, and clustering coefficient. "
        "Compares heart, lung, liver, and bowel epithelia against mathematical reference patterns."
    ),
    relevance=(
        "Graphlet frequency analysis is a richer description of local network topology than clustering coefficient alone. "
        "EpiGraph is open source and applicable to your label images. Directly extends your current graph analysis."
    ),
    display="Radar plots comparing graphlet frequencies across conditions. Polygon distribution histograms.",
    controls=(
        "Three reference patterns: mathematical hexagonal grid, randomized, and Voronoi tessellation. "
        "Results compared against all three to determine which reference the observed tissue most resembles."
    )
)

pdf.paper_entry(
    title="Evolving topological order in the postnatal visceral pleura",
    authors_journal="Liu et al.  -  Developmental Dynamics 2024",
    pmid="38169311",
    doi="10.1002/dvdy.688",
    abstract_bullets=(
        "Applies Voronoi tessellation + graphlet motif frequencies + graph theory (clustering coefficient, network heterogeneity) "
        "to track developmental changes in tissue organization from postnatal day 1 to P15. "
        "Clustering coefficient decreases progressively  -  showing these metrics track biologically meaningful changes."
    ),
    relevance=(
        "Template for comparing spatial topology across experimental time points or conditions. "
        "Shows that graph metrics can detect subtle progressive changes in tissue organization."
    ),
    display="Line plots of clustering coefficient over developmental stages. Side-by-side polygon distribution bar charts.",
    controls="Developmental progression used as positive control (P1 vs P15 expected to differ)."
)

pdf.paper_entry(
    title="Fundamental physical cellular constraints drive self-organization of tissues",
    authors_journal="Sanchez-Gutierrez et al.  -  EMBO Journal 2015",
    pmid="26598531",
    doi="10.15252/embj.201592374",
    abstract_bullets=(
        "Uses Voronoi tessellation to characterize cell packing across diverse tissues including Drosophila. "
        "Shows polygon frequency distributions correlate with cell area distributions across species. "
        "Challenges the assumption of a universal stereotyped polygon distribution."
    ),
    relevance=(
        "Directly uses Drosophila tissue and demonstrates Voronoi analysis reveals differences between normal and "
        "perturbed tissue states (disease, genetic). Voronoi tessellation could complement your face-adjacency contact graph."
    ),
    display="Polygon type frequency distributions (bar charts). Scatter of polygon frequency vs. cell area CV.",
    controls="Computer model perturbations of force balance. Comparison across disease/genetic conditions and species."
)

# -- SECTION 3 ---------------------------------------------------------------
pdf.section_title("SECTION 3  -  3D Segmentation and Spatial Phenotyping Pipelines")

pdf.paper_entry(
    title="ShapeMetrics: A user-friendly pipeline for 3D cell segmentation and spatial tissue analysis",
    authors_journal="Takko et al.  -  Developmental Biology 2020 / Pajanoja & Kerosuo  -  Methods Mol Biol 2024",
    pmid="32061886 / 37219813",
    doi="10.1016/j.ydbio.2020.02.003",
    abstract_bullets=(
        "MATLAB pipeline: Ilastik-based segmentation -> 3D morphometrics (volume, surface area, ellipticity, elongation, longest axis) -> "
        "unsupervised heatmap clustering by morphometric features -> spatial mapping of clusters back to tissue."
    ),
    relevance=(
        "The spatial remapping step is powerful: it reveals whether morphometrically distinct cell subpopulations "
        "are spatially clustered. You could apply this to your VASA cell morphometrics to ask whether larger/smaller cells "
        "are located in specific ovary regions."
    ),
    display="Heatmaps of morphometric clusters. 3D spatial maps color-coded by cluster membership. Volume/surface scatter plots.",
    controls="Unsupervised clustering used without prior assumptions about subgroups."
)

pdf.paper_entry(
    title="Integrated Cytometry With Machine Learning for human kidney tissue (VTEA)",
    authors_journal="Winfree et al.  -  Laboratory Investigation 2023",
    pmid="36867975",
    doi="10.1016/j.labinv.2023.100104",
    abstract_bullets=(
        "VTEA (Volumetric Tissue Exploration and Analysis): integrates 3D segmentation, interactive cytometry, "
        "machine learning cell classification, and neighborhood analysis for multiplexed confocal images of human kidney."
    ),
    relevance=(
        "The neighborhood analysis module computes cell-type enrichment in local neighborhoods. "
        "Applicable to asking: do VASA cells near TJ cells differ morphometrically from isolated VASA cells?"
    ),
    display="Interactive scatter plots (cytometry-style). Spatial maps of cell subtypes and neighborhoods.",
    controls="Machine learning cross-validation for cell classification accuracy."
)

pdf.paper_entry(
    title="EASI-FISH for thick tissue defines lateral hypothalamus spatio-molecular organization",
    authors_journal="Wang et al.  -  Cell 2021",
    pmid="34875226",
    doi="10.1016/j.cell.2021.11.024",
    abstract_bullets=(
        "Expansion microscopy + StarDist 3D segmentation + spatial mapping of dozens of molecularly defined cell types "
        "in 300 um thick brain sections. Identifies 9 spatially defined subregions invisible to traditional anatomy."
    ),
    relevance=(
        "Demonstrates that 3D spatial analysis of segmented cell types can reveal tissue subdomains not visible by anatomy alone. "
        "Inspires asking whether VASA cell populations have spatially distinct subregions within the ovary."
    ),
    display="3D spatial maps with cell types color-coded. Cluster centroid heatmaps across tissue volume.",
    controls="scRNA-seq cross-validation of spatially-defined clusters. Iterative marker refinement."
)

# -- SECTION 4 ---------------------------------------------------------------
pdf.section_title("SECTION 4  -  Directly Relevant Biology (Drosophila Ovary)")

pdf.paper_entry(
    title="Specification and spatial arrangement of cells in the germline stem cell niche of the Drosophila ovary",
    authors_journal="Panchal et al.  -  PLoS Genetics 2017",
    pmid="28542174",
    doi="10.1371/journal.pgen.1006790",
    abstract_bullets=(
        "Studies Traffic jam (Tj) transcription factor  -  the same TJ marker used in the pipeline  -  and its role in "
        "determining spatial organization of germline stem cell niche cells (cap, escort, terminal filament cells). "
        "Shows Tj controls niche architecture and stem cell carrying capacity (normally 2-3 GSCs per niche)."
    ),
    relevance=(
        "Direct biological context for your TJ channel. Establishes that TJ-expressing cells' spatial arrangement "
        "is functionally significant. Provides baseline values for GSC number and niche cell organization in wildtype."
    ),
    display="Confocal images of niche architecture. Cell count quantifications per niche. Genetic perturbation comparisons.",
    controls="Loss-of-function and partial loss-of-function compared to wildtype. Notch pathway interaction as control."
)

# -- SECTION 5  -  SUMMARY TABLES -----------------------------------------------
pdf.add_page()
pdf.section_title("SECTION 5  -  Summary: New Metrics to Consider")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "The following metrics are used in the literature reviewed and could be added to your spatial analysis pipeline. "
    "All are applicable to segmented label images with known physical pixel sizes.",
    new_x="LMARGIN"
)
pdf.ln(2)

headers = ["Metric", "Key Paper", "What it adds vs. current pipeline"]
widths  = [48, 52, 90]
pdf.table_row(headers, widths, header=True)
rows = [
    ("Pair correlation\nfunction g(r)",
     "Soupir 2025",
     "Derivative of K(r); shows clustering at specific spatial scales rather than cumulatively. Higher statistical power than K alone."),
    ("M function\n(normalized K)",
     "Creed 2021\n(spatialTIME)",
     "Scale-free version of K. Comparable across samples of different sizes  -  critical when ovaries vary in volume."),
    ("K at fixed radius\n(scalar summary)",
     "Chakiryan 2021",
     "Single number per sample from K curve. Enables boxplots, ANOVA, regression across conditions without curve comparison."),
    ("NN distance between\ntwo cell types",
     "Chakiryan 2021",
     "Direct biological proximity: e.g., median distance from each VASA cell to the nearest TJ cell."),
    ("Graphlet frequency\n(EpiGraph)",
     "Liu 2023/2024",
     "Richer local topology descriptor than clustering coefficient alone. Detects subtle topological differences."),
    ("Polygon distribution",
     "Sanchez-Gutierrez\n2015, Liu 2023",
     "Cell packing topology from Voronoi. Compare to hexagonal/random/Voronoi references."),
    ("Morphometric cluster +\nspatial remapping",
     "Takko 2020\n(ShapeMetrics)",
     "Reveals spatial gradients in cell shape  -  are larger VASA cells located in specific ovary regions?"),
    ("Cell-to-boundary\nproximity",
     "Benimam 2025\n(Spatiopath)",
     "Distance of VASA cells from tissue boundary or from TJ-labeled region. Adds structural context."),
]
for row in rows:
    pdf.table_row(row, widths)

# -- SECTION 6  -  CONTROLS -----------------------------------------------------
pdf.ln(6)
pdf.section_title("SECTION 6  -  Critical Controls: What the Literature Recommends")

controls = [
    ("1. Cell density as covariate",
     "Higher cell density mechanically forces shorter nearest-neighbor distances. Always report density alongside "
     "spatial metrics and test whether differences in spatial patterns remain after controlling for density. "
     "(Chakiryan 2021, Soupir 2025)"),
    ("2. Permutation test for Ripley's K",
     "Randomly shuffle cell positions (or cell type labels) within each sample n=1000 times to build a null "
     "distribution. Your current pipeline uses the configuration model for graph topology  -  extend this to K as well. "
     "(Wilson 2022, Benimam 2025)"),
    ("3. Edge correction for bounded tissues",
     "Cells near the tissue boundary have fewer potential neighbors, artificially reducing K. Apply isotropic "
     "or Ripley's border correction. Critical when ovaries vary in shape and size. (Benimam 2025, Konstantinou 2022)"),
    ("4. Mixed model for replicated data",
     "When comparing conditions with multiple images per condition, treat each image as one replicate. "
     "Do not pool all images from a condition  -  this ignores within-condition biological variability. "
     "Summarize each image to a scalar (e.g., K at fixed radius) then compare scalars across conditions. "
     "(Myllymaki 2012)"),
    ("5. Type I error validation",
     "Before applying to real data, run your spatial metrics on simulated random point patterns. "
     "Verify that the test correctly does not reject CSR when data are actually random. "
     "(Soupir 2025, Benimam 2025)"),
    ("6. Biological positive control",
     "A genetic or pharmacological perturbation known to disrupt cell organization should produce a detectable "
     "change in your spatial metrics. If it does not, your metrics may lack sensitivity. "
     "(Panchal 2017, Sanchez-Gutierrez 2015)"),
    ("7. Reference pattern comparison for graphs",
     "When reporting clustering coefficient or graphlet frequencies, always compare to at least two reference patterns: "
     "(a) a fully random graph with the same degree sequence (configuration model  -  you already do this), and "
     "(b) a Voronoi tessellation of randomly placed points in the same volume. "
     "(Liu 2023, Sanchez-Gutierrez 2015)"),
]
for title, body in controls:
    pdf.set_fill_color(*LGRAY)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 5, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*BLACK)
    pdf.set_x(pdf.l_margin + 4)
    pdf.multi_cell(0, 4.5, body, new_x="LMARGIN")
    pdf.ln(2)

# -- REFERENCE LIST ------------------------------------------------------------
pdf.add_page()
pdf.section_title("Reference List")

refs = [
    ("Benimam MM et al.", "2025", "Statistical analysis of spatial patterns in tumor microenvironment images.",
     "Nature Communications 16(1):3090", "10.1038/s41467-025-57943-y", "40164621"),
    ("Soupir AC et al.", "2025", "Benchmarking Spatial Co-Localization Methods for Single-Cell Multiplex Imaging Data.",
     "Statistics and Data Science in Imaging 2(1)", "10.1080/29979676.2024.2437947", "40051984"),
    ("Wilson C et al.", "2022", "Tumor immune cell clustering and its association with survival in African American women with ovarian cancer.",
     "PLoS Computational Biology 18(3):e1009900", "10.1371/journal.pcbi.1009900", "35235563"),
    ("Creed JH et al.", "2021", "spatialTIME and iTIME: R package and Shiny application for visualization and analysis of immunofluorescence data.",
     "Bioinformatics 37(23):4584-4586", "10.1093/bioinformatics/btab757", "34734969"),
    ("Chakiryan NH et al.", "2021", "Geospatial Cellular Distribution of Cancer-Associated Fibroblasts Significantly Impacts Clinical Outcomes in Metastatic Clear Cell Renal Cell Carcinoma.",
     "Cancers 13(15)", "10.3390/cancers13153743", "34359645"),
    ("Myllymaki M et al.", "2012", "Analysis of spatial structure of epidermal nerve entry point patterns based on replicated data.",
     "Journal of Microscopy 247(3):228-39", "10.1111/j.1365-2818.2012.03636.x", "22906010"),
    ("Konstantinou K & Sarkka A", "2022", "Pairwise interaction Markov model for 3D epidermal nerve fibre endings.",
     "Journal of Microscopy 288(1):54-67", "10.1111/jmi.13142", "36106649"),
    ("Liu BS et al.", "2023", "Geometric and network organization of visceral organ epithelium.",
     "Frontiers in Network Physiology 3:1144186", "10.3389/fnetp.2023.1144186", "37234691"),
    ("Liu BS et al.", "2024", "Evolving topological order in the postnatal visceral pleura.",
     "Developmental Dynamics 253(8):711-721", "10.1002/dvdy.688", "38169311"),
    ("Sanchez-Gutierrez D et al.", "2015", "Fundamental physical cellular constraints drive self-organization of tissues.",
     "EMBO Journal 35(1):77-88", "10.15252/embj.201592374", "26598531"),
    ("Takko H et al.", "2020", "ShapeMetrics: A userfriendly pipeline for 3D cell segmentation and spatial tissue analysis.",
     "Developmental Biology 462(1):7-19", "10.1016/j.ydbio.2020.02.003", "32061886"),
    ("Pajanoja C & Kerosuo L", "2024", "ShapeMetrics: A 3D Cell Segmentation Pipeline for Single-Cell Spatial Morphometric Analysis.",
     "Methods in Molecular Biology 2767:263-273", "10.1007/7651_2023_489", "37219813"),
    ("Winfree S et al.", "2023", "Integrated Cytometry With Machine Learning Applied to High-Content Imaging of Human Kidney Tissue.",
     "Laboratory Investigation 103(6):100104", "10.1016/j.labinv.2023.100104", "36867975"),
    ("Wang Y et al.", "2021", "EASI-FISH for thick tissue defines lateral hypothalamus spatio-molecular organization.",
     "Cell 184(26):6361-6377.e24", "10.1016/j.cell.2021.11.024", "34875226"),
    ("Panchal T et al.", "2017", "Specification and spatial arrangement of cells in the germline stem cell niche of the Drosophila ovary depend on the Maf transcription factor Traffic jam.",
     "PLoS Genetics 13(5):e1006790", "10.1371/journal.pgen.1006790", "28542174"),
]

for authors, year, title, journal, doi, pmid in refs:
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*BLACK)
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, 4, f"{authors} ({year}). {title}", new_x="LMARGIN")
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.set_x(pdf.l_margin + 4)
    pdf.write(4, f"{journal}. DOI: ")
    pdf.set_text_color(*LINK)
    pdf.write(4, doi, link=f"https://doi.org/{doi}")
    pdf.set_text_color(*GRAY)
    pdf.write(4, f"  |  PMID: {pmid}")
    pdf.ln(4)
    pdf.ln(2)

pdf.output(OUTPUT)
print(f"PDF saved to: {OUTPUT}")
