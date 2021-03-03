from manim import *
import math

class convolutionAnimation(GraphScene):
    def __init__(self, **kwargs):
        GraphScene.__init__(
            self,
            x_min=-10,
            x_max=10,
            num_graph_anchor_points=100,
            y_min=-5,
            y_max=5,
            graph_origin=ORIGIN,
            x_axis_label='$u$',
            y_axis_label='',
            exclude_zero_label=False,
            **kwargs
        )
        self.function_color = RED

    def construct(self):

        self.setup_axes(animate=True)

        x = self.get_graph(lambda u: math.sin(0.9 * u) - 2, x_min=-10, x_max=10)
        y = self.get_graph(lambda u: math.cos(1/4 * u - 1) + 2, x_min=-10, x_max=10)
        x_path = self.get_graph(lambda u: math.sin(0.9 * u) - 2, x_min=-5, x_max=7)
        y_path = self.get_graph(lambda u: math.cos(1/4 * u - 1) + 2, x_min=7, x_max=-5)

        x_label = self.get_graph_label(x, label="x")
        y_label = self.get_graph_label(y, label="y")
        t_label_prev = MathTex(r"t = 2", color=YELLOW).move_to(3 * UR)

        convolution = MathTex(r"(x*y)(t) = \int_{-\infty}^{+\infty}x(u)y(t-u)du").move_to(3 * UL).scale(0.7)
        
        self.play(FadeIn(x), FadeIn(x_label), run_time=0.5)
        self.play(FadeIn(y), FadeIn(y_label), run_time=0.5)
        self.play(FadeIn(convolution))

        line_left_x = Line(self.input_to_graph_point(-5, x), self.input_to_graph_point(-5, y), color=ORANGE)
        line_right_x = Line(self.input_to_graph_point(5, x), self.input_to_graph_point(5, y), color=ORANGE)
        self.play(ShowCreation(line_left_x), ShowCreation(line_right_x))

        point_x = Dot().move_to(x.points[0])
        point_y = Dot().move_to(y.points[0])

        line_t = None
        line_left_y = Line(self.input_to_graph_point(-3, x), self.input_to_graph_point(-3, y), color=RED)
        line_right_y = Line(self.input_to_graph_point(7, x), self.input_to_graph_point(7, y), color=RED)
        for t in range(2, 5):

            x_path = self.get_graph(lambda u: math.sin(0.9 * u) - 2, x_min=-5, x_max=5)
            y_path = self.get_graph(lambda u: math.cos(1/4 * u - 1) + 2, x_min=t+5, x_max=t-5)

            self.remove(line_t)
            line_t = Line(self.input_to_graph_point(t, x), self.input_to_graph_point(t, y), color=YELLOW)
            t_label_next = MathTex(r"t = " + str(t), color=YELLOW).move_to(3 * UR)
            self.play(Transform(t_label_prev, t_label_next), ShowCreation(line_t), run_time=0.5)
            
            self.remove(line_left_y, line_right_y)
            line_left_y = Line(self.input_to_graph_point(t - 5, x), self.input_to_graph_point(t - 5, y), color=RED)
            line_right_y = Line(self.input_to_graph_point(t + 5, x), self.input_to_graph_point(t + 5, y), color=RED)
            self.play(ShowCreation(line_left_y), ShowCreation(line_right_y), run_time=0.5)
            self.play(MoveAlongPath(point_x, x_path, rate_func=linear), MoveAlongPath(point_y, y_path, rate_func=linear), run_time=1.25) 

            self.play(FadeOut(point_x), FadeOut(point_y))
