import matplotlib.patches as mpatches

def generate_handles(labels, colors, edge='k', alpha=1):
    """
    Generate matplotlib patch handles to create a legend of each of the features in the map.

    Parameters
    ----------

    labels : list(str)
        the text labels of the features to add to the legend

    colors : list(matplotlib color)
        the colors used for each of the features included in the map.

    edge : matplotlib color (default: 'k')
        the color to use for the edge of the legend patches.

    alpha : float (default: 1.0)
        the alpha value to use for the legend patches.

    Returns
    -------

    handles : list(matplotlib.patches.Rectangle)
        the list of legend patches to pass to ax.legend()
    """
    lc = len(colors)  # get the length of the color list
    handles = [] # create an empty list
    for ii in range(len(labels)): # for each label and color pair that we're given, make an empty box to pass to our legend
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[ii % lc], edgecolor=edge, alpha=alpha))
    return handles

# ----------------------------------------------------------------------------------------------------------------------

def scale_bar(ax, length=20, location=(0.92, 0.95)):
    """
    Create a scale bar in a cartopy GeoAxes.

    Parameters
    ----------

    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes to add the scalebar to.

    length : int, float (default 20)
        the length of the scalebar, in km

    location : tuple(float, float) (default (0.92, 0.95))
        the location of the center right corner of the scalebar, in fractions of the axis.

    Returns
    -------
    ax : cartopy.mpl.geoaxes.GeoAxes
        the cartopy GeoAxes object

    """
    x0, x1, y0, y1 = ax.get_extent()  # get the current extent of the axis
    sbx = x0 + (x1 - x0) * location[0]  # get the right x coordinate of the scale bar
    sby = y0 + (y1 - y0) * location[1]  # get the right y coordinate of the scale bar

    ax.plot([sbx, sbx - length * 1000], [sby, sby], color='k', linewidth=4,
            transform=ax.projection)  # plot a thick black line
    ax.plot([sbx - (length / 2) * 1000, sbx - length * 1000], [sby, sby], color='w', linewidth=2,
            transform=ax.projection)  # plot a white line from 0 to halfway

    ax.text(sbx, sby - (length / 4) * 1000, f"{length} km", ha='center', transform=ax.projection,
            fontsize=6)  # add a label at the right side
    ax.text(sbx - (length / 2) * 1000, sby - (length / 4) * 1000, f"{int(length / 2)} km", ha='center',
            transform=ax.projection, fontsize=6)  # add a label in the center
    ax.text(sbx - length * 1000, sby - (length / 4) * 1000, '0 km', ha='center', transform=ax.projection,
            fontsize=6)  # add a label at the left side

    return ax