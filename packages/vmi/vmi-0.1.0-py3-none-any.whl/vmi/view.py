import sys
from typing import Dict, Any

import vtk
import numpy.linalg as npl
from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtOpenGL import QGLWidget
from PySide2.QtWidgets import *

from vmi import vio


class Mouse:
    def __init__(self, view=None, menu=None):
        self._Enter = self._Leave = self._Wheel = self._Move = self.pass_
        self._LeftButtonPress = self._LeftButtonPressMove = self.pass_
        self._LeftButtonPressMoveRelease = self._LeftButtonPressRelease = self.pass_
        self._MidButtonPress = self._MidButtonPressMove = self.pass_
        self._MidButtonPressMoveRelease = self._MidButtonPressRelease = self.pass_
        self._RightButtonPress = self._RightButtonPressMove = self.pass_
        self._RightButtonPressMoveRelease = self._RightButtonPressRelease = self.pass_

        self.mouse = {
            'NoButton': {
                'Enter': self._Enter,
                'Leave': self._Leave,
                'Wheel': self._Wheel,
                'Move': self._Move},
            'LeftButton': {
                'Press': self._LeftButtonPress,
                'PressMove': self._LeftButtonPressMove,
                'PressMoveRelease': self._LeftButtonPressMoveRelease,
                'PressRelease': self._LeftButtonPressRelease},
            'MidButton': {
                'Press': self._MidButtonPress,
                'PressMove': self._MidButtonPressMove,
                'PressMoveRelease': self._MidButtonPressMoveRelease,
                'PressRelease': self._MidButtonPressRelease},
            'RightButton': {
                'Press': self._RightButtonPress,
                'PressMove': self._RightButtonPressMove,
                'PressMoveRelease': self._RightButtonPressMoveRelease,
                'PressRelease': self._RightButtonPressRelease}}

        if view:
            for b in self.mouse:
                for e in self.mouse[b]:
                    self.mouse[b][e] = view.mouse[b][e]

        if menu:
            self.mouse['RightButton']['PressRelease'] = menu.execMenu

    @staticmethod
    def pass_(**kwargs):
        return 'pass'


class Menu:
    def __init__(self, name=None):
        self.menu = QMenu()
        self.actions: Dict[str, QAction] = {}

        if name:
            self.menu.setTitle(name)

    def execMenu(self, **kwargs):
        self.menu.exec_(QCursor.pos())


class View(QGLWidget, Menu, Mouse):
    """vtk场景"""

    def __init__(self, name=None, parent=None):
        QGLWidget.__init__(self, parent)

        self.name = name if name else self.tr('视图 (View)')
        Menu.__init__(self, name=self.name)
        self.actions['ResetFOV'] = self.menu.addAction(self.tr('重置视野 (Reset FOV)'))
        self.actions['ResetFOV'].triggered.connect(self.resetFOV)

        Mouse.__init__(self, view=self, menu=self)
        self.mouse['LeftButton']['PressMove'] = self.mouseButtonRotateFocal
        self.mouse['MidButton']['PressMove'] = self.mouseButtonPan
        self.mouse['RightButton']['PressMove'] = self.mouseButtonZoom

        rect = QGuiApplication.screens()[0].geometry()
        rect = QRect(rect.center() - QPoint(800, 450), QSize(1600, 900))
        self.setGeometry(rect)
        self.setAttribute(Qt.WA_OpaquePaintEvent)
        self.setAttribute(Qt.WA_PaintOnScreen)
        self.setFocusPolicy(Qt.WheelFocus)
        self.setMouseTracking(True)

        # 渲染器
        self._Renderer = vtk.vtkRenderer()
        self._Renderer.SetUseHiddenLineRemoval(1)  # 隐线消除
        self._Renderer.SetUseFXAA(False)  # 快速近似抗锯齿
        self._Renderer.SetBackground(1, 1, 1)

        # 渲染窗口
        self._RenderWindow = vtk.vtkRenderWindow()
        self._RenderWindow.SetWindowInfo(str(int(self.winId())))
        self._RenderWindow.AddRenderer(self._Renderer)

        # 交互器
        self._Interactor = vtk.vtkGenericRenderWindowInteractor()
        self._Interactor.SetRenderWindow(self._RenderWindow)
        self._Interactor.Initialize()

        # 方位标
        self._OrientationMarker = init_orientation_marker(self._Interactor)

        # 照相机
        self._Camera = self.camera()
        self.camera().SetParallelProjection(True)  # 平行投影

        # 拾取器
        self._Picker = vtk.vtkPicker()
        self._PickerProp = vtk.vtkPropPicker()
        self._PickerPoint = vtk.vtkPointPicker()
        self._PickerCell = vtk.vtkCellPicker()
        self._Picker.SetTolerance(0.005)
        self._PickerPoint.SetTolerance(0.005)
        self._PickerCell.SetTolerance(0.005)

        # 刷新计时器
        self._Timer = QTimer(self)
        self._Timer.timeout.connect(self.timeout)
        self._Timer.start(10)

        self._Time = QTime()
        self._Time.start()
        self._FPS = self._UpdateSum = 0

        # 创建一个隐藏控件，当销毁时调用清理vtk元素
        self._Hidden = QWidget(self)
        self._Hidden.hide()
        self._Hidden.destroyed.connect(self.delete)

        # 更新请求
        self._UpdateAtOnce: bool = False

        # 鼠标位置
        self._DblClick = ''
        self._MousePosLast: QPoint = QPoint(0, 0)
        self._MousePos: QPoint = QPoint(0, 0)

        # 鼠标正在交互的对象
        self.activated = None
        self._PropEnter: vtk.vtkProp = None
        self._WidgetEnter: View = None

        # 鼠标按键状态
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

    def __setstate__(self, s):
        self.__init__(s['name'])
        self.__dict__.update(s)

        for kw in s['_VTKGets']:
            vio.vtkset(getattr(self, kw), s['_VTKGets'][kw])

    def __getstate__(self):
        s = self.__dict__.copy()
        for kw in ['menu', 'actions', '_OrientationMarker', '_Timer', '_Hidden', '__METAOBJECT__']:
            if kw in s:
                del s[kw]

        s['_VTKGets'] = {name: vio.vtkget(getattr(self, name)) for name in
                         ['_RenderWindow', '_Renderer', '_Interactor', '_Camera',
                          '_Picker', '_PickerProp', '_PickerPoint', '_PickerCell']}

        for kw in s['_VTKGets']:
            del s[kw]
        return s

    def camera(self, *args):
        if len(args) == 0:
            return self._Renderer.GetActiveCamera()
        elif len(args) > 0:
            fp = list(self.camera().GetFocalPoint())
            cp = list(self.camera().GetPosition())
            up = list(self.camera().GetViewUp())

            look, right = [fp[i] - cp[i] for i in range(3)], [0] * 3

            vtk.vtkMath.Cross(look, up, right)
            vtk.vtkMath.Normalize(look)
            vtk.vtkMath.Normalize(right)
            vtk.vtkMath.Normalize(up)

            t, value = [], {'focal': fp, 'position': cp, 'up': up, 'look': look, 'right': right}
            for key in args:
                if key in value.keys():
                    t.append(value[key])
            if len(t) == 1:
                t = t[0]
            return t

    def closeEvent(self, ev):
        self.delete()

    def delete(self):
        self._Timer.stop()
        self._RenderWindow.Finalize()

    def entered(self):
        """返回鼠标悬停状态，在物体上->prop/在场景内->vmi/在场景外->None"""
        return self._PropEnter if self._PropEnter else (self._WidgetEnter if self._WidgetEnter else self)

    def enterEvent(self, ev):
        self._WidgetEnter = self
        c, b, e = self, 'NoButton', 'Enter'
        if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
            c.mouse[b][e](caller=c, event=e, button=b)

        self._PropEnter, *_ = self.pickProp(ev.pos())
        if self._PropEnter:
            c = self._PropEnter
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                c.mouse[b][e](caller=c, event=e, button=b)

    def leaveEvent(self, ev):
        if self._WidgetEnter:
            c, b, e = self, 'NoButton', 'Leave'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                c.mouse[b][e](caller=c, event=e, button=b)
        if self._PropEnter:
            c, b, e = self._PropEnter, 'NoButton', 'Leave'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                c.mouse[b][e](caller=c, event=e, button=b)
        self._WidgetEnter = self._PropEnter = None
        self._ButtonPress = self._ButtonPressMove = 'NoButton'

    def mouseButtonRotateFocal(self, **kwargs):
        if kwargs['event'] == 'PressMove':
            dx, dy = self.mouseOverDisplay()
            rx, ry = -200 * dx / self.height(), 200 * dy / self.width()
            self.camera().Azimuth(rx)
            self.camera().Elevation(ry)
            self.camera().OrthogonalizeViewUp()
            self.updateInTime()

    def mouseButtonPan(self, **kwargs):
        if kwargs['event'] == 'PressMove':
            dp = self.mouseOverFPlane()
            fp, cp = self.camera('focal', 'position')
            fp = [fp[i] - dp[i] for i in range(3)]
            cp = [cp[i] - dp[i] for i in range(3)]
            self.camera().SetFocalPoint(fp)
            self.camera().SetPosition(cp)

            if self._Interactor.GetLightFollowCamera():
                self._Renderer.UpdateLightsGeometryToFollowCamera()

            self.updateInTime()

    def mouseButtonZoom(self, **kwargs):
        if kwargs['event'] == 'PressMove':
            c = self._Renderer.GetCenter()
            _, dy = self.mouseOverDisplay()
            factor = 1.1 ** (10 * -dy / c[1])

            if self.camera().GetParallelProjection():
                self.camera().SetParallelScale(self.camera().GetParallelScale() / factor)
            else:
                self.camera().Dolly(factor)

            if self._Interactor.GetLightFollowCamera():
                self._Renderer.UpdateLightsGeometryToFollowCamera()

            self.updateInTime()

    def mouseMoveEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            prop, *_ = self.pickProp(ev.pos())
            last_prop, self._PropEnter = self._PropEnter, prop

            if not last_prop and not prop:
                c, b, e = self, 'NoButton', 'Move'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
            elif not last_prop and prop:
                c, b, e = prop, 'NoButton', 'Enter'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and not prop:
                c, b, e = last_prop, 'NoButton', 'Leave'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and prop and last_prop is prop:
                c, b, e = prop, 'NoButton', 'Move'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
            elif last_prop and prop and last_prop is not prop:
                c, b, e = last_prop, 'NoButton', 'Leave'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
                c, b, e = prop, 'NoButton', 'Enter'
                if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                    c.mouse[b][e](caller=c, event=e, button=b)
        elif self._MousePosLast != self._MousePos:
            self._ButtonPressMove = self._ButtonPress
            c, b, e = self.entered(), self._ButtonPressMove, 'PressMove'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                c.mouse[b][e](caller=c, event=e, button=b)

    def mouseOverDisplay(self):
        """返回鼠标位移向量
        -> (dx, dy)"""
        return self._MousePos.x() - self._MousePosLast.x(), self._MousePos.y() - self._MousePosLast.y()

    def mouseOverFPlane(self):
        """返回鼠标在焦平面上的位移向量
        -> (x, y, z)"""
        pt = self.pickFPlane(self._MousePos)
        ptLast = self.pickFPlane(self._MousePosLast)
        return [pt[i] - ptLast[i] for i in range(3)]

    def mousePos(self):
        """返回当前鼠标位置"""
        return self._MousePos

    def mousePosLast(self):
        """返回上一鼠标位置"""
        return self._MousePosLast

    def mousePressEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if self._ButtonPress == 'NoButton':
            self._ButtonPress = ev.button().name.decode()
            if ev.type() == QEvent.Type.MouseButtonDblClick:
                self._DblClick = 'Double'

            c, b, e = self.entered(), self._ButtonPress, 'Press'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b,
                                                                          double=self._DblClick):
                c.mouse[b][e](caller=c, event=e, button=b, double=self._DblClick)

    def mouseReleaseEvent(self, ev):
        self._MousePosLast, self._MousePos = self._MousePos, ev.pos()

        if ev.button().name.decode() == self._ButtonPressMove:
            c, b, e = self.entered(), self._ButtonPressMove, 'PressMoveRelease'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b):
                c.mouse[b][e](caller=c, event=e, button=b)
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
        elif ev.button().name.decode() == self._ButtonPress:
            c, b, e = self.entered(), self._ButtonPress, 'PressRelease'
            if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b,
                                                                          double=self._DblClick):
                c.mouse[b][e](caller=c, event=e, button=b, double=self._DblClick)
            self._ButtonPress = self._ButtonPressMove = 'NoButton'
            self._DblClick = ''

    def paintEngine(self):
        return None

    def paintEvent(self, ev):
        self._Interactor.Render()

    def pick(self, pos: QPoint, picker):
        """拾取场景对象"""

        picker.Pick(pos.x(), self.height() - pos.y(), 0, self._Renderer)
        prop = picker.GetViewProp()
        prop = prop._Prop if prop else None
        return prop, picker.GetPickPosition(), picker

    def pickBBox(self, pos: QPoint):
        """拾取场景对象的包围盒
        pickBBox(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._Picker)

    def pickCell(self, pos: QPoint):
        """拾取场景对象的单元
        pickCell(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerCell)

    def pickFPlane(self, pos: QPoint):
        """拾取场景的焦平面
        pickFPlane(QPoint(x, y)) -> (x, y, z)"""
        t = [0] * 4
        vtk.vtkInteractorObserver.ComputeDisplayToWorld(
            self._Renderer, pos.x(), self.height() - pos.y(), 0, t)
        pt = [_ / t[3] for _ in t[:3]]

        fp, look = self.camera('position', 'look')
        vtk.vtkPlane.ProjectPoint(pt, fp, look, pt)
        return pt

    def pickPoint(self, pos: QPoint):
        """拾取场景对象的点
        pickPoint(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerPoint)

    def pickProp(self, pos: QPoint):
        """拾取场景对象
        pickProp(QPoint(x, y)) -> (x, y, z)"""
        return self.pick(pos=pos, picker=self._PickerProp)

    def pickToDisplay(self, pt: list):
        """拾取的场景坐标转换为屏幕坐标
        pickToDisplay((x, y, z) -> QPoint(x, y)"""
        t = [0] * 3
        vtk.vtkInteractorObserver.ComputeWorldToDisplay(
            self._Renderer, pt[0], pt[1], pt[2], t)
        return QPoint(t[0], self.height() - t[1])

    def resizeEvent(self, ev):
        w = self.width()
        h = self.height()
        vtk.vtkRenderWindow.SetSize(self._RenderWindow, w, h)
        self._Interactor.SetSize(w, h)
        self._Interactor.ConfigureEvent()
        self.update()

    def setCamera(self, *args, face=None, b6=None, focal=None):
        if face is not None:
            face = face.lower()
            vu = {'sagittal': [0, 0, 1],
                  'coronal': [0, 0, 1],
                  'axial': [0, -1, 0]}[face]
            vr = {'sagittal': [0, -1, 0],
                  'coronal': [1, 0, 0],
                  'axial': [1, 0, 0]}[face]
            vl = [0] * 3
            vtk.vtkMath.Cross(vu, vr, vl)

            fp = self.camera('focal')
            d = self.camera().GetDistance()
            cp = [fp[i] - d * vl[i] for i in range(3)]

            self.camera().SetPosition(cp)
            self.camera().SetFocalPoint(fp)
            self.camera().SetViewUp(vu)
            self._Renderer.ResetCameraClippingRange()
        if b6 is not None:
            if isinstance(b6, str) and b6.lower() == 'all':
                b6 = self._Renderer.ComputeVisiblePropBounds()
            b6 = list(b6)

            if focal is not None:
                c = [0.5 * (b6[0] + b6[1]), 0.5 * (b6[2] + b6[3]), 0.5 * (b6[4] + b6[5])]
                c = [focal[i] - c[i] for i in range(3)]
                for i in range(3):
                    if c[i] < 0:
                        b6[2 * i] += 2 * c[i]
                    else:
                        b6[2 * i + 1] += 2 * c[i]

            dxyz = b6[1] - b6[0], b6[3] - b6[2], b6[5] - b6[4]
            self._Renderer.ResetCamera(b6)

            vr, vu = self.camera('right', 'up')
            dr = [abs(_) / npl.norm(vr) for _ in vr]
            dr = dr[0] * dxyz[0] + dr[1] * dxyz[1] + dr[2] * dxyz[2]
            dr = dr if dr != 0 else 1
            du = [abs(_) / npl.norm(vu) for _ in vu]
            du = du[0] * dxyz[0] + du[1] * dxyz[1] + du[2] * dxyz[2]
            du = du if du != 0 else 1

            scale = 0.5 * du
            if du / dr < self.height() / self.width():
                scale = 0.5 * dr * self.height() / self.width()
            self.camera().SetParallelScale(scale)
        if focal is not None:
            vl = self.camera('look')
            b6 = self._Renderer.ComputeVisiblePropBounds()
            d = 0.5 * ((b6[1] - b6[0]) ** 2 + (b6[3] - b6[2]) ** 2 + (b6[5] - b6[4]) ** 2) ** 0.5
            cp = [focal[i] - d * vl[i] for i in range(3)]

            self.camera().SetPosition(cp)
            self.camera().SetFocalPoint(focal)
            self._Renderer.ResetCameraClippingRange()
        self.updateInTime()

    def resetFOV(self, **kwargs):
        self.setCamera(b6='all')

    def setOrientationMarkerVisible(self, arg: bool):
        """显示/隐藏方位标"""
        self._OrientationMarker.GetOrientationMarker().SetVisibility(arg)
        self.updateInTime()

    def sizeHint(self):
        return QSize(1600, 900)

    def timeout(self):
        if self._UpdateAtOnce:
            self.updateAtOnce()
        self._UpdateSum += 1

        if self._Time.elapsed() > 0.5e3:
            self._FPS = 1000 * self._UpdateSum / self._Time.elapsed()
            self.setWindowTitle(QApplication.applicationName() + ' FPS: {:.0f}'.format(self._FPS))
            self._Time.restart()
            self._UpdateSum = 0

    def updateInTime(self):
        """及时刷新视图"""
        self._UpdateAtOnce = True

    def updateAtOnce(self):
        if self._Timer.isActive():
            self._UpdateAtOnce = False
            self._Renderer.ResetCameraClippingRange()
            self._RenderWindow.Render()

    def wheelEvent(self, ev):
        d = ev.delta() / 120
        c, b, e = self.entered(), 'NoButton', 'Wheel'
        if not self.activated or 'pass' == self.activated.mouse[b][e](caller=c, event=e, button=b, delta=d):
            c.mouse[b][e](caller=c, event=e, button=b, delta=d)


def init_orientation_marker(i):
    """
    :param i: vtk.vtkRenderWindowInteractor
    :return: vtk.vtkOrientationMarkerWidget
    """

    vtk.vtkMapper.SetResolveCoincidentTopologyToPolygonOffset()

    cube = vtk.vtkAnnotatedCubeActor()
    cube.SetFaceTextScale(0.65)
    cube.SetXPlusFaceText("L")
    cube.SetXMinusFaceText("R")
    cube.SetYPlusFaceText("P")
    cube.SetYMinusFaceText("A")
    cube.SetZPlusFaceText("S")
    cube.SetZMinusFaceText("I")

    prop = cube.GetCubeProperty()
    prop.SetColor(0.75, 0.75, 1)

    prop = cube.GetTextEdgesProperty()
    prop.SetLineWidth(1)
    prop.SetDiffuse(0)
    prop.SetAmbient(1)
    prop.SetColor(0, 0, 0)

    prop = cube.GetXPlusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetXMinusFaceProperty()
    prop.SetColor(1, 0, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYPlusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetYMinusFaceProperty()
    prop.SetColor(0, 1, 0)
    prop.SetInterpolationToFlat()
    prop = cube.GetZPlusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()
    prop = cube.GetZMinusFaceProperty()
    prop.SetColor(0, 0, 1)
    prop.SetInterpolationToFlat()

    axes = vtk.vtkAxesActor()

    axes.SetShaftTypeToCylinder()
    axes.SetXAxisLabelText("X")
    axes.SetYAxisLabelText("Y")
    axes.SetZAxisLabelText("Z")

    axes.SetTotalLength(1.5, 1.5, 1.5)
    axes.SetCylinderRadius(0.500 * axes.GetCylinderRadius())
    axes.SetConeRadius(1.025 * axes.GetConeRadius())
    axes.SetSphereRadius(1.500 * axes.GetSphereRadius())

    prop = axes.GetXAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(1, 0, 0)

    prop = axes.GetYAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 1, 0)

    prop = axes.GetZAxisCaptionActor2D().GetCaptionTextProperty()
    prop.BoldOn()
    prop.ItalicOn()
    prop.ShadowOn()
    prop.SetFontFamilyToArial()
    prop.SetColor(0, 0, 1)

    assembly = vtk.vtkPropAssembly()
    assembly.AddPart(axes)
    assembly.AddPart(cube)

    ort = vtk.vtkOrientationMarkerWidget()
    ort.SetOrientationMarker(assembly)
    ort.SetViewport(0.0, 0.0, 0.2, 0.2)
    ort.SetInteractor(i)
    ort.SetEnabled(1)
    ort.SetInteractive(0)
    ort.On()

    return ort


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setOrganizationName('vmi')
    app.setApplicationName('vmi')

    w = View()
    w.show()
    w._Renderer.SetBackground(1, 0.5, 0.5)

    import shelve

    with shelve.open('C:/Users/Medraw/Desktop/d') as db:
        db['w'] = w

    with shelve.open('C:/Users/Medraw/Desktop/d') as db:
        v = db['w']
        v.show()

    sys.exit(app.exec_())
