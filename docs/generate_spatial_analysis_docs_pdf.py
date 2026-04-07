"""
generate_spatial_analysis_docs_pdf.py
Technical reference for all metrics produced by spatial_analysis_tools.py.
Run from any directory: python docs/generate_spatial_analysis_docs_pdf.py
Requires: fpdf2 >= 2.7   (pip install fpdf2)
"""
from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "spatial_analysis_metrics_reference.pdf")

# ---------- colour palette ----------
BLUE       = (30, 80, 160)
BLUE_LIGHT = (235, 242, 255)
GREEN      = (0, 110, 60)
GREEN_LIGHT= (230, 248, 238)
AMBER      = (160, 100, 0)
AMBER_LIGHT= (255, 248, 225)
PURPLE     = (100, 30, 140)
PURPLE_LIGHT=(245, 235, 255)
GRAY       = (80, 80, 80)
LGRAY      = (210, 210, 210)
LGRAY2     = (245, 245, 245)
BLACK      = (0, 0, 0)
WHITE      = (255, 255, 255)
RED        = (180, 30, 30)

# level colour coding
CELL_COLOR   = GREEN        # per-cell metrics
CELL_BG      = GREEN_LIGHT
SAMPLE_COLOR = BLUE         # per-sample summary
SAMPLE_BG    = BLUE_LIGHT
CTRL_COLOR   = PURPLE       # graph control / null test
CTRL_BG      = PURPLE_LIGHT
RIPLEY_COLOR = AMBER
RIPLEY_BG    = AMBER_LIGHT


class PDF(FPDF):
    def header(self):
        self.set_fill_color(*BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6,
            "Technical Reference  |  spatial_analysis_tools.py  |  VASA Cell Spatial Analysis Pipeline",
            new_x="RIGHT", new_y="TOP")
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6,
            f"Page {self.page_no()}  |  fly_ovaries_processing_pipeline  |  March 2026",
            align="C")

    # ---- structural helpers ----
    def section_title(self, title, color=BLUE):
        self.ln(4)
        self.set_fill_color(*color)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(1)

    def subsection_title(self, title, color=BLUE):
        self.ln(3)
        self.set_fill_color(*LGRAY)
        self.set_text_color(*color)
        self.set_font("Helvetica", "B", 9)
        self.cell(0, 5, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(1)

    def level_legend(self):
        """Colour key for the four metric levels."""
        self.ln(2)
        pairs = [
            (CELL_COLOR,   CELL_BG,   "Per-cell  (cell_metrics DataFrame)"),
            (SAMPLE_COLOR, SAMPLE_BG, "Per-sample summary  (summary dict / CSV)"),
            (CTRL_COLOR,   CTRL_BG,   "Graph control  (computeGraphControl)"),
            (RIPLEY_COLOR, RIPLEY_BG, "Ripley / Geometric  (computeRipleysK / computeGeometricMetrics)"),
        ]
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 4, "Colour key:", new_x="LMARGIN", new_y="NEXT")
        self.ln(1)
        for fc, bg, label in pairs:
            self.set_fill_color(*bg)
            self.set_draw_color(*fc)
            self.set_line_width(0.5)
            self.rect(self.l_margin, self.get_y(), 5, 4, "FD")
            self.set_x(self.l_margin + 7)
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*BLACK)
            self.cell(0, 4, label, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def _row(self, label, value, label_w=40):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*GRAY)
        self.cell(label_w, 4, label + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 4, value, new_x="LMARGIN")

    def metric_box(self, name, csv_col, level, units, formula, interpretation,
                   note="", color=BLUE, bg=LGRAY2):
        """One metric documentation card."""
        self.set_fill_color(*bg)
        self.set_draw_color(*color)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, 190, 5, "FD")
        # header bar
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*color)
        self.set_xy(self.l_margin + 2, y0 + 0.8)
        # name left, csv_col right
        self.cell(130, 3.5, name, new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "I", 7.5)
        self.set_text_color(*GRAY)
        self.cell(0, 3.5, f"col: {csv_col}", align="R", new_x="LMARGIN", new_y="NEXT")
        # body rows
        self._row("Level", level)
        self._row("Units", units)
        self._row("Formula / method", formula)
        self._row("Interpretation", interpretation)
        if note:
            self._row("Note", note)
        self.ln(3)

    def function_banner(self, fname, description):
        """Grey banner for each function."""
        self.ln(2)
        self.set_fill_color(*LGRAY)
        self.set_draw_color(*LGRAY)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BLUE)
        self.cell(55, 6, f"  {fname}()", fill=True, new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.set_fill_color(*LGRAY2)
        self.cell(0, 6, f"  {description}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def param_row(self, name, default, desc):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.cell(40, 4, f"  {name}", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(22, 4, default, new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 4, desc, new_x="LMARGIN")

    def info_box(self, text, color=BLUE):
        self.set_fill_color(*(BLUE_LIGHT if color == BLUE else AMBER_LIGHT))
        self.set_draw_color(*color)
        self.set_line_width(0.3)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*color)
        self.multi_cell(0, 4, text, fill=True, border=1, new_x="LMARGIN")
        self.ln(2)


# ============================================================
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=18)
pdf.add_page()

# ---- TITLE ----
pdf.set_font("Helvetica", "B", 18)
pdf.set_text_color(*BLUE)
pdf.cell(0, 10, "Spatial Analysis Metrics Reference", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*GRAY)
pdf.cell(0, 6, "spatial_analysis_tools.py  |  fly_ovaries_processing_pipeline", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(4)

# ---- OVERVIEW ----
pdf.section_title("Overview")
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "This module quantifies the spatial organisation of VASA+ germ cells in 3D Drosophila ovary "
    "fluorescence images. All analysis is performed exclusively on the VASA label image "
    "(instance segmentation, uint16 or uint8 TIFF). No co-registration with TJ or other channels "
    "is required.\n\n"
    "The pipeline detects cell-to-cell contacts from shared voxel faces, builds a weighted "
    "NetworkX contact graph, and derives a hierarchical set of metrics at three levels: "
    "individual cell, population (per image), and spatial statistics.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.level_legend()

# ---- INPUT / OUTPUT TABLE ----
pdf.section_title("Input / Output")
cols = [65, 125]
headers = ["Item", "Description"]
pdf.set_fill_color(*LGRAY)
pdf.set_text_color(*BLACK)
pdf.set_font("Helvetica", "B", 8)
for h, w in zip(headers, cols):
    pdf.cell(w, 6, f"  {h}", border=1, fill=True)
pdf.ln()
rows = [
    ("Label image (input)", "3D ZYX uint array -- refined VASA instance segmentation (*_masks_refined.tif)"),
    ("px_size (input)", "[Z, Y, X] voxel size in micrometers. Default pipeline: [0.25, 0.14, 0.14]"),
    ("cell_metrics (output)", "pandas DataFrame -- one row per cell, all per-cell columns"),
    ("G (output)", "networkx.Graph -- weighted contact graph (edge weight = shared surface area in um2)"),
    ("summary (output)", "dict -- population-level scalars for the image"),
    ("control (output)", "dict -- graph topology null test results"),
    ("ripley (output)", "dict -- K/L function arrays and CSR envelope"),
    ("geom (output)", "dict -- geometric shape metrics"),
    ("*_VASA_neighbor_metrics.csv", "Per-cell metrics exported by exportVASANeighborMetrics()"),
    ("*_VASA_neighbor_summary.csv", "Per-sample summary exported by exportVASANeighborMetrics()"),
]
pdf.set_font("Helvetica", "", 8)
for i, (a, b) in enumerate(rows):
    fill = i % 2 == 0
    pdf.set_fill_color(*(LGRAY2 if fill else WHITE))
    pdf.cell(cols[0], 5, f"  {a}", border=1, fill=fill)
    pdf.multi_cell(cols[1], 5, f"  {b}", border=1, fill=fill, new_x="LMARGIN")

pdf.ln(4)

# ============================================================
pdf.add_page()
pdf.section_title("1  analyzeVASANeighbors  --  Per-Cell Metrics")

pdf.function_banner(
    "analyzeVASANeighbors",
    "Contact detection + graph construction + per-cell metrics")

pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(*GRAY)
pdf.cell(0, 5, "Key parameters:", new_x="LMARGIN", new_y="NEXT")
pdf.param_row("noise_threshold", "default=5",
    "Minimum number of shared voxel faces to recognise a VASA-VASA contact. "
    "Filters sub-pixel noise at cell boundaries. Increase for noisier segmentations.")
pdf.param_row("px_size", "required",
    "Voxel size [Z, Y, X] in micrometers. All surface and volume outputs are in physical units only if provided.")
pdf.ln(2)

pdf.info_box(
    "Contact detection: the label image is padded by 1 voxel and shifted along each axis. "
    "Pairs of different labels at each face boundary are collected and grouped. Each face "
    "contributes a physical area = px_size[Y]*px_size[X] (Z-faces), px_size[Z]*px_size[X] "
    "(Y-faces), or px_size[Z]*px_size[Y] (X-faces). Pairs below noise_threshold faces are "
    "discarded before graph construction.")

pdf.subsection_title("1A  Morphology  (per cell)", color=CELL_COLOR)

pdf.metric_box(
    name="Cell volume",
    csv_col="volume_um3",
    level="Per cell  |  analyzeVASANeighbors",
    units="micrometers^3 (um3)",
    formula="voxel count (area from regionprops) x voxel_volume (pz x py x px)",
    interpretation="Physical volume of the segmented cell. Used to compute equivalent diameter, "
                   "mean_volume_um3 (population), and R_eq (geometric metrics).",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="Equivalent sphere diameter",
    csv_col="equivalent_diameter_um",
    level="Per cell  |  analyzeVASANeighbors",
    units="micrometers (um)",
    formula="d = (6 * volume_um3 / pi)^(1/3)  -- diameter of a sphere with the same volume",
    interpretation="Size proxy independent of cell shape. Used to normalise Ripley's r axis "
                   "(r / mean_diameter_um) for cross-sample comparison.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.subsection_title("1B  Contact Graph  (per cell)", color=CELL_COLOR)

pdf.metric_box(
    name="Degree  (number of VASA neighbours)",
    csv_col="vasa_neighbors",
    level="Per cell  |  analyzeVASANeighbors",
    units="integer",
    formula="k_i = degree of node i in the VASA contact graph G",
    interpretation="How many other VASA cells cell i physically touches (above noise_threshold). "
                   "k=0: isolated cell; k=1-2: peripheral; high k: interior/hub cell. "
                   "Population distribution described by mean_k and std_k in the summary.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="Component (cluster) size",
    csv_col="cluster_size",
    level="Per cell  |  analyzeVASANeighbors",
    units="integer (number of cells)",
    formula="Size of the connected component to which cell i belongs in G",
    interpretation="All cells in the same connected component share the same value. "
                   "Isolated cells have cluster_size=1. The largest value across all cells equals lcc_size.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="VASA shared surface area",
    csv_col="vasa_surface",
    level="Per cell  |  analyzeVASANeighbors",
    units="um2",
    formula="Sum of contact areas between cell i and all its VASA neighbours",
    interpretation="Raw contact area. Increases with both number of neighbours and the extent "
                   "of contact per neighbour. Use shared_boundary_ratio for a normalised version.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="Non-VASA surface area",
    csv_col="non_vasa_surface",
    level="Per cell  |  analyzeVASANeighbors",
    units="um2",
    formula="Surface area of faces touching label 0 (background / non-VASA space)",
    interpretation="Surface not touching another segmented VASA cell. Includes contact with TJ "
                   "cells, extracellular matrix, tissue boundary, and imaging artefacts. "
                   "Cannot distinguish between these -- it is the embedding surface.",
    note="TJ cells are segmented in a separate channel without spatial co-registration; "
         "their contribution to this surface cannot be separated.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.add_page()

pdf.metric_box(
    name="Total surface area",
    csv_col="total_surface",
    level="Per cell  |  analyzeVASANeighbors",
    units="um2",
    formula="total_surface = vasa_surface + non_vasa_surface",
    interpretation="Approximate total surface area of the cell estimated from face counting. "
                   "Not a marching-cubes surface (blocky voxel estimate). Use for ratios, "
                   "not as an absolute morphometric.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="Shared boundary ratio  (SBR)",
    csv_col="shared_boundary_ratio",
    level="Per cell  |  analyzeVASANeighbors",
    units="dimensionless  [0, 1]",
    formula="SBR_i = vasa_surface_i / total_surface_i",
    interpretation="Fraction of cell surface in contact with other VASA cells. "
                   "SBR ~ 0: isolated, mostly embedded in non-VASA tissue. "
                   "SBR ~ 1: almost fully surrounded by VASA neighbours (deep interior cell). "
                   "Population mean SBR reflects how tightly the cluster is packed.",
    note="SBR does NOT measure homotypic vs. heterotypic mixing because the 'other side' "
         "is undefined (could be TJ, ECM, or background). It measures embedding depth.",
    color=CELL_COLOR, bg=CELL_BG)

pdf.metric_box(
    name="Clustering coefficient  (CC)",
    csv_col="clustering_coeff",
    level="Per cell  |  analyzeVASANeighbors",
    units="dimensionless  [0, 1]",
    formula="CC_i = (triangles through i) / (possible triangles through i) = 2*t_i / (k_i*(k_i-1))\n"
            "Computed by networkx.clustering(G, i). Undefined (set to 0) when k_i < 2.",
    interpretation="Probability that two neighbours of cell i also touch each other. "
                   "CC=0: none of the neighbours are mutually connected (star/chain motif). "
                   "CC=1: all neighbours form a complete clique. "
                   "High mean CC implies compact, locally dense packing.",
    note="CC is mathematically undefined for cells with degree < 2 (no triangle is possible). "
         "NetworkX assigns CC=0 in this case. Use mean_CC_defined in the summary, which "
         "excludes these cells. frac_CC_undefined quantifies how many cells are affected.",
    color=CELL_COLOR, bg=CELL_BG)

# ---- SECTION 2: POPULATION SUMMARY ----
pdf.section_title("2  analyzeVASANeighbors  --  Population Summary Metrics")

pdf.info_box(
    "All summary metrics are in the summary dict returned by analyzeVASANeighbors() and are "
    "exported to *_VASA_neighbor_summary.csv by exportVASANeighborMetrics(). One row per image.")

pdf.subsection_title("2A  Cell count and size", color=SAMPLE_COLOR)

pdf.metric_box(
    name="Number of cells",
    csv_col="n_cells",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="integer",
    formula="Count of unique non-zero labels in the refined label image",
    interpretation="Total VASA cells after IQR outlier removal. Always report alongside all "
                   "other metrics as a covariate (many metrics scale with N).",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Mean cell volume",
    csv_col="mean_volume_um3",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="um3",
    formula="mean(volume_um3) across all cells in the image",
    interpretation="Average cell size. Used to compute R_eq (geometric metrics) and "
                   "equivalent_diameter_um. Differences across conditions may indicate "
                   "changes in cell size independent of packing.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Mean equivalent diameter",
    csv_col="mean_diameter_um",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="um",
    formula="mean(equivalent_diameter_um) across all cells in the image",
    interpretation="Mean cell diameter used to normalise the Ripley r axis. "
                   "Typical value: 5-8 um for Drosophila germ cells at 0.14 um/px.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.add_page()
pdf.subsection_title("2B  Connectivity and fragmentation", color=SAMPLE_COLOR)

pdf.metric_box(
    name="Number of connected components",
    csv_col="n_components",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="integer",
    formula="networkx.number_connected_components(G)  -- isolated cells count as size-1 components",
    interpretation="Number of distinct disconnected groups of VASA cells. "
                   "1 = fully connected cluster. >1 = satellite groups or isolated cells. "
                   "Increases with fragmentation_index.",
    note="n_clusters is kept as a backward-compatible alias for n_components.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Largest connected component size  (LCC)",
    csv_col="lcc_size",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="integer (cells)",
    formula="Size of the largest connected component in G",
    interpretation="Number of cells in the main cluster. lcc_size / n_cells = fraction of "
                   "cells in the dominant cluster. Used by computeGraphControl for CPL.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Fragmentation index  (FI)",
    csv_col="fragmentation_index",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="dimensionless  [0, 1)",
    formula="FI = 1 - lcc_size / n_cells\n"
            "Derived from Schurch et al. 2020 (PMID 32763154)",
    interpretation="FI = 0: single connected cluster (all cells in LCC). "
                   "FI -> 1: all cells isolated. "
                   "FI = 0.036: 96.4% of cells are in the main cluster, 3.6% are in satellite groups. "
                   "More sensitive to small isolated groups than n_components alone.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Component size distribution",
    csv_col="comp_size_p25 / p50 / p75 / max",
    level="Per sample  |  exportVASANeighborMetrics (CSV only)",
    units="integer (cells)",
    formula="Percentiles of the list of all connected component sizes, sorted descending",
    interpretation="Describes the size distribution of all clusters. p50 = median cluster size. "
                   "max = lcc_size. A bimodal distribution (one large + many size-1) indicates "
                   "a compact main cluster with isolated satellites.",
    note="The raw component_sizes list is not saved to CSV. The p25/p50/p75/max columns are "
         "written instead to avoid variable-length columns.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Number of isolated cells",
    csv_col="n_isolated_cells",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="integer",
    formula="Count of cells with degree k = 0",
    interpretation="Cells with no VASA-VASA contacts above noise_threshold. "
                   "May be genuine outliers, segmentation fragments, or cells at the cluster periphery.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Fraction isolated",
    csv_col="frac_isolated",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="dimensionless  [0, 1]",
    formula="frac_isolated = n_isolated_cells / n_cells",
    interpretation="Normalised version of n_isolated_cells. Comparable across images with different N.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.add_page()
pdf.subsection_title("2C  Degree distribution", color=SAMPLE_COLOR)

pdf.metric_box(
    name="Mean degree",
    csv_col="mean_k",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="float",
    formula="mean(vasa_neighbors) across all cells",
    interpretation="Average number of VASA-VASA contacts per cell. Reflects packing density. "
                   "Higher mean_k = cells are more embedded in the cluster. "
                   "Typical range for a compact 3D cluster: 3-7.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Standard deviation of degree",
    csv_col="std_k",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="float",
    formula="std(vasa_neighbors) across all cells",
    interpretation="Heterogeneity of connectivity. Low std_k: cells are uniformly connected "
                   "(regular packing). High std_k: hub cells and peripheral cells coexist.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.subsection_title("2D  Clustering coefficient summary", color=SAMPLE_COLOR)

pdf.metric_box(
    name="Mean CC (degree >= 2 only)",
    csv_col="mean_CC_defined",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="dimensionless  [0, 1]",
    formula="mean(clustering_coeff) restricted to cells where vasa_neighbors >= 2",
    interpretation="The only meaningful population-level CC average. Cells with degree < 2 "
                   "have CC=0 by convention (undefined), and including them would bias the mean "
                   "downward in fragmented samples. "
                   "High mean_CC_defined: local triangular motifs are common = compact packing.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

pdf.metric_box(
    name="Fraction CC undefined",
    csv_col="frac_CC_undefined",
    level="Per sample  |  analyzeVASANeighbors summary",
    units="dimensionless  [0, 1]",
    formula="fraction of cells with vasa_neighbors < 2",
    interpretation="Fraction of cells for which CC is undefined (degree 0 or 1). "
                   "High values indicate a fragmented or sparsely connected population. "
                   "Report alongside mean_CC_defined to contextualise it.",
    color=SAMPLE_COLOR, bg=SAMPLE_BG)

# ---- SECTION 3: GRAPH CONTROL ----
pdf.add_page()
pdf.section_title("3  computeGraphControl  --  Graph Topology Null Test")

pdf.function_banner(
    "computeGraphControl",
    "Configuration model null hypothesis test: is the observed graph topology non-random?")

pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(*GRAY)
pdf.cell(0, 5, "Key parameters:", new_x="LMARGIN", new_y="NEXT")
pdf.param_row("n_iterations", "default=1000",
    "Number of random graph realisations. Use 200 for exploratory runs, 1000 for publication. "
    "p-value resolution = 1/n_iterations.")
pdf.ln(2)

pdf.info_box(
    "Null model: Molloy-Reed configuration model (networkx.configuration_model). "
    "Each random graph preserves the exact degree sequence of the observed graph but randomises "
    "which nodes are connected. Multi-edges and self-loops are removed after construction. "
    "CPL is always computed on the LCC of each random graph because the configuration model "
    "can produce disconnected graphs after edge removal.\n\n"
    "p-values are one-sided. Higher CC = more clustered, so p(CC) = fraction of null >= observed. "
    "Lower CPL = more compact, so p(CPL) = fraction of null <= observed.\n\n"
    "Warning: CPL computation is O(V x E) per graph. A warning is emitted if N > 300. "
    "Reduce n_iterations for large graphs.")

pdf.subsection_title("Observed metrics", color=CTRL_COLOR)

pdf.metric_box(
    name="Mean clustering coefficient (observed)",
    csv_col="ctrl_mean_clustering",
    level="Per sample  |  computeGraphControl observed",
    units="dimensionless  [0, 1]",
    formula="networkx.average_clustering(G)  -- includes all cells (degree < 2 get CC=0)",
    interpretation="Observed graph-level CC. Compare to the null distribution mean to assess "
                   "whether local clustering exceeds random expectation. "
                   "p(CC) << 0.05: significantly more triangular motifs than random.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.metric_box(
    name="Average shortest path length  (CPL)",
    csv_col="ctrl_cpl",
    level="Per sample  |  computeGraphControl observed",
    units="hops (graph distance, not micrometers)",
    formula="networkx.average_shortest_path_length(G_LCC)  -- computed on LCC only",
    interpretation="Mean number of contact-graph steps between any two cells in the LCC. "
                   "p(CPL) = 1.0: all null graphs have shorter CPL than observed. This is expected "
                   "for a physical 3D spatial graph -- random graphs have long-range shortcuts "
                   "absent in a contact graph (lattice-like structure).",
    note="CPL is in graph hops, not physical distance. A spatial contact graph always has "
         "longer CPL than a random graph of the same degree because spatial proximity "
         "constrains connections.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.metric_box(
    name="Normalised CPL",
    csv_col="ctrl_cpl_norm",
    level="Per sample  |  computeGraphControl observed",
    units="dimensionless",
    formula="CPL_norm = CPL / ln(N_LCC)  -- removes N-dependence",
    interpretation="Size-corrected path length for comparing across images with different N. "
                   "For a random graph, CPL ~ ln(N)/ln(<k>), so CPL_norm ~ 1/ln(<k>). "
                   "For a spatial lattice, CPL_norm is larger.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.add_page()

pdf.metric_box(
    name="Small-world index  (SW)",
    csv_col="ctrl_sw",
    level="Per sample  |  computeGraphControl observed",
    units="dimensionless",
    formula="SW = (CC_obs / CC_rand_mean) / (CPL_obs / CPL_rand_mean)\n"
            "Based on Watts & Strogatz 1998 (PMID 9623998)",
    interpretation="SW > 1: the graph has higher CC AND/OR lower CPL than random. "
                   "SW >> 1 for a compact physical cell cluster: CC_obs >> CC_rand dominates. "
                   "SW ~ 1: topology is indistinguishable from random at both scales. "
                   "Observed values 7-10 for control VASA clusters confirm strong small-world character.",
    note="SW is sensitive to the ratio of both metrics. Because CPL_obs > CPL_rand for spatial "
         "graphs, SW is driven almost entirely by the CC ratio. Do not interpret as evidence "
         "of 'shortcuts'; interpret as evidence of local compactness.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.subsection_title("p-values", color=CTRL_COLOR)

pdf.metric_box(
    name="p-value: mean clustering coefficient",
    csv_col="ctrl_p_mean_clustering",
    level="Per sample  |  computeGraphControl p_values",
    units="dimensionless  [0, 1]",
    formula="fraction of null graphs with CC >= observed CC  (one-sided, upper tail)",
    interpretation="p << 0.05: observed CC is significantly higher than random rewiring. "
                   "p = 0.000 (floor at 1/n_iterations): all null graphs have lower CC.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.metric_box(
    name="p-value: CPL",
    csv_col="ctrl_p_cpl",
    level="Per sample  |  computeGraphControl p_values",
    units="dimensionless  [0, 1]",
    formula="fraction of null graphs with CPL <= observed CPL  (one-sided, lower tail)",
    interpretation="p = 1.0: all null CPL <= observed CPL -- the observed graph has LONGER paths "
                   "than any random rewiring. This is expected for spatial contact graphs "
                   "(lattice-like; see CPL interpretation above). NOT evidence of poor clustering.",
    color=CTRL_COLOR, bg=CTRL_BG)

pdf.metric_box(
    name="p-value: n_components",
    csv_col="ctrl_p_n_components",
    level="Per sample  |  computeGraphControl p_values",
    units="dimensionless  [0, 1]",
    formula="fraction of null graphs with n_components >= observed n_components",
    interpretation="p = 1.0: random graphs are more fragmented than observed (expected: compact cluster). "
                   "p << 0.05: observed graph has MORE components than expected from the degree "
                   "sequence alone -- genuine spatial fragmentation beyond what random wiring predicts.",
    color=CTRL_COLOR, bg=CTRL_BG)

# ---- SECTION 4: RIPLEY'S K ----
pdf.add_page()
pdf.section_title("4  computeRipleysK  --  Spatial Point Statistics")

pdf.function_banner(
    "computeRipleysK",
    "3D Ripley's K and L functions with Monte Carlo CSR confidence envelope")

pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(*GRAY)
pdf.cell(0, 5, "Key parameters:", new_x="LMARGIN", new_y="NEXT")
pdf.param_row("n_simulations", "default=100",
    "Number of CSR Monte Carlo realisations for the confidence envelope. "
    "Increase to 500-1000 for publication-quality envelopes.")
pdf.param_row("n_steps", "default=50",
    "Number of r values evaluated. Increase for smoother curves.")
pdf.param_row("mean_diameter_um", "optional",
    "Pass summary['mean_diameter_um'] to obtain r_normalized output for cross-sample comparison.")
pdf.ln(2)

pdf.info_box(
    "Ripley's K uses cell centroids (in physical micrometers) as a spatial point pattern. "
    "It does NOT use the contact graph. K(r) counts how many cell pairs have centroids "
    "within distance r, normalised by point density. The L-transform L(r) = (3K/(4pi))^(1/3) - r "
    "linearises K so that L=0 under CSR. The 95% Monte Carlo CSR envelope is computed by "
    "randomly placing N points uniformly in the bounding box N_simulations times.\n\n"
    "Voxel anisotropy is corrected by converting centroid coordinates to physical micrometers "
    "before any distance computation.")

pdf.subsection_title("Outputs", color=RIPLEY_COLOR)

pdf.metric_box(
    name="r  (distance axis)",
    csv_col="r  [array, not in CSV]",
    level="Per sample  |  computeRipleysK",
    units="micrometers",
    formula="linspace(0, r_max, n_steps)  where r_max = min(vol_dims) / 4",
    interpretation="Distance values at which K and L are evaluated. r_max is set to 1/4 of the "
                   "smallest image dimension to avoid edge effects.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="L_observed  (L-function)",
    csv_col="L_observed  [array, not in CSV]",
    level="Per sample  |  computeRipleysK",
    units="micrometers",
    formula="L(r) = (3 * K_observed(r) / (4*pi))^(1/3) - r\n"
            "L(r) = 0 under CSR (complete spatial randomness)",
    interpretation="L(r) > 0: cells are more clustered at scale r than CSR. "
                   "L(r) above the 95% envelope: statistically significant clustering. "
                   "The scale of the peak indicates the characteristic cluster size.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="r_normalized  (diameter-normalised distance)",
    csv_col="r_normalized  [array, not in CSV]",
    level="Per sample  |  computeRipleysK",
    units="mean cell diameters (dimensionless)",
    formula="r_normalized = r / mean_diameter_um\n"
            "mean_diameter_um from analyzeVASANeighbors summary",
    interpretation="Converts the r axis from micrometers to units of mean cell diameter. "
                   "Enables direct comparison of L(r) curves across samples with different "
                   "cell sizes. r_norm = 1 corresponds to one mean cell diameter.",
    note="Only computed if mean_diameter_um is passed to computeRipleysK(). "
         "Pass summary['mean_diameter_um'] from the same image.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="CSR confidence envelope",
    csv_col="L_envelope_lo / L_envelope_hi  [arrays]",
    level="Per sample  |  computeRipleysK",
    units="micrometers",
    formula="2.5th and 97.5th percentiles of L(r) from n_simulations CSR point patterns "
            "with the same N placed uniformly at random in the bounding box",
    interpretation="The 95% pointwise envelope under the null hypothesis of CSR. "
                   "L_observed above L_envelope_hi: significant clustering at that scale. "
                   "L_observed below L_envelope_lo: significant regularity (inhibition).",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

# ---- SECTION 5: GEOMETRIC METRICS ----
pdf.add_page()
pdf.section_title("5  computeGeometricMetrics  --  Domain Shape Metrics")

pdf.function_banner(
    "computeGeometricMetrics",
    "Radius of gyration + surface/volume ratio of the merged VASA binary domain")

pdf.info_box(
    "These metrics describe the SHAPE and EXTENT of the whole VASA cell population, "
    "not individual cells. Two complementary views:\n"
    "  (1) Centroid cloud geometry: radius of gyration Rg -- how spread are the cell centres?\n"
    "  (2) Domain surface geometry: S/V of the merged binary mask -- how complex is the boundary?\n\n"
    "Both are normalised by R_eq = (3*N*V_mean/(4*pi))^(1/3), the radius of a sphere "
    "containing the same total VASA cell volume. This removes the N- and size-dependence "
    "so values are comparable across images.")

pdf.subsection_title("Radius of gyration", color=RIPLEY_COLOR)

pdf.metric_box(
    name="Radius of gyration  (Rg)",
    csv_col="geom_rg_um",
    level="Per sample  |  computeGeometricMetrics",
    units="micrometers",
    formula="Rg = sqrt( mean( |r_i - r_cm|^2 ) )\n"
            "r_i = centroid of cell i in physical um (ZYX);  r_cm = mean centroid",
    interpretation="RMS distance of cell centroids from the cluster centre of mass. "
                   "Larger Rg = more spread out cluster. Scales with N^(1/3) for a compact sphere, "
                   "so always report alongside n_cells.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="Equivalent sphere radius  (R_eq)",
    csv_col="geom_r_eq_um",
    level="Per sample  |  computeGeometricMetrics",
    units="micrometers",
    formula="R_eq = (3 * N * V_mean / (4*pi))^(1/3)\n"
            "Radius of a sphere with the same total VASA cell volume",
    interpretation="Reference size for normalisation. Does NOT depend on spatial arrangement -- "
                   "it is a volume-based quantity derived from cell count and mean cell volume. "
                   "Larger R_eq = more cells or larger cells.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="Normalised radius of gyration  (Rg_norm)",
    csv_col="geom_rg_norm",
    level="Per sample  |  computeGeometricMetrics",
    units="dimensionless",
    formula="Rg_norm = Rg / R_eq\n"
            "Reference: uniform solid sphere -> Rg/R = sqrt(3/5) ~ 0.775",
    interpretation="Rg_norm ~ 0.775: centroid cloud consistent with a compact sphere. "
                   "Rg_norm > 0.775: cluster more spread than a sphere of the same total volume. "
                   "Note: discrete cell packing adds ~10-15% above 0.775 even for a compact cluster, "
                   "so the effective compact reference is ~ 0.85-0.90. "
                   "Observed values 1.06-1.24 indicate a moderately elongated cluster "
                   "consistent with the tubular germarium geometry.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.add_page()
pdf.subsection_title("Surface / volume ratio", color=RIPLEY_COLOR)

pdf.metric_box(
    name="Domain surface / volume ratio  (S/V)",
    csv_col="geom_sv_ratio",
    level="Per sample  |  computeGeometricMetrics",
    units="um^-1",
    formula="sv_ratio = S_domain / V_domain\n"
            "S_domain: marching-cubes surface area of binary mask (label_image > 0) with px_size spacing\n"
            "V_domain: N * mean_volume_um3  (total VASA cell volume)",
    interpretation="For a sphere of radius R: S/V = 3/R. Larger S/V = more complex boundary "
                   "relative to the contained volume. Sensitive to cluster shape, surface "
                   "roughness, and internal gaps between cells.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

pdf.metric_box(
    name="Normalised S/V  (sv_ratio_norm)",
    csv_col="geom_sv_ratio_norm",
    level="Per sample  |  computeGeometricMetrics",
    units="dimensionless",
    formula="sv_ratio_norm = sv_ratio * R_eq / 3\n"
            "Reference: perfect sphere -> sv_ratio_norm = 1",
    interpretation="sv_ratio_norm = 1: domain surface equals that of an equivalent sphere. "
                   "> 1: excess surface from irregular shape, cell-boundary roughness, or internal gaps. "
                   "Observed values 3.8-4.9 in control data. These high values reflect that marching "
                   "cubes resolves individual cell surfaces, not just the outer hull. "
                   "Use for RELATIVE comparison between conditions, not as an absolute shape descriptor. "
                   "A significant decrease across conditions would indicate increased surface sharing.",
    note="S_domain is computed from the merged binary mask using skimage.measure.marching_cubes "
         "with the physical voxel spacing. Each cell's outer surface is included except where "
         "cells share voxel-face boundaries. Internal gaps between cells contribute extra surface.",
    color=RIPLEY_COLOR, bg=RIPLEY_BG)

# ---- SECTION 6: OUTPUT FILES ----
pdf.add_page()
pdf.section_title("6  Output Files  --  Column Reference")

pdf.subsection_title("*_VASA_neighbor_metrics.csv  (per-cell)", color=BLUE)

cols_w = [60, 20, 110]
pdf.set_fill_color(*LGRAY)
pdf.set_font("Helvetica", "B", 7.5)
pdf.set_text_color(*BLACK)
for h, w in zip(["Column", "Units", "Description"], cols_w):
    pdf.cell(w, 5.5, f"  {h}", border=1, fill=True)
pdf.ln()

cell_csv = [
    ("label",                 "int",  "Cell instance ID from label image"),
    ("centroid_z/y/x",        "vox",  "Cell centroid in voxel coordinates (ZYX)"),
    ("volume_um3",            "um3",  "Cell volume in cubic micrometers"),
    ("equivalent_diameter_um","um",   "Equivalent sphere diameter"),
    ("vasa_neighbors",        "int",  "Degree: number of VASA-VASA contacts (k_i)"),
    ("cluster_size",          "int",  "Size of connected component containing this cell"),
    ("vasa_surface",          "um2",  "Shared surface area with VASA neighbours"),
    ("non_vasa_surface",      "um2",  "Surface area not touching another VASA cell"),
    ("total_surface",         "um2",  "Total cell surface (vasa + non_vasa)"),
    ("shared_boundary_ratio", "[0,1]","Fraction of surface touching VASA cells (SBR)"),
    ("clustering_coeff",      "[0,1]","Local clustering coefficient (0 if degree < 2)"),
    ("dataset",               "str",  "Dataset identifier (added in pipeline notebook)"),
    ("condition",             "str",  "Experimental condition (added in pipeline notebook)"),
]

pdf.set_font("Helvetica", "", 7.5)
for i, (col, unit, desc) in enumerate(cell_csv):
    fill = i % 2 == 0
    pdf.set_fill_color(*(LGRAY2 if fill else WHITE))
    pdf.cell(cols_w[0], 4.5, f"  {col}", border=1, fill=fill)
    pdf.cell(cols_w[1], 4.5, f"  {unit}", border=1, fill=fill)
    pdf.multi_cell(cols_w[2], 4.5, f"  {desc}", border=1, fill=fill, new_x="LMARGIN")

pdf.ln(4)
pdf.subsection_title("*_VASA_neighbor_summary.csv  (per sample)", color=BLUE)

cols_w2 = [65, 20, 105]
pdf.set_fill_color(*LGRAY)
pdf.set_font("Helvetica", "B", 7.5)
for h, w in zip(["Column", "Units", "Description"], cols_w2):
    pdf.cell(w, 5.5, f"  {h}", border=1, fill=True)
pdf.ln()

summary_csv = [
    ("n_cells",             "int",   "Total VASA cells"),
    ("n_components",        "int",   "Number of connected components"),
    ("lcc_size",            "int",   "Largest connected component size"),
    ("fragmentation_index", "[0,1)", "FI = 1 - lcc_size/n_cells"),
    ("mean_cluster_size",   "float", "Mean component size (cells)"),
    ("median_cluster_size", "float", "Median component size"),
    ("n_isolated_cells",    "int",   "Cells with degree = 0"),
    ("frac_isolated",       "[0,1]", "n_isolated / n_cells"),
    ("mean_k",              "float", "Mean degree"),
    ("std_k",               "float", "Std of degree distribution"),
    ("mean_CC_defined",     "[0,1]", "Mean CC for cells with degree >= 2"),
    ("frac_CC_undefined",   "[0,1]", "Fraction of cells with degree < 2"),
    ("mean_volume_um3",     "um3",   "Mean cell volume"),
    ("mean_diameter_um",    "um",    "Mean equivalent diameter"),
    ("comp_size_p25/p50/p75", "int", "Percentiles of component size distribution"),
    ("comp_size_max",       "int",   "Largest component size (= lcc_size)"),
]

pdf.set_font("Helvetica", "", 7.5)
for i, (col, unit, desc) in enumerate(summary_csv):
    fill = i % 2 == 0
    pdf.set_fill_color(*(LGRAY2 if fill else WHITE))
    pdf.cell(cols_w2[0], 4.5, f"  {col}", border=1, fill=fill)
    pdf.cell(cols_w2[1], 4.5, f"  {unit}", border=1, fill=fill)
    pdf.multi_cell(cols_w2[2], 4.5, f"  {desc}", border=1, fill=fill, new_x="LMARGIN")

# ---- SECTION 7: INTERPRETATION GUIDE ----
pdf.add_page()
pdf.section_title("7  Quick Interpretation Guide")

pdf.info_box(
    "Use this table to assess what each result means for a VASA germ cell cluster. "
    "Compact, healthy germ-cell niche = right column. Dispersed / perturbed = left column.",
    color=BLUE)

guide = [
    ("Metric",              "Dispersed / fragmented",          "Compact / clustered"),
    ("fragmentation_index", "High (> 0.1)",                    "Low (< 0.03)"),
    ("n_components",        "Many (> 5)",                      "1 or 2"),
    ("mean_k",              "Low (< 3)",                       "High (> 5)"),
    ("shared_boundary_ratio","Low mean (< 0.2)",               "High mean (> 0.4)"),
    ("mean_CC_defined",     "Low (< 0.3)",                     "High (> 0.5)"),
    ("ctrl_p_CC",           "High (CC not unusual)",           "Low ~ 0 (CC >> random)"),
    ("ctrl_sw",             "~ 1 (no small-world character)",  ">> 1 (compact topology)"),
    ("L(r) vs envelope",    "Within or below CSR envelope",    "Above envelope at small r"),
    ("geom_rg_norm",        "High (>> 1)",                     "Closer to 0.85-0.90"),
    ("geom_sv_ratio_norm",  "High (excess surface)",           "Relatively lower"),
]

col_w = [55, 67, 68]
pdf.set_fill_color(*LGRAY)
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(*BLACK)
for h, w in zip(guide[0], col_w):
    pdf.cell(w, 6, f"  {h}", border=1, fill=True)
pdf.ln()

pdf.set_font("Helvetica", "", 8)
for i, (m, lo, hi) in enumerate(guide[1:]):
    fill = i % 2 == 0
    pdf.set_fill_color(*(LGRAY2 if fill else WHITE))
    pdf.set_text_color(*BLACK)
    pdf.cell(col_w[0], 5, f"  {m}", border=1, fill=fill)
    pdf.set_text_color(*RED)
    pdf.cell(col_w[1], 5, f"  {lo}", border=1, fill=fill)
    pdf.set_text_color(*GREEN)
    pdf.cell(col_w[2], 5, f"  {hi}", border=1, fill=fill, new_x="LMARGIN", new_y="NEXT")

pdf.set_text_color(*BLACK)
pdf.ln(4)

pdf.info_box(
    "General rules:\n"
    "  - Always report n_cells as a covariate (most metrics scale with N).\n"
    "  - Use mean_CC_defined, NOT mean clustering_coeff, for CC summary.\n"
    "  - CPL p = 1.0 is expected for spatial graphs; it does NOT indicate poor clustering.\n"
    "  - S/V norm >> 1 is expected; use it for relative comparison between conditions only.\n"
    "  - Ripley's L and graph metrics are complementary: L uses centroids (continuous space); "
    "graph metrics use contact topology (discrete). Use both.",
    color=BLUE)

pdf.output(OUTPUT)
print(f"Saved: {OUTPUT}")
