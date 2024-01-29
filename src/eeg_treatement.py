import matplotlib.pyplot as plt
import numpy as np
import s3fs

# Gradient Color Bar Plots
from matplotlib import cm
from scipy import signal
from scipy.signal import welch


# basic preprocessing
def eeg_filter(
    eeg,
    btype,
    eeg_sr=250,
    freq_high=0.5,
    freq_stop=60,
    freq_band=[1, 50],
    eeg_butter_order=3,
):
    f_n = eeg_sr / 2
    b = 1
    a = 1
    if btype == "highpass":
        b, a = signal.butter(
            eeg_butter_order, freq_high / f_n, btype=btype, analog=False
        )
    elif btype == "bandstop":
        b, a = signal.butter(
            eeg_butter_order,
            [(freq_stop - 1) / f_n, (freq_stop + 1) / f_n],
            btype,
            analog=False,
        )
    elif btype == "bandpass":
        b, a = signal.butter(
            eeg_butter_order,
            np.array(freq_band) / f_n,
            btype,
            analog=False,
        )

    filtered_eeg = signal.filtfilt(
        b,
        a,
        eeg,
        axis=0,
        padtype="odd",
        padlen=3 * (max(len(b), len(a)) - 1),
    )
    return filtered_eeg


def apply_filter(eeg_raw_data):
    filtered_data = []
    eeg = eeg_raw_data

    eeg_aug = np.append(np.flipud(eeg), eeg, axis=0)
    eeg_aug = np.append(eeg_aug, np.flipud(eeg), axis=0)

    applied_notch = eeg_filter(eeg_raw_data, "bandstop")
    applied_highpass = eeg_filter(applied_notch, "highpass")
    applied_bandpass = eeg_filter(applied_highpass, "bandpass")

    filt_eeg = applied_bandpass

    return filt_eeg


def epoching_for_fft(eeg, nperseg):
    epochs = []
    overlap = len(eeg) - nperseg
    epoch_count = len(eeg) // nperseg + 1

    first_seg = eeg[0:nperseg]
    second_seg = eeg[len(eeg) // 2 - nperseg // 2 : len(eeg) // 2 + nperseg // 2]
    third_seg = eeg[-nperseg:]

    epochs.append(first_seg)
    epochs.append(second_seg)
    epochs.append(third_seg)

    return epochs


def segment_per_second(eeg, nperseg):
    epochs = [eeg[i * nperseg : (i + 1) * nperseg] for i in range(len(eeg) // nperseg)]

    return epochs


def psd_norm(psd):
    denom = psd.sum(axis=1, keepdims=True)
    normed = psd / denom
    return normed


# def calculate_psd_from_fft(eeg, nperseg, relative=True):
#     MIN_FREQ_INDEX = 1
#     MAX_FREQ_INDEX = 55

#     epoch_seg = 128
#     all_psds = []
#     segments = segment_per_second(eeg, nperseg)
#     for segment in segments:
#         segment_psds = []

#         epochs = epoching_for_fft(segment, epoch_seg)
#         for epoch in epochs:
#             fft_result = np.fft.fft(epoch)
#             power_spectrum = np.sqrt(np.abs(fft_result)**2)
# #             psd = power_spectrum / len(epoch) / 250 * 2
#             segment_psds.append(power_spectrum)

#         segment_psds = np.array(segment_psds)
#         f = np.fft.fftfreq(len(epochs[0]), 1/128)

#         idx_crop = (MIN_FREQ_INDEX <= f) & (f <= MAX_FREQ_INDEX)
#         segment_psds = segment_psds[:, idx_crop]
#         f = f[idx_crop]

#         if relative:
#             segment_psd_norm = psd_norm(segment_psds)
#             segment_psd_avg = np.mean(segment_psd_norm, axis=0)
#         all_psds.append(segment_psd_avg)
#     return f, np.array(all_psds)


def calculate_psd_from_fft(eeg, nperseg, relative=True):
    MIN_FREQ_INDEX = 1
    MAX_FREQ_INDEX = 50

    all_psds = []
    segments = segment_per_second(eeg, nperseg)
    for segment in segments:
        fft_result = np.fft.fft(segment)
        power_spectrum = np.sqrt(np.abs(fft_result) ** 2)
        #         psd = power_spectrum / len(segment) / 250 * 2
        # 아랫줄만 밀어넣을 것
        segment_psd = np.array(power_spectrum)

        f = np.fft.fftfreq(len(segment), 1 / 250)
        idx_crop = (MIN_FREQ_INDEX <= f) & (f <= MAX_FREQ_INDEX)
        segment_psd = segment_psd[idx_crop]
        f = f[idx_crop]

        if relative:
            segment_psd = psd_norm_without_epoch(segment_psd)
        all_psds.append(segment_psd)
    return f, np.array(all_psds)


def load_raw_data_list(userId, crownId, bucket):
    sf = s3fs.S3FileSystem(anon=False)
    path_obj = f"{bucket}/focus-timer/{userId}/{crownId}"
    raw_data_files = sf.glob(f"{path_obj}//**")
    raw_data_files.sort()

    return raw_data_files


def psd_norm_without_epoch(psd):
    denom = psd.sum(axis=0, keepdims=True)
    normed = psd / denom
    return normed


def calculate_PSD_without_epoch(eeg, nperseg, relative=True):
    # Calculate relative PSD
    MIN_FREQ_INDEX = 1
    MAX_FREQ_INDEX = 55
    f, psd = welch(eeg, fs=250, nperseg=nperseg, axis=0, window="hamming")

    idx_crop = (MIN_FREQ_INDEX <= f) & (f <= MAX_FREQ_INDEX)
    psd = psd[idx_crop]
    f = f[idx_crop]

    if relative:
        psd = psd_norm_without_epoch(psd)

    return f, psd


# find slope, intercept
def linear_function_from_points(x1, y1, x2, y2):
    # Calculate the slope (m)
    slope = (y2 - y1) / (x2 - x1)

    # Calculate the y-intercept (b) using the point-slope form of a line
    # y - y1 = m(x - x1)
    # y = mx - mx1 + y1
    intercept = y1 - slope * x1

    return slope, intercept


# rel beta


def rel_mapping_function(x):
    slope, intercept = linear_function_from_points(
        0.1259656620109476, 0.1, 0.9240767476420029, 0.99
    )

    result = slope * x + intercept

    if result > 0.99:
        result = 0.99
    elif result < 0.1:
        result = 0.1

    return result


# abs beta


def abs_mapping_function(x):
    slope, intercept = linear_function_from_points(
        20.939314485618187, 0.1, 30.637675003992527, 0.99
    )

    result = slope * x - intercept
    result = 1 / (1 + np.e ** (-x + 9.718946665209524))
    #     if result > 0.99:
    #         result = 0.99
    #     if result < 0.1:
    #         result = 0.1

    return result


def gradientbars(bars, ydata, cmap):
    ax = bars[0].axes
    lim = ax.get_xlim() + ax.get_ylim()
    ax.axis(lim)
    for bar in bars:
        bar.set_facecolor("none")
        x, y = bar.get_xy()
        w, h = bar.get_width(), bar.get_height()
        grad = np.atleast_2d(np.linspace(0, 1 * h / max(ydata), 256)).T
        ax.imshow(
            grad,
            extent=[x, x + w, y, y + h],
            origin="lower",
            aspect="auto",
            norm=cm.colors.NoNorm(vmin=0, vmax=1),
            cmap=plt.get_cmap(cmap),
        )


def get_eeg_frequency(fft):
    delta = np.sum(fft[:, 0:3], axis=1)
    theta = np.sum(fft[:, 3:7], axis=1)
    alpha = np.sum(fft[:, 7:13], axis=1)
    beta = np.sum(fft[:, 13:30], axis=1)
    gamma = np.sum(fft[:, 30:], axis=1)

    return delta, theta, alpha, beta, gamma


def chunk_data(freq_data, n):
    freq_data = freq_data[: (len(freq_data) // n) * n]
    new_data = freq_data.reshape(-1, n)

    meaned_new_data = np.mean(new_data, axis=1)

    return meaned_new_data
