import os
import pathlib
import shutil
import sys
import tempfile

import SimpleITK as sitk
import pydicom
import vtk

from vmi import vio
from vmi.view import *


def sortSeries(dcmdir, recursive=True):
    roots, series = {dcmdir}, []
    if recursive:
        roots = {root for root, *_ in os.walk(dcmdir)}
    for root in roots:
        with tempfile.TemporaryDirectory() as p:
            if vio.diffEncode(root):
                for f in os.listdir(root):
                    f = os.path.join(root, f)
                    if os.path.isfile(f):
                        shutil.copy2(f, p)
                root = p

            ids = sitk.ImageSeriesReader.GetGDCMSeriesIDs(root)

            for i in ids:
                filenames = sitk.ImageSeriesReader.GetGDCMSeriesFileNames(root, i)
                series.append(Series(filenames))
    return series


class Series(QObject, Menu):
    def __init__(self, filenames, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('系列 （Series)')
        Menu.__init__(self, name=self.name)

        self._Filenames = filenames
        self._Directory = tempfile.TemporaryDirectory()

        if len(self._Filenames) > 0:
            self._Filenames = [shutil.copy2(f, self._Directory.name) for f in self._Filenames]

    def __setstate__(self, s):
        self.__init__(s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Filenames = []
        self._Directory = tempfile.TemporaryDirectory()
        for kw in s['_Bytes']['_Files']:
            p = pathlib.Path(self._Directory.name) / kw
            p.write_bytes(s['_Bytes']['_Files'][kw])
            self._Filenames.append(str(p))

        del s['_Bytes']

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['_Filenames', 'menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Bytes'] = {'_Files': {pathlib.Path(f).name: pathlib.Path(f).read_bytes() for f in self._Filenames}}
        return s

    def __str__(self):
        with pydicom.dcmread(self._Filenames[0]) as ds:
            r = ['', '', '', '', '']
            for e in [_ for _ in ds if _.VR != 'SQ']:
                e.showVR = False
                if e.name in ['Modality', 'Slice Thickness', 'Rows', 'Columns', 'Pixel Spacing', 'Pixel Data']:
                    r[0] += repr(e) + '\n'
                elif e.name.startswith('Patient'):
                    r[1] += repr(e) + '\n'
                elif e.name.startswith('Study'):
                    r[2] += repr(e) + '\n'
                elif e.name.startswith('Series'):
                    r[3] += repr(e) + '\n'
                elif e.name.startswith('Image'):
                    r[4] += repr(e) + '\n'
            return 'slices: {}\n'.format(len(self._Filenames)) + r[0] + r[1] + r[2] + r[3] + r[4]

    def __repr__(self):
        return self.__str__()

    def filenames(self):
        return self._Filenames

    def readITK(self):
        r = sitk.ImageSeriesReader()
        r.SetFileNames(self._Filenames)
        return r.Execute()

    def read(self):
        with tempfile.TemporaryDirectory() as p:
            p = pathlib.Path(p) / '.nii'

            w = sitk.ImageFileWriter()
            w.SetFileName(str(p))
            w.SetImageIO('NiftiImageIO')
            w.Execute(self.readITK())

            r = vtk.vtkNIFTIImageReader()
            r.SetFileName(str(p))
            r.Update()
            return r.GetOutput()


if __name__ == '__main__':
    from PySide2.QtWidgets import *
    from vmi.view import View

    app = QApplication(sys.argv)
    app.setOrganizationName('Vi')
    app.setApplicationName('Vi')

    w = View()
    w.setMouseStyle("Volume")

    dcmdir = 'C:/Users/Medraw/Desktop/DICOM/bingu'
    series = sortSeries(dcmdir)

    from vmi.vrop import ImageSlice, ImageVolume

    img = ImageSlice(w)
    img.clone(series[0].read())
    img.setSlicePlane(origin='c', normal='axial')
    img.setWindow('soft')

    vol = ImageVolume(w)
    vol.bindDataset(img)

    w._Renderer.ResetCamera()
    w._Renderer.ResetCameraClippingRange()
    w._Renderer.SetBackground(1, 0.5, 0.5)
    w.updateInTime()
    w.show()
    app.exec_()

    import shelve
    from pickle import HIGHEST_PROTOCOL

    with shelve.open('C:/Users/Medraw/Desktop/db', 'n', HIGHEST_PROTOCOL) as db:
        db['ViDICOM'] = {'vmi': w, 'img': img, 'vol': vol}

    with shelve.open('C:/Users/Medraw/Desktop/db', 'r') as db:
        db = db['ViDICOM']
        db['vmi'].show()
        db['vol'].delete()

    sys.exit(app.exec_())

    # input('EXIT_SUCCESS')
