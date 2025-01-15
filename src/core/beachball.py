import logging
import sys

from .dependencies.check_dependencies import check
from .dependencies.lib import init_site_packages

site_packages = init_site_packages()
sys.path.append(site_packages)

try:
    import matplotlib.pyplot as plt
    import numpy as np
    from obspy.imaging.beachball import beachball
except Exception as e:
    try:
        did_install = check(["obspy", "matplotlib", "numpy"], target=site_packages)
        if did_install:
            import matplotlib.pyplot as plt
            import numpy as np
            from obspy.imaging.beachball import beachball
    finally:
        logging.exception(e)


def depth_to_color(val, v_min=10.0, v_max=700.0, cmap="viridis", log=True):
    """
    Convert hypocentral depth to color.

    Args:
        val (_type_): _description_
        v_min (float, optional): _description_. Defaults to 10.0.
        v_max (float, optional): _description_. Defaults to 700.0.
        cmap (str, optional): _description_. Defaults to "viridis".
        log (bool, optional): _description_. Defaults to True.

    Returns:
        _type_: _description_
    """

    colormap = plt.get_cmap(cmap)

    if log is True:
        v_min_ = np.log(v_min)
        v_max_ = np.log(v_max)
        val_ = np.log(val)

    else:
        v_min_ = v_min
        v_max_ = v_max
        val_ = val

    return colormap((val_ - v_min_) / (v_max_ - v_min_))


def make_beachball(
    event,
    directory,
    fig_format="svg",
    bb_linewidth=2,
    bb_size=20,
    bb_width=10,
    bb_color="b",
    event_id="Event",
    depth_based_color=True,
    depth_field="Depth",
    tensor_components=None,
    sdp_components=None,
):
    # tensor_components = tensor_components or ["Mrr", "Mtt", "Mpp", "Mrt", "Mrp", "Mtp"]

    ev = event
    focal_mechanism = None
    if tensor_components:
        mt = [ev[component] for component in tensor_components]
        focal_mechanism = [float(x) for x in mt]

    if sdp_components:
        sdp = [ev[component] for component in sdp_components]
        focal_mechanism = [float(x) for x in sdp]

    if not tensor_components and not sdp_components:
        logging.error("No tensor or sdp components provided.")
        raise ValueError("No tensor or strike/dip/rake components provided.")

    # Default black
    bb_color = "k"
    if depth_based_color:
        bb_color = depth_to_color(float(ev[depth_field]))

    outfile = f"{directory}/{event[event_id]}.{fig_format}"

    fig = plt.figure(0)
    try:
        logging.info("Making beachball for %s", event[event_id])
        beachball(
            focal_mechanism,
            linewidth=bb_linewidth,
            size=bb_size,
            width=bb_width,
            outfile=outfile,
            fig=fig,
            facecolor=bb_color,
            bgcolor="w",
            # format=fig_format,
        )
        plt.close(fig)

    except Exception as e:
        logging.exception(e)
    return
