import numpy as np, matplotlib.pyplot as plt
from thunderlab.powerspectrum import decibel

freqs = np.load(
    "wavetracker/fine_freqs.npy",
    allow_pickle=True,
)
times = np.load(
    "wavetracker/fine_times.npy",
    allow_pickle=True,
)
shape = np.load(
    "wavetracker/fine_spec_shape.npy",
    allow_pickle=True,
)
spec_mm = np.memmap(
    "wavetracker/fine_spec.npy",
    dtype="float",
    mode="r",
    shape=shape,
    order="F",
)

# display first x mins, 0–1.2 kHz
fmask = (freqs >= 1800) & (freqs <= 3000)
tmask = (times >= 1800) & (times <= 3000)
S_db = decibel(spec_mm[fmask][:, tmask])

plt.pcolormesh(times[tmask], freqs[fmask], S_db, cmap="viridis")
plt.xlabel("Time [s]")
plt.ylabel("Frequency [Hz]")
plt.title("Fine spectrogram (dB)")
plt.colorbar(label="Power [dB]")
plt.savefig("spectrogramm.pdf")
plt.show()
