import numpy as np
from scipy import signal


class AudioAnalyzer:
    """Convert three frequency bands into Arduino PWM brightness values."""

    def __init__(self, sample_rate: int, chunk_size: int) -> None:
        self.filters = (
            signal.butter(2, (50.0, 100.0), btype="bandpass", fs=sample_rate, output="sos"),
            signal.butter(2, (100.0, 300.0), btype="bandpass", fs=sample_rate, output="sos"),
            signal.butter(4, (5000.0, 7000.0), btype="bandpass", fs=sample_rate, output="sos"),
        )
        self.filter_states = tuple(signal.sosfilt_zi(f) * 0.0 for f in self.filters)

        # Dynamic range compression parameters
        self.max_rms = [0.02, 0.02, 0.02]
        self.decay_rate = float(np.exp(-chunk_size / (sample_rate * 0.5)))

        # Smoothing parameters
        self.current_brightness = [0.0, 0.0, 0.0]
        self.prev_rms_sum = 0.0
        self.activeness_score = 0.0

    def apply_smoothing_and_gamma(self, target_values: list[int], smoothing_factor: float) -> list[int]:
        """Apply exponential moving average smoothing and gamma correction."""
        final_values = []
        for i in range(3):
            # Dynamic EMA Smoothing
            self.current_brightness[i] = (smoothing_factor * target_values[i]) + (
                (1.0 - smoothing_factor) * self.current_brightness[i]
            )
            # Gamma correction
            gamma_corrected = (self.current_brightness[i] ** 2) / 254.0
            final_values.append(int(np.clip(gamma_corrected, 0, 254)))
        return final_values

    def brightness(self, samples: np.ndarray) -> tuple[int, int, int, int]:
        normalized = samples.astype(np.float32) / 32768.0
        brightness_values: list[int] = []
        updated_states = []
        current_rms_sum = 0.0

        for i, (filter_, state) in enumerate(zip(self.filters, self.filter_states)):
            filtered, state = signal.sosfilt(filter_, normalized, zi=state)
            rms = float(np.sqrt(np.mean(np.square(filtered))))
            current_rms_sum += rms

            # Dynamic range compression
            if rms > self.max_rms[i]:
                self.max_rms[i] = rms
            else:
                self.max_rms[i] *= self.decay_rate
            self.max_rms[i] = max(self.max_rms[i], 0.02)
            # Noise Gate
            if rms < 0.002:
                brightness = 0
            else:
                brightness = int(np.clip((rms / self.max_rms[i]) * 254.0, 0, 254))
            brightness_values.append(brightness)
            updated_states.append(state)
        self.filter_states = tuple(updated_states)
        # Activeness calculation
        delta_rms = abs(current_rms_sum - self.prev_rms_sum)
        self.prev_rms_sum = current_rms_sum
        total_max_rms = sum(self.max_rms)
        relative_change = delta_rms / (total_max_rms + 1e-6)

        self.activeness_score = (0.05 * relative_change) + (0.95 * self.activeness_score)
        dynamic_smoothing = float(np.clip(0.1 + (self.activeness_score * 2.5), 0.1, 0.85))

        smoothed_values = self.apply_smoothing_and_gamma(brightness_values, dynamic_smoothing)
        return tuple([255] + smoothed_values)  # type: ignore[return-value]
