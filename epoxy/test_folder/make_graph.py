import numpy as np


def assign_taxi_zones(df, lon_var, lat_var, locid_var):
    import geopandas
    from shapely.geometry import Point

    localdf = df[[lon_var, lat_var]].copy()

    localdf[lon_var] = localdf[lon_var].fillna(value=0.)
    localdf[lat_var] = localdf[lat_var].fillna(value=0.)

    shape_df = geopandas.read_file('../Capstone/taxi_zones/taxi_zones.shp')
    shape_df = shape_df.to_crs({'init': 'epsg:4326'})
    try:
        local_gdf = geopandas.GeoDataFrame(
            localdf, crs={'init': 'epsg:4326'},
            geometry=[Point(xy) for xy in
                      zip(localdf[lon_var], localdf[lat_var])])

        local_gdf = geopandas.sjoin(
            local_gdf, shape_df, how='left', op='within')

        return local_gdf.OBJECTID.rename(locid_var)
    except ValueError as ve:
        print(ve)
        print(ve.stacktrace())
        series = localdf[lon_var]
        series = np.nan
        return series

dff = dff.join(assign_taxi_zones(dff, " pickup_longitude", " pickup_latitude", "pickup_taxizone_id"))
dff = dff.join(assign_taxi_zones(dff, " dropoff_longitude", " dropoff_latitude", "dropoff_taxizone_id"))