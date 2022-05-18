from pathlib import Path
from typing import List, Optional

from .utils import (
    prepare_output_directory,
    align_tilt_series_aretomo,
    find_binning_factor,
    check_aretomo_availability,
)


def run_aretomo_alignment(
        tilt_series_file: Path,
        tilt_angles: List[float],
        pixel_size: float,
        output_directory: Path,
        aretomo_executable: Optional[Path] = None,
        local_align: Optional[bool] = False,
        target_pixel_size: Optional[float] = 10,
        nominal_rotation_angle: Optional[float] = None,
        n_patches_xy: Optional[tuple[int, int]] = (5, 4),
        correct_tilt_angle_offset: Optional[bool] = False,
        thickness_for_alignment: Optional[float] = 800
):
    """Run aretomo alignment on a single tilt-series
    
    Parameters
    ----------
    
    tilt_series_file: file containing tilt-series images
    tilt_angles: nominal stage tilt-angles from the microscope.
    pixel_size: pixel size of the tilt-series in angstroms-per-pixel
    output_directory: tilt-series directory.
    aretomo_executable: path to the AreTomo executable file
    (optional) local_align: carry out local tilt series alignments? Yes or no, default is no
    (optional) target_pixel_size: the ideal pixel size at which TSA is carried out. Default is 10A
    (optional) nominal_rotation_angle: initial estimate for the rotation angle of the tilt
    axis. AreTomo does not need this information but it might help.
    (optional) n_patches_xy: if local_align is True, AreTomo will carry out patch tracking. 
    Specify the number of patches in X and Y here as tuple. Default is 5 in X,4 in Y.
    (optional) correct_tilt_angle_offset: Apply tilt angle offset correction, yes or no.
    Default is no. See AreTomo manual for full explanation: yes adds the -TiltCor 1 argument.
    (optional) thickness_for_alignment: thickness in Z in unbinned pixels for which AreTomo will use in the alignment.
    This is useful is there is a lot of empty space at the top and bottom of your tomogram.
    See AreTomo manual for full explanation: this sets -AlignZ. Default is 800.
    """
    if check_aretomo_availability() is False and aretomo_executable is None:
        raise RuntimeError('AreTomo executable not found.')

    tilt_series_file = prepare_output_directory(
        tilt_series_file=tilt_series_file,
        tilt_angles=tilt_angles,
        output_directory=output_directory
    )

    binning = find_binning_factor(
        pixel_size=pixel_size,
        target_pixel_size=target_pixel_size
    )

    align_tilt_series_aretomo(
        tilt_series_file=tilt_series_file,
        output_directory=output_directory,
	    binning=binning,
        aretomo_executable=aretomo_executable,
        nominal_rotation_angle=nominal_rotation_angle,
        local_align=local_align,
        n_patches_xy=n_patches_xy,
        correct_tilt_angle_offset=correct_tilt_angle_offset,
        thickness_for_alignment=thickness_for_alignment
    )
