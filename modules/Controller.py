class AbstractController:
    def __init__(self):
        self.goal = (0, 0, 0)
        # motorspeeds:
        # [
        #  front left, front right,
        #  back left,  back right
        # ] (0-1)

    def set_goal(self, new_goal):
        self.goal = new_goal


class SimpleController(AbstractController):

    # [x, z, y]
    def on_update(self, heading, motorspeeds):
        # ignore z for now...
        if heading[0] < self.goal[0]:
            # less power on the back motors
            # more on the front
            motorspeeds[0] -= 2  # back left
            motorspeeds[1] -= 2  # back right

            motorspeeds[2] += 2  # front left
            motorspeeds[3] += 2  # front right
        else:
            # less power on the front motors
            # more power on the back
            motorspeeds[0] += 2  # back left
            motorspeeds[1] += 2  # back right

            motorspeeds[2] -= 2  # front left
            motorspeeds[3] -= 2  # front right

        if heading[2] < self.goal[2]:
            # less power on the left motors
            # more on the front motors
            motorspeeds[1] -= 2  # back left
            motorspeeds[3] -= 2  # front left

            motorspeeds[0] += 2  # front right
            motorspeeds[2] += 2  # back right
        else:
            # less power on the right side
            # more power on the left side
            motorspeeds[1] += 2  # back left
            motorspeeds[3] += 2  # front left

            motorspeeds[0] -= 2  # front right
            motorspeeds[2] -= 2  # back right

        for i in range(len(motorspeeds)):
            if motorspeeds[i] > 45:
                motorspeeds[i] = 45
            if motorspeeds[i] < 0:
                motorspeeds[i] = 0
            if not (0 <= motorspeeds[i] <= 50):
                print(f"motorspeeds were out of bounds!! {motorspeeds}")
                return [0, 0, 0, 0]

        return motorspeeds
