class PID():
    def __init__(self, Kp, Ki, Kd, simple_threshold, sse_threshold, minout, maxout, deltaTime=0.02):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd

        self.min = minout
        self.max = maxout

        self.simple_threshold = simple_threshold
        self.sse_threshold = sse_threshold

        self.old_error = 0
        self.error_sum = 0
        self.deltaTime = deltaTime

    def calculate(self, error):
        output = 0.0
        # print(error)
        # if error is larger than simple_threshold only use Kp
        if abs(error) > self.simple_threshold:
            output = self.Kp * error

        else:
            # apply Kp value
            output += self.Kp * error
            # apply Kd value
            dt_error = (error - self.old_error) / self.deltaTime
            # save error
            self.old_error = error
            # apply Kd
            output += self.Kd * dt_error

            # if error is smaller than sse_threshold its probably
            # steady state error
            # apply Ki
            if abs(error) <= self.sse_threshold:
                self.error_sum += self.deltaTime * error
                output += self.Ki * self.error_sum
        # return output
        return self.clamp(output, self.min, self.max)

    def reset(self):
        self.old_error = 0
        self.error_sum = 0

    def clamp(self, value, minval, maxval):
        return max(min(value, maxval), minval)
