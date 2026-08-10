# PID Control System Demonstration

## Objective
Learn closed-loop feedback control principles by tuning Proportional ($K_p$), Integral ($K_i$), and Derivative ($K_d$) gain parameters on a standard 2nd-order plant model.

## Engineering Concept
Feedback control minimizes tracking error $e(t) = r(t) - y(t)$:
$$u(t) = K_p e(t) + K_i \int_0^t e(\tau)d\tau + K_d \frac{de(t)}{dt}$$

## Parameters
- **Kp (Proportional Gain):** Increases overall response speed.
- **Ki (Integral Gain):** Eliminates steady-state offset error.
- **Kd (Derivative Gain):** Dampens overshoot and transient oscillations.
