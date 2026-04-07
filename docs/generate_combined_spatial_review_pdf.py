from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "literature_review_spatial_metrics_combined.pdf")

BLUE  = (30, 80, 160)
LINK  = (0, 100, 200)
GRAY  = (80, 80, 80)
LGRAY = (230, 230, 230)
LGRAY2= (245, 245, 245)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
AMBER = (160, 100, 0)
AMBERLIGHT = (255, 248, 225)
GREEN = (0, 110, 60)
GREENLIGHT = (225, 245, 230)


class PDF(FPDF):
    def header(self):
        self.set_fill_color(*BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6,
            "Literature Review - VASA Cell Spatial Analysis: Compactness, Embedding, and Spatial Statistics",
            new_x="RIGHT", new_y="TOP")
        self.ln(14)

    def footer(self):
        self.set_y(-12)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*GRAY)
        self.cell(0, 6,
            f"Page {self.page_no()} | PubMed search - March 2026 | fly_ovaries_processing_pipeline",
            align="C")

    def part_banner(self, letter, title, subtitle, current=True):
        self.ln(3)
        color = BLUE if current else AMBER
        self.set_fill_color(*color)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 12)
        self.cell(0, 10, f"  PART {letter}: {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.set_fill_color(*(LGRAY2 if current else AMBERLIGHT))
        self.set_text_color(*(BLUE if current else AMBER))
        self.set_font("Helvetica", "I", 9)
        self.cell(0, 6, f"  {subtitle}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(2)

    def section_title(self, title):
        self.ln(3)
        self.set_fill_color(*BLUE)
        self.set_text_color(*WHITE)
        self.set_font("Helvetica", "B", 10)
        self.cell(0, 7, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
        self.ln(1)

    def subsection_title(self, title):
        self.ln(2)
        self.set_fill_color(*LGRAY)
        self.set_text_color(*BLUE)
        self.set_font("Helvetica", "B", 9)
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
        self._labeled_block("Display", display)
        self._labeled_block("Controls", controls)
        self.ln(3)

    def _labeled_block(self, label, text):
        self.set_font("Helvetica", "B", 8)
        self.set_text_color(*BLUE)
        self.cell(26, 4, label + ":", new_x="RIGHT", new_y="TOP")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*BLACK)
        self.multi_cell(0, 4, text, new_x="LMARGIN")

    def metric_box(self, name, formula, interpretation, pipeline, difficulty,
                   future=False, published="", doi=""):
        bg = AMBERLIGHT if future else LGRAY2
        border_color = AMBER if future else BLUE
        self.set_fill_color(*bg)
        self.set_draw_color(*border_color)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, 190, 4.5, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*border_color)
        self.set_xy(self.l_margin + 2, y0 + 0.5)
        self.cell(0, 3.5, name, new_x="LMARGIN", new_y="NEXT")
        self._labeled_block("Formula / method", formula)
        self._labeled_block("Interpretation", interpretation)
        self._labeled_block("Pipeline", pipeline)
        self._labeled_block("Effort", difficulty)
        if published:
            self.set_font("Helvetica", "B", 8)
            self.set_text_color(*border_color)
            self.cell(26, 4, "Source:", new_x="RIGHT", new_y="TOP")
            self.set_font("Helvetica", "", 8)
            self.set_text_color(*BLACK)
            if doi:
                self.write(4, published + "  ")
                self.set_text_color(*LINK)
                self.write(4, doi, link=f"https://doi.org/{doi}")
                self.set_text_color(*BLACK)
                self.ln(4)
            else:
                self.multi_cell(0, 4, published, new_x="LMARGIN")
        self.ln(2)
        self.set_line_width(0.2)

    def table_row(self, cols, widths, header=False, future_row=False):
        if header:
            self.set_fill_color(*BLUE)
            self.set_text_color(*WHITE)
            self.set_font("Helvetica", "B", 8)
        elif future_row:
            self.set_fill_color(*AMBERLIGHT)
            self.set_text_color(*BLACK)
            self.set_font("Helvetica", "I", 8)
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
            fill = header or future_row
            self.multi_cell(w, 4, text, border=1, fill=fill, max_line_height=4,
                            new_x="RIGHT", new_y="TOP")
            x0 += w
        self.set_xy(self.l_margin, y0 + max_h)

    def note_box(self, text, future=False):
        color = AMBER if future else BLUE
        light = AMBERLIGHT if future else (220, 230, 245)
        self.set_fill_color(*light)
        self.set_draw_color(*color)
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


# =============================================================================
pdf = PDF()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ---- TITLE ------------------------------------------------------------------
pdf.set_font("Helvetica", "B", 15)
pdf.set_text_color(*BLUE)
pdf.ln(2)
pdf.multi_cell(0, 7, "Spatial Analysis of VASA Germ Cells:\nCombined Metric Reference for Compactness,\nEmbedding, and Cell-Type Association", align="C", new_x="LMARGIN")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*GRAY)
pdf.multi_cell(0, 5, "PubMed literature review | fly_ovaries_processing_pipeline | March 2026", align="C", new_x="LMARGIN")
pdf.ln(3)
pdf.set_draw_color(*BLUE)
pdf.set_line_width(0.5)
pdf.line(pdf.l_margin, pdf.get_y(), 210 - pdf.r_margin, pdf.get_y())
pdf.ln(4)

# ---- DATA AVAILABLE ---------------------------------------------------------
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Data available from the current pipeline", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)
pdf.multi_cell(0, 5,
    "* VASA instance segmentation label image (3D, uint16)\n"
    "* Per-cell surface area (marching cubes) and volume (voxel count) in physical units (um, um2, um3)\n"
    "* Per-cell centroid coordinates (Z, Y, X) in physical units\n"
    "* VASA-VASA contact graph (NetworkX): nodes = VASA cells, edges = face-adjacent cell pairs\n"
    "* Per-cell: degree (N VASA-VASA contacts), clustering coefficient, surface sharing ratio\n"
    "  Surface sharing ratio = (surface area shared with VASA neighbors) / (total cell surface area);\n"
    "  the remainder is surface facing non-VASA entities (ECM, other cell types, tissue boundary - unknown)\n"
    "* TJ cells are segmented separately in a different channel with no spatial co-registration to VASA",
    new_x="LMARGIN")
pdf.ln(3)

# ---- COLOUR KEY -------------------------------------------------------------
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLACK)
pdf.cell(0, 5, "Colour code used throughout this document", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 9)

pdf.set_fill_color(*LGRAY2)
pdf.set_draw_color(*BLUE)
pdf.set_line_width(0.3)
pdf.cell(5, 5, "", border=1, fill=True)
pdf.set_x(pdf.get_x() + 1)
pdf.cell(0, 5, "BLUE / white background = Part A: applicable NOW with current VASA-only data", new_x="LMARGIN", new_y="NEXT")

pdf.set_fill_color(*AMBERLIGHT)
pdf.set_draw_color(*AMBER)
pdf.cell(5, 5, "", border=1, fill=True)
pdf.set_x(pdf.get_x() + 1)
pdf.cell(0, 5, "AMBER / yellow background = Part B: requires future multi-channel spatial co-registration", new_x="LMARGIN", new_y="NEXT")
pdf.set_line_width(0.2)
pdf.set_draw_color(*BLACK)
pdf.ln(4)

# =============================================================================
# PART A
# =============================================================================
pdf.part_banner("A", "CURRENTLY APPLICABLE METRICS",
    "All metrics below use only VASA segmentation data: label image, contact graph, centroids, surface areas.",
    current=True)

# ---- A1: GRAPH TOPOLOGY -----------------------------------------------------
pdf.section_title("A1 - Graph Topology of the VASA Contact Network")
pdf.note_box(
    "The VASA contact graph represents every pair of VASA cells that physically share a face (voxel-adjacency). "
    "All metrics in this section work on this graph. The null hypothesis for graph metrics is the "
    "configuration model: a random graph that preserves the degree sequence but randomizes connectivity. "
    "This is already implemented in the pipeline (computeGraphControl). "
    "Key question: is the VASA contact network more locally clustered and/or more compact (shorter paths) "
    "than a random graph with the same degree sequence?")

pdf.paper_entry(
    title="Human Cancer Cell Radiation Response Investigated through Topological Analysis of 2D Cell Networks",
    authors_journal="Tirinato L et al. | Annals of Biomedical Engineering 2023",
    pmid="37093401",
    doi="10.1007/s10439-023-03215-z",
    summary=(
        "Builds 2D fluorescence-image cell contact graphs for 4 cancer lines at 0-6 Gy radiation. "
        "Computes clustering coefficient (CC), characteristic path length (CPL), and small-world "
        "coefficient (SW = (CC/CC_rand)/(CPL/CPL_rand)). Higher radiation dose -> higher CC + lower CPL. "
        "SW > 1 quantifies departure from a random graph layout toward a small-world / compact topology."
    ),
    relevance=(
        "Most directly applicable paper: same framework (physical cell contact graph -> CC, CPL, SW) "
        "as the VASA pipeline. Compact ball cluster = high CC + low CPL; spread chain = low CC + high CPL. "
        "SW normalizes both metrics relative to a random graph with the same N and degree sequence, "
        "making it comparable across ovary images with different N_VASA."
    ),
    display="Bar charts CC, CPL, SW per condition. Scatter CC vs CPL per image, colour by condition.",
    controls=(
        "Configuration model null (preserves degree sequence, n=1000 permutations) -- already implemented. "
        "Normalize CPL and diameter by ln(N_VASA) to remove N-dependence. "
        "Dose-response in original paper = biological positive control idea."
    )
)

pdf.paper_entry(
    title="Human lung-cancer-cell radioresistance investigated through 2D network topology",
    authors_journal="Tirinato L et al. | Scientific Reports 2022",
    pmid="35902618",
    doi="10.1038/s41598-022-17018-0",
    summary=(
        "Predecessor paper. Applies CC, CPL, SW to 2D cell contact graphs (H460, A549, Calu-1) at 0-8 Gy. "
        "SW > 1 = 'discontinuous inhomogeneous cell layout' (spread); compact clusters approach SW ~ 1 "
        "(regular-lattice-like). Graph built from Delaunay triangulation + proximity threshold."
    ),
    relevance=(
        "Confirms SW sensitivity to cell arrangement. Face-adjacency (our pipeline) is a stricter criterion "
        "than Delaunay proximity, so our CC and CPL values reflect true physical contact, not just proximity."
    ),
    display="SW vs radiation dose per cell line. Heatmap of CC x CPL space.",
    controls="Proximity threshold sensitivity analysis. Random graph with same N and edge count as null."
)

pdf.paper_entry(
    title="Collective dynamics of 'small-world' networks",
    authors_journal="Watts DS & Strogatz SH | Nature 1998",
    pmid="9623998",
    doi="10.1038/30918",
    summary=(
        "Foundational definitions: CC = fraction of a node's neighbors that are also connected to each other. "
        "CPL = average shortest path length over all node pairs. "
        "Small-world: high CC AND low CPL simultaneously. SW = (CC_obs/CC_rand)/(CPL_obs/CPL_rand)."
    ),
    relevance=(
        "Essential reference for CC, CPL, SW definitions. A compact cell cluster resembles a regular lattice "
        "(high CC, moderate CPL); a chain-like cluster has low CC and high CPL."
    ),
    display="cc/cpl vs rewiring probability plot (Fig 2 of paper). Adapt for cell contact data.",
    controls="Compare against equivalent Erdos-Renyi random graph and regular ring lattice."
)

# ---- A2: CLUSTER TOPOLOGY (fragmentation, components) -----------------------
pdf.section_title("A2 - Cluster Topology: Fragmentation and Component Structure")
pdf.note_box(
    "While A1 metrics assume the graph is one connected component, in practice VASA cells may form "
    "multiple disconnected clusters. These metrics characterize how fragmented the VASA contact network is. "
    "Note: the pipeline currently checks for connected components; these metrics quantify it systematically.")

pdf.paper_entry(
    title="Understanding heterogeneous tumor microenvironment in metastatic melanoma",
    authors_journal="Yan Y et al. | PLoS ONE 2019",
    pmid="31166985",
    doi="10.1371/journal.pone.0216485",
    summary=(
        "Introduces the Cell Aggregate Algorithm (CAA): identifies connected components within the "
        "same-type contact subgraph. Reports N_components, size distribution of components (exponential vs. "
        "heavy-tailed), and size of the largest connected component (LCC). "
        "A well-clustered population has one LCC containing most cells; a dispersed population has many "
        "small components. Companion Cell Neighborhood Analysis counts neighbors of each type within a radius."
    ),
    relevance=(
        "CAA maps exactly onto our VASA contact graph: the graph IS the same-type subgraph. "
        "Apply nx.connected_components() to get all components. "
        "Fragmentation Index FI = 1 - N_LCC/N_VASA: FI=0 means one perfect cluster; "
        "FI near 1 means all cells isolated. Also report N_components and the size distribution histogram."
    ),
    display=(
        "Histogram of component sizes per image. "
        "Label image painted by component membership, coloured by component size. "
        "Bar chart of FI per condition."
    ),
    controls=(
        "FI depends on N_VASA -- larger populations have lower FI by chance. "
        "Normalize FI*ln(N_VASA) for size-fair comparison. "
        "Run on simulated CSR point patterns with same N and V to get null FI distribution."
    )
)

# ---- A3: CELL EMBEDDING -----------------------------------------------------
pdf.section_title("A3 - Cell-Level Embedding Depth in the VASA Cluster")
pdf.note_box(
    "These metrics describe how deeply embedded each cell is within the VASA cluster, "
    "using only the per-cell information already available in the pipeline. "
    "No information about non-VASA cell identities is needed.")

pdf.paper_entry(
    title="Aggregation dynamics of active cells on non-adhesive substrate",
    authors_journal="Mukhopadhyay S & De R | Physical Biology 2019",
    pmid="31042683",
    doi="10.1088/1478-3975/ab1e76",
    summary=(
        "Models self-assembling cell aggregates. Defines compactness as the ratio of boundary cells to "
        "total cells: a boundary cell has at least one non-cell neighbor (exposed surface). "
        "For a filled 3D sphere: boundary cells ~ surface cells ~ N^(2/3); ratio -> 0 as N grows. "
        "For a chain: every cell is a boundary cell; ratio = 1. "
        "Also tracks fractal dimension of the boundary as the aggregate grows."
    ),
    relevance=(
        "Defines 'boundary vs. interior cells' for a cell aggregate. In our pipeline: "
        "a cell is an interior cell if its surface sharing ratio is high (almost all surface touching VASA). "
        "A boundary cell has low surface sharing ratio (much surface exposed to non-VASA). "
        "Fraction of interior cells (e.g. surface sharing ratio > 0.8) is a compactness scalar. "
        "This reframes the surface sharing ratio as an embedding depth metric."
    ),
    display="Histogram of surface sharing ratio per image. Fraction interior cells per condition (bar chart).",
    controls=(
        "Simulate random packing of spheres in a volume -- what is the expected surface sharing ratio distribution? "
        "Use this as null. Report with mean cell size and N_VASA."
    )
)

# ---- A4: GEOMETRIC METRICS --------------------------------------------------
pdf.section_title("A4 - Geometric Metrics from Centroids and Label Image")

pdf.note_box(
    "These metrics use VASA cell centroid positions and the merged VASA binary mask. "
    "They describe the 3D geometry of the VASA population, complementing the graph topology metrics above.")

pdf.paper_entry(
    title="ShapeMetrics: A Python-based pipeline for 3D cell morphometrics and spatial mapping",
    authors_journal="Takko H et al. | Developmental Biology 2020",
    pmid="32061886",
    doi="10.1016/j.ydbio.2020.01.011",
    summary=(
        "End-to-end Python pipeline: 3D segmentation -> morphometrics -> unsupervised clustering -> "
        "spatial remapping onto tissue. Per-cell metrics include: volume, surface area, "
        "ellipticity (ratio of principal axes of inertia tensor), sphericity. "
        "Spatial remapping shows morphometric gradients within the tissue (e.g. elongated cells at tissue boundary). "
        "Applied to zebrafish lateral line primordium."
    ),
    relevance=(
        "Directly applicable framework for computing per-cell morphometrics from 3D label images. "
        "Population-level geometric metrics: centroid cloud radius of gyration (Rg), "
        "asphericity from gyration tensor eigenvalues, convex hull volume vs. total cell volume. "
        "Spatial morphometric gradients within the VASA cluster (do core cells differ in shape from periphery?)."
    ),
    display="Per-cell morphometrics painted on label image. PCA of centroid cloud. Rg vs condition boxplot.",
    controls=(
        "Random placement of N spheres with same size distribution in same bounding volume -> expected Rg. "
        "Compare gyration tensor eigenvalues to those of a uniform sphere."
    )
)

pdf.paper_entry(
    title="Lung cancer - a fractal viewpoint",
    authors_journal="Lennon FE et al. | Nature Reviews Clinical Oncology 2015",
    pmid="26169924",
    doi="10.1038/nrclinonc.2015.108",
    summary=(
        "Review of FD and lacunarity for tumor morphology. FD (box-counting): "
        "measures how fully a structure fills its bounding box across scales. FD = 3 for solid sphere in 3D. "
        "Lacunarity: measures 'gappiness' -- how uniformly cells fill space. "
        "Low lacunarity = homogeneous fill (compact cluster). High lacunarity = gappy / heterogeneous (spread or scattered)."
    ),
    relevance=(
        "Establishes FD + lacunarity as a 2D descriptor space for aggregate morphology, applicable to 3D binary label images. "
        "Compact VASA cluster: FD near 3, lacunarity low. "
        "Spread/branching: FD < 3, lacunarity high. Gliding-box lacunarity algorithm directly applicable "
        "to our 3D VASA binary mask (merged label image)."
    ),
    display="FD vs lacunarity scatter per sample, colour by condition. FD and lacunarity boxplots.",
    controls="Solid sphere and random point cloud as reference extremes. Permutation test on FD values."
)

pdf.paper_entry(
    title="Fractal dimension and lacunarity of glioma subcomponents discriminate grade and IDH status",
    authors_journal="Yadav D et al. | NMR in Biomedicine 2024",
    pmid="39367752",
    doi="10.1002/nbm.5272",
    summary=(
        "Applies 3D FD and 3D lacunarity to glioma from MRI volumes. High-grade (more compact/enhancing): "
        "higher FD + lower lacunarity. Machine learning on FD alone achieves 97.9% sensitivity for grade discrimination. "
        "Validates the 3D FD + lacunarity framework in volumetric imaging analogous to 3D confocal stacks."
    ),
    relevance=(
        "Confirms that 3D FD and lacunarity computed from volumetric segmentation are meaningful and discriminative. "
        "Implementation: skimage.measure.label on merged VASA binary mask -> box-counting via iterative downsampling "
        "or regionprops on the merged object."
    ),
    display="FD3D vs Lac3D scatter. Boxplots by condition. ROC if binary classification needed.",
    controls="Cross-image validation. Permutation test. Report voxel size and anisotropy correction."
)

pdf.paper_entry(
    title="Fractal analysis: revisiting Whittle's approach to the fractal dimension of cellular networks",
    authors_journal="Cross SS | Journal of Pathology 1997",
    pmid="9227334",
    doi="10.1002/(SICI)1096-9896(199707)182:3<371::AID-PATH872>3.0.CO;2-B",
    summary=(
        "Foundational review of box-counting fractal dimension for biological structures including tumors and neurons. "
        "Defines FD algorithm: cover image with grids of decreasing box size r, count occupied boxes N(r), "
        "FD = -slope of log(N(r)) vs log(r). Discusses biological interpretation and pitfalls "
        "(image resolution limits, size of structure relative to box sizes used)."
    ),
    relevance=(
        "Essential reference for the FD method. In 3D: FD = -slope of log(N_occupied_boxes(r)) vs log(r). "
        "Pitfall: result depends on image resolution and range of r values used -- always report these. "
        "FD of VASA binary mask quantifies spatial complexity of the cell aggregate."
    ),
    display="Log-log plot of N(r) vs r with linear fit slope reported as FD.",
    controls="Use at least 6 box sizes spanning 1 order of magnitude. Report R2 of log-log fit."
)

# ---- A5: SPATIAL STATISTICS -------------------------------------------------
pdf.section_title("A5 - Spatial Statistics on VASA Centroid Positions")

pdf.note_box(
    "Ripley's K and the pair correlation function treat each VASA cell centroid as a point and test whether "
    "the overall spatial distribution is more clustered than complete spatial randomness (CSR). "
    "No information about non-VASA cells is needed. The null is simulated by randomly placing N_VASA points "
    "uniformly within the tissue bounding volume (Monte Carlo CSR).")

pdf.paper_entry(
    title="Tumor immune cell clustering and its association with survival in African American women with ovarian cancer",
    authors_journal="Wilson C, Soupir AC et al. | PLoS Computational Biology 2022",
    pmid="35235563",
    doi="10.1371/journal.pcbi.1009900",
    summary=(
        "Applies Ripley's K with Monte Carlo CSR permutation envelope to quantify immune cell clustering in ovarian cancer. "
        "K at fixed radius r (scalar nK(r)) enables ANOVA-style group comparisons. "
        "Key finding: combining cell abundance with spatial clustering K(r) gives better survival discrimination "
        "than either alone -- spatial arrangement matters beyond cell count."
    ),
    relevance=(
        "Already implemented in our pipeline (computeRipleysK). "
        "L(r) - r > 0 = clustered at scale r. The peak of L(r)-r gives the characteristic cluster scale. "
        "nK(r*) at r* = 2-3 cell diameters as a per-image scalar for boxplot comparisons across conditions."
    ),
    display="L(r)-r curve with 95% CSR Monte Carlo envelope. nK(r*) boxplot per condition.",
    controls=(
        "100 CSR simulations within tissue bounding box. "
        "Edge correction (isotropic or border method). "
        "Always report N_VASA and tissue volume alongside K metric."
    )
)

pdf.paper_entry(
    title="Extended correlation functions for spatial analysis of multiplex imaging data",
    authors_journal="Bull JA, Mulholland EJ et al. | Biological Imaging 2024",
    pmid="38516631",
    doi="10.1017/S2633903X24000011",
    summary=(
        "Extends the pair correlation function (PCF) in three ways: "
        "(1) Topographical correlation maps (TCM): local g(r) computed per cell position rather than globally; "
        "(2) Neighbourhood correlation functions (NCF): co-localization of multiple cell types simultaneously; "
        "(3) Weighted-PCF: continuous labels (marker intensity) instead of discrete cell types. "
        "Applied to intestinal crypt and breast cancer data."
    ),
    relevance=(
        "For VASA-only analysis: g_VASA(r) = (observed VASA centroid pairs at distance r) / (expected from CSR). "
        "g(r) > 1 = VASA cells cluster at scale r. g(r) derived from K(r): g(r) = K'(r)/(4*pi*r^2) in 3D. "
        "The TCM extension is useful for current pipeline: compute a local density-weighted g(r) "
        "per cell to map where clustering is strongest within the tissue. "
        "NCF and cross-type TCM are reserved for future multi-channel analysis (see Part B)."
    ),
    display="g(r) curve with CSR envelope. Peak g(r) location = characteristic cluster scale. TCM painted on label image.",
    controls=(
        "CSR envelope from 100 Monte Carlo simulations. "
        "g(r) scalar at r = 1 cell diameter as compactness index. "
        "Sensitivity to bandwidth (smoothing parameter in KDE-based g(r) estimate)."
    )
)

# ---- A6: METRIC CATALOG -----------------------------------------------------
pdf.section_title("A6 - Complete Metric Catalog (Part A)")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "All metrics use VASA-only data. Ordered within each group from easiest to most involved. "
    "Status: 'done' = already in pipeline; 'trivial' = <1h; 'easy' = 1-3h; 'moderate' = 3-8h.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.subsection_title("Group 1: Contact graph metrics (use NetworkX graph)")

pdf.metric_box(
    name="1. Surface sharing ratio (mean per image)",
    formula=(
        "SSR_i = (surface area of cell i shared with VASA neighbors) / (total surface area of cell i). "
        "Already computed per cell. Population metric: mean(SSR), std(SSR), fraction of cells with SSR > 0.8 (interior cells)."
    ),
    interpretation=(
        "SSR_i near 1: cell deeply embedded in VASA cluster (interior cell). "
        "SSR_i near 0: isolated VASA cell or surface cell. "
        "Mean SSR across all VASA cells is the primary embedding-depth index. "
        "High mean SSR = compact, well-clustered population."
    ),
    pipeline="Already in neighbor metrics CSV. Add: mean SSR per image, fraction interior cells (SSR>0.8).",
    difficulty="Done -- just aggregate the per-cell values",
    published="Adapted (Mukhopadhyay & De 2019) -- boundary/interior cell ratio concept",
    doi="10.1088/1478-3975/ab1e76"
)

pdf.metric_box(
    name="2. Fragmentation Index (FI) and component size distribution",
    formula=(
        "G_vasa = full VASA contact graph (already is the VASA subgraph -- no TJ nodes). "
        "CCs = list(nx.connected_components(G_vasa)). "
        "FI = 1 - max(len(c) for c in CCs) / N_VASA. "
        "Also: N_components, component size histogram."
    ),
    interpretation=(
        "FI = 0: one connected cluster (all cells reachable). FI near 1: all cells isolated. "
        "N_components = 1 and FI = 0: perfect single cluster. "
        "Component size distribution: exponential = random fragmentation; heavy-tailed = one dominant cluster + outliers."
    ),
    pipeline="~3 lines of NetworkX. Add to analyzeVASANeighbors() output or as new function.",
    difficulty="Trivial",
    published="Yes (Schurch et al. 2020) -- CN fragmentation = 1 - N_LCC/N_total",
    doi="10.1016/j.cell.2020.07.005"
)

pdf.metric_box(
    name="3. Degree distribution (VASA-VASA contacts per cell)",
    formula=(
        "k_i = degree of node i in VASA contact graph = number of VASA-VASA contacts. "
        "Report: mean k, std k, fraction cells with k=0 (isolated VASA cells with no VASA contact)."
    ),
    interpretation=(
        "High mean k = dense VASA-VASA contact network = compact cluster. "
        "Fraction with k=0 = isolated VASA cells = quick dispersion proxy. "
        "k distribution shape: Poisson-like (random) vs. bimodal (core + surface cells)."
    ),
    pipeline="Already stored as 'num_neighbors'. Compute mean, std, fraction k=0 per image.",
    difficulty="Done -- just aggregate",
    published="Derived -- no direct cell biology reference for this specific formulation"
)

pdf.metric_box(
    name="4. Clustering coefficient (CC)",
    formula=(
        "CC_i = (edges among neighbors of i) / (k_i*(k_i-1)/2). "
        "Mean CC = nx.average_clustering(G). "
        "Compare to CC_rand from configuration model null."
    ),
    interpretation=(
        "High CC: neighbors of each VASA cell are also in contact with each other -> compact local topology. "
        "Low CC: chain-like or tree-like structure. "
        "CC / CC_rand > 1 = more locally clustered than random graph with same degrees."
    ),
    pipeline="Already computed per cell and as mean. Normalize vs configuration model (already implemented).",
    difficulty="Done",
    published="Yes (Tirinato et al. 2023; Watts & Strogatz 1998) -- applied to physical cell contact networks",
    doi="10.1007/s10439-023-03215-z"
)

pdf.metric_box(
    name="5. Characteristic path length (CPL) and graph diameter",
    formula=(
        "CPL = nx.average_shortest_path_length(G) -- only valid if G is connected (check first). "
        "Diameter = max shortest path length. Normalize: CPL_norm = CPL / ln(N_VASA)."
    ),
    interpretation=(
        "Low CPL: cells reachable in few hops = compact. High CPL: long chains. "
        "CPL_norm / CPL_rand < 1 = shorter paths than random -> compact. "
        "If G is disconnected, compute CPL per connected component, report for the LCC."
    ),
    pipeline="Add to computeGraphControl(). Run on LCC only if disconnected. ~5 lines.",
    difficulty="Easy",
    published="Yes (Tirinato et al. 2023; Watts & Strogatz 1998) -- applied to physical cell contact networks",
    doi="10.1007/s10439-023-03215-z"
)

pdf.metric_box(
    name="6. Small-world coefficient (SW)",
    formula=(
        "SW = (CC_obs/CC_rand) / (CPL_obs/CPL_rand). "
        "CC_rand and CPL_rand from configuration model (n=1000 permutations, already implemented). "
        "SW > 1: more clustered AND shorter paths than random = compact / small-world."
    ),
    interpretation=(
        "SW integrates both CC and CPL into one scalar. "
        "Compact ball cluster: SW >> 1 (high CC + low CPL). "
        "Chain/tree: SW < 1 (low CC + high CPL). "
        "Comparable across images with different N_VASA because it is normalized by random graphs."
    ),
    pipeline="Derive from CC_obs, CC_rand, CPL_obs, CPL_rand already computed. ~2 lines.",
    difficulty="Easy -- all inputs already available",
    published="Yes (Watts & Strogatz 1998; Tirinato et al. 2022/2023) -- foundational small-world metric",
    doi="10.1038/30918"
)

pdf.metric_box(
    name="7. Eccentricity distribution and betweenness centrality CV",
    formula=(
        "Eccentricity e_i = max shortest path from i to any other node. "
        "Narrow, low eccentricity distribution -> compact. "
        "Betweenness centrality CV = std(BC)/mean(BC): high CV = few hub cells bridging subclusters."
    ),
    interpretation=(
        "Eccentricity: compact clusters have low max eccentricity (= diameter) and narrow distribution. "
        "Spread chains: high max eccentricity, broad distribution. "
        "High betweenness CV: a few cells act as bridges between subclusters = fragile connectivity."
    ),
    pipeline="nx.eccentricity(G), nx.betweenness_centrality(G). Compute on LCC. Moderate compute for large graphs.",
    difficulty="Easy (add to graph analysis); moderate if graph is large (>500 nodes)",
    published="Derived -- standard graph metrics not yet published for physical cell contact networks in this form"
)

pdf.subsection_title("Group 2: Geometric metrics from centroids")

pdf.metric_box(
    name="8. Radius of gyration (Rg) of centroid cloud",
    formula=(
        "Rg = sqrt(sum(|r_i - r_cm|^2) / N_VASA), where r_cm = centroid of centroids. "
        "Compact = small Rg. Sprawling = large Rg. "
        "Normalize by R_sphere = (3*V_total/(4*pi))^(1/3) to remove N-dependence: Rg / R_sphere."
    ),
    interpretation=(
        "Rg measures how spread out the VASA population is in 3D space. "
        "A perfect solid sphere of N spheres: Rg/R_sphere = 0.775. "
        "A thin shell or elongated cluster: Rg/R_sphere > 0.775. "
        "Rg/R_sphere < 0.775 is not physically possible for a solid object."
    ),
    pipeline="~5 lines: extract centroid columns from counts CSV, compute with NumPy.",
    difficulty="Trivial",
    published="Adapted (Takko et al. 2020) -- applied to per-cell morphometrics; here adapted to centroid cloud",
    doi="10.1016/j.ydbio.2020.01.011"
)

pdf.metric_box(
    name="9. Asphericity / anisotropy (gyration tensor)",
    formula=(
        "Gyration tensor T_ij = (1/N) * sum((r_i - r_cm)_a * (r_i - r_cm)_b). "
        "Eigenvalues lam1 >= lam2 >= lam3. "
        "Asphericity b = lam1 - (lam2+lam3)/2. Acylindricity c = lam2 - lam3. "
        "Shape anisotropy k^2 = (b^2 + 3/4*c^2) / Rg^4: 0 = sphere, 1 = rod."
    ),
    interpretation=(
        "k^2 near 0: the VASA centroid cloud is approximately spherical -> compact isotropic cluster. "
        "k^2 near 1: elongated rod-like arrangement. "
        "b and c together describe whether the shape is prolate (rod) or oblate (disc)."
    ),
    pipeline="~10 lines with numpy.linalg.eigh on the 3x3 gyration tensor.",
    difficulty="Easy",
    published="Derived -- gyration tensor used in polymer physics but not yet published for cell centroid clouds"
)

pdf.metric_box(
    name="10. Convex hull ratio",
    formula=(
        "CHR = sum(cell volumes) / V_convex_hull, "
        "where V_convex_hull = volume of the convex hull of all VASA centroids. "
        "CHR near 1: cells pack the convex hull densely -> compact. "
        "CHR << 1: large empty spaces inside the hull -> hollow / branching / scattered."
    ),
    interpretation=(
        "Directly measures packing efficiency: what fraction of the bounding convex volume is actually occupied by VASA cells? "
        "A solid sphere of identical spheres: CHR ~ 0.64 (random packing). "
        "A shell or ring: CHR << 0.64."
    ),
    pipeline="scipy.spatial.ConvexHull on centroid array. V_cells from per-cell volume column. ~5 lines.",
    difficulty="Easy",
    published="Derived -- no direct published reference for cell cluster packing efficiency in this form"
)

pdf.metric_box(
    name="11. Radial density profile R50 and R90",
    formula=(
        "R50 = radius from centroid of centroids within which 50% of VASA cells fall. "
        "R90 = same for 90%. "
        "Compact cluster: small R50; dispersed: large R50."
    ),
    interpretation=(
        "R50/R_sphere gives a size-normalized version. "
        "Plotting the radial density profile (fraction of cells vs. distance from COM) "
        "reveals whether the cluster is homogeneous or has a dense core + sparse periphery."
    ),
    pipeline="Compute pairwise distances from COM, rank, find percentiles. ~5 lines.",
    difficulty="Trivial",
    published="Derived -- simple percentile metric; no direct published reference"
)

pdf.subsection_title("Group 3: Label image metrics (from merged VASA binary mask)")

pdf.metric_box(
    name="12. Surface-to-volume ratio of merged VASA domain",
    formula=(
        "Merge all VASA labels into binary mask. "
        "S_domain = marching_cubes surface area of merged mask. "
        "V_domain = sum of all VASA cell volumes. "
        "S/V ratio. Isoperimetric ratio: IP = S^3 / (36*pi*V^2); IP=1 for sphere, IP>1 for irregular shapes."
    ),
    interpretation=(
        "Low S/V (IP near 1): compact blob-like VASA domain. "
        "High S/V (IP >> 1): highly convoluted, branching, or scattered domain with many holes. "
        "This is the geometry of the merged VASA territory, not of individual cells."
    ),
    pipeline=(
        "Create binary mask from VASA label image. "
        "Apply skimage.measure.marching_cubes to get S_domain. ~10 lines."
    ),
    difficulty="Easy",
    published="Derived -- isoperimetric ratio concept is standard geometry; not published for VASA-type cell domains"
)

pdf.metric_box(
    name="13. Box-counting fractal dimension (FD) of merged VASA domain",
    formula=(
        "Apply box-counting to 3D binary VASA mask across decreasing box sizes r. "
        "FD = -slope of log(N_occupied(r)) vs log(r). "
        "Solid sphere: FD = 3. Branching/filamentous: FD < 3. Scattered points: FD = 0."
    ),
    interpretation=(
        "FD near 3: VASA domain fills 3D space compactly. "
        "FD ~ 2: VASA cells arranged in sheet-like layers. "
        "FD ~ 1: VASA cells arranged in chain/tube. "
        "FD is scale-invariant: meaningful even if cluster changes size."
    ),
    pipeline=(
        "Implement box-counting on binary 3D array using successive 2x2x2 pooling (downsampling). "
        "~20 lines. Alternatively use existing regionprops + bounding box approach."
    ),
    difficulty="Moderate -- ~1 day to implement and validate",
    published="Yes (Cross 1997; Lennon et al. 2015; Yadav et al. 2024) -- box-counting FD for biological volumes",
    doi="10.1038/nrclinonc.2015.108"
)

pdf.metric_box(
    name="14. Lacunarity L(r) of merged VASA domain",
    formula=(
        "Gliding-box algorithm: slide box of size r through binary 3D mask, "
        "count occupied voxels S in each box position. "
        "L(r) = var(S)/mean(S)^2 + 1. Report L(r) curve or L at a fixed r."
    ),
    interpretation=(
        "L(r) near 1: uniform, gap-free filling (compact). "
        "L(r) >> 1: heterogeneous, gappy distribution (scattered or branching). "
        "Lacunarity is independent of FD and captures a different aspect of spatial texture."
    ),
    pipeline="Implement gliding-box with scipy.ndimage or manual rolling window. ~30 lines. Most effort in this group.",
    difficulty="Moderate -- ~1 day",
    published="Yes (Lennon et al. 2015; Yadav et al. 2024) -- lacunarity for 3D biological volumes",
    doi="10.1038/nrclinonc.2015.108"
)

# ---- A7: CONTROLS -----------------------------------------------------------
pdf.section_title("A7 - Controls and Validation (Part A)")

controls_A = [
    ("Configuration model (graph metrics)",
     "Already implemented (computeGraphControl). Preserves degree sequence, randomizes connections. "
     "n=1000 permutations. Use for CC, CPL, SW. Reports p-value and z-score per metric."),
    ("CSR Monte Carlo (spatial statistics)",
     "Simulate N_VASA points uniformly in tissue bounding volume, n=100 simulations. "
     "Use for Ripley's K/L and PCF g(r). Already implemented in computeRipleysK."),
    ("Sphere reference (geometric metrics)",
     "For Rg, CHR, S/V: compute expected value for a solid sphere of N cells with same mean volume. "
     "Report observed metric as ratio to sphere reference."),
    ("Size normalization",
     "N_VASA affects almost every metric. Always: (a) normalize CPL and diameter by ln(N_VASA); "
     "(b) report N_VASA on every plot; (c) test correlation of metrics with N_VASA across images "
     "and regress it out if significant."),
    ("Tissue volume normalization",
     "Larger ovaries have more space for cells to spread. Normalize Rg, R50, convex hull by "
     "tissue bounding volume or by the equivalent sphere radius R_sphere = (3V/(4pi))^(1/3)."),
    ("Type I error check",
     "Simulate random point patterns with same N and V as real data. "
     "Verify SW ~ 1, L(r)-r ~ 0, FI ~ null, FD ~ expected for random packing. "
     "Confirms metrics are not trivially detecting random structure."),
    ("Biological positive control",
     "A perturbation known to disperse germ cells should increase FI, decrease mean SSR, increase CPL, "
     "decrease L(r)-r. Use this to validate that metrics are biologically sensitive."),
]

for ctrl_name, ctrl_text in controls_A:
    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*BLUE)
    pdf.cell(55, 4, ctrl_name + ":", new_x="RIGHT", new_y="TOP")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 4, ctrl_text, new_x="LMARGIN")
    pdf.ln(1)

# =============================================================================
# PART B
# =============================================================================
pdf.add_page()
pdf.part_banner("B", "FUTURE EXTENSIONS",
    "Requires spatial co-registration of VASA and TJ (or other cell type) segmentations. "
    "Not applicable to current pipeline. Saved here for future reference.",
    current=False)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "These metrics require knowing the spatial position and identity of non-VASA cells (e.g. TJ+ follicle cells) "
    "within the same 3D coordinate space. Currently TJ segmentation is done in a separate channel with no spatial "
    "mapping onto the VASA channel. If in the future a multi-channel pipeline registers both segmentations into a "
    "shared coordinate system, the following metrics become applicable.",
    new_x="LMARGIN")
pdf.ln(3)

# ---- B1: NEIGHBORHOOD ENRICHMENT -------------------------------------------
pdf.section_title("B1 - Neighborhood Enrichment: Homotypic vs. Heterotypic Contact")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "Once TJ cells are spatially mapped, we can build a mixed cell-type contact graph with both VASA and TJ nodes. "
    "This allows measuring how much VASA cells prefer same-type (VASA-VASA) over cross-type (VASA-TJ) contacts. "
    "The surface sharing ratio (SSR) already captures this implicitly -- high SSR means little surface exposed "
    "to non-VASA entities -- but with TJ positions we can compute it explicitly and assign the 'lost' surface.",
    new_x="LMARGIN")
pdf.ln(2)

pdf.paper_entry(
    title="Squidpy: a scalable framework for spatial omics analysis",
    authors_journal="Palla G et al. | Nature Methods 2022",
    pmid="35102346",
    doi="10.1038/s41592-021-01358-2",
    summary=(
        "Python framework for spatial omics including: spatial neighbor graph from segmentation masks, "
        "neighborhood enrichment score (NES) for each cell-type pair, co-occurrence score, Ripley's L. "
        "NES = z-score of same-type contacts vs. 1000 label permutations. "
        "NES heatmap shows which pairs are enriched (clustered) or depleted (mutually excluded)."
    ),
    relevance=(
        "NES answers: do VASA cells contact other VASA cells more than expected if TJ and VASA cells "
        "were randomly shuffled in space (preserving their counts)? "
        "Requires: single contact graph containing both VASA and TJ nodes. "
        "Implementation: Squidpy sq.gr.nhood_enrichment() or replicate permutation logic in NetworkX."
    ),
    display="NES heatmap (VASA x TJ). Per-cell NES painted on spatial map.",
    controls=(
        "1000 label permutations preserving VASA and TJ cell counts. "
        "Report mean and 95% CI of permutation distribution. "
        "Run on simulated random data to verify NES ~ 0 (Type I error check)."
    )
)

pdf.paper_entry(
    title="GraphCompass: spatial metrics for differential analyses of cell organization across conditions",
    authors_journal="Ali M et al. | Bioinformatics 2024",
    pmid="38940138",
    doi="10.1093/bioinformatics/btae242",
    summary=(
        "Extends Squidpy for cross-condition comparison. Adds: per-cell niche composition vectors "
        "(local fraction of each cell type), unsupervised clustering of cells by niche profile, "
        "statistical tests comparing niche metrics across conditions/samples. "
        "Applicable to MIBI-TOF, Visium, Stereo-seq."
    ),
    relevance=(
        "Niche composition per VASA cell: for each VASA cell, compute the fraction of neighbors "
        "that are VASA vs. TJ. Cluster cells by niche profile: 'core VASA' (surrounded mostly by VASA) "
        "vs. 'peripheral VASA' (surrounded mostly by TJ). "
        "GraphCompass provides the cross-condition statistical framework to compare these profiles."
    ),
    display="UMAP of niche vectors. Spatial map coloured by niche cluster. Boxplots per condition.",
    controls="NES permutation test per condition. Batch effect control if multiple images per condition."
)

pdf.paper_entry(
    title="Coordinated Cellular Neighborhoods Orchestrate Antitumoral Immunity at the Colorectal Cancer Invasive Front",
    authors_journal="Schurch CM et al. | Cell 2020",
    pmid="32763154",
    doi="10.1016/j.cell.2020.07.005",
    summary=(
        "CODEX multiplexed imaging (56 markers). Defines 'cellular neighborhoods' (CNs) by k-NN composition clustering. "
        "Reports CN fragmentation (= 1 - N_LCC/N_total per CN, where LCC is the largest spatially contiguous CN patch) "
        "and CN coupling (number of boundaries between two CN types). "
        "High coupling between VASA and TJ CNs = interdigitated; low coupling = sharply segregated."
    ),
    relevance=(
        "CN fragmentation for the VASA-only domain (Part A FI) is already applicable now. "
        "CN coupling between VASA and TJ CNs requires TJ positions: it measures how interleaved the two "
        "cell populations are at their boundary. High coupling = dispersed interleaving; low coupling = sharp boundary."
    ),
    display="CN identity map. Fragmentation bar chart per CN type. CN-CN coupling heatmap.",
    controls="Label permutation null for coupling scores. N_cells per CN as covariate."
)

# ---- B2: LOCAL COMPOSITION --------------------------------------------------
pdf.section_title("B2 - Local Cell-Type Composition and Spatial Mixing")

pdf.paper_entry(
    title="CytoMAP: A Spatial Analysis Toolbox Reveals Features of Myeloid Cell Organization in Lymphoid Tissues",
    authors_journal="Stoltzfus CR et al. | Cell Reports 2020",
    pmid="32320656",
    doi="10.1016/j.celrep.2020.107523",
    summary=(
        "For each cell, computes local cell-type composition within radius r. "
        "Clusters cells by composition vector using SOM/k-means -> 'cellular neighborhoods' (CNs). "
        "Positional correlation: Pearson r between cell-type frequency profiles across tissue positions. "
        "Reveals segregated DC subtypes in murine lymph nodes."
    ),
    relevance=(
        "With TJ positions: local VASA fraction map f_VASA(x,y,z) = fraction of cells within radius r "
        "that are VASA. High f_VASA regions = VASA cluster core; low f_VASA = TJ-dominated. "
        "Bimodal f_VASA distribution = two distinct domains. Unimodal = uniform mixing."
    ),
    display="Spatial map of f_VASA. Histogram of f_VASA. CN identity painted on tissue.",
    controls="Compare f_VASA distribution to label permutation null. Test sensitivity to radius r."
)

pdf.paper_entry(
    title="Extended correlation functions for spatial analysis of multiplex imaging data",
    authors_journal="Bull JA et al. | Biological Imaging 2024",
    pmid="38516631",
    doi="10.1017/S2633903X24000011",
    summary=(
        "Cross-PCF g_AB(r): clustering of cell type B around cell type A at distance r. "
        "Topographical correlation maps (TCM): local cross-PCF per cell, maps where VASA-TJ mixing peaks. "
        "NCF: co-localization of 3+ cell types simultaneously."
    ),
    relevance=(
        "With TJ positions: g_VASA-TJ(r) directly measures VASA-TJ spatial association at scale r. "
        "g > 1 = VASA and TJ tend to be near each other (interleaved). "
        "g < 1 = VASA and TJ are spatially segregated. "
        "TCM maps where VASA-TJ mixing is strongest within the tissue."
    ),
    display="g_VASA-TJ(r) curve with CSR envelope. TCM painted on tissue image.",
    controls="CSR envelope from 100 Monte Carlo simulations with both cell types."
)

# ---- B3: FUTURE METRIC CATALOG ----------------------------------------------
pdf.section_title("B3 - Future Metric Summary (Part B)")

pdf.metric_box(
    name="B1. Neighborhood Enrichment Score (NES) -- VASA-VASA contact enrichment",
    formula=(
        "Build mixed VASA+TJ contact graph. "
        "NES = (n_VASA-VASA_obs - mean(n_VASA-VASA_perm)) / std(n_VASA-VASA_perm), "
        "where permutations shuffle VASA/TJ labels 1000x preserving counts."
    ),
    interpretation=(
        "NES >> 0: VASA cells contact other VASA cells more than expected by chance = clustered. "
        "NES ~ 0: random mixing. NES << 0: VASA cells avoid each other = dispersed. "
        "Comparable across images (z-score normalized for cell count and graph density)."
    ),
    pipeline="Build mixed graph, run permutation loop. Squidpy sq.gr.nhood_enrichment() does this automatically.",
    difficulty="Easy once mixed graph is available",
    future=True,
    published="Yes (Palla et al. 2022) -- NES defined and implemented in Squidpy",
    doi="10.1038/s41592-021-01358-2"
)

pdf.metric_box(
    name="B2. Local VASA fraction map f_VASA(i)",
    formula=(
        "For each VASA cell i, f_VASA(i) = N_VASA within sphere of radius r / N_total within sphere. "
        "r = 3 * mean_cell_diameter. "
        "Requires TJ centroid positions in the same coordinate system as VASA centroids."
    ),
    interpretation=(
        "f_VASA near 1: cell in VASA-dominated region (cluster core). "
        "f_VASA near VASA_fraction_global: random mixing. "
        "Bimodal histogram = distinct core + boundary populations."
    ),
    pipeline="KD-tree on merged VASA+TJ centroid array. Query radius r per cell. ~15 lines.",
    difficulty="Easy once TJ positions are co-registered",
    future=True,
    published="Yes (Stoltzfus et al. 2020) -- local cell-type composition windows in CytoMAP",
    doi="10.1016/j.celrep.2020.107523"
)

pdf.metric_box(
    name="B3. Cross-PCF g_VASA-TJ(r)",
    formula=(
        "g_AB(r) = (observed VASA-TJ pairs at distance r) / (expected from CSR of both cell types). "
        "g > 1 = VASA and TJ tend to co-locate at scale r. g < 1 = they avoid each other."
    ),
    interpretation=(
        "g_VASA-TJ(r) < 1 at all r = VASA and TJ are spatially segregated (what we expect for a compact VASA cluster). "
        "g_VASA-TJ(r) > 1 = interleaved / mixed populations."
    ),
    pipeline="Extend computeRipleysK() to cross-type variant. Or compute directly from pairwise VASA-TJ distances.",
    difficulty="Easy-moderate once TJ positions are co-registered",
    future=True,
    published="Yes (Bull et al. 2024) -- cross-PCF and topographical correlation maps",
    doi="10.1017/S2633903X24000011"
)

pdf.metric_box(
    name="B4. CN coupling between VASA and TJ domains",
    formula=(
        "Count spatial boundary contacts between VASA-labeled and TJ-labeled regions in the merged label image. "
        "Coupling = number of voxel-face contacts between VASA and TJ domains (normalized by perimeter length)."
    ),
    interpretation=(
        "Low coupling = sharp boundary, little interleaving. "
        "High coupling = highly interdigitated VASA-TJ interface = dispersed mixing."
    ),
    pipeline="Requires registered VASA+TJ label images in the same volume. Detect face-adjacency between types.",
    difficulty="Moderate once label images are co-registered",
    future=True,
    published="Yes (Schurch et al. 2020) -- CN coupling between cellular neighborhood types",
    doi="10.1016/j.cell.2020.07.005"
)

# =============================================================================
# COMBINED SUMMARY TABLE
# =============================================================================
pdf.add_page()
pdf.section_title("Complete Summary Table -- All Metrics")

pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(*GRAY)
pdf.multi_cell(0, 4,
    "Blue background = Part A (current). Yellow background = Part B (future, requires TJ co-registration).",
    new_x="LMARGIN")
pdf.ln(2)

W = [42, 22, 22, 22, 16, 32, 34]
pdf.table_row(["Metric", "Group", "Level", "Null", "Effort", "Key source", "Published?"], W, header=True)

# Published? legend:
#   Yes      = metric used in this form in a cited paper for cell populations
#   Adapted  = metric exists in literature but adapted here (different domain or formulation)
#   Derived  = computed from first principles; no direct cited precedent for cell populations

rows_A = [
    ("Surface sharing ratio (mean SSR)", "Contact", "Cell", "sphere packing", "done", "Mukhopadhyay 2019", "Adapted"),
    ("Fragmentation Index (FI)", "Contact", "Topology", "CSR sim.", "trivial", "Schurch 2020", "Yes"),
    ("Fraction isolated (k=0)", "Contact", "Cell", "CSR sim.", "done", "Yan 2019", "Adapted"),
    ("Degree distribution (mean k)", "Contact", "Cell", "config. model", "done", "pipeline", "Derived"),
    ("Clustering coeff. (CC)", "Graph", "Network", "config. model", "done", "Tirinato 2023", "Yes"),
    ("Char. path length (CPL)", "Graph", "Network", "config. model", "easy", "Tirinato 2023", "Yes"),
    ("Small-world coeff. (SW)", "Graph", "Network", "config. model", "easy", "Watts 1998", "Yes"),
    ("Eccentricity distribution", "Graph", "Network", "config. model", "easy", "pipeline", "Adapted"),
    ("Betweenness centrality CV", "Graph", "Network", "config. model", "easy", "pipeline", "Adapted"),
    ("Radius of gyration Rg", "Geometric", "Population", "sphere ref.", "trivial", "Takko 2020", "Adapted"),
    ("Asphericity / anisotropy k2", "Geometric", "Population", "sphere ref.", "easy", "Takko 2020", "Adapted"),
    ("Convex hull ratio (CHR)", "Geometric", "Population", "sphere ref.", "easy", "pipeline", "Derived"),
    ("R50 radial density", "Geometric", "Population", "sphere ref.", "trivial", "pipeline", "Derived"),
    ("Ripley L(r)-r scalar", "Spatial", "Population", "CSR Monte Carlo", "done", "Wilson 2022", "Yes"),
    ("Pair corr. g(r) VASA-VASA", "Spatial", "Population", "CSR Monte Carlo", "easy", "Bull 2024", "Yes"),
    ("Domain S/V (isoperimetric)", "Label image", "Domain", "sphere ref.", "easy", "pipeline", "Derived"),
    ("Box-counting FD", "Label image", "Domain", "rnd. packing ref.", "moderate", "Lennon 2015", "Yes"),
    ("Lacunarity L(r)", "Label image", "Domain", "rnd. packing ref.", "moderate", "Lennon 2015", "Yes"),
]
rows_B = [
    ("Neighborhood Enrichment Score", "Contact", "Population", "label perm.", "easy*", "Palla 2022", "Yes"),
    ("Local VASA fraction f_VASA", "Composition", "Spatial", "label perm.", "easy*", "Stoltzfus 2020", "Yes"),
    ("Cross-PCF g_VASA-TJ(r)", "Spatial", "Population", "CSR Monte Carlo", "easy*", "Bull 2024", "Yes"),
    ("CN coupling VASA-TJ", "Domain", "Topology", "label perm.", "moderate*", "Schurch 2020", "Yes"),
]

for row in rows_A:
    pdf.table_row(list(row), W)
for row in rows_B:
    pdf.table_row(list(row), W, future_row=True)

pdf.set_font("Helvetica", "I", 8)
pdf.set_text_color(*AMBER)
pdf.multi_cell(0, 4, "* Effort once TJ and VASA label images are co-registered into a shared 3D coordinate system.", new_x="LMARGIN")
pdf.set_text_color(*GRAY)
pdf.multi_cell(0, 4,
    "Published? -- Yes: metric used in this form in a cited paper for cell populations. "
    "Adapted: metric exists in literature but applied here to a different domain or in a different formulation. "
    "Derived: computed from first principles; no direct cited precedent for cell populations in this form.",
    new_x="LMARGIN")
pdf.ln(4)

# ---- IMPLEMENTATION PRIORITY ------------------------------------------------
pdf.section_title("Implementation Priority (Part A -- current pipeline)")

priority_steps = [
    ("NOW (done or trivial, <30 min each)",
     "mean SSR per image | FI + N_components | fraction isolated (k=0) | Rg | R50",
     "All these aggregate existing per-cell columns; no new computation needed."),
    ("SHORT TERM (easy, <2h each)",
     "SW (CPL + config model already available) | CHR (scipy ConvexHull) | asphericity (numpy gyration tensor) | g(r) from K(r)",
     "Extend computeGraphControl() for SW. Add geometric metrics as separate analysis function."),
    ("MEDIUM TERM (moderate, 1-2 days each)",
     "Box-counting FD | Lacunarity | Domain S/V (merged mask)",
     "Require binary mask processing. Domain S/V is easiest (marching cubes on merged mask)."),
    ("FUTURE (requires TJ co-registration)",
     "NES | f_VASA map | Cross-PCF VASA-TJ | CN coupling",
     "Requires a pipeline step that places VASA and TJ segmentations into the same 3D coordinate space."),
]

for timing, metrics, note in priority_steps:
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 5, timing, new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 8)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 4, metrics, new_x="LMARGIN")
    pdf.set_font("Helvetica", "I", 8)
    pdf.set_text_color(*GRAY)
    pdf.multi_cell(0, 4, note, new_x="LMARGIN")
    pdf.ln(2)

# ---- REFERENCES -------------------------------------------------------------
pdf.section_title("References (PubMed)")

refs = [
    ("Tirinato L et al.", "2023", "Ann Biomed Eng", "Cancer cell radiation response: 2D cell network topology", "37093401", "10.1007/s10439-023-03215-z"),
    ("Tirinato L et al.", "2022", "Sci Rep", "Lung cancer radioresistance: 2D network topology", "35902618", "10.1038/s41598-022-17018-0"),
    ("Watts DS & Strogatz SH", "1998", "Nature", "Collective dynamics of 'small-world' networks", "9623998", "10.1038/30918"),
    ("Mukhopadhyay S & De R", "2019", "Phys Biol", "Aggregation dynamics: compactness as boundary/total cell ratio", "31042683", "10.1088/1478-3975/ab1e76"),
    ("Lennon FE et al.", "2015", "Nat Rev Clin Oncol", "Lung cancer -- a fractal viewpoint (FD + lacunarity)", "26169924", "10.1038/nrclinonc.2015.108"),
    ("Yadav D et al.", "2024", "NMR Biomed", "3D FD + lacunarity for glioma grade discrimination", "39367752", "10.1002/nbm.5272"),
    ("Cross SS", "1997", "J Pathol", "Fractal analysis: box-counting FD for biological structures", "9227334", "10.1002/(SICI)1096-9896(199707)182:3<371::AID-PATH872>3.0.CO;2-B"),
    ("Takko H et al.", "2020", "Dev Biol", "ShapeMetrics: 3D morphometrics + spatial mapping pipeline", "32061886", "10.1016/j.ydbio.2020.01.011"),
    ("Yan Y et al.", "2019", "PLoS ONE", "Cell aggregate algorithm + cell neighborhood analysis (melanoma)", "31166985", "10.1371/journal.pone.0216485"),
    ("Wilson C et al.", "2022", "PLoS Comput Biol", "Tumor immune cell clustering + Ripley's K with CSR envelope", "35235563", "10.1371/journal.pcbi.1009900"),
    ("Bull JA et al.", "2024", "Biol Imaging", "Extended cross-PCF: topographical correlation maps + NCF", "38516631", "10.1017/S2633903X24000011"),
    ("Palla G et al.", "2022", "Nat Methods", "Squidpy: scalable spatial omics framework with NES", "35102346", "10.1038/s41592-021-01358-2"),
    ("Ali M et al.", "2024", "Bioinformatics", "GraphCompass: cross-condition spatial organization comparison", "38940138", "10.1093/bioinformatics/btae242"),
    ("Schurch CM et al.", "2020", "Cell", "Coordinated cellular neighborhoods (CODEX): CN fragmentation + coupling", "32763154", "10.1016/j.cell.2020.07.005"),
    ("Stoltzfus CR et al.", "2020", "Cell Rep", "CytoMAP: local cell-type composition + positional correlation", "32320656", "10.1016/j.celrep.2020.107523"),
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
