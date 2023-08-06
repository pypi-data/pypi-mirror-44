import pytest
import numpy as np
import numpy.testing as npt

from lenstronomy.ImSim.image_numerics import ImageNumerics
from lenstronomy.Data.imaging_data import Data
from lenstronomy.Data.psf import PSF


class TestImageNumerics(object):

    def setup(self):
        self.numPix = 10
        kwargs_data = {'image_data': np.zeros((self.numPix, self.numPix))}
        self.Data = Data(kwargs_data)
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': 1}
        self.PSF = PSF(kwargs_psf)
        kwargs_numerics = {'subgrid_res': 2, 'psf_subgrid': True}
        self.ImageNumerics = ImageNumerics(self.Data, self.PSF, **kwargs_numerics)

    def test_psf_cutout(self):
        idex_mask = np.zeros((5, 5))
        idex_mask[3, 2] = 1
        idex_mask[1, 1] = 1
        image_data = np.zeros((5, 5))
        image_data[1, 1] = 1
        kwargs_data = {'image_data': image_data}
        data = Data(kwargs_data)
        kwargs_numerics = {'idex_mask': idex_mask}
        imageNumerics = ImageNumerics(data, self.PSF, **kwargs_numerics)
        cut_data = imageNumerics._cutout_psf(image_data, subgrid_res=1)
        print(cut_data)
        assert cut_data[0, 0] == 1
        assert cut_data[2, 1] == 0
        nx, ny = np.shape(cut_data)
        assert nx == 3
        assert ny == 2

        idex_mask = np.ones((5, 5))
        kwargs_data = {'image_data': image_data}
        data = Data(kwargs_data)
        kwargs_numerics = {'idex_mask': idex_mask}
        imageNumerics = ImageNumerics(data, self.PSF, **kwargs_numerics)
        cut_data = imageNumerics._cutout_psf(image_data, subgrid_res=1)
        assert cut_data[1, 1] == 1

    def test_idex_subgrid(self):
        idex_mask = np.zeros(self.numPix**2)
        n = 8
        nx, ny = int(np.sqrt(len(idex_mask))), int(np.sqrt(len(idex_mask)))
        idex_mask[n] = 1
        subgrid_res = 2
        idex_mask_subgrid = self.ImageNumerics._subgrid_idex(idex_mask, subgrid_res, nx, ny)
        assert idex_mask_subgrid[(n + 1) * subgrid_res - 1] == 1
        assert idex_mask_subgrid[(n + 1) * subgrid_res - 2] == 1
        print(type(nx * subgrid_res + (n + 1) * subgrid_res - 1))
        print(type((n + 1) * subgrid_res - 2))
        assert idex_mask_subgrid[nx * subgrid_res + (n + 1) * subgrid_res - 1] == 1

    def test_point_source_rendering(self):
        numPix = 20
        deltaPix = 0.05
        ra_at_xy_0 = 0
        dec_at_xy_0 = 0
        kwargs_data = {'image_data': np.zeros((numPix, numPix))}
        data = Data(kwargs_data)
        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': 1., 'point_source_subgrid': 1}
        psf = PSF(kwargs_psf)
        kwargs_numerics = {'subgrid_res': 2, 'psf_subgrid': True}
        imageNumerics = ImageNumerics(data, psf, **kwargs_numerics)
        ra_pos = np.array([10, 7])
        dec_pos = np.array([6, 7])
        amp = np.array([10, 10])
        image = imageNumerics.point_source_rendering_old(ra_pos, dec_pos, amp)
        image_subgrid = imageNumerics.point_source_rendering(ra_pos, dec_pos, amp)
        npt.assert_almost_equal(image[10, 7], image_subgrid[10, 7], decimal=8)

        kwargs_psf = {'psf_type': 'GAUSSIAN', 'fwhm': 2., 'point_source_subgrid': 3}
        psf = PSF(kwargs_psf)
        kwargs_numerics = {'subgrid_res': 1, 'psf_subgrid': True}
        imageNumerics = ImageNumerics(data, psf, **kwargs_numerics)
        ra_pos = np.array([7.1, 14])
        dec_pos = np.array([7, 7.32])
        amp = np.array([10, 10])
        image = imageNumerics.point_source_rendering(ra_pos, dec_pos, amp)
        image_subgrid = imageNumerics.point_source_rendering(ra_pos, dec_pos, amp)
        image_sum = np.sum(image)
        image_subgrid_sum = np.sum(image_subgrid)
        npt.assert_almost_equal(image_sum/image_subgrid_sum, 1, decimal=5)

        assert image[7, 14] <= image_subgrid[7, 14]
        npt.assert_almost_equal(image[0, 0], image_subgrid[0, 0], decimal=8)


if __name__ == '__main__':
    pytest.main()