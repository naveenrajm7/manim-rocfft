from manim import *
from fourierscene import FourierSceneAbstract


class FourierScene(FourierSceneAbstract):
    def __init__(self):
        super().__init__()
    def construct(self):
        # Load the AMD logo from the SVG file 
        # (For proper drawing, make sure each the letters are split into separate paths)
        amd_logo = SVGMobject("assets/AMD_Logo_splitpath.svg")

        # Scale the logo if needed
        amd_logo.scale(1)

        # Print the length of submobjects 
        print(f"Number of submobjects: {len(amd_logo.submobjects)}")

        # Assign submobjects to variables (We know the order from the SVG file, so hardcoding the indices)
        small_arrow = amd_logo.submobjects[0]
        big_arrow = amd_logo.submobjects[1]
        letter_d = amd_logo.submobjects[2]
        letter_m = amd_logo.submobjects[3]
        letter_a = amd_logo.submobjects[4]

        # Set fill color and opacity for each submobject
        for submobject in amd_logo.submobjects:
            submobject.set_fill(WHITE, opacity=1)

        # Create a VGroup for the letters
        letters = VGroup(letter_a, letter_m, letter_d)
        arrows = VGroup(small_arrow, big_arrow)

        # Fourier series for small arrow
        vectors1 = self.get_fourier_vectors(small_arrow)
        circles1 = self.get_circles(vectors1)
        drawn_path1 = self.get_drawn_path(vectors1).set_color(PURE_RED)

        # Fourier series for big arrow
        vectors2 = self.get_fourier_vectors(big_arrow)
        circles2 = self.get_circles(vectors2)
        drawn_path2 = self.get_drawn_path(vectors2).set_color(PURE_RED)

        all_mobs = VGroup(letters, arrows)

        # Camera updater
        last_vector = vectors1[-1]

        def follow_end_vector(camera): 
            camera.move_to(last_vector.get_end())

        # Scene start
        self.wait(1)
        self.play(
            *[
                GrowArrow(arrow)
                for vector_group in [vectors1, vectors2]
                for arrow in vector_group
            ],
            *[
                Create(circle)
                for circle_group in [circles1, circles2]
                for circle in circle_group
            ],
            run_time=2.5,
        )

        # Add objects to scene
        self.add( 
            vectors1,
            circles1,
            drawn_path1.set_stroke(width = 0),
            vectors2,
            circles2,
            drawn_path2.set_stroke(width = 0),
        )

        # Camera move
        self.play(self.camera.frame.animate.scale(0.3).move_to(last_vector.get_end()), run_time = 2)

        # Add updaters and start vector clock
        self.camera.frame.add_updater(follow_end_vector)
        vectors1.add_updater(self.update_vectors)
        circles1.add_updater(self.update_circles)
        vectors2.add_updater(self.update_vectors)
        circles2.add_updater(self.update_circles)
        drawn_path1.add_updater(self.update_path)
        drawn_path2.add_updater(self.update_path)
        self.start_vector_clock()

        self.play(self.slow_factor_tracker.animate.set_value(1), run_time = 0.5 * self.cycle_seconds)
        self.wait(1 * self.cycle_seconds)

        # Move camera then write text
        self.camera.frame.remove_updater(follow_end_vector)
        self.play(
            self.camera.frame.animate.set_width(all_mobs.width * 1.5).move_to(all_mobs.get_center()),
            Write(letters),
            run_time = 1 * self.cycle_seconds,
        )
        self.wait(0.8 * self.cycle_seconds)
        self.play(self.slow_factor_tracker.animate.set_value(0), run_time = 0.5 * self.cycle_seconds)
        
        # Remove updaters so can animate
        self.stop_vector_clock()
        drawn_path1.clear_updaters()
        drawn_path2.clear_updaters()
        vectors1.clear_updaters()
        vectors2.clear_updaters()
        circles1.clear_updaters()
        circles2.clear_updaters()

        self.play(
            *[
                Uncreate(vmobject)
                for vgroup in [vectors1, vectors2, circles1, circles2]
                for vmobject in vgroup
            ],
            FadeOut(drawn_path1, drawn_path2),
            FadeIn(small_arrow, big_arrow),
            run_time = 2.5,
        )

        self.wait(3)
