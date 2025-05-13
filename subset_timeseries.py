import xarray as xr
import easygems.healpix as egh
import healpy as hp
import pandas as pd

model = 'UM'

path = "/g/data/qx55/uk_node/glm.n2560_RAL3p3/data.healpix.PT1H.z10.zarr" #PT1H is hourly data
ds = xr.open_zarr(path)

def get_nside(ds):
    return ds.crs.healpix_nside

def get_nest(ds):
    return ds.crs.healpix_order == "nest"

def subset_timeseries(ds, name, this_lon, this_lat, model):

    cell = hp.ang2pix(get_nside(ds), this_lon, this_lat, lonlat = True, nest = get_nest(ds))
    data = ds.tas.isel(cell = cell)

    df = pd.DataFrame(data, columns=["tas"])
    df.insert(1, 'time', data['time'])
    df.insert(2, 'lon', this_lon)
    df.insert(3, 'lat', this_lat)

    path = '/home/565/pc2687/code/hk25-AusNode-PBL/data/' + name + '_' + model + '.csv'
    df.to_csv(path, index = False) 

subset_timeseries(ds, 'Melbourne', 144.9631, -37.8136, model)
subset_timeseries(ds, 'Sidney', 151.2093, -33.8688, model)
subset_timeseries(ds, 'BuenosAires', -58.3821, -34.6037, model)
subset_timeseries(ds, 'Cordoba', -64.1888, -31.4201, model)