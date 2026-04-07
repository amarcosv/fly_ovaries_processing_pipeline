from fpdf import FPDF
import os

OUTPUT = os.path.join(os.path.dirname(__file__), "literature_review_cluster_compactness.pdf")

BLUE  = (30, 80, 160)
LINK  = (0, 100, 200)
GRAY  = (80, 80, 80)
LGRAY = (230, 230, 230)
LGRAY2= (245, 245, 245)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 110, 60)


class PDF(FPDF):
    def header(self):
        self.set_fill_color(*BLUE)
        self.rect(0, 0, 210, 12, "F")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*WHITE)
        self.set_xy(10, 3)
        self.cell(0, 6, "Literature Review - Quantifying Cluster Compactness vs. Spread in Connected Cell Populations", new_x="RIGHT", new_y="TOP")
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
        # colored header
        self.set_fill_color(*LGRAY2)
        self.set_draw_color(*BLUE)
        self.set_line_width(0.4)
        y0 = self.get_y()
        self.rect(self.l_margin, y0, 190, 4.5, "FD")
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*BLUE)
        self.set_xy(self.l_margin + 2, y0 + 0.5)
        self.cell(0, 3.5, name, new_x="LMARGIN", new_y="NEXT")
        # body
        self._labeled_block("Formula / method", formula)
        self._labeled_block("Interpretation", interpretation)
        self._labeled_block("Pipeline", pipeline)
        self._labeled_block("Effort", difficulty)
        self.ln(2)
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
pdf.multi_cell(0, 7, "Quantifying Cluster Compactness vs. Spread\nin a Connected Cell Population", align="C", new_x="LMARGIN")
pdf.set_font("Helvetica", "", 10)
pdf.set_text_color(*GRAY)
pdf.cell(0, 6, "Literature review for the fly_ovaries_processing_pipeline project", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.cell(0, 6, "PubMed search conducted March 2026", new_x="LMARGIN", new_y="NEXT", align="C")
pdf.ln(4)

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
intro = (
    "This review addresses a specific analytical question: given that all VASA+ germ cells form a single "
    "connected component in the face-adjacency contact graph, how do we quantify whether they aggregate into "
    "a compact sphere-like mass, or whether they are dispersed throughout the tissue volume while maintaining "
    "a connection path between them? "
    "The review covers (1) graph-theoretic topology metrics applied to physical cell contact networks, "
    "(2) fractal dimension and lacunarity as shape descriptors for cell aggregates, and "
    "(3) geometric/spatial metrics derivable from cell centroid coordinates. "
    "For each metric, its interpretation, implementation in the existing pipeline, and required controls are described."
)
pdf.multi_cell(0, 5, intro, new_x="LMARGIN")
pdf.ln(2)

# Biological context box
pdf.set_fill_color(220, 230, 245)
pdf.set_draw_color(*BLUE)
pdf.set_line_width(0.4)
y0 = pdf.get_y()
pdf.rect(pdf.l_margin, y0, 190, 21, "FD")
pdf.set_font("Helvetica", "B", 8)
pdf.set_text_color(*BLUE)
pdf.set_xy(pdf.l_margin + 2, y0 + 1.5)
pdf.cell(0, 4, "Biological question:", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", "", 8)
pdf.set_text_color(*BLACK)
pdf.set_x(pdf.l_margin + 2)
pdf.multi_cell(186, 4,
    "All VASA cells are in one connected component (confirmed by existing pipeline). "
    "But a single connected component can look very different: a dense ball of touching cells (compact) vs. a "
    "branching tree of cells strung together in chains (spread). The metrics below discriminate between these extremes "
    "and provide a scalar per sample for statistical comparison across conditions.",
    new_x="LMARGIN")
pdf.ln(2)
pdf.set_line_width(0.2)

# =============================================================================
pdf.section_title("SECTION 1 - Graph Topology Metrics Applied to Physical Cell Contact Networks")

pdf.paper_entry(
    title="Human Cancer Cell Radiation Response Investigated through Topological Analysis of 2D Cell Networks",
    authors_journal="Tirinato et al. - Annals of Biomedical Engineering 2023",
    pmid="37093401",
    doi="10.1007/s10439-023-03215-z",
    summary=(
        "Subjects 4 human cancer cell lines (H4, H460, PC3, T24) to photon radiation (0-6 Gy) and builds 2D "
        "cell contact graphs from fluorescence images. Computes clustering coefficient (cc), characteristic path "
        "length (cpl), and small-world coefficient (SW = cc/cpl ratio vs. random). "
        "Key result: higher radiation dose -> higher cc + lower cpl, meaning cells cluster tightly and "
        "are closer together in the graph. SW > 1 quantifies departure from random layout."
    ),
    relevance=(
        "MOST DIRECTLY RELEVANT. This is exactly the framework you need: applies graph metrics (cc, cpl, SW) "
        "to a physical cell contact network from microscopy images - the same network your pipeline builds. "
        "cc: how tightly are each cell's neighbors interconnected. "
        "cpl: average shortest path length across all cell pairs. "
        "Compact cluster = high cc + low cpl. Spread chain = low cc + high cpl. "
        "SW coefficient normalizes both relative to a random graph with the same N and degree sequence."
    ),
    display=(
        "Bar charts of cc, cpl, SW per condition with error bars. Scatter plots cc vs. cpl coloring by condition. "
        "Correlation matrix of topology metrics vs. biological parameters."
    ),
    controls=(
        "Null: shuffle cell positions within each sample (preserve N and volume, randomize contacts). "
        "Compare SW to SW_random = 1 by definition. Dose-response curve serves as biological positive control."
    )
)

pdf.paper_entry(
    title="Human lung-cancer-cell radioresistance investigated through 2D network topology",
    authors_journal="Tirinato et al. - Scientific Reports 2022",
    pmid="35902618",
    doi="10.1038/s41598-022-17018-0",
    summary=(
        "Predecessor paper from same group. Applies cc, cpl, and SW to 2D cell networks of H460, A549, Calu-1 lung "
        "cancer lines at 0-8 Gy radiation. Defines SW > 1 as evidence of 'discontinuous and inhomogeneous cell "
        "spatial layout' (spread). Shows that SW is sensitive to radiation dose and cell line radioresistance."
    ),
    relevance=(
        "Demonstrates that the SW coefficient is a sensitive, interpretable scalar for compactness/spread of a "
        "cell population from a 2D contact graph. Provides the methodological detail: graph built from Delaunay "
        "triangulation of cell centroids, edge added if cells are within a proximity threshold. "
        "Your face-adjacency graph is more biologically grounded (cells must physically touch) - a stricter criterion "
        "that should yield more meaningful cc and cpl values."
    ),
    display="SW vs. dose curves per cell line. Heatmap of cc x cpl space per sample.",
    controls=(
        "Random graph with same N and edge count as null. Varying proximity threshold as sensitivity analysis."
    )
)

pdf.paper_entry(
    title="Collective dynamics of 'small-world' networks",
    authors_journal="Watts & Strogatz - Nature 1998",
    pmid="9623998",
    doi="10.1038/30918",
    summary=(
        "Foundational paper defining small-world networks. Regular lattices: high cc, high cpl. "
        "Random graphs: low cc, low cpl. Small-world networks: high cc AND low cpl simultaneously. "
        "The small-world coefficient SW = (cc_obs/cc_rand) / (cpl_obs/cpl_rand) > 1 identifies "
        "small-world topology. Demonstrates in C. elegans neural network, power grid, and actor network."
    ),
    relevance=(
        "Provides the foundational definitions for cc, cpl, and SW. Essential reference when reporting these "
        "metrics. Critically: a compact cell cluster resembles a regular lattice (high cc, moderate cpl); "
        "a spread chain-like cluster resembles a random graph but with lower cc and high cpl. "
        "This paper gives you the vocabulary to interpret your cell network topology."
    ),
    display="The classic cc/cpl vs. rewiring probability plot (Figure 2 of Watts & Strogatz). Adapt for cell data.",
    controls="Compare against equivalent random and regular lattice reference graphs."
)

# =============================================================================
pdf.section_title("SECTION 2 - Fractal Dimension and Lacunarity for Cell Aggregate Geometry")

pdf.paper_entry(
    title="Aggregation dynamics of active cells on non-adhesive substrate",
    authors_journal="Mukhopadhyay & De - Physical Biology 2019",
    pmid="31042683",
    doi="10.1088/1478-3975/ab1e76",
    summary=(
        "Cellular automata model of self-assembling cell aggregates on non-adhesive substrate. "
        "Directly tracks: (1) compactness of aggregates as a scalar over time, defined as ratio of "
        "boundary cells to total cells; (2) fractal dimension of the growing aggregate boundary "
        "by box-counting - D=2 for compact filled disc, D<2 for rough/branching boundary; "
        "(3) cohesive strength (related to edge density in contact graph). "
        "Model captures transition from dispersed single cells to compact tissue structures."
    ),
    relevance=(
        "Directly defines 'compactness' as boundary-to-total-cell ratio for a connected cell aggregate - "
        "directly applicable to your 3D label images. In 3D: compactness = surface cells / total cells "
        "(cells with at least one non-cell neighbor). Compact ball -> small ratio. Spread structure -> large ratio. "
        "Fractal dimension of the outer surface boundary is also computable from your label image."
    ),
    display="Time series of compactness and FD during aggregate growth. Phase diagrams of cohesion vs. compactness.",
    controls="Simulated random aggregate as null. Compactness = 1 for a linear chain (all boundary), <1 for filled sphere."
)

pdf.paper_entry(
    title="Lung cancer - a fractal viewpoint",
    authors_journal="Lennon et al. - Nature Reviews Clinical Oncology 2015",
    pmid="26169924",
    doi="10.1038/nrclinonc.2015.108",
    summary=(
        "Review of fractal dimension (FD) and lacunarity for lung tumor morphology in CT/PET images. "
        "FD (box-counting): measures how a structure fills space across scales. FD=3 for solid sphere, "
        "FD<3 for branching/filamentous. Lacunarity: complementary measure of the 'gappiness' or "
        "texture of spatial distribution - how uniformly cells fill their bounding volume. "
        "High lacunarity = heterogeneous, gappy distribution. Low lacunarity = homogeneous filling."
    ),
    relevance=(
        "Introduces LACUNARITY as a key complement to FD. For a compact cell cluster: low lacunarity "
        "(cells fill space uniformly, few gaps). For a spread cluster: high lacunarity (large gaps between cell chains). "
        "Lacunarity is computed from a gliding-box algorithm on the binary label image - "
        "directly applicable to your 3D VASA label images. The combination FD + lacunarity gives a 2D descriptor space "
        "for cluster morphology that is more informative than either alone."
    ),
    display="FD vs. lacunarity scatter plot per sample, colored by condition. FD + lacunarity together on bivariate plot.",
    controls="Simulated solid sphere (high FD, low lacunarity) vs. random point cloud (low FD, high lacunarity) as reference."
)

pdf.paper_entry(
    title="Fractal dimension and lacunarity measures of glioma subcomponents are discriminative of grade and IDH status",
    authors_journal="Yadav et al. - NMR in Biomedicine 2024",
    pmid="39367752",
    doi="10.1002/nbm.5272",
    summary=(
        "Applies 3D fractal dimension (FD3D) and 3D lacunarity (Lac3D) to glioma subcomponents from MRI. "
        "High-grade gliomas: higher FD (more irregular, complex geometry) + lower lacunarity (denser tumor) "
        "in the enhancing region. IDH-mutant vs. wild-type show distinct FD + lacunarity signatures. "
        "Machine learning on FD3D alone discriminates grade with 97.9% sensitivity."
    ),
    relevance=(
        "Validates the 3D FD + lacunarity framework in volumetric imaging (analogous to your 3D confocal stacks). "
        "Key conceptual point: higher FD = more complex, space-filling (compact); lower FD = simpler, "
        "branching/filamentous (spread). Lower lacunarity = more uniform filling (compact). "
        "Both metrics are calculable from your 3D VASA binary label image using skimage.measure."
    ),
    display="FD3D vs. Lac3D 2D scatter per sample. Box plots of FD3D and Lac3D by condition. ML classifier ROC.",
    controls=(
        "Solid sphere and random point cloud controls. Cross-cohort validation (TCGA + UCSF datasets). "
        "Permutation test on FD values."
    )
)

pdf.paper_entry(
    title="Fractals in pathology",
    authors_journal="Cross - Journal of Pathology 1997",
    pmid="9227334",
    doi="10.1002/(SICI)1096-9896(199705)182:1<1::AID-PATH808>3.0.CO;2-B",
    summary=(
        "Foundational review. Fractal dimension measures 'space-filling properties.' "
        "Box-counting method: cover structure with boxes of side r, count N(r), FD = -log(N(r))/log(r). "
        "Applications: tumor boundary irregularity, vascular branching, neuronal arborization. "
        "Key insight: FD quantifies structural complexity at multiple scales simultaneously."
    ),
    relevance=(
        "Essential methodological reference for box-counting FD. For a 3D cell cluster: "
        "FD=3 means cells fill a 3D volume (compact ball). FD=2 means cells form a sheet-like surface. "
        "FD=1 means cells form a linear chain. Real clusters will fall between these ideals. "
        "The box-counting algorithm is easy to implement on your 3D label image."
    ),
    display="Log-log plot of N(r) vs. r (slope = FD). This is the standard quality-control plot for FD measurement.",
    controls="Measure FD on a simulated solid sphere and on a random walk to bracket the expected range."
)

# =============================================================================
pdf.section_title("SECTION 3 - Geometric Metrics from Cell Centroid Coordinates")

pdf.paper_entry(
    title="Characterization and classification of tumor lesions using fractal-based texture analysis and SVMs in mammograms",
    authors_journal="Guo et al. - International Journal of Computer Assisted Radiology and Surgery 2008",
    pmid="20033598",
    doi="10.1007/s11548-008-0276-8",
    summary=(
        "Compares 5 fractal dimension estimation methods for mammographic mass lesions. "
        "Key finding: FD of mass lesions is significantly LOWER than normal parenchyma (less space-filling). "
        "Lacunarity of mass lesions is HIGHER than normal (more gappy/heterogeneous). "
        "Combining FD + lacunarity yields highest classification performance (AUC = 0.90). "
        "Fractional Brownian motion (FBM) method outperforms standard box-counting for self-affine structures."
    ),
    relevance=(
        "Validates FD + lacunarity as paired descriptors of spatial distribution heterogeneity in biomedical images. "
        "Provides practical guidance: lacunarity as computed by gliding-box algorithm captures gap distribution "
        "at multiple scales. The FBM method may be worth comparing to box-counting for your 3D data."
    ),
    display="ROC curves comparing FD alone vs. FD + lacunarity. Scatter of FD vs. lacunarity per sample group.",
    controls="5-fold cross-validation for classifier. Multiple FD methods compared (sensitivity analysis)."
)

# =============================================================================
pdf.add_page()
pdf.section_title("SECTION 4 - Metric Catalog: What to Compute and How")

intro2 = (
    "The following metrics are ordered from easiest to implement (using existing pipeline code) to most complex. "
    "All can be calculated from data already produced by the pipeline. "
    "Graph metrics require only the NetworkX contact graph. Spatial metrics require cell centroid coordinates. "
    "Fractal metrics require the 3D binary label image of the connected component."
)
pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5, intro2, new_x="LMARGIN")
pdf.ln(3)

# ---- GRAPH METRICS ----------------------------------------------------------
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLUE)
pdf.cell(0, 6, "A.  Graph Topology Metrics (from existing NetworkX contact graph)", new_x="LMARGIN", new_y="NEXT")
pdf.set_draw_color(*BLUE)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 190, pdf.get_y())
pdf.ln(3)

pdf.metric_box(
    name="Characteristic Path Length (CPL) - Average shortest path",
    formula="CPL = mean of all pairwise shortest paths: (1/n(n-1)) * sum_uv d(u,v). nx.average_shortest_path_length(G).",
    interpretation=(
        "Compact ball: small CPL (cells across the cluster are few hops apart). "
        "Chain / branching: large CPL. Single number per sample -> directly comparable across conditions."
    ),
    pipeline="Requires connected component (already verified). Add to neighbor_summary CSV. O(n^3) runtime.",
    difficulty="Easy - one NetworkX call. Slow for N > 2000; use nx.single_source_shortest_path_length with sampling."
)

pdf.metric_box(
    name="Graph Diameter",
    formula="Diameter = max of all pairwise shortest paths: max_uv d(u,v). nx.diameter(G).",
    interpretation=(
        "The longest 'shortest journey' between any two cells. Compact = small diameter. "
        "A linear chain of N cells has diameter N-1. A complete graph has diameter 1."
    ),
    pipeline="Add to neighbor_summary CSV alongside CPL.",
    difficulty="Easy - one NetworkX call. Same runtime concern as CPL."
)

pdf.metric_box(
    name="Small-World Coefficient (SW)",
    formula=(
        "SW = (CC_obs / CC_rand) / (CPL_obs / CPL_rand). "
        "CC_rand = 2*E / (N*(N-1)) (expected for random graph). CPL_rand = ln(N) / ln(mean_degree). "
        "SW > 1: more clustered + shorter paths than random -> compact/small-world. "
        "SW < 1: less clustered + longer paths than random -> spread/chain-like."
    ),
    interpretation=(
        "Normalizes CC and CPL relative to a random graph with the same N and edge count. "
        "SW > 1 is the fingerprint of a compact, locally well-connected cluster. "
        "SW < 1 means cells form long chains with few redundant connections (spread)."
    ),
    pipeline=(
        "CC already computed. Add CPL. Compute random graph references analytically or via "
        "nx.erdos_renyi_graph(N, p) with p = 2E/(N*(N-1)). Compute SW per sample."
    ),
    difficulty="Easy once CPL is added. Reference values can be computed analytically."
)

pdf.metric_box(
    name="Graph Eccentricity Distribution",
    formula=(
        "Eccentricity of node u = max_v d(u,v). nx.eccentricity(G). "
        "Summary stats: mean eccentricity, radius = min(eccentricity), diameter = max(eccentricity)."
    ),
    interpretation=(
        "Peripheral cells (far from the cluster center) have high eccentricity. "
        "Compact cluster: narrow eccentricity distribution (all cells are similarly central). "
        "Spread structure: wide distribution with a few very peripheral cells."
    ),
    pipeline="Use nx.eccentricity() - returns per-cell values. Map onto label image with paintLabelsByMetric.",
    difficulty="Easy - already have the graph. Visualize as per-cell heatmap (eccentricity-painted labels)."
)

pdf.metric_box(
    name="Betweenness Centrality Distribution",
    formula=(
        "BC(v) = fraction of all shortest paths that pass through node v. "
        "nx.betweenness_centrality(G, normalized=True)."
    ),
    interpretation=(
        "In a chain-like cluster, a few bridge nodes have very high BC (bottlenecks). "
        "In a compact cluster, BC is low and uniformly distributed. "
        "Gini coefficient or coefficient of variation of BC distribution = single scalar for inequality."
    ),
    pipeline="Map BC onto label image to visualize bridge cells. Compute CV(BC) as compactness proxy.",
    difficulty="Moderate - O(n^3). For large graphs use approximation: nx.betweenness_centrality(G, k=100)."
)

# ---- SPATIAL GEOMETRY -------------------------------------------------------
pdf.ln(2)
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLUE)
pdf.cell(0, 6, "B.  Spatial Geometry Metrics (from cell centroid coordinates)", new_x="LMARGIN", new_y="NEXT")
pdf.set_draw_color(*BLUE)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 190, pdf.get_y())
pdf.ln(3)

pdf.metric_box(
    name="Radius of Gyration (Rg)",
    formula=(
        "Rg = sqrt( mean_i |r_i - r_cm|^2 ), where r_cm = mean centroid of all cells. "
        "np.sqrt(np.mean(np.sum((centroids - centroid_mean)**2, axis=1)))."
    ),
    interpretation=(
        "Mean RMS distance of cells from the cluster center of mass. "
        "Compact sphere: small Rg. Spread structure: large Rg. "
        "Normalize by expected Rg for a uniform sphere of same N and cell volume -> dimensionless index."
    ),
    pipeline="Cell centroids already in regionprops output. One line of numpy. Add to neighbor_summary CSV.",
    difficulty="Trivial - pure numpy."
)

pdf.metric_box(
    name="Asphericity / Anisotropy (from gyration tensor)",
    formula=(
        "Build gyration tensor T_ab = (1/N) sum_i (r_ia - r_a_cm)(r_ib - r_b_cm). "
        "Eigenvalues l1 >= l2 >= l3. "
        "Asphericity = l1 - (l2+l3)/2. Anisotropy = (l1-l3)/(l1+l2+l3). "
        "np.linalg.eigh(gyration_tensor)."
    ),
    interpretation=(
        "l1 = l2 = l3: perfect sphere (compact). l1 >> l2, l3: elongated cigar (spread in one direction). "
        "l1 = l2 >> l3: flat disc. Asphericity = 0 for sphere, > 0 for elongated/flat. "
        "These metrics detect directionality of spreading, not just total spread."
    ),
    pipeline="Add after centroid extraction. Yields 3 scalars: asphericity, anisotropy, shape parameter.",
    difficulty="Easy - 10 lines of numpy."
)

pdf.metric_box(
    name="Convex Hull Volume Ratio",
    formula=(
        "Convex hull of all cell centroids: from scipy.spatial import ConvexHull; hull = ConvexHull(centroids). "
        "Ratio = sum(cell_volumes) / hull.volume."
    ),
    interpretation=(
        "Fraction of the convex hull volume actually occupied by cells. "
        "Compact sphere: ratio near 1 (cells fill the hull). "
        "Spread branching structure: ratio near 0 (large empty hull volume with sparse cells inside)."
    ),
    pipeline="Cell centroids and volumes from regionprops. scipy.spatial.ConvexHull available in environment.",
    difficulty="Easy. Note: ConvexHull degenerates for collinear/coplanar sets - add jitter guard."
)

pdf.metric_box(
    name="Radial Cell Density Profile",
    formula=(
        "Compute distances of all cell centroids from cluster centroid. "
        "Bin by radial distance (e.g. 2 um bins) -> N(r) per bin. "
        "Normalize by shell volume (4 pi r^2 dr) -> local density rho(r)."
    ),
    interpretation=(
        "Compact spherical cluster: rho(r) peaks near r=0 then drops to zero at the cluster edge. "
        "Spread cluster: rho(r) is flatter, or peaks at a non-zero r (ring-like), or has a long tail. "
        "Full profile per sample -> scalar summary: e.g., half-radius R50 (radius containing 50% of cells)."
    ),
    pipeline="Pure numpy/scipy. Produces a curve analogous to Ripley's K but for own-cluster density.",
    difficulty="Easy. R50, R80 are compact scalars for statistical comparison across conditions."
)

# ---- FRACTAL METRICS --------------------------------------------------------
pdf.add_page()
pdf.set_font("Helvetica", "B", 10)
pdf.set_text_color(*BLUE)
pdf.cell(0, 6, "C.  Fractal Dimension and Lacunarity (from 3D binary label image)", new_x="LMARGIN", new_y="NEXT")
pdf.set_draw_color(*BLUE)
pdf.line(pdf.l_margin, pdf.get_y(), pdf.l_margin + 190, pdf.get_y())
pdf.ln(3)

pdf.metric_box(
    name="3D Box-Counting Fractal Dimension (FD)",
    formula=(
        "Binarize 3D VASA label image to 1=cell, 0=background. "
        "Cover with boxes of side r (e.g. r = 2, 4, 8, 16, 32 voxels). "
        "Count N(r) = number of boxes containing at least one cell voxel. "
        "FD = -slope of log(N(r)) vs. log(r). "
        "skimage.measure provides tools; custom box-counting ~20 lines."
    ),
    interpretation=(
        "FD = 3: cells fill a solid 3D volume (maximally compact). "
        "FD ~ 2: cells form a shell or surface (hollow ball or flat sheet). "
        "FD ~ 1: cells form a linear chain (maximally spread). "
        "Real clusters: FD between 2 and 3. Higher = more compact."
    ),
    pipeline=(
        "Applies to the 3D VASA refined label image (_refined.tif), binarized. "
        "Isotropic resampling first (already done at 0.25 um isotropic in the pipeline). "
        "Log-log linearity check (R^2 > 0.99) required for valid FD."
    ),
    difficulty="Moderate - implement box-counting loop (20-30 lines). Add FD and R^2 to summary CSV."
)

pdf.metric_box(
    name="Lacunarity",
    formula=(
        "Gliding-box algorithm: slide a box of side r through the 3D binary image. "
        "For each position, count S = sum of occupied voxels in box (0 to r^3). "
        "Compute Q(S,r) = probability distribution of S. "
        "Lacunarity L(r) = E[S^2] / E[S]^2 = (mean(S^2)) / (mean(S))^2. "
        "Average L(r) across scales for a scalar summary."
    ),
    interpretation=(
        "L(r) = 1: cells are uniformly distributed (translationally invariant). "
        "L(r) > 1: heterogeneous, gappy distribution. "
        "Compact cluster: low lacunarity (cells fill boxes uniformly). "
        "Spread cluster: high lacunarity (many empty boxes, some dense boxes). "
        "L(r) is scale-dependent -> plot L vs. r for full characterization."
    ),
    pipeline=(
        "Implement gliding-box on 3D binary label. Can subsample volume for speed. "
        "Scalar summary: mean L over a biologically relevant range of r (e.g. 2-20 um)."
    ),
    difficulty="Moderate. The 3D gliding-box is O(n^3 * n_scales). Use stride > 1 for speed."
)

pdf.metric_box(
    name="Surface-to-Volume Ratio of the Connected Component",
    formula=(
        "Already computed per cell: surface area and volume from marching cubes (skimage). "
        "For the WHOLE connected component: sum of exposed surface (faces not shared with another VASA cell) "
        "divided by total cell volume. "
        "Equivalently: surface_area_component / volume_component."
    ),
    interpretation=(
        "Compact sphere: S/V = 4pi*r^2 / (4/3 pi r^3) = 3/r (minimal S/V for given volume). "
        "Spread structure: S/V is much larger (more exposed surface per unit volume). "
        "S/V ~ compactness in 3D - directly related to Mukhopadhyay's 'boundary cell ratio' metric."
    ),
    pipeline=(
        "Largely already computed per cell. Aggregate to whole-component: "
        "S_component = sum of per-cell faces NOT shared with another VASA cell (external faces only). "
        "V_component = sum of all VASA cell volumes."
    ),
    difficulty="Easy - extend existing regionprops extraction. One nested loop over face-adjacency graph."
)

# =============================================================================
pdf.add_page()
pdf.section_title("SECTION 5 - Summary Comparison Table")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "Summary of all metrics, ordered by implementation effort. "
    "All can be added to the existing spatial analysis pipeline with minimal refactoring.",
    new_x="LMARGIN")
pdf.ln(2)

headers = ["Metric", "Compact value", "Spread value", "Data needed", "Effort"]
widths  = [40, 30, 30, 50, 40]
pdf.table_row(headers, widths, header=True)
rows = [
    ("Graph diameter",
     "Small (few hops)",
     "Large (many hops)",
     "Contact graph (G)",
     "Easy - nx.diameter(G)"),
    ("Char. path length (CPL)",
     "Low",
     "High",
     "Contact graph (G)",
     "Easy - nx.avg_shortest_path_length"),
    ("Small-world coeff. (SW)",
     "SW > 1",
     "SW < 1",
     "G + degree sequence",
     "Easy - formula after CPL"),
    ("Eccentricity\ndistribution",
     "Narrow, low mean",
     "Wide, high mean",
     "Contact graph (G)",
     "Easy - nx.eccentricity"),
    ("Betweenness centrality\nCV",
     "Low CV (uniform)",
     "High CV (bottlenecks)",
     "Contact graph (G)",
     "Moderate - O(n^3)"),
    ("Radius of gyration (Rg)",
     "Small",
     "Large",
     "Centroids (regionprops)",
     "Trivial - numpy"),
    ("Asphericity / anisotropy",
     "Near 0",
     "Large",
     "Centroids",
     "Easy - numpy.linalg"),
    ("Convex hull ratio",
     "Near 1.0",
     "Near 0",
     "Centroids + volumes",
     "Easy - scipy.spatial"),
    ("Radial density R50",
     "Small",
     "Large",
     "Centroids",
     "Easy - numpy"),
    ("Surface/volume ratio",
     "Low (3/r for sphere)",
     "High",
     "Label image + adjacency",
     "Moderate - extend existing"),
    ("Box-counting FD",
     "Near 3.0",
     "Near 1-2",
     "3D binary label",
     "Moderate - implement loop"),
    ("Lacunarity L(r)",
     "Low (near 1)",
     "High (>1)",
     "3D binary label",
     "Moderate - gliding box"),
]
for row in rows:
    pdf.table_row(row, widths)

# =============================================================================
pdf.ln(6)
pdf.section_title("SECTION 6 - Recommended Implementation Order and Controls")

pdf.set_font("Helvetica", "", 9)
pdf.set_text_color(*BLACK)
pdf.multi_cell(0, 5,
    "Recommended order: start with graph metrics (already have the graph) + geometric metrics "
    "(already have centroids). Add fractal metrics last. Use multiple metrics together - they capture "
    "different aspects of compactness.",
    new_x="LMARGIN")
pdf.ln(3)

steps = [
    ("Step 1 (immediate): Add CPL + diameter to existing pipeline",
     "In analyzeVASANeighbors(), after graph construction: add nx.average_shortest_path_length(G) and "
     "nx.diameter(G) to the summary dict. Also add SW = (cc_mean/cc_rand) / (cpl/cpl_rand) where "
     "cc_rand = 2*E/(N*(N-1)) and cpl_rand = ln(N)/ln(k_mean). Zero additional dependencies."),
    ("Step 2 (easy): Add geometric metrics from centroids",
     "From regionprops (already available): extract centroid array. Compute Rg, gyration tensor eigenvalues "
     "(asphericity, anisotropy), convex hull ratio (scipy.spatial.ConvexHull), radial density profile and R50. "
     "Add all to neighbor_summary CSV."),
    ("Step 3 (moderate): Add eccentricity + betweenness centrality",
     "nx.eccentricity(G) and nx.betweenness_centrality(G). Use paintLabelsByMetric to visualize "
     "eccentricity and BC per cell - highlights peripheral and bridge cells visually. "
     "For large N, use approximated betweenness (k=100 sampling)."),
    ("Step 4 (moderate): Add surface/volume ratio for whole component",
     "Extend processVASASegmentationMasks: identify 'external' cell faces (faces bordering background or "
     "TJ cells, not shared VASA-VASA faces). S_external = sum of exposed face areas. "
     "S/V_component = S_external / sum(cell_volumes). Already have per-cell surfaces from marching cubes."),
    ("Step 5 (project): Box-counting FD + lacunarity",
     "Implement on the 3D refined label image. Binarize, run box-counting at 6-8 scales, "
     "fit log-log line. Run gliding-box lacunarity at same scales. "
     "Add FD, L_mean, and log-log R^2 (quality flag) to summary CSV."),
]
for title, body in steps:
    pdf.set_fill_color(*LGRAY)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*BLUE)
    pdf.cell(0, 5, f"  {title}", new_x="LMARGIN", new_y="NEXT", fill=True)
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*BLACK)
    pdf.set_x(pdf.l_margin + 4)
    pdf.multi_cell(0, 4.5, body, new_x="LMARGIN")
    pdf.ln(2)

pdf.ln(2)
controls_title = "Critical controls for compactness metrics"
pdf.set_fill_color(*LGRAY)
pdf.set_font("Helvetica", "B", 9)
pdf.set_text_color(*BLUE)
pdf.cell(0, 5, f"  {controls_title}", new_x="LMARGIN", new_y="NEXT", fill=True)
pdf.ln(2)

controls_list = [
    ("Cell number (N) as covariate",
     "All graph metrics (CPL, diameter, SW) depend on N. Larger clusters mechanically have larger diameter. "
     "Always report N alongside topology metrics. If comparing conditions with different N, "
     "normalize or correct for N: e.g., CPL / ln(N) removes the baseline N-dependence."),
    ("Cell density as covariate",
     "In denser tissue, cells are mechanically forced to touch more neighbors, increasing CC and decreasing CPL. "
     "Report mean_degree alongside CC and CPL."),
    ("Null model - configuration model",
     "Your pipeline already implements configuration model permutations for CC. Extend to also "
     "permute for CPL and SW: build 1000 random graphs preserving degree sequence, compute CPL_null distribution, "
     "test whether observed CPL is outside the null envelope."),
    ("Null model - random spatial placement",
     "For geometric metrics (Rg, S/V, FD, lacunarity): place N cells randomly in the same bounding volume. "
     "This gives the expected values for a completely dispersed cluster and defines the 'maximally spread' reference."),
    ("Geometric shape of the tissue as reference",
     "The overall ovary geometry constrains how spread the cell population can be. "
     "Normalize Rg and convex hull ratio by the tissue bounding volume or convex hull."),
]
for title, body in controls_list:
    pdf.set_font("Helvetica", "B", 8.5)
    pdf.set_text_color(*BLUE)
    pdf.set_x(pdf.l_margin + 4)
    pdf.write(4.5, f"* {title}: ")
    pdf.set_font("Helvetica", "", 8.5)
    pdf.set_text_color(*BLACK)
    pdf.multi_cell(0, 4.5, body, new_x="LMARGIN")
    pdf.ln(1)

# =============================================================================
pdf.add_page()
pdf.section_title("Reference List")

refs = [
    ("Tirinato L et al.", "2023",
     "Human Cancer Cell Radiation Response Investigated through Topological Analysis of 2D Cell Networks.",
     "Annals of Biomedical Engineering 51(8):1859-1871",
     "10.1007/s10439-023-03215-z", "37093401"),
    ("Tirinato L et al.", "2022",
     "Human lung-cancer-cell radioresistance investigated through 2D network topology.",
     "Scientific Reports 12(1):12980",
     "10.1038/s41598-022-17018-0", "35902618"),
    ("Watts DJ & Strogatz SH", "1998",
     "Collective dynamics of 'small-world' networks.",
     "Nature 393(6684):440-442",
     "10.1038/30918", "9623998"),
    ("Mukhopadhyay D & De R", "2019",
     "Aggregation dynamics of active cells on non-adhesive substrate.",
     "Physical Biology 16(4):046006",
     "10.1088/1478-3975/ab1e76", "31042683"),
    ("Lennon FE et al.", "2015",
     "Lung cancer - a fractal viewpoint.",
     "Nature Reviews Clinical Oncology 12(11):664-675",
     "10.1038/nrclinonc.2015.108", "26169924"),
    ("Yadav N et al.", "2024",
     "Fractal dimension and lacunarity measures of glioma subcomponents are discriminative of grade and IDH status.",
     "NMR in Biomedicine 37(12):e5272",
     "10.1002/nbm.5272", "39367752"),
    ("Cross SS", "1997",
     "Fractals in pathology.",
     "Journal of Pathology 182(1):1-8",
     "10.1002/(SICI)1096-9896(199705)182:1<1::AID-PATH808>3.0.CO;2-B", "9227334"),
    ("Guo Q et al.", "2008",
     "Characterization and classification of tumor lesions using computerized fractal-based texture analysis "
     "and support vector machines in digital mammograms.",
     "International Journal of Computer Assisted Radiology and Surgery 4(1):11-25",
     "10.1007/s11548-008-0276-8", "20033598"),
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
