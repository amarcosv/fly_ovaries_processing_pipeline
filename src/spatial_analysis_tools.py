import os
import numpy as np
import pandas as pd
import networkx as nx
from skimage import measure
from scipy.spatial.distance import pdist


def analyzeVASANeighbors(label_image, noise_threshold=5, px_size=None):
    """
    1. Finds contact areas between cells using face-adjacency (pad + shift).
    2. Filters out small contacts (noise).
    3. Builds a weighted NetworkX graph.
    4. Returns per-cell metrics DataFrame, graph, and summary dict.
    """

    # --- STEP 1: Setup ---
    label_image = np.asarray(label_image)
    all_cells = np.unique(label_image[label_image > 0])

    if px_size is not None:
        pz, py, pxl = float(px_size[0]), float(px_size[1]), float(px_size[2])
        face_areas = {0: py * pxl, 1: pz * pxl, 2: pz * py}
        voxel_volume = pz * py * pxl
    else:
        pz, py, pxl = 1.0, 1.0, 1.0
        face_areas = {0: 1.0, 1: 1.0, 2: 1.0}
        voxel_volume = 1.0

    # --- STEP 2: Find Neighbor Pairs (Pad + Shift Method) ---
    padded = np.pad(label_image, pad_width=1, mode='constant', constant_values=0)

    edge_list = []
    for axis in range(3):
        sl_left = [slice(None)] * 3
        sl_right = [slice(None)] * 3
        sl_left[axis] = slice(0, -1)
        sl_right[axis] = slice(1, None)

        left = padded[tuple(sl_left)]
        right = padded[tuple(sl_right)]

        mask = (left != right)
        u = left[mask]
        v = right[mask]

        edge_list.append(pd.DataFrame({
            'cell_id': np.minimum(u, v),
            'neighbor_id': np.maximum(u, v),
            'face_area': face_areas[axis]
        }))

    all_pairs = pd.concat(edge_list, ignore_index=True)

    # Groupby to get contact area for every pair
    contact_counts = all_pairs.groupby(['cell_id', 'neighbor_id']).agg(
        surface_area=('face_area', 'sum'),
        n_faces=('face_area', 'count')
    ).reset_index()

    # --- STEP 3: Separate Vasa vs Non-Vasa Contacts ---
    non_vasa_df = contact_counts[contact_counts['cell_id'] == 0].set_index('neighbor_id')['surface_area']

    vasa_contacts = contact_counts[
        (contact_counts['cell_id'] > 0) &
        (contact_counts['n_faces'] >= noise_threshold)
    ]

    # --- STEP 4: Build Graph for Connectivity ---
    G = nx.from_pandas_edgelist(vasa_contacts, 'cell_id', 'neighbor_id',
                                 edge_attr='surface_area')
    G.add_nodes_from(all_cells)
    # Rename edge attribute to 'weight' for NetworkX compatibility
    nx.set_edge_attributes(G, {(u, v): d['surface_area'] for u, v, d in G.edges(data=True)}, 'weight')

    # --- STEP 5: Get Centroids and Volumes ---
    props = measure.regionprops_table(label_image, properties=['label', 'centroid', 'area'])
    rp_df = pd.DataFrame(props)
    rp_df.columns = ['label', 'centroid_z', 'centroid_y', 'centroid_x', 'area_vox']
    rp_df = rp_df.set_index('label')
    rp_df['volume_um3'] = rp_df['area_vox'] * voxel_volume
    rp_df['equivalent_diameter_um'] = (6.0 * rp_df['volume_um3'] / np.pi) ** (1.0 / 3.0)

    # --- STEP 6: Compile Final Metrics Table ---
    results = []
    for cell in all_cells:
        # Vasa surface
        this_cell_contacts = vasa_contacts[
            (vasa_contacts['cell_id'] == cell) | (vasa_contacts['neighbor_id'] == cell)
        ]
        vasa_surf = this_cell_contacts['surface_area'].sum()

        # Non-Vasa surface
        non_vasa_surf = non_vasa_df.get(cell, 0)

        # Graph metrics
        if cell in G:
            neighbors = G.degree(cell)
            cluster = nx.node_connected_component(G, cell)
            cluster_size = len(cluster)
        else:
            neighbors = 0
            cluster_size = 1

        # Clustering coefficient
        cc = nx.clustering(G, cell) if cell in G else 0.0

        # Boundary ratio
        total_surf = vasa_surf + non_vasa_surf
        shared_ratio = vasa_surf / total_surf if total_surf > 0 else 0

        # Centroid and volume
        cz = rp_df.loc[cell, 'centroid_z'] if cell in rp_df.index else 0.0
        cy = rp_df.loc[cell, 'centroid_y'] if cell in rp_df.index else 0.0
        cx = rp_df.loc[cell, 'centroid_x'] if cell in rp_df.index else 0.0
        vol_um3 = rp_df.loc[cell, 'volume_um3'] if cell in rp_df.index else 0.0
        diam_um = rp_df.loc[cell, 'equivalent_diameter_um'] if cell in rp_df.index else 0.0

        results.append({
            'label': cell,
            'centroid_z': cz,
            'centroid_y': cy,
            'centroid_x': cx,
            'volume_um3': vol_um3,
            'equivalent_diameter_um': diam_um,
            'vasa_neighbors': neighbors,
            'cluster_size': cluster_size,
            'vasa_surface': vasa_surf,
            'non_vasa_surface': non_vasa_surf,
            'total_surface': total_surf,
            'shared_boundary_ratio': shared_ratio,
            'clustering_coeff': cc,
        })

    cell_metrics = pd.DataFrame(results)

    # --- STEP 7: Summary ---
    all_components = list(nx.connected_components(G))
    component_sizes = sorted([len(c) for c in all_components], reverse=True)
    lcc_size = component_sizes[0] if component_sizes else 0
    n_components = len(all_components)
    n_cells = len(all_cells)
    n_isolated = int((cell_metrics['vasa_neighbors'] == 0).sum())

    # Degree distribution
    degrees = np.array([G.degree(c) for c in all_cells])
    mean_k = float(np.mean(degrees))
    std_k = float(np.std(degrees))

    # Clustering coefficient — exclude cells where CC is mathematically undefined (degree < 2)
    cc_vals = cell_metrics['clustering_coeff'].values
    deg_vals = cell_metrics['vasa_neighbors'].values
    defined_mask = deg_vals >= 2
    mean_CC_defined = float(np.mean(cc_vals[defined_mask])) if defined_mask.any() else float('nan')
    frac_CC_undefined = float(np.sum(~defined_mask) / n_cells) if n_cells > 0 else float('nan')

    # Volume and diameter
    mean_volume_um3 = float(cell_metrics['volume_um3'].mean()) if n_cells > 0 else 0.0
    mean_diameter_um = float(cell_metrics['equivalent_diameter_um'].mean()) if n_cells > 0 else 0.0

    summary = {
        'n_cells': n_cells,
        'n_components': n_components,
        'n_clusters': n_components,          # backward-compat alias
        'lcc_size': lcc_size,
        'fragmentation_index': 1.0 - lcc_size / n_cells if n_cells > 0 else float('nan'),
        'component_sizes': component_sizes,   # list; serialized to percentiles on export
        'mean_cluster_size': float(np.mean(component_sizes)) if component_sizes else 1.0,
        'median_cluster_size': float(np.median(component_sizes)) if component_sizes else 1.0,
        'n_isolated_cells': n_isolated,
        'frac_isolated': float(n_isolated / n_cells) if n_cells > 0 else float('nan'),
        'mean_k': mean_k,
        'std_k': std_k,
        'mean_CC_defined': mean_CC_defined,
        'frac_CC_undefined': frac_CC_undefined,
        'mean_volume_um3': mean_volume_um3,
        'mean_diameter_um': mean_diameter_um,
    }

    print(f'[analyzeVASANeighbors] {n_cells} cells, '
          f'{n_components} components (LCC={lcc_size}), '
          f'{n_isolated} isolated, FI={summary["fragmentation_index"]:.3f}')

    return cell_metrics, G, summary


def computeGraphControl(G, n_iterations=1000):
    """
    Test whether the observed graph topology is non-random using the
    configuration model (preserves degree sequence, randomizes connections).

    CPL is computed on the LCC of both the observed and each random graph
    (the configuration model can produce disconnected graphs).

    Parameters
    ----------
    G : networkx.Graph
        Weighted graph from analyzeVASANeighbors.
    n_iterations : int, optional
        Number of random graph realizations. Default is 1000.

    Returns
    -------
    control_results : dict
        'observed' : dict of metric_name -> observed value
        'null_distributions' : dict of metric_name -> numpy array of null values
        'p_values' : dict of metric_name -> one-sided p-value
    """
    import warnings

    n_cells = len(G)
    if n_cells > 300:
        warnings.warn(
            f'[computeGraphControl] N={n_cells} > 300: CPL computation may be slow. '
            'Consider reducing n_iterations.',
            RuntimeWarning
        )

    degree_seq = [d for _, d in G.degree()]

    # LCC of observed graph
    lcc_nodes = max(nx.connected_components(G), key=len)
    G_lcc = G.subgraph(lcc_nodes)
    N_lcc = len(G_lcc)

    # Observed metrics
    cc_obs = nx.average_clustering(G)
    cpl_obs = nx.average_shortest_path_length(G_lcc) if N_lcc > 1 else float('nan')
    cpl_norm_obs = cpl_obs / np.log(N_lcc) if N_lcc > 1 else float('nan')

    observed = {
        'mean_clustering': cc_obs,
        'n_components': nx.number_connected_components(G),
        'largest_component': N_lcc,
        'cpl': cpl_obs,
        'cpl_norm': cpl_norm_obs,
    }

    null_keys = ['mean_clustering', 'n_components', 'largest_component', 'cpl', 'cpl_norm']
    null_dists = {k: np.zeros(n_iterations) for k in null_keys}

    for i in range(n_iterations):
        # Configuration model: random multigraph with same degree sequence
        R = nx.configuration_model(degree_seq)
        R = nx.Graph(R)
        R.remove_edges_from(nx.selfloop_edges(R))

        null_dists['mean_clustering'][i] = nx.average_clustering(R)
        null_dists['n_components'][i] = nx.number_connected_components(R)

        r_lcc_nodes = max(nx.connected_components(R), key=len)
        R_lcc = R.subgraph(r_lcc_nodes)
        N_r_lcc = len(R_lcc)
        null_dists['largest_component'][i] = N_r_lcc

        cpl_r = nx.average_shortest_path_length(R_lcc) if N_r_lcc > 1 else float('nan')
        null_dists['cpl'][i] = cpl_r
        null_dists['cpl_norm'][i] = cpl_r / np.log(N_r_lcc) if N_r_lcc > 1 else float('nan')

    # Small-world coefficient: SW = (CC_obs / CC_rand_mean) / (CPL_obs / CPL_rand_mean)
    cc_rand_mean = float(np.mean(null_dists['mean_clustering']))
    cpl_rand_mean = float(np.nanmean(null_dists['cpl']))
    if cc_rand_mean > 0 and cpl_rand_mean > 0 and not np.isnan(cpl_obs):
        sw = (cc_obs / cc_rand_mean) / (cpl_obs / cpl_rand_mean)
    else:
        sw = float('nan')
    observed['sw'] = sw

    # p-values (one-sided)
    # Higher CC = more clustered → p = fraction of null >= observed
    # Lower CPL = more compact → p = fraction of null <= observed
    p_values = {
        'mean_clustering': float(np.mean(null_dists['mean_clustering'] >= cc_obs)),
        'n_components': float(np.mean(null_dists['n_components'] >= observed['n_components'])),
        'largest_component': float(np.mean(null_dists['largest_component'] >= observed['largest_component'])),
        'cpl': float(np.nanmean(null_dists['cpl'] <= cpl_obs)),
        'cpl_norm': float(np.nanmean(null_dists['cpl_norm'] <= cpl_norm_obs)),
    }

    print(f'[computeGraphControl] p-values: ' +
          ', '.join(f'{k}={v:.4f}' for k, v in p_values.items()) +
          f'  SW={sw:.3f}')

    return {
        'observed': observed,
        'null_distributions': null_dists,
        'p_values': p_values,
    }


def computeRipleysK(cell_metrics, px_size, volume_shape, n_steps=50, n_simulations=100,
                    mean_diameter_um=None):
    """
    Compute 3D Ripley's K and L functions for germ cell centroids, with
    CSR confidence envelope from Monte Carlo simulations.

    Parameters
    ----------
    cell_metrics : pandas.DataFrame
        Must contain centroid_z, centroid_y, centroid_x columns (in voxels).
    px_size : list or tuple of float
        Physical pixel spacing as [Z, Y, X] in micrometers.
    volume_shape : tuple
        Shape of the label image (Z, Y, X) in voxels.
    n_steps : int, optional
        Number of distance values to evaluate. Default is 50.
    n_simulations : int, optional
        Number of CSR simulations for confidence envelope. Default is 100.
    mean_diameter_um : float, optional
        Mean equivalent cell diameter in µm (from analyzeVASANeighbors summary).
        Used to compute r_normalized = r / mean_diameter_um for cross-sample comparison.
        If None, r_normalized is None in the output.

    Returns
    -------
    ripley_results : dict
        'r'             : distance values in µm
        'K_observed'    : observed K(r)
        'K_csr'         : theoretical K(r) under CSR
        'L_observed'    : L(r) - r (observed)
        'L_csr'         : L(r) - r under CSR (= 0)
        'L_envelope_lo' : 2.5th percentile of Monte Carlo CSR envelope
        'L_envelope_hi' : 97.5th percentile of Monte Carlo CSR envelope
        'r_normalized'  : r / mean_diameter_um (or None)
        'mean_diameter_um' : value used for normalization (or None)
    """
    pz, py, pxl = float(px_size[0]), float(px_size[1]), float(px_size[2])

    # Physical centroids
    centroids = cell_metrics[['centroid_z', 'centroid_y', 'centroid_x']].values.copy()
    centroids[:, 0] *= pz
    centroids[:, 1] *= py
    centroids[:, 2] *= pxl

    # Volume dimensions in physical units
    vol_dims = np.array([volume_shape[0] * pz, volume_shape[1] * py, volume_shape[2] * pxl])
    V = np.prod(vol_dims)
    N = len(centroids)

    # Distance range
    r_max = np.min(vol_dims) / 4
    r_values = np.linspace(0, r_max, n_steps)

    def compute_K(points, r_values, V, N):
        if N < 2:
            return np.zeros(len(r_values))
        dists = pdist(points)
        K = np.zeros(len(r_values))
        for i, r in enumerate(r_values):
            K[i] = (V / (N * (N - 1))) * 2 * np.sum(dists <= r)
        return K

    # Observed K
    K_obs = compute_K(centroids, r_values, V, N)

    # Theoretical CSR K for 3D
    K_csr = (4.0 / 3.0) * np.pi * r_values ** 3

    # L-transform: L(r) = (3*K/(4*pi))^(1/3) - r
    def L_transform(K, r):
        return np.cbrt(3 * K / (4 * np.pi)) - r

    L_obs = L_transform(K_obs, r_values)
    L_csr = np.zeros(n_steps)  # L = 0 under CSR

    # Monte Carlo CSR envelope
    L_sims = np.zeros((n_simulations, n_steps))
    for sim in range(n_simulations):
        random_points = np.random.uniform(
            low=[0, 0, 0], high=vol_dims, size=(N, 3))
        K_sim = compute_K(random_points, r_values, V, N)
        L_sims[sim] = L_transform(K_sim, r_values)

    L_lo = np.percentile(L_sims, 2.5, axis=0)
    L_hi = np.percentile(L_sims, 97.5, axis=0)

    # Normalized r axis (in units of mean cell diameters)
    r_normalized = (r_values / mean_diameter_um
                    if mean_diameter_um is not None and mean_diameter_um > 0
                    else None)

    print(f'[computeRipleysK] Computed K/L for {N} cells over r=[0, {r_max:.1f}] um')

    return {
        'r': r_values,
        'K_observed': K_obs,
        'K_csr': K_csr,
        'L_observed': L_obs,
        'L_csr': L_csr,
        'L_envelope_lo': L_lo,
        'L_envelope_hi': L_hi,
        'r_normalized': r_normalized,
        'mean_diameter_um': mean_diameter_um,
    }


def computeGeometricMetrics(cell_metrics, label_image, px_size):
    """
    Compute geometric shape metrics for the VASA cell population domain.

    Parameters
    ----------
    cell_metrics : pandas.DataFrame
        Must contain centroid_z, centroid_y, centroid_x (voxels) and volume_um3 columns.
        Produced by analyzeVASANeighbors with px_size specified.
    label_image : numpy.ndarray
        3D integer label array (ZYX).
    px_size : list or tuple of float
        Physical pixel spacing as [Z, Y, X] in micrometers.

    Returns
    -------
    geom : dict
        'rg_um'        : radius of gyration of centroid cloud in µm
                         rg = sqrt(mean(|r_i - r_cm|^2))
        'r_eq_um'      : equivalent sphere radius = (3*N*V_mean / (4*pi))^(1/3)
                         radius of a sphere with the same total VASA cell volume
        'rg_norm'      : rg_um / r_eq_um  (compact sphere -> ~0.775; dispersed >> 0.775)
        'sv_ratio'     : S_domain / V_domain in µm^-1
                         S_domain = marching-cubes surface of merged VASA binary mask
                         V_domain = N * mean_volume_um3
        'sv_ratio_norm': sv_ratio * r_eq_um / 3  (= 1 for a perfect sphere)
    """
    pz, py, pxl = float(px_size[0]), float(px_size[1]), float(px_size[2])
    px_arr = np.array([pz, py, pxl])

    N = len(cell_metrics)
    if N == 0:
        nan = float('nan')
        return {'rg_um': nan, 'r_eq_um': nan, 'rg_norm': nan,
                'sv_ratio': nan, 'sv_ratio_norm': nan}

    # --- Radius of gyration ---
    centroids_vox = cell_metrics[['centroid_z', 'centroid_y', 'centroid_x']].values
    centroids_um = centroids_vox * px_arr          # ZYX broadcast -> physical µm
    r_cm = centroids_um.mean(axis=0)
    rg_um = float(np.sqrt(np.mean(np.sum((centroids_um - r_cm) ** 2, axis=1))))

    # --- Equivalent sphere radius ---
    V_mean_um3 = float(cell_metrics['volume_um3'].mean())
    V_total_um3 = N * V_mean_um3
    r_eq_um = float((3.0 * V_total_um3 / (4.0 * np.pi)) ** (1.0 / 3.0))
    rg_norm = rg_um / r_eq_um if r_eq_um > 0 else float('nan')

    # --- Surface / volume ratio of merged VASA domain ---
    binary_mask = (np.asarray(label_image) > 0).astype(np.uint8)
    try:
        verts, faces, _, _ = measure.marching_cubes(
            binary_mask, level=0.5, spacing=tuple(px_arr))
        S_domain = float(measure.mesh_surface_area(verts, faces))
    except Exception as e:
        print(f'[computeGeometricMetrics] marching_cubes failed: {e}')
        S_domain = float('nan')

    sv_ratio = (S_domain / V_total_um3
                if V_total_um3 > 0 and not np.isnan(S_domain)
                else float('nan'))
    sv_ratio_norm = (sv_ratio * r_eq_um / 3.0
                     if r_eq_um > 0 and not np.isnan(sv_ratio)
                     else float('nan'))

    print(f'[computeGeometricMetrics] Rg={rg_um:.1f} um, R_eq={r_eq_um:.1f} um, '
          f'Rg_norm={rg_norm:.3f}, S/V={sv_ratio:.4f} um^-1, S/V_norm={sv_ratio_norm:.3f}')

    return {
        'rg_um': rg_um,
        'r_eq_um': r_eq_um,
        'rg_norm': rg_norm,
        'sv_ratio': sv_ratio,
        'sv_ratio_norm': sv_ratio_norm,
    }


def paintLabelsByMetric(label_image, cell_metrics, metric_column):
    """
    Create a 3D volume where each cell's voxels are painted with a metric value.

    Parameters
    ----------
    label_image : numpy.ndarray
        3D integer label array (ZYX).
    cell_metrics : pandas.DataFrame
        Must contain 'label' column and the specified metric_column.
    metric_column : str
        Column name to paint (e.g. 'cluster_size', 'shared_boundary_ratio',
        'vasa_neighbors', 'clustering_coeff').

    Returns
    -------
    painted : numpy.ndarray
        3D float32 array, same shape as label_image. Background = 0.
    """
    lookup = np.zeros(label_image.max() + 1, dtype=np.float32)
    for _, row in cell_metrics.iterrows():
        lookup[int(row['label'])] = float(row[metric_column])

    painted = lookup[label_image]
    return painted


def exportVASANeighborMetrics(cell_metrics, summary, outputpath, basename):
    """Export neighbor analysis results to CSV files.

    component_sizes (a list) is not written directly; instead the p25/p50/p75/max
    of the distribution are saved as separate scalar columns.
    """
    cell_metrics.to_csv(
        os.path.join(outputpath, basename + '_VASA_neighbor_metrics.csv'),
        index=False
    )

    # Build summary row — expand component_sizes list into percentile scalars
    summary_export = {k: v for k, v in summary.items() if k != 'component_sizes'}
    comp_sizes = summary.get('component_sizes', [])
    if comp_sizes:
        summary_export['comp_size_p25'] = float(np.percentile(comp_sizes, 25))
        summary_export['comp_size_p50'] = float(np.percentile(comp_sizes, 50))
        summary_export['comp_size_p75'] = float(np.percentile(comp_sizes, 75))
        summary_export['comp_size_max'] = int(np.max(comp_sizes))
    else:
        for col in ['comp_size_p25', 'comp_size_p50', 'comp_size_p75', 'comp_size_max']:
            summary_export[col] = float('nan')

    summary_df = pd.DataFrame([summary_export])
    summary_df.to_csv(
        os.path.join(outputpath, basename + '_VASA_neighbor_summary.csv'),
        index=False
    )
