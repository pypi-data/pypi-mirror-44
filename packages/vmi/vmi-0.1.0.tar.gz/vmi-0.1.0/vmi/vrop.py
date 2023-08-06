import sys

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import vtk

from vmi import vio
from vmi.view import *


class PolyActor(QObject, Menu, Mouse):
    def __init__(self, view: View, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('物体 （Poly)')
        Menu.__init__(self, name=self.name)

        self.view = view
        Mouse.__init__(self, view=self.view, menu=self)

        self._Mapper = vtk.vtkPolyDataMapper()
        self._Prop = vtk.vtkActor()
        self._Prop._Prop = self
        self.view._Renderer.AddActor(self._Prop)

        self._Property: vtk.vtkProperty = self._Prop.GetProperty()
        self._Pickable = False
        self.pickable(False)
        self._Shade = True
        self.shade(True)
        self._AlwaysOnTop = False
        self.alwaysOnTop(False)

        self._Dataset = vtk.vtkPolyData()
        self._BindDataset = self
        self.bindDataset()

        for b in self.mouse:
            for e in self.mouse[b]:
                self.mouse[b][e] = self.view.mouse[b][e]

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vio.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vio.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vio.dumps(self._Dataset)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vio.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]
        return s

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self._Dataset.ShallowCopy(self._Dataset.__class__())
        elif hasattr(other, '_Dataset'):
            self._Dataset.ShallowCopy(other._Dataset)
        elif isinstance(other, self._Dataset.__class__):
            self._Dataset.ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def alwaysOnTop(self, arg=None):
        self.view.updateInTime()
        if arg is True:
            self._AlwaysOnTop = True
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(0, -66000)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-66000)
        elif arg is False:
            self._AlwaysOnTop = False
            self._Mapper.SetRelativeCoincidentTopologyLineOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPolygonOffsetParameters(-1, -1)
            self._Mapper.SetRelativeCoincidentTopologyPointOffsetParameter(-1)
        return self._AlwaysOnTop

    def color(self, **kwargs):
        self.view.updateInTime()
        if 'rgb' in kwargs:
            self._Property.SetColor(kwargs['rgb'])
        if 'a' in kwargs:
            self._Property.SetOpacity(kwargs['a'])
        return {'rgb': list(self._Property.GetColor()),
                'a': self._Property.GetOpacity()}

    def delete(self):
        self._Dataset.ReleaseData()
        self.view._Renderer.RemoveActor(self._Prop)

    def pickable(self, arg=None):
        self.view.updateInTime()
        if arg is True:
            self._Pickable = True
            self._Prop.SetPickable(1)
        elif arg is False:
            self._Pickable = False
            self._Prop.SetPickable(0)
        return self._Pickable

    def rep(self, arg=None):
        self.view.updateInTime()
        if isinstance(arg, str):
            if arg.lower() == 'points':
                self._Property.SetRepresentationToPoints()
            elif arg.lower() == 'wireframe':
                self._Property.SetRepresentationToWireframe()
            elif arg.lower() == 'surface':
                self._Property.SetRepresentationToSurface()
            elif arg.lower() == 'toggle':
                r = (self._Property.GetRepresentation() + 1) % 3
                self.rep(('points', 'wireframe', 'surface')[r])
        return ('points', 'wireframe', 'surface')[self._Property.GetRepresentation()]

    def shade(self, arg=None):
        self.view.updateInTime()
        if arg is True:
            self._Shade = True
            self._Property.SetAmbient(0.1)
            self._Property.SetDiffuse(0.9)
        elif arg is False:
            self._Shade = False
            self._Property.SetAmbient(1)
            self._Property.SetDiffuse(0)
        return self._Shade

    def size(self, **kwargs):
        self.view.updateInTime()
        if 'point' in kwargs:
            self._Property.SetPointSize(kwargs['point'])
        if 'line' in kwargs:
            self._Property.SetLineWidth(kwargs['line'])
        return {'point': self._Property.GetPointSize(),
                'line': self._Property.GetLineWidth()}


class ImageSlice(QObject, Menu, Mouse):
    """场景表示，图像数据的断层表示
    vtk.vtkImageData -> vtk.vtkImageSlice"""

    def __init__(self, view: View, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('图面 （Image slice)')
        Menu.__init__(self, name=self.name)
        self.actions['WindowAuto'] = self.menu.addAction(self.tr('自动窗 (Auto window)'))
        self.actions['WindowAuto'].triggered.connect(self.setWindowAuto)
        self.actions['WindowBone'] = self.menu.addAction(self.tr('骨骼窗 (Bone window)'))
        self.actions['WindowBone'].triggered.connect(self.setWindowBone)
        self.actions['WindowSoft'] = self.menu.addAction(self.tr('组织窗 (Soft window)'))
        self.actions['WindowSoft'].triggered.connect(self.setWindowSoft)

        self.view = view
        Mouse.__init__(self, view=self.view, menu=self)
        self.mouse['NoButton']['Wheel'] = self.slice
        self.mouse['LeftButton']['PressMove'] = self.window

        self._Mapper = vtk.vtkImageResliceMapper()
        self._Prop = vtk.vtkImageSlice()
        self._Prop._Prop = self
        self.view._Renderer.AddViewProp(self._Prop)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToCubic()
        self._Property.SetUseLookupTableScalarRange(1)

        self._Dataset = vtk.vtkImageData()
        self._BindDataset = self

        self._SlicePlane = vtk.vtkPlane()
        self._BindSlicePlane = self

        self._LookupTable = vtk.vtkLookupTable()
        self._BindLookupTable = self

        self._WindowWidth = self._WindowLevel = 400

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()
        self.setWindowSoft()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vio.loads(s['_Dumps']['_Dataset']))
        self._LookupTable.DeepCopy(vio.loads(s['_Dumps']['_LookupTable']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vio.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()
        self.bindSlicePlane()
        self.bindLookupTable()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vio.dumps(self._Dataset),
                       '_LookupTable': vio.dumps(self._LookupTable)}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vio.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property', '_SlicePlane']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def bindSlicePlane(self, other=None):
        if hasattr(other, '_SlicePlane'):
            self._BindSlicePlane = other
        self._Mapper.SetSlicePlane(self._BindSlicePlane._SlicePlane)
        self.view.updateInTime()

    def bindLookupTable(self, other=None):
        if hasattr(other, '_LookupTable'):
            self._BindLookupTable = other
        self._Property.SetLookupTable(self._BindLookupTable._LookupTable)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self._Dataset.ShallowCopy(self._Dataset.__class__())
        elif hasattr(other, '_Dataset'):
            self._Dataset.ShallowCopy(other._Dataset)
        elif isinstance(other, self._Dataset.__class__):
            self._Dataset.ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def delete(self, *args):
        self._Dataset.ReleaseData()
        self.view._Renderer.RemoveViewProp(self._Prop)

    def setSlicePlane(self, preset=None, origin=None, normal=None):
        if isinstance(origin, str):
            if origin.lower() == 'c':
                o = self._BindDataset._Dataset.GetCenter()
                self._BindSlicePlane._SlicePlane.SetOrigin(o[0], o[1], o[2])
            elif origin.lower() in ('b0', 'b1', 'b2', 'b3', 'b4', 'b5'):
                i = int(origin[-1])
                o = list(self._BindDataset._Dataset.GetCenter())
                o[int(i / 2)] = self._BindDataset._Dataset.GetBounds()[i]
                self._BindSlicePlane._SlicePlane.SetOrigin(o[0], o[1], o[2])
        elif origin is not None:
            self._BindSlicePlane._SlicePlane.SetOrigin(origin[0], origin[1], origin[2])
        if isinstance(normal, str):
            if normal.lower() == 'sagittal':
                self._BindSlicePlane._SlicePlane.SetNormal(1, 0, 0)
            elif normal.lower() == 'coronal':
                self._BindSlicePlane._SlicePlane.SetNormal(0, 1, 0)
            elif normal.lower() == 'axial':
                self._BindSlicePlane._SlicePlane.SetNormal(0, 0, 1)
        elif normal is not None:
            self._BindSlicePlane._SlicePlane.SetNormal(normal[0], normal[1], normal[2])
        self.view.updateInTime()

    def setWindow(self, preset=None, width=None, level=None):
        if preset is None:
            if width is not None:
                self._WindowWidth = width
            if level is not None:
                self._WindowLevel = level

            self._WindowWidth = int(self._WindowWidth)
            self._WindowLevel = int(self._WindowLevel)

            r = [self._WindowLevel - 0.5 * self._WindowWidth,
                 self._WindowLevel + 0.5 * self._WindowWidth]

            t = self._BindLookupTable._LookupTable
            t.SetNumberOfTableValues(self._WindowWidth)
            t.SetTableRange(r)
            t.SetBelowRangeColor(0, 0, 0, 1.0)
            t.SetAboveRangeColor(1, 1, 1, 1.0)
            t.SetUseBelowRangeColor(1)
            t.SetUseAboveRangeColor(1)

            for i in range(self._WindowWidth):
                v = i / self._WindowWidth
                t.SetTableValue(i, (v, v, v, 1.0))
            self.view.updateInTime()

        elif preset.lower() == 'auto':
            r = vtk.vtkImageHistogramStatistics()
            r.SetInputData(self._BindDataset._Dataset)
            r.SetAutoRangePercentiles(1, 99)
            r.SetGenerateHistogramImage(0)
            r.Update()
            r = r.GetAutoRange()

            self.setWindow(width=r[1] - r[0], level=0.5 * (r[0] + r[1]))
        elif preset.lower() == 'bone':
            self.setWindow(width=1000, level=400)
        elif preset.lower() == 'soft':
            self.setWindow(width=350, level=50)

    def setWindowAuto(self, **kwargs):
        self.setWindow('auto')

    def setWindowBone(self, **kwargs):
        self.setWindow('bone')

    def setWindowSoft(self, **kwargs):
        self.setWindow('soft')

    def slice(self, **kwargs):
        o = list(self._BindSlicePlane._SlicePlane.GetOrigin())
        n = self._BindSlicePlane._SlicePlane.GetNormal()
        dim = self._BindDataset._Dataset.GetDimensions()
        dxyz = self._BindDataset._Dataset.GetSpacing()

        n = [abs(_) / (n[0] ** 2 + n[1] ** 2 + n[2] ** 2) ** 0.5 for _ in n]
        dn = n[0] * dxyz[0] + n[1] * dxyz[1] + n[2] * dxyz[2]

        for i in range(3):
            if dim[i] > 1:
                o[i] += kwargs['delta'] * dn * n[i]

        if vtk.vtkMath.PlaneIntersectsAABB(self._Dataset.GetBounds(), n, o) == 0:
            self.setSlicePlane(origin=o)

    def window(self, **kwargs):
        dx, dy = self.view.mouseOverDisplay()

        r = self._Dataset.GetScalarRange()
        t = (r[1] - r[0]) / 2048
        self._WindowWidth += t * dx
        self._WindowLevel -= t * dy

        self._WindowWidth = max(self._WindowWidth, 0)
        self._WindowWidth = min(self._WindowWidth, r[1] - r[0])
        self._WindowLevel = max(self._WindowLevel, r[0])
        self._WindowLevel = min(self._WindowLevel, r[1])
        self.setWindow()


class ImageVolume(QObject, Menu, Mouse):
    """场景表示，图像数据的立体表示
    vtk.vtkImageData -> vtk.vtkVolume"""

    def __init__(self, view: View, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('图体 （Image volume)')
        Menu.__init__(self, name=self.name)

        self.view = view
        Mouse.__init__(self, view=self.view, menu=self)

        self._Mapper = vtk.vtkGPUVolumeRayCastMapper()
        self._Prop = vtk.vtkVolume()
        self._Prop._Prop = self
        self.view._Renderer.AddVolume(self._Prop)

        self._Mapper.SetBlendModeToComposite()
        self._Mapper.SetMaxMemoryInBytes(4096)
        self._Mapper.SetMaxMemoryFraction(1)
        self._Mapper.SetAutoAdjustSampleDistances(0)
        self._Mapper.SetLockSampleDistanceToInputSpacing(1)
        self._Mapper.SetUseJittering(1)

        self._Property = self._Prop.GetProperty()
        self._Property.SetInterpolationTypeToLinear()
        self._Property.SetAmbient(0.1)
        self._Property.SetDiffuse(0.9)
        self._Property.SetShade(1)

        self._Dataset = vtk.vtkImageData()
        self._BindDataset = self

        self._Color = {0: (1, 1, 1)}
        self._ScalarOpacity = {0: 0, 400: 1}
        self._GradientOpacity = {}

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

        self._Dataset.DeepCopy(vio.loads(s['_Dumps']['_Dataset']))
        del s['_Dumps']

        for kw in s['_VTKGets']:
            vio.vtkset(getattr(self, kw), s['_VTKGets'][kw])
        del s['_VTKGets']

        self.bindDataset()
        self.setColor()
        self.setScalarOpacity()
        self.setGradientOpacity()

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_Dumps'] = {'_Dataset': vio.dumps(self._Dataset),
                       '_Color': self._Color}
        for kw in s['_Dumps']:
            del s[kw]

        s['_VTKGets'] = {name: vio.vtkget(getattr(self, name)) for name in
                         ['_Mapper', '_Prop', '_Property']}
        for kw in s['_VTKGets']:
            del s[kw]

        return s

    def bindDataset(self, other=None):
        if hasattr(other, '_Dataset'):
            self._BindDataset = other
        self._Mapper.SetInputData(self._BindDataset._Dataset)
        self._Prop.SetMapper(self._Mapper)
        self.view.updateInTime()

    def clone(self, other):
        if other is None:
            self._Dataset.ShallowCopy(self._Dataset.__class__())
        elif hasattr(other, '_Dataset'):
            self._Dataset.ShallowCopy(other._Dataset)
        elif isinstance(other, self._Dataset.__class__):
            self._Dataset.ShallowCopy(other)
        else:
            raise TypeError(type(other))

    def delete(self):
        self._Dataset.ReleaseData()
        self.view._Renderer.RemoveVolume(self._Prop)

    def setColor(self, scalar_rgb=None):
        if scalar_rgb is None:
            f = vtk.vtkColorTransferFunction()
            for x in self._Color:
                r, g, b = self._Color[x]
                f.AddRGBPoint(x, r, g, b)
            self._Property.SetColor(f)
        else:
            self._Color = scalar_rgb
            self.setColor()

    def setScalarOpacity(self, scalar_opacity=None):
        if scalar_opacity is None:
            f = vtk.vtkPiecewiseFunction()
            for x in self._ScalarOpacity:
                f.AddPoint(x, self._ScalarOpacity[x])
            self._Property.SetScalarOpacity(f)
        else:
            self._Color = scalar_opacity
            self.setScalarOpacity()

    def setGradientOpacity(self, gradient_opacity=None):
        if gradient_opacity is None:
            f = vtk.vtkPiecewiseFunction()
            for x in self._GradientOpacity:
                f.AddPoint(x, self._GradientOpacity[x])
            self._Property.SetGradientOpacity(f)
        else:
            self._Color = gradient_opacity
            self.setGradientOpacity()


class RegionEdit(QObject, Menu, Mouse):
    def __init__(self, view: View, name=None):
        QObject.__init__(self)

        self.name = name if name else self.tr('区域编辑 (Region edit)')
        Menu.__init__(self, name=self.name)
        self.actions['Activate'] = self.menu.addAction(self.tr('激活 (Activate)'))
        self.actions['Activate'].triggered.connect(self.activate)
        self.actions['Cancel'] = self.menu.addAction(self.tr('取消 (Cancel)'))
        self.actions['Cancel'].triggered.connect(self.cancel)
        self.actions['Apply'] = self.menu.addAction(self.tr('应用 (Apply)'))
        self.actions['Apply'].triggered.connect(self.apply)

        def aboutToShow():
            self.actions['Activate'].setEnabled(not self.activated())
            self.actions['Cancel'].setEnabled(self.activated())
            self.actions['Apply'].setEnabled(len(self.nodes) > 2)
        self.menu.aboutToShow.connect(aboutToShow)

        self.view = view
        Mouse.__init__(self, view=self.view, menu=self)
        self.mouse['LeftButton']['PressRelease'] = self.addNode

        self.nodes = []
        self.path = PolyActor(self.view)
        self.path.color(rgb=(1, 0.2, 0.2))
        self.path.size(line=3)
        self.path.alwaysOnTop(True)

        self.nodes = []

    def __setstate__(self, s):
        self.__init__(s['view'], s['name'])
        self.__dict__.update(s)
        s = self.__dict__

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '__METAOBJECT__']:
            if kw in s:
                del s[kw]
        return s

    def activate(self):
        self.view.activated = self

    def activated(self):
        return self.view.activated is self

    def apply(self):
        self.view.activated = None

    def cancel(self):
        self.view.activated = None
        self.path.clone(None)
        self.view.updateInTime()

    def addNode(self, **kwargs):
        self.nodes.append(self.view.pickFPlane(self.view.mousePos()))
        node = PolyActor(self.view)
        return

    def rebuild(self):
        print(self)
