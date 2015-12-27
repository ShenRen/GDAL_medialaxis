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

from osgeo import gdal
from skimage.morphology import medial_axis


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

    getSkeleton(input_raster, out_raster)
