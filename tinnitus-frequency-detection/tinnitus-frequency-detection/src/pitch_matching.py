"""
pitch_matching.py
-------------------
Implements a binary-search pitch-matching procedure: on each step,
a test tone is played and the patient reports whether their
perceived tinnitus tone is higher, lower, or the same. The search
window narrows on a log-frequency scale (pitch perception is closer
to logarithmic than linear), converging on an estimated frequency.

This is a simplified, educational implementation of a real audiometric
technique (pitch-matching / tinnitus frequency matching) -- it is not
a certified clinical diagnostic tool.
"""

import math
from dataclasses import dataclass, field


@dataclass
class ComparisonResult:
    step: int
    test_frequency_hz: float
    patient_response: str  # "higher", "lower", "same"


@dataclass
class PitchMatchingSession:
    freq_min_hz: float
    freq_max_hz: float
    max_comparisons: int
    convergence_threshold_hz: float
    history: list = field(default_factory=list)

    def _log_midpoint(self, low: float, high: float) -> float:
        # Geometric mean = midpoint on a log scale, which better matches
        # how pitch is perceived than a plain arithmetic midpoint.
        return math.sqrt(low * high)

    def run(self, response_fn) -> dict:
        """
        Runs the search loop.

        response_fn: a callable that takes a test_frequency_hz and
        returns "higher", "lower", or "same" -- this is where the
        actual patient input (CLI, GUI, or hardware button) plugs in.
        """
        low, high = self.freq_min_hz, self.freq_max_hz

        for step in range(1, self.max_comparisons + 1):
            test_freq = self._log_midpoint(low, high)
            response = response_fn(test_freq)
            self.history.append(ComparisonResult(step, test_freq, response))

            if response == "same":
                return self._result(test_freq, step, converged=True)
            elif response == "higher":
                # Patient's tinnitus is higher-pitched than the test tone
                low = test_freq
            elif response == "lower":
                low, high = low, test_freq
            else:
                raise ValueError(f"Unexpected response: {response}")

            if (high - low) <= self.convergence_threshold_hz:
                estimated = self._log_midpoint(low, high)
                return self._result(estimated, step, converged=True)

        estimated = self._log_midpoint(low, high)
        return self._result(estimated, self.max_comparisons, converged=False)

    def _result(self, estimated_freq_hz: float, steps_taken: int, converged: bool) -> dict:
        return {
            "estimated_frequency_hz": round(estimated_freq_hz, 1),
            "steps_taken": steps_taken,
            "converged": converged,
            "history": self.history,
        }
