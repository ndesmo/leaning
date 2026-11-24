import Mathlib
example (u v Q Qp : ℝ) :
    v^2 - (u^3*v*Q + (1/4)*u^6*Qp) = (v - (1/2)*u^3*Q)^2 - (1/4)*u^6*(Qp + Q^2) := by ring
