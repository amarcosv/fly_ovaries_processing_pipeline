from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "literature_review_clusterization_degree.pdf")

BLUE  = (30, 80, 160)
LINK  = (0, 100, 200)
GRAY  = (80, 80, 80)
LGRAY = (230, 230, 230)
LGRAY2= (245, 245, 245)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 110, 60)
TEAL  = (0, 120, 120)


class PDF(FPDF):
    def header(self):
        self.set_fill_color(*BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6, "Literature Review - Degree of Clusterization: Homotypic Association & Cell-Type Spatial Segregation", new_x="RIGHT", new_y="TOP")
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
        self.set_fill_color(*LGRAY)
        self.set_text_color(*BLUE)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 6, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(1)

    def paper_entry(self, title, authors_journal, pmid, doi, summary, relevance, display, controls):
        self.set_fill_color(*LGRAY)
        self.set_text_color(*BLACK)
        self.set_font("Helvetica", "B", 9)
        self.multi_cell(0, 5, title, fill=True, new_x="LMARGIN")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.set_x(self.l_margin)
        self.write(4, f"{authors_journal}  |  PMID: {pmid}  |  DOI: ")
        self.set_text_color(*LINK)
        self.write(4, doi, link=f"https://doi.org/{doi}")
        self.set_text_color(*GRAY)
        self.ln(4)
        self.ln(1)
        self._labeled_block("Summary", summary)
        self._labeled_block("Relevance", relevance)
        self._labeled_block("Display ideas", display)
        self._labeled_block("Controls", controls)
        self.ln(3)

    def _labeled_block(self, label, text):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.cell(26, 4, label + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 4, text, new_x="LMARGIN")

    def metric_box(self, name, formula, interpretation, pipeline, difficulty):
        self.set_fill_color(*LGRAY2)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, 190, 4.5, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BLUE)
        self.set_xy(self.l_margin + 2, y0 + 0.5)
        self.cell(0, 3.5, name, new_x="LMARGIN", new_y="NEXT")
        self._labeled_block("Formula / method", formula)
        self._labeled_block("Interpretation", interpretation)
        self._labeled_block("Pipeline", pipeline)
        self._labeled_block("Effort", difficulty)
        self.ln(2)
        self.set_line_width(0.2)

    def info_box(self, text):
        self.set_fill_color(235, 245, 255)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.3)
        x0 = self.l_margin
        y0 = self.get_y()
        self.set_xy(x0 + 2, y0 + 1)
        self.set_font("Helvetica", "", 9)
        self.set_text_color(*BLACK)
        self.multi_cell(186, 4.5, text, new_x="LMARGIN")
        y1 = self.get_y() + 2
        self.rect(x0, y0, 190, y1 - y0, "FD")
        self.set_xy(x0 + 2, y0 + 1)
        self.multi_cell(186, 4.5, text, new_x="LMARGIN")
        self.set_y(y1)
        self.set_line_width(0.2)

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
        for text, w in zip(cols, widths):
            lines = self.multi_cell(w, 4, text, dry_run=True, output="LINES")
            max_h = max(max_h, len(lines) * 4 + 2)
        for text, w in zip(cols, widths):
            self.set_xy(x0, y0)
            self.multi_cell(w, 4, text, border=1, fill=header, max_line_height=4,
                            new_x="RIGHT", new_y="TOP")
            x0 += w
        self.set_xy(self.l_margin, y0 + max_h)


# =============================================================================
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ---- TITLE BLOCK ------------------------------------------------------------
pdf.set_font("Helvetica", "B", 15)
pdf.set_text_color(*BLUE)
pdf.ln(2)
pdf.multi_cell(0, 7, "Degree of Clusterization in Cell Populations:\nHomotypic Association, Neighborhood Enrichment,\nand Cell-Type Spatial Segregation", align="C", new_x="LMARGIN")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*GRAY)
pdf.multi_cell(0, 5, "Literature review for quantifying how much a cell type preferentially associates with itself\nvs. mixing with other cell types in 2D/3D tissue images", align="C", new_x="LMARGIN")
pdf.ln(3)
pdf.set_draw_color(*BLUE)
pdf.set_line_width(0.5)
pdf.line(pdf.l_margin, pdf.get_y(), 210 - pdf.r_margin, pdf.get_y())
pdf.ln(4)

# ---- OVERVIEW BOX -----------------------------------------------------------
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Scope and motivation", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "This review addresses how to quantify the degree of clusterization of a single cell type (VASA+ germ cells) "
    "within a 3D tissue volume containing a second cell type (TJ+ follicle/escort cells). "
    "The pipeline already produces: (1) a contact graph of VASA-VASA cell adjacencies (NetworkX), "
    "(2) per-cell surface area (marching cubes), and (3) per-cell fraction of surface shared with other VASA cells vs. non-VASA cells.\n\n"
    "Key question: is the VASA population compact (all cells in one dense ball, contacting mainly each other) "
    "or dispersed (cells scattered, each surrounded predominantly by TJ cells)?\n\n"
    "IMPORTANT DISTINCTION: This review focuses on *mixing/segregation* -- how much VASA cells prefer same-type "
    "neighbors -- NOT on the shape of the resulting cluster (compactness/topology), which is covered in a separate review.",
    new_x="LMARGIN")
pdf.ln(2)

# ---- SECTION 1: CONCEPTUAL FRAMEWORK ----------------------------------------
pdf.section_title("1. Conceptual Framework: What is 'Degree of Clusterization'?")

pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Three levels of clusterization", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "Clusterization can be thought of at three scales, each requiring different tools:\n"
    "  1. Cell level: does cell i have more same-type neighbors than expected by chance? "
    "-> homotypic contact fraction (HCF), neighborhood enrichment per cell\n"
    "  2. Population level: does the VASA population as a whole segregate from TJ cells? "
    "-> mean HCF, neighborhood enrichment score (NES), Ripley's L function\n"
    "  3. Topology level: is the VASA contact graph fragmented (many small clusters) or "
    "one giant connected component? -> fragmentation index, largest connected component size",
    new_x="LMARGIN")
pdf.ln(2)

pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Relationship to cell sorting (developmental biology)", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "In developmental biology, cell sorting describes the self-organization of mixed cell populations into "
    "distinct domains. The differential adhesion hypothesis (Steinberg 1963, later Foty & Steinberg) proposes that "
    "cells sort to minimize surface free energy: cells with higher mutual adhesion move to the interior. "
    "This produces core-periphery topology: highly cohesive cells form a central sphere, weakly cohesive cells "
    "surround them. Quantifying how far sorting has proceeded -- i.e. how homotypic the contact network is -- "
    "is exactly the 'degree of clusterization' problem.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Null hypothesis for all metrics", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "All clusterization metrics require comparison to a null (random) distribution. Two approaches are used:\n"
    "  (a) Label permutation: randomly reassign cell type labels across the same spatial positions; "
    "preserves cell count and density; tests whether observed contact pattern exceeds chance\n"
    "  (b) Complete spatial randomness (CSR): simulate uniformly random cell positions; "
    "appropriate for spatial statistics (Ripley's K) but ignores tissue geometry constraints\n"
    "Label permutation is preferred for contact-graph metrics because it respects tissue geometry "
    "and the constraint that each cell has a fixed number of physical neighbors.",
    new_x="LMARGIN")
pdf.ln(3)

# ---- SECTION 2: KEY PAPERS ---------------------------------------------------
pdf.section_title("2. Key Papers")

# --- 2.1 Neighborhood enrichment / contact-graph approaches
pdf.subsection_title("2.1  Neighborhood Enrichment and Contact-Graph Methods")

pdf.paper_entry(
    title="Squidpy: a scalable framework for spatial omics analysis",
    authors_journal="Palla G et al. | Nature Methods 2022 | Vol 19, pp 171-178",
    pmid="35102346",
    doi="10.1038/s41592-021-01358-2",
    summary=(
        "Python framework (built on AnnData/Scanpy) for spatial omics. Core spatial analysis methods include: "
        "(1) building spatial neighbor graphs from cell coordinates or segmentation masks; "
        "(2) neighborhood enrichment score (NES): for each pair of cell types, count contacts in the "
        "observed graph, permute labels 1000x, compute z-score = (obs - mean_perm) / std_perm; "
        "(3) co-occurrence score based on spatial point processes; "
        "(4) Ripley's L function with CSR envelope. NES heatmap shows which cell-type pairs are "
        "significantly co-located vs. mutually excluded."
    ),
    relevance=(
        "NES directly answers 'are VASA cells enriched for VASA-VASA contacts?' using the existing "
        "contact graph. Positive NES = homotypic enrichment (clustered); negative NES = exclusion (dispersed). "
        "The z-score normalizes for cell count and graph density. Can be applied directly to our NetworkX graph "
        "by replicating the permutation logic."
    ),
    display="NES heatmap (cell type x cell type); per-cell NES painted on label image",
    controls=(
        "Run 1000 label permutations (preserve cell type counts, shuffle positions); "
        "report mean +/- SD of NES distribution across permutations; "
        "verify NES ~ 0 for simulated random data (Type I error check)"
    ),
)

pdf.paper_entry(
    title="GraphCompass: spatial metrics for differential analyses of cell organization across conditions",
    authors_journal="Ali M, Kuijs M et al. | Bioinformatics 2024 | Vol 40, Suppl 1, pp i548-i557",
    pmid="38940138",
    doi="10.1093/bioinformatics/btae242",
    summary=(
        "Extends Squidpy for cross-condition comparison of cell spatial organization. Provides: "
        "(1) per-cell-type neighborhood enrichment profiles; "
        "(2) cell-type niche composition vectors for unsupervised clustering; "
        "(3) statistical tests to compare spatial metrics across samples/conditions. "
        "Applied to MIBI-TOF (spatial proteomics), Visium (spot-based), and Stereo-seq (single-cell resolved). "
        "Builds directly on Squidpy's neighborhood enrichment framework."
    ),
    relevance=(
        "Provides a validated framework for comparing VASA clusterization across genotypes or conditions. "
        "The niche composition approach -- computing the local cell-type composition vector per cell, "
        "then clustering cells by their neighborhood profile -- could identify VASA cells at the cluster "
        "core (surrounded by VASA) vs. cluster periphery (surrounded by TJ cells)."
    ),
    display="UMAP of niche composition vectors; spatial map colored by niche cluster; boxplots per condition",
    controls=(
        "Permutation test for NES at each condition separately; "
        "test for batch effects if multiple images; "
        "report N cells per cell type per condition"
    ),
)

pdf.paper_entry(
    title="Coordinated Cellular Neighborhoods Orchestrate Antitumoral Immunity at the Colorectal Cancer Invasive Front",
    authors_journal="Schurch CM, Bhate SS et al. | Cell 2020 | Vol 182, pp 1341-1359",
    pmid="32763154",
    doi="10.1016/j.cell.2020.07.005",
    summary=(
        "CODEX multiplexed imaging (56 markers) of 140 tissue regions from 35 CRC patients. "
        "Defines 'cellular neighborhoods' (CNs) as spatially recurring patterns of cell-type composition "
        "using a window-based k-means approach: for each cell, take the k nearest neighbors, build a cell-type "
        "composition vector, cluster all vectors into CNs. "
        "Key metrics: CN fragmentation = 1 - (size of largest patch / total CN cells); "
        "CN coupling = number of CN-CN boundaries. "
        "High fragmentation = scattered cells of that CN type; low fragmentation = one large cohesive domain. "
        "CN coupling measures how much two CN types are spatially adjacent."
    ),
    relevance=(
        "CN fragmentation is a direct 'degree of clusterization' metric at the domain level. "
        "For our pipeline: label each VASA cell as 'VASA CN' and compute fragmentation of the VASA domain. "
        "Fragmentation Index (FI) = 1 - N_LCC / N_total_VASA, where N_LCC is the largest connected component "
        "in the VASA contact subgraph. FI=0 = perfect single cluster; FI near 1 = all cells isolated. "
        "CN coupling between VASA and TJ CNs = how interleaved they are at their interface."
    ),
    display="Spatial map of CN labels; FI bar chart per sample; CN coupling heatmap",
    controls=(
        "Compare FI to label permutation null; "
        "control for N_VASA (larger N -> lower FI by chance); "
        "normalize FI by ln(N) to remove size dependence"
    ),
)

pdf.paper_entry(
    title="CytoMAP: A Spatial Analysis Toolbox Reveals Features of Myeloid Cell Organization in Lymphoid Tissues",
    authors_journal="Stoltzfus CR, Filipek J et al. | Cell Reports 2020 | Vol 31(3), 107523",
    pmid="32320656",
    doi="10.1016/j.celrep.2020.107523",
    summary=(
        "Histo-cytometric multidimensional analysis pipeline (CytoMAP) for multiplexed imaging. "
        "Core approach: for each cell, define a local neighborhood window (radius r), "
        "compute the cell-type composition vector (fraction of each cell type within r), "
        "cluster all vectors using SOM/k-means to find 'cellular neighborhoods' (CNs). "
        "Outputs: CN assignment per cell, CN frequency maps, positional correlation (Pearson r between "
        "cell-type frequency profiles at different positions), 2D/3D spatial region reconstruction. "
        "Revealed mutually exclusive segregation of DC subtypes in murine lymph nodes."
    ),
    relevance=(
        "The 'positional correlation' metric quantifies how cell-type composition varies across tissue: "
        "high correlation = spatially uniform mixing; low/negative = segregation into distinct domains. "
        "For our pipeline: the local VASA fraction at each position can be plotted as a spatial map; "
        "regions of high VASA fraction indicate cluster cores. "
        "The CN approach applied to VASA + TJ would identify pure-VASA regions, pure-TJ regions, and mixed boundaries."
    ),
    display="Spatial map of local VASA fraction; CN identity map; positional correlation heatmap",
    controls=(
        "Compare local VASA fraction distribution to label permutation null; "
        "test window radius sensitivity (r = 1, 2, 3 cell diameters); "
        "report CN stability across multiple k values"
    ),
)

# --- 2.2 Spatial statistics
pdf.subsection_title("2.2  Spatial Statistics: Pair Correlation and Cross-Type Clustering")

pdf.paper_entry(
    title="Extended correlation functions for spatial analysis of multiplex imaging data",
    authors_journal="Bull JA, Mulholland EJ et al. | Biological Imaging 2024 | Vol 4, e2",
    pmid="38516631",
    doi="10.1017/S2633903X24000011",
    summary=(
        "Extends the pair correlation function (PCF) in three ways: "
        "(1) Topographical correlation maps (TCM): instead of a single global g(r) value, compute a local "
        "version of g(r) at each cell position -- this maps where clustering or exclusion occurs spatially. "
        "(2) Neighbourhood correlation functions (NCF): extends cross-PCF to triplets of cell types -- "
        "does cell type C co-locate near pairs of A+B? Identifies colocalization of >2 cell types. "
        "(3) Weighted-PCF: handles continuous labels (e.g. marker intensity) rather than discrete cell types. "
        "Applied to intestinal crypt data."
    ),
    relevance=(
        "For our pipeline, the cross-PCF g_VASA-VASA(r) directly quantifies VASA-VASA clustering at "
        "distance scale r: g(r) > 1 = more VASA-VASA pairs at distance r than expected from CSR; "
        "g(r) = 1 = random; g(r) < 1 = VASA cells avoid each other at that scale. "
        "Plotting g(r) vs. r shows at what spatial scale clustering peaks. "
        "TCM can reveal whether VASA clustering is uniform or localized to specific tissue regions."
    ),
    display=(
        "g(r) vs. r curve with CSR confidence envelope; "
        "TCM heatmap overlaid on tissue image; "
        "g(r) at fixed r as scalar for boxplot comparison across conditions"
    ),
    controls=(
        "CSR envelope via Monte Carlo: simulate N_VASA points uniformly in tissue bounding box (100 realizations); "
        "edge correction (isotropic or border method); "
        "compare g(r=1 cell diameter) as a scalar across conditions"
    ),
)

pdf.paper_entry(
    title="Tumor immune cell clustering and its association with survival in African American women with ovarian cancer",
    authors_journal="Wilson C, Soupir AC et al. | PLoS Computational Biology 2022 | Vol 18(3), e1009900",
    pmid="35235563",
    doi="10.1371/journal.pcbi.1009900",
    summary=(
        "Uses Ripley's K + permutation CSR envelope to quantify immune cell clustering in ovarian cancer TME. "
        "K at fixed radius (scalar nK(r)) enables ANOVA/boxplot group comparisons. "
        "Key finding: combining cell abundance with spatial clustering (K) provides better survival "
        "discrimination than either alone -- demonstrating that *how cells are arranged* matters "
        "beyond just how many there are. Applies to multiplex IF data on TMAs."
    ),
    relevance=(
        "Validates the approach of using Ripley's K/L as a clusterization scalar: "
        "L(r) - r > 0 = clustered; L(r) - r = 0 = random. "
        "The nK(r) scalar at a biologically relevant radius (e.g. r = 3 cell diameters) "
        "can be reported per ovary image and compared across genotypes. "
        "Already implemented in our pipeline (computeRipleysK); reframed here as a clusterization metric."
    ),
    display="L(r)-r curve with Monte Carlo envelope; nK(r) boxplot per condition",
    controls=(
        "100 CSR Monte Carlo simulations; "
        "edge correction; "
        "normalize for VASA cell count and tissue volume; "
        "test whether L(r) responds to known perturbations"
    ),
)

# --- 2.3 Cell aggregate / neighborhood analysis tools
pdf.subsection_title("2.3  Cell Aggregate and Neighborhood Analysis Algorithms")

pdf.paper_entry(
    title="Understanding heterogeneous tumor microenvironment in metastatic melanoma",
    authors_journal="Yan Y, Leontovich AA et al. | PLoS ONE 2019 | Vol 14(6), e0216485",
    pmid="31166985",
    doi="10.1371/journal.pone.0216485",
    summary=(
        "Introduces two custom algorithms for multiplexed IF analysis of melanoma TME: "
        "(1) Cell Aggregate Algorithm (CAA): identifies contiguous groups of same-type cells -- "
        "a cell aggregate is a connected component in the contact graph restricted to one cell type. "
        "Reports aggregate size distribution, number of aggregates, mean aggregate size. "
        "(2) Cell Neighborhood Analysis (CNA): for each cell, counts the number of each other cell "
        "type within a defined radius -- produces a neighborhood composition profile per cell. "
        "Used to correlate HLA-1 expression with T-cell infiltration pattern."
    ),
    relevance=(
        "CAA = exactly our 'connected component analysis' of the VASA contact subgraph. "
        "Applying it: (1) extract the VASA-only subgraph from our contact graph; "
        "(2) find connected components; (3) report: N_components, size of largest CC, "
        "size distribution (power law vs. exponential), mean aggregate size. "
        "A perfectly clusterized population = 1 large aggregate containing all cells. "
        "Dispersed = many small aggregates of size 1-3."
    ),
    display=(
        "Bar chart of aggregate size distribution; "
        "map of aggregate membership colored by size; "
        "scatter plot: N_aggregates vs. mean_aggregate_size per image"
    ),
    controls=(
        "Compare to label permutation null (shuffle VASA/TJ labels, recompute aggregates); "
        "report mean aggregate size normalized by N_VASA; "
        "test sensitivity to contact detection threshold"
    ),
)

# ---- SECTION 3: METRIC CATALOG -----------------------------------------------
pdf.section_title("3. Metric Catalog - Degree of Clusterization")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "Metrics are grouped by what data they require. All are applicable to our pipeline. "
    "Ordered within each group from easiest to implement to most involved.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.subsection_title("3.1  From the existing VASA contact graph (trivial to easy)")

pdf.metric_box(
    name="1. Homotypic Contact Fraction (HCF) -- per cell",
    formula=(
        "HCF_i = (number of VASA-VASA contacts of cell i) / (total contacts of cell i). "
        "Surface-weighted variant: HCF_SW_i = (shared surface area with VASA neighbors) / (total cell surface area). "
        "Already computed in pipeline as 'surface sharing ratio'."
    ),
    interpretation=(
        "HCF_i = 1: cell i is completely surrounded by VASA cells (core cluster cell). "
        "HCF_i = 0: cell i has no VASA neighbors (isolated / boundary cell). "
        "Mean HCF across all VASA cells is the population-level clusterization index. "
        "Compare mean HCF to null distribution from label permutations. "
        "Core (HCF ~ 1) vs. peripheral (HCF ~ 0) VASA cells can be mapped spatially."
    ),
    pipeline="Already available as 'surface_sharing_ratio' in VASA neighbor metrics CSV. Compute mean and compare to permutation null.",
    difficulty="Trivial -- no new code needed; reframe existing metric",
)

pdf.metric_box(
    name="2. Neighborhood Enrichment Score (NES) -- population level",
    formula=(
        "NES = (n_obs - mean(n_perm)) / std(n_perm), "
        "where n_obs = number of VASA-VASA contact pairs in graph, "
        "n_perm = same count after permuting VASA/TJ labels 1000 times (preserving counts). "
        "Implementation: Squidpy sq.gr.nhood_enrichment() -- or replicate with nx.Graph + np.random.permutation."
    ),
    interpretation=(
        "NES > 0 (positive z-score): VASA cells contact other VASA cells more than expected by chance -- clustered. "
        "NES ~ 0: random mixing. NES < 0: VASA cells avoid each other -- dispersed/interdigitated. "
        "NES is normalized for graph density and cell count, so comparable across images."
    ),
    pipeline=(
        "Add to computeGraphControl() or new function: "
        "count VASA-VASA edges in observed graph; "
        "permute node labels N=1000 times; compute NES. "
        "Output: NES scalar per image."
    ),
    difficulty="Easy -- extends existing configuration model code; ~10 lines",
)

pdf.metric_box(
    name="3. Fragmentation Index (FI) -- topology level",
    formula=(
        "FI = 1 - (N_LCC / N_VASA), "
        "where N_LCC = size of largest connected component in the VASA-only contact subgraph, "
        "N_VASA = total number of VASA cells. "
        "Also report: N_components (number of separate VASA clusters), "
        "component size distribution (sizes of all CCs)."
    ),
    interpretation=(
        "FI = 0: all VASA cells in one giant connected component -- perfect single cluster. "
        "FI = 1 - 1/N ~ 1: all VASA cells isolated -- maximum fragmentation. "
        "N_components = 1: one cluster. N_components >> 1: scattered. "
        "Size distribution: exponential = many small fragments; right-skewed = one large + few small."
    ),
    pipeline=(
        "Extract VASA subgraph: G_vasa = G.subgraph([n for n in G if G.nodes[n]['type']=='VASA']). "
        "ccs = list(nx.connected_components(G_vasa)). "
        "FI = 1 - max(len(c) for c in ccs) / len(G_vasa)."
    ),
    difficulty="Trivial -- 3 lines of NetworkX code",
)

pdf.metric_box(
    name="4. Clustering coefficient of VASA subgraph",
    formula=(
        "CC_vasa = nx.average_clustering(G_vasa), "
        "where G_vasa is the VASA-only contact subgraph "
        "(nodes = VASA cells, edges = VASA-VASA contacts). "
        "Per-cell: nx.clustering(G_vasa)."
    ),
    interpretation=(
        "CC_vasa measures triangle closure within the VASA contact network: "
        "if VASA cell A contacts B and C, what fraction of B-C pairs are also in contact? "
        "High CC_vasa = dense local clustering (cells form compact groups). "
        "Low CC_vasa = chain-like or tree-like VASA subgraph. "
        "Compare to random graph with same degree sequence (configuration model)."
    ),
    pipeline=(
        "Already computing CC on the full graph. "
        "Re-run on G_vasa subgraph. "
        "Normalize vs. CC of random graph: SW_vasa = CC_vasa / CC_rand."
    ),
    difficulty="Trivial -- already implemented, just apply to subgraph",
)

pdf.metric_box(
    name="5. Mean same-type neighbor count (degree in VASA subgraph)",
    formula=(
        "k_hom_i = degree of cell i in G_vasa = number of VASA-VASA contacts. "
        "Report: mean k_hom, distribution of k_hom, fraction of VASA cells with k_hom = 0 "
        "(isolated VASA cells with no VASA-VASA contacts)."
    ),
    interpretation=(
        "Mean k_hom / mean k_total = population-level HCF (contact-count version). "
        "Fraction isolated (k_hom=0) is a simple scalar clusterization metric: "
        "low fraction = well-clustered population; high fraction = dispersed. "
        "Directly interpretable biologically."
    ),
    pipeline="Already stored in neighbor metrics CSV as 'num_neighbors'. Extract VASA-VASA degree from graph.",
    difficulty="Trivial",
)

pdf.subsection_title("3.2  From cell centroids / spatial coordinates (easy to moderate)")

pdf.metric_box(
    name="6. Pair correlation function g(r) for VASA-VASA pairs (cross-PCF)",
    formula=(
        "g_VASA(r) = (observed VASA-VASA pairs at distance r) / (expected from CSR at distance r). "
        "g(r) > 1 = clustered at scale r; g(r) = 1 = random; g(r) < 1 = repulsion. "
        "Scalar version: g at r = 1 cell diameter (or at peak of g(r))."
    ),
    interpretation=(
        "g(r) reveals the spatial scale of clustering: if VASA cells cluster at ~ 2 cell diameters, "
        "g will peak at r ~ 2D and drop to 1 at larger r. "
        "The area under g(r)-1 from 0 to some r_max is a single-number clusterization index. "
        "Compare to g(r) of label-permuted data."
    ),
    pipeline=(
        "Extend computeRipleysK() to also return g(r) = K'(r) / (2*pi*r) in 3D (= derivative of K divided by 4*pi*r^2). "
        "Or compute directly as histogram of pairwise distances / expected from CSR."
    ),
    difficulty="Easy -- derive from existing Ripley's K; or compute directly with ~20 lines",
)

pdf.metric_box(
    name="7. Ripley's L(r) - r scalar at fixed radius (existing metric, re-framed)",
    formula=(
        "L(r) = (3*K(r) / (4*pi))^(1/3) in 3D. "
        "Clusterization scalar: L(r*) - r* where r* = 1-2 cell diameters. "
        "Positive = clustered at that scale; compare to CSR Monte Carlo envelope."
    ),
    interpretation=(
        "Already implemented in the pipeline. "
        "L(r)-r > 0 confirms VASA spatial clustering at scale r. "
        "The peak location of L(r)-r indicates the characteristic cluster scale. "
        "This is the spatial statistics equivalent of HCF: both measure same-type association."
    ),
    pipeline="Already implemented in computeRipleysK(). Output L(r)-r curve and peak value as scalar.",
    difficulty="Trivial -- already implemented",
)

pdf.metric_box(
    name="8. Local VASA fraction map (CytoMAP-style)",
    formula=(
        "For each cell i (VASA or TJ), f_VASA(i) = (N_VASA within radius r of cell i) / (N_total within radius r). "
        "Report: spatial map of f_VASA, histogram of f_VASA values for VASA cells, "
        "fraction of VASA cells in 'VASA-rich' zones (f_VASA > 0.5)."
    ),
    interpretation=(
        "f_VASA(i) = 1 for a cell deep inside a VASA cluster; f_VASA(i) ~ fraction_VASA_global for random mixing. "
        "Painting f_VASA on the spatial image reveals cluster boundaries. "
        "Bimodal histogram of f_VASA for VASA cells = distinct core + periphery populations."
    ),
    pipeline=(
        "Use KD-tree on VASA + TJ centroids. "
        "For each VASA cell, query sphere of radius r (e.g. r = 3 * mean_cell_diameter). "
        "Compute VASA fraction in sphere. Add as column in neighbor metrics CSV."
    ),
    difficulty="Easy -- ~15 lines with scipy.spatial.cKDTree",
)

pdf.subsection_title("3.3  From the label image (moderate)")

pdf.metric_box(
    name="9. VASA domain surface-to-volume ratio",
    formula=(
        "Treat all VASA-labeled voxels as one binary mask. "
        "Compute surface area S_vasa (marching cubes) and volume V_vasa (voxel count). "
        "Ratio: S/V. For a sphere: S/V = 3/r; high S/V = irregular/branching shape. "
        "Compare to S/V of a sphere with same volume: Isoperimetric ratio = (S^3) / (36*pi*V^2); = 1 for sphere."
    ),
    interpretation=(
        "S/V measures surface complexity of the VASA domain as a whole (all cells together). "
        "Low S/V = compact, blob-like domain. High S/V = highly convoluted, branching, or scattered. "
        "This is a shape metric of the merged VASA domain, not of individual cells. "
        "Complements FI (connectivity) by capturing geometry."
    ),
    pipeline=(
        "Create binary mask from VASA label image (any VASA label -> 1). "
        "Apply skimage.measure.marching_cubes to get S_total_domain. "
        "V_total_domain = sum(VASA voxels) * voxel_volume."
    ),
    difficulty="Moderate -- requires binary domain mask; ~10 lines",
)

# ---- SECTION 4: IMPLEMENTATION GUIDE ----------------------------------------
pdf.section_title("4. Implementation Priority and Workflow")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "Recommended implementation order, from quickest wins to most involved:",
    new_x="LMARGIN")
pdf.ln(2)

steps = [
    ("Step 1 (trivial, ~1h)",
     "ALREADY DONE: HCF (surface_sharing_ratio) is already computed per cell.",
     "Add: compute mean HCF per image and compare to label permutation null (reuse configuration model)."),
    ("Step 2 (trivial, ~30 min)",
     "Fragmentation Index (FI): extract VASA subgraph, find connected components, compute FI = 1 - N_LCC/N_VASA.",
     "Also report: N_components, component size distribution histogram."),
    ("Step 3 (trivial, ~30 min)",
     "Neighborhood Enrichment Score (NES): count VASA-VASA edges in observed vs. permuted graphs.",
     "Add NES as a summary scalar alongside existing configuration model output."),
    ("Step 4 (trivial, ~30 min)",
     "CC of VASA subgraph: run nx.average_clustering on G_vasa. Compare to CC on full G (already done).",
     "Normalized CC_vasa / CC_rand tells you clustering within the VASA network specifically."),
    ("Step 5 (easy, ~2h)",
     "Pair correlation g(r): derive from existing K(r) computation or compute directly from pairwise distances.",
     "Output: g(r) curve + g(r*) scalar at r* = 2 cell diameters."),
    ("Step 6 (easy, ~1h)",
     "Local VASA fraction map: KD-tree query at radius r = 3 cell diameters, compute f_VASA per cell.",
     "Paint map on label image using paintLabelsByMetric()."),
]

for title, action, note in steps:
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 5, title, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 4, action, new_x="LMARGIN")
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4, note, new_x="LMARGIN")
    pdf.ln(1)

# ---- SECTION 5: CONTROLS AND VALIDATION -------------------------------------
pdf.section_title("5. Controls and Validation")

pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLACK)
controls_list = [
    ("Label permutation (primary null)",
     "Shuffle VASA/TJ labels N=1000 times preserving counts; recompute all metrics. "
     "Report observed metric as z-score or percentile of permutation distribution. "
     "Source: Squidpy (Palla 2022), Schurch 2020, Wilson 2022."),
    ("Cell density as covariate",
     "Higher VASA cell density -> more VASA-VASA contacts by chance. "
     "Always report VASA cell count and tissue volume with every metric. "
     "Test correlation of NES with N_VASA / V_tissue to check for density confounding."),
    ("Normalize FI and component size by ln(N)",
     "Larger populations have lower FI by chance. "
     "Report FI*ln(N_VASA) or compare FI only within samples matched for N_VASA."),
    ("Biological positive control",
     "A known genotype that disrupts VASA cell clustering should show decreased NES, higher FI, "
     "lower mean HCF vs. wildtype. If no such control is available, use synthetic data: "
     "generate a point pattern with known degree of clustering and verify metric recovers it."),
    ("Type I error check",
     "Run all metrics on simulated CSR point patterns with same N and V as real data. "
     "Verify NES ~ 0, FI ~ expected null, g(r) ~ 1. "
     "Source: Wilson 2022 recommends this for Ripley's K; same logic applies here."),
    ("Report all three levels together",
     "Cell level (mean HCF), population level (NES, L(r)), topology level (FI, N_components). "
     "These are complementary: a population can have high NES but high FI (many small dense clusters). "
     "Reporting all three gives a complete picture."),
]

for ctrl_name, ctrl_text in controls_list:
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*BLUE)
    pdf.cell(50, 4, ctrl_name + ":", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 4, ctrl_text, new_x="LMARGIN")
    pdf.ln(1)

# ---- SECTION 6: SUMMARY TABLE -----------------------------------------------
pdf.section_title("6. Summary Table")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "All metrics applicable to the fly ovaries pipeline, ordered by implementation effort.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.table_row(["Metric", "Level", "Null", "Effort", "Source"], [55, 28, 38, 20, 49], header=True)
rows = [
    ("Surface-weighted HCF (mean)", "cell", "label perm.", "done", "this pipeline"),
    ("Neighborhood Enrichment Score", "population", "label perm.", "easy", "Palla 2022"),
    ("Fragmentation Index (FI)", "topology", "label perm.", "trivial", "Schurch 2020"),
    ("CC of VASA subgraph", "topology", "config. model", "trivial", "existing code"),
    ("k_hom mean + frac isolated", "cell", "label perm.", "trivial", "Yan 2019"),
    ("Ripley's L(r)-r scalar", "population", "CSR Monte Carlo", "done", "Wilson 2022"),
    ("Pair correlation g(r)", "population", "CSR Monte Carlo", "easy", "Bull 2024"),
    ("Local VASA fraction map", "spatial", "label perm.", "easy", "Stoltzfus 2020"),
    ("VASA domain S/V ratio", "geometry", "sphere reference", "moderate", "this pipeline"),
]
for row in rows:
    pdf.table_row(list(row), [55, 28, 38, 20, 49])

pdf.ln(4)

# ---- REFERENCES --------------------------------------------------------------
pdf.section_title("References (PubMed)")

refs = [
    ("Palla G et al.", "2022", "Nat Methods", "Squidpy: scalable framework for spatial omics analysis", "35102346", "10.1038/s41592-021-01358-2"),
    ("Ali M et al.", "2024", "Bioinformatics", "GraphCompass: spatial metrics for differential analyses of cell organization", "38940138", "10.1093/bioinformatics/btae242"),
    ("Schurch CM et al.", "2020", "Cell", "Coordinated Cellular Neighborhoods Orchestrate Antitumoral Immunity", "32763154", "10.1016/j.cell.2020.07.005"),
    ("Stoltzfus CR et al.", "2020", "Cell Rep", "CytoMAP: Spatial Analysis Toolbox for Cell Organization in Lymphoid Tissues", "32320656", "10.1016/j.celrep.2020.107523"),
    ("Bull JA et al.", "2024", "Biol Imaging", "Extended correlation functions for spatial analysis of multiplex imaging data", "38516631", "10.1017/S2633903X24000011"),
    ("Yan Y et al.", "2019", "PLoS ONE", "Understanding heterogeneous tumor microenvironment in metastatic melanoma", "31166985", "10.1371/journal.pone.0216485"),
    ("Wilson C et al.", "2022", "PLoS Comput Biol", "Tumor immune cell clustering and association with survival in ovarian cancer", "35235563", "10.1371/journal.pcbi.1009900"),
]

pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(*BLACK)
for i, (authors, year, journal, title, pmid, doi) in enumerate(refs, 1):
    pdf.set_x(pdf.l_margin)
    pdf.write(4, f"[{i}] {authors} ({year}). {title}. {journal}. PMID: {pmid}. DOI: ")
    pdf.set_text_color(*LINK)
    pdf.write(4, doi, link=f"https://doi.org/{doi}")
    pdf.set_text_color(*BLACK)
    pdf.ln(5)

pdf.output(OUTPUT)
print(f"PDF written to: {OUTPUT}")
