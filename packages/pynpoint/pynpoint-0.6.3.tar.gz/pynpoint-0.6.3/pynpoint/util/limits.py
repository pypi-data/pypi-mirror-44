"""
Functions for calculating detection limits.
"""

import sys
import warnings

import numpy as np

from scipy.interpolate import interp1d

from pynpoint.util.analysis import student_fpf, fake_planet, false_alarm
from pynpoint.util.image import create_mask, polar_to_cartesian
from pynpoint.util.psf import pca_psf_subtraction
from pynpoint.util.residuals import combine_residuals


def contrast_limit(tmp_images,
                   tmp_psf,
                   parang,
                   psf_scaling,
                   extra_rot,
                   magnitude,
                   pca_number,
                   threshold,
                   accuracy,
                   aperture,
                   ignore,
                   cent_size,
                   edge_size,
                   pixscale,
                   position,
                   residuals,
                   queue):

    """
    Function for calculating the contrast limit at a specified position by iterating towards
    a threshold for the false positive fraction, with a correction for small sample statistics.

    Parameters
    ----------
    images : str
        System location of the stack of images.
    psf : str
        System location of the PSF template for the fake planet. Either a single image or a stack
        of images equal in size to *images*.
    parang : numpy.ndarray
        Derotation angles (deg).
    psf_scaling : float
        Additional scaling factor of the planet flux (e.g., to correct for a neutral density
        filter). Should have a positive value.
    extra_rot : float
        Additional rotation angle of the images in clockwise direction (deg).
    magnitude : tuple(float, float)
        Initial magnitude value and step size for the fake planet, specified as (planet magnitude,
        magnitude step size).
    pca_number : int
        Number of principal components used for the PSF subtraction.
    threshold : tuple(str, float)
        Detection threshold for the contrast curve, either in terms of "sigma" or the false
        positive fraction (FPF). The value is a tuple, for example provided as ("sigma", 5.) or
        ("fpf", 1e-6). Note that when sigma is fixed, the false positive fraction will change with
        separation. Also, sigma only corresponds to the standard deviation of a normal distribution
        at large separations (i.e., large number of samples).
    accuracy : float
        Fractional accuracy of the false positive fraction. When the accuracy condition is met, the
        final magnitude is calculated with a linear interpolation.
    aperture : float
        Aperture radius (arcsec) for the calculation of the false positive fraction.
    ignore : bool
        Ignore the two neighboring apertures that may contain self-subtraction from the planet.
    cent_size : float
        Central mask radius (arcsec). No mask is used when set to None.
    edge_size : float
        Outer edge radius (arcsec) beyond which pixels are masked. No outer mask is used when set
        to None. If the value is larger than half the image size then it will be set to half the
        image size.
    pixscale : float
        Pixel scale (arcsec pix-1).
    position : tuple(float, float)
        The separation (pix) and position angle (deg) of the fake planet.
    residuals : str
        Method used for combining the residuals ("mean", "median", "weighted", or "clipped").

    Returns
    -------
    float
        Separation (pix).
    float
        Position angle (deg).
    float
        Magnitude (mag).
    float
        False positive fraction.
    """

    images = np.load(tmp_images)
    psf = np.load(tmp_psf)

    if threshold[0] == "sigma":
        fpf_threshold = student_fpf(sigma=threshold[1],
                                    radius=position[0],
                                    size=aperture,
                                    ignore=ignore)

    elif threshold[0] == "fpf":
        fpf_threshold = threshold[1]

    else:
        raise ValueError("Threshold type not recognized.")

    xy_fake = polar_to_cartesian(images, position[0], position[1]-extra_rot)

    list_fpf = []
    list_mag = [magnitude[0]]
    mag_step = magnitude[1]

    iteration = 1

    fake_mag = None

    while True:
        mag = list_mag[-1]

        fake = fake_planet(images=images,
                           psf=psf,
                           parang=parang,
                           position=(position[0], position[1]),
                           magnitude=mag,
                           psf_scaling=psf_scaling)

        im_shape = (fake.shape[-2], fake.shape[-1])

        mask = create_mask(im_shape, [cent_size, edge_size])

        _, im_res = pca_psf_subtraction(images=fake*mask,
                                        angles=-1.*parang+extra_rot,
                                        pca_number=pca_number)

        stack = combine_residuals(method=residuals, res_rot=im_res)

        _, _, fpf = false_alarm(image=stack[0, ],
                                x_pos=xy_fake[0],
                                y_pos=xy_fake[1],
                                size=aperture,
                                ignore=ignore)

        list_fpf.append(fpf)

        if abs(fpf_threshold-list_fpf[-1]) < accuracy*fpf_threshold:
            if len(list_fpf) == 1:
                fake_mag = list_mag[0]
                break

            else:
                if (fpf_threshold > list_fpf[-2] and fpf_threshold < list_fpf[-1]) or \
                   (fpf_threshold < list_fpf[-2] and fpf_threshold > list_fpf[-1]):

                    fpf_interp = interp1d(list_fpf[-2:], list_mag[-2:], 'linear')
                    fake_mag = fpf_interp(fpf_threshold)
                    break

                else:
                    pass

        if list_fpf[-1] < fpf_threshold:
            if list_mag[-1]+mag_step in list_mag:
                mag_step /= 2.

            list_mag.append(list_mag[-1]+mag_step)

        else:
            if np.size(list_fpf) > 2 and \
               list_mag[-1] < list_mag[-2] and list_mag[-2] < list_mag[-3] and \
               list_fpf[-1] > list_fpf[-2] and list_fpf[-2] < list_fpf[-3]:

                warnings.warn("Magnitude decreases but false positive fraction "
                              "increases. Adjusting magnitude to %s and step size "
                              "to %s" % (list_mag[-3], mag_step/2.))

                list_fpf = []
                list_mag = [list_mag[-3]]
                mag_step /= 2.

            else:
                if list_mag[-1]-mag_step in list_mag:
                    mag_step /= 2.

                list_mag.append(list_mag[-1]-mag_step)

        if list_mag[-1] <= 0.:
            warnings.warn("The relative magnitude has become smaller or equal to "
                          "zero. Adjusting magnitude to 7.5 and step size to 0.1.")

            list_mag[-1] = 7.5
            mag_step = 0.1

        iteration += 1

        if iteration == 50:
            warnings.warn("ContrastModule could not converge at the position of "
                          "%s arcsec and %s deg." % (position[0]*pixscale, position[1]))

            fake_mag = np.nan

            sys.stdout.write("\n")
            sys.stdout.flush()

            break

    result = (position[0], position[1], fake_mag, fpf_threshold)
    queue.put(result)

    return position[0], position[1], fake_mag, fpf_threshold
