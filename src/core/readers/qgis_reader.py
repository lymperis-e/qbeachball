"""
Read focal mechanism features from a QGIS layer and return them as a list of dictionaries.  
"""


def read_from_layer(layer, max_rows=None):
    """
    Read from a QGIS layer.

    layer: a QgsVectorLayer object
    """
    fields = layer.fields()
    rows = []
    for feature in layer.getFeatures():
        row = {field.name(): feature[field.name()] for field in fields}
        rows.append(row)
    return rows
    # for i, feature in enumerate(layer.getFeatures()):
    #     if max_rows and i >= max_rows:
    #         break
    #     row = {field.name(): feature[field.name()] for field in fields}
    #     rows.append(row)
