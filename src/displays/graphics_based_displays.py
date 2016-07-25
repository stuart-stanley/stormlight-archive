# todo: ABC for all displays. Maybe auto-detect fake vs real
from .display_base import DisplayDriver, LEDThing, Gradient
import vtk

class GraphicsDisplay(DisplayDriver):
    def __init__(self):
        self.__renderer = vtk.vtkRenderer()
        self.__rend_win = vtk.vtkRenderWindow()
        self.__rend_win.SetSize(1280, 1024)
        self.__rend_win.AddRenderer(self.__renderer)
        self.__rend_win_interactor = vtk.vtkRenderWindowInteractor()
        self.__rend_win_interactor.SetRenderWindow(self.__rend_win)
        self.__update_list = []
        self.__xxx_color = 10
        width, height = self.__rend_win.GetSize()
        #print self.__rend_win.GetSize()
        #super(GraphicsDisplay, self).__init__(width, height)
        super(GraphicsDisplay, self).__init__()

    def _led_display_context(self, led):
        assert isinstance(led, LEDThing), \
            '{0} must be an LEDThing'.format(led)
        source = vtk.vtkSphereSource()
        source.SetCenter(led.x, led.y, led.z)
        source.SetRadius(led.radius)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(source.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        self.__renderer.AddActor(actor)
        return actor

    def _start_update(self):
        self.__update_list = []

    def _add_set_to_update(self, led):
        self.__update_list.append((led,
                                   (led.red / 255.0, led.green / 255.0, led.blue / 255.0)))

    def _complete_update(self):
        #print "start _complete_update"
        for led, color in self.__update_list:
            actor = led.display_context
            actor.GetProperty().SetColor(color[0], color[1], color[2])

        #print("end _complete_update")
        self.__rend_win.Render()
        self.__update_list = []
        

    def __tick_callback(self, obj, event):
        c = self.__xxx_color
        rg = Gradient(c, 5)
        gg = Gradient(c, -5)
        bg = Gradient(c, 0)

        self.set_gradient(rg, gg, bg)
        c += 10
        if c > 255:
            c = 0
        self.__xxx_color = c
        print "tick", c

    def run(self, algo_tick_callback):
        self.__rend_win_interactor.Initialize()
        self.__rend_win.Render()
        self.__rend_win_interactor.AddObserver('TimerEvent', algo_tick_callback)
        timer_id = self.__rend_win_interactor.CreateRepeatingTimer(1)
        self.__rend_win_interactor.Start()

        
