# -*- coding: utf-8 -*-
# ---
# jupyter:
#   jupytext:
#     formats: ipynb,py:light
#     text_representation:
#       extension: .py
#       format_name: light
#       format_version: '1.5'
#       jupytext_version: 1.11.5
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# +
# %run __init__.py

import time
import pathlib
import uuid
from mf_file_utilities.applauncher_wrapper import go, get_fpth_win
from mf_file_utilities.constants import PATH_CDRIVE
import logging
logger = logging


# -

def docx_to_pdf(fpth_docx: pathlib.Path, fpth_pdf: pathlib.Path):
    batch_name = f"process_{str(uuid.uuid4())}"
    fdir_batch = pathlib.Path(fpth_docx).parent

    win_path_docx = get_fpth_win(fpth_docx, newroot=PATH_CDRIVE)  # get windows path from linux path
    win_path_pdf = get_fpth_win(fpth_pdf, newroot=PATH_CDRIVE) 
    
    fpth_pdf.unlink(missing_ok=True)  # Delete pdf in output folder if exists

    fdir_batch.mkdir(parents=True, exist_ok=True)  # Make dir if doesn't exist.
    fn = f"{batch_name}.bat"  # Make batch file.
    fpth_batch = fdir_batch / fn
    cmd = "call C:\engDev\git_mf\docx_to_pdf\test\docx_to_pdf.exe --fpth_docx C:\engDev\git_mf\project_tracker\appdata\AecTemplater\out-AecTemplater.docx --openfile True --update_toc True"
    cmd = f"""call^
"C:\engDev\git_mf\docx_to_pdf\test\docx_to_pdf.exe"^
 --fpth_docx {win_path_docx}^
 --fpth_pdf {win_path_pdf}^
 --update_toc True^
 --openfile False
 """  # cmd to perform conversion # --openfile True^

    with fpth_batch.open("w", encoding ="utf-8") as f:
        f.write(cmd)  # write to batch file

    go(fpth_batch) # open batch file

    timeout = 60  # [seconds]
    time_start = time.time()

    while fpth_pdf.is_file() is False:
        if time.time() > time_start + timeout:
            logger.warning("☠️ PDF took too long to produce.")
            #fpth_batch.unlink(missing_ok=True)  # Delete batch file.
            break
    
    if fpth_pdf.is_file() is True:  # If pdf exists then file creation has been successful.
        logger.info(f"👍 created pdf: {fpth_pdf}")

    #fpth_batch.unlink(missing_ok=True)  # Delete batch file.
    return fpth_pdf


if __name__ == "__main__":
    fpth_docx = pathlib.Path('/home/jovyan/jobs/J5001/Jupyter/Schedule/06667-MXF-XX-XX-SH-M-20003-GrilleSchedule.docx')
    fpth_pdf = pathlib.Path('/home/jovyan/jobs/J5001/Schedule/06667-MXF-XX-XX-SH-M-20003-GrilleSchedule.pdf')
    docx_to_pdf(fpth_docx, fpth_pdf)


