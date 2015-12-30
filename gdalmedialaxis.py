# -*- coding: utf-8 -*-
#
#  Author: Cayetano Benavent, 2015.
#  cayetano.benavent@geographica.gs
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#

import numpy as np
import pandas as pd
from osgeo import gdal
from skimage.morphology import medial_axis


def raster2xyz(input_raster, out_xyz, n_band=1, flt_val=1):
    src_raster = gdal.Open(input_raster)
    raster_bnd = src_raster.GetRasterBand(n_band)
    raster_values = raster_bnd.ReadAsArray()

    gtr = src_raster.GetGeoTransform()

    y, x = np.where(raster_values == 1)

    gtr_x = gtr[0] + (x + 0.5) * gtr[1] + (y + 0.5) * gtr[2]
    gtr_y = gtr[3] + (x + 0.5) * gtr[4] + (y + 0.5) * gtr[5]

    data_vals = np.extract(raster_values == 1, raster_values)

    data_dict = {
        "x": gtr_x,
        "y": gtr_y,
        "z": data_vals
    }

    df = pd.DataFrame(data_dict)

    df.to_csv(out_xyz, index=False)

    src_raster = None

    print("New XYZ (csv file) created...")


def readRaster(input_raster, n_band=1, nodata_val=-9999):
    src_raster = gdal.Open(input_raster)
    raster_bnd = src_raster.GetRasterBand(n_band)
    raster_values = raster_bnd.ReadAsArray()

    data = raster_values != nodata_val

    src_raster = None

    print("Raster readed...")

    return data

def writeRaster(out_raster, src_raster, skel_data, n_band=1, nodata_val=0):
    drv_gtif = gdal.GetDriverByName("GTiff")
    src_ds = gdal.Open(src_raster)
    dst_raster = drv_gtif.CreateCopy(out_raster, src_ds, 0, options=["COMPRESS=LZW"])

    out_band = dst_raster.GetRasterBand(n_band)
    out_band.SetNoDataValue(nodata_val)
    out_band.WriteArray(skel_data)

    src_ds = None
    dst_raster = None

    print("New raster created...")

def computeSkeleton(data):
    skel, dist = medial_axis(data, return_distance=True)

    dist_on_skel = dist * skel

    print("Medial axis computed...")

    return(skel, dist, dist_on_skel)

def getSkeleton(input_raster, out_raster):
    data = readRaster(input_raster)
    skel_data, dist, dist_on_skel = computeSkeleton(data)
    writeRaster(out_raster, input_raster, skel_data)

if __name__ == "__main__":
    input_raster = "./data/input_raster.tif"
    out_raster = "/tmp/medial_axis.tif"
    out_csv = "/tmp/medial_axis.csv"

    getSkeleton(input_raster, out_raster)
    raster2xyz(out_raster, out_csv)
