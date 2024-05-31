import json
import math
import os
import re
import numpy as np
import onnxruntime
from typing import List, Literal
from piper_phonemize import phonemize_espeak, tashkeel_run
import scipy
from pydub import AudioSegment

class TTS():
    def __init__(self, model_name, config_path, speed=1.0):
        self.sess_options = onnxruntime.SessionOptions()
        self.sess_options.enable_mem_pattern = False
        self.model = onnxruntime.InferenceSession(model_name, sess_options=self.sess_options)

        with open(config_path, "r") as file:
            self.config = json.load(file)

        self.speed = float(speed)
        self.SAMPLE_RATE = 22050
        self.NOISE_SCALE_W = 0.8
        self.NOISE_SCALE = 0.667
        self.PAD = "_"  # padding (0)
        self.BOS = "^"  # beginning of sentence
        self.EOS = "$"  # end of sentence

    def inference(self, text: str, audio_path: str, option: Literal["all", "separated"] = "separated"):    
        if option == "all":
            combined_audio_array = self.inference_sentence(text)
        elif option == "separated":
            list_text = re.split(r';|\.|\?|!|…', text)
            all_audio_segments = []
            silence = AudioSegment.silent(duration=500)  # 500ms silence

            for sentence in list_text:
                sentence = sentence.strip().strip(',')
                if len(sentence) > 0:
                    audio = self.inference_sentence(sentence)
                    audio_segment = AudioSegment(
                        audio.tobytes(), 
                        frame_rate=self.SAMPLE_RATE, 
                        sample_width=audio.dtype.itemsize, 
                        channels=1
                    ) 
                    all_audio_segments.append(audio_segment)
                    all_audio_segments.append(silence)

            combined_audio = sum(all_audio_segments[:-1])  # Remove last silence
            combined_audio_array = np.array(combined_audio.get_array_of_samples())
        
        scipy.io.wavfile.write(audio_path, self.SAMPLE_RATE, combined_audio_array)

    def inference_sentence(self, text, chunk_size=100):
        text = text.strip()
        phonemes_list = self.phonemize(self.config, text)
        phoneme_ids = []
        for phonemes in phonemes_list:
            phoneme_ids.append(self.phonemes_to_ids(self.config, phonemes))

        chunks = [phoneme_ids[i * chunk_size:(i + 1) * chunk_size] for i in range((len(phoneme_ids) + chunk_size - 1) // chunk_size)] 
        list_audio = []
        for chunk_ids in chunks:
            audio = self.inference_chunk(chunk_ids)
            list_audio.append(audio)

        return np.concatenate(list_audio)

    def inference_chunk(self, phoneme_ids):
        speaker_id = None
        phoneme_ids_flatten = []
        for i in phoneme_ids:
            phoneme_ids_flatten += i
        text = np.expand_dims(np.array(phoneme_ids_flatten, dtype=np.int64), 0)
        text_lengths = np.array([text.shape[1]], dtype=np.int64)
        scales = np.array(
            [self.NOISE_SCALE, self.speed, self.NOISE_SCALE_W],
            dtype=np.float32,
        )
        sid = None

        if speaker_id is not None:
            sid = np.array([speaker_id], dtype=np.int64)

        audio = self.model.run(
            None,
            {
                "input": text,
                "input_lengths": text_lengths,
                "scales": scales,
                "sid": sid,
            },
        )[0].squeeze((0, 1))
        # audio = denoise(audio, bias_spec, 10)
        audio = self.audio_float_to_int16(audio.squeeze())
        return audio

    def audio_float_to_int16(self,
        audio: np.ndarray, max_wav_value: float = 32767.0
    ) -> np.ndarray:
        """Normalize audio and convert to int16 range"""
        audio = audio.astype(np.float32)  # Ensure audio is of type float
        audio_norm = audio * (max_wav_value / max(0.01, np.max(np.abs(audio))))
        audio_norm = np.clip(audio_norm, -max_wav_value, max_wav_value)
        audio_norm = audio_norm.astype("int16")
        return audio_norm

    def phonemize(self, config, text: str) -> List[List[str]]:
        """Text to phonemes grouped by sentence."""
        if config["espeak"]["voice"] == "ar":
            # Arabic diacritization
            # https://github.com/mush42/libtashkeel/
            text = tashkeel_run(text)
        return phonemize_espeak(text, config["espeak"]["voice"])


    def phonemes_to_ids(self, config, phonemes: List[str]) -> List[int]:
        """Phonemes to ids."""
        id_map = config["phoneme_id_map"]
        ids: List[int] = list(id_map[self.BOS])
        for phoneme in phonemes:
            if phoneme not in id_map:
                print("Missing phoneme from id map: %s", phoneme)
                continue
            ids.extend(id_map[phoneme])
            ids.extend(id_map[self.PAD])
        ids.extend(id_map[self.EOS])
        return ids

    def denoise(self, 
        audio: np.ndarray, bias_spec: np.ndarray, denoiser_strength: float
    ) -> np.ndarray:
        audio_spec, audio_angles = self.transform(audio)

        a = bias_spec.shape[-1]
        b = audio_spec.shape[-1]
        repeats = max(1, math.ceil(b / a))
        bias_spec_repeat = np.repeat(bias_spec, repeats, axis=-1)[..., :b]

        audio_spec_denoised = audio_spec - (bias_spec_repeat * denoiser_strength)
        audio_spec_denoised = np.clip(audio_spec_denoised, a_min=0.0, a_max=None)
        audio_denoised = self.inverse(audio_spec_denoised, audio_angles)

        return audio_denoised


    def stft(self, x, fft_size, hopsamp):
        """Compute and return the STFT of the supplied time domain signal x.
        Args:
            x (1-dim Numpy array): A time domain signal.
            fft_size (int): FFT size. Should be a power of 2, otherwise DFT will be used.
            hopsamp (int):
        Returns:
            The STFT. The rows are the time slices and columns are the frequency bins.
        """
        window = np.hanning(fft_size)
        fft_size = int(fft_size)
        hopsamp = int(hopsamp)
        return np.array(
            [
                np.fft.rfft(window * x[i : i + fft_size])
                for i in range(0, len(x) - fft_size, hopsamp)
            ]
        )


    def istft(self, X, fft_size, hopsamp):
        """Invert a STFT into a time domain signal.
        Args:
            X (2-dim Numpy array): Input spectrogram. The rows are the time slices and columns are the frequency bins.
            fft_size (int):
            hopsamp (int): The hop size, in samples.
        Returns:
            The inverse STFT.
        """
        fft_size = int(fft_size)
        hopsamp = int(hopsamp)
        window = np.hanning(fft_size)
        time_slices = X.shape[0]
        len_samples = int(time_slices * hopsamp + fft_size)
        x = np.zeros(len_samples)
        for n, i in enumerate(range(0, len(x) - fft_size, hopsamp)):
            x[i : i + fft_size] += window * np.real(np.fft.irfft(X[n]))
        return x


    def inverse(self, magnitude, phase):
        recombine_magnitude_phase = np.concatenate(
            [magnitude * np.cos(phase), magnitude * np.sin(phase)], axis=1
        )

        x_org = recombine_magnitude_phase
        n_b, n_f, n_t = x_org.shape  # pylint: disable=unpacking-non-sequence
        x = np.empty([n_b, n_f // 2, n_t], dtype=np.complex64)
        x.real = x_org[:, : n_f // 2]
        x.imag = x_org[:, n_f // 2 :]
        inverse_transform = []
        for y in x:
            y_ = self.istft(y.T, fft_size=1024, hopsamp=256)
            inverse_transform.append(y_[None, :])

        inverse_transform = np.concatenate(inverse_transform, 0)

        return inverse_transform


    def transform(self, input_data):
        x = input_data
        real_part = []
        imag_part = []
        for y in x:
            y_ = self.stft(y, fft_size=1024, hopsamp=256).T
            real_part.append(y_.real[None, :, :])  # pylint: disable=unsubscriptable-object
            imag_part.append(y_.imag[None, :, :])  # pylint: disable=unsubscriptable-object
        real_part = np.concatenate(real_part, 0)
        imag_part = np.concatenate(imag_part, 0)

        magnitude = np.sqrt(real_part**2 + imag_part**2)
        phase = np.arctan2(imag_part.data, real_part.data)

        return magnitude, phase