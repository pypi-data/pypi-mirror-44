(define-transfer-function pid-controller-base
  "Representation of a PID controller"
  (numerator Kd*s^2 + Kp*s + Ki)
  (denominator s))
