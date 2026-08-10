import os

with open("lecture_27.md", "a", encoding="utf-8") as f:
    f.write(r'''
---

## 11. Extended Topics: Mathematical Properties of the 2D DFT

To further solidify our understanding, let's explore some key mathematical properties of the 2D DFT that make it so powerful for image processing:

### 11.1 Translation (Spatial Shift)
If we shift an image in the spatial domain by $(m_0, n_0)$, this corresponds to a phase shift in the frequency domain. 
$$f[m - m_0, n - n_0] \longleftrightarrow F[k,l] e^{-j\frac{2\pi}{M}km_0} e^{-j\frac{2\pi}{N}ln_0}$$
This property is critical for image registration (aligning two images). Even if the object moves, the magnitude spectrum $|F[k,l]|$ remains identical; only the phase changes.

### 11.2 Rotation
If an image is rotated in the spatial domain by an angle $\theta$, its 2D Fourier spectrum is also rotated by the exact same angle $\theta$.
This property is utilized in orientation analysis and texture recognition. If you look at the Fourier spectrum of a woven fabric, the principal angles of the threads will show up as bright lines at the exact same angles in the frequency domain.

### 11.3 Scaling
Scaling an image in the spatial domain (e.g., zooming in) causes an inverse scaling in the frequency domain. 
If an object becomes wider in the spatial domain, its frequency components become narrower (compress towards the DC center). 
Mathematically:
$$f(a\cdot x, b\cdot y) \longleftrightarrow \frac{1}{|ab|} F\left(\frac{u}{a}, \frac{v}{b}\right)$$
This inverse relationship is why tiny, sharp details (narrow spatial width) correspond to very high frequencies (wide spectral width).

---

## 12. Extended Topics: Advanced Edge Detection Operators

While Sobel is the most common, other operators are used depending on the specific application requirements.

### 12.1 The Prewitt Operator
The Prewitt operator is very similar to Sobel, but it does not place extra weight on the center pixel. It provides a standard average rather than a weighted average.
$$H_x = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}, \quad H_y = \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}$$
**Trade-offs:** Prewitt is slightly more sensitive to diagonal edges than Sobel, but it is also more sensitive to random noise because it lacks the Gaussian-like weighting in the orthogonal direction.

### 12.2 The Scharr Operator
When highly accurate gradient angles are required, the Scharr operator is preferred. It provides much better rotational symmetry than Sobel.
$$H_x = \begin{bmatrix} -3 & 0 & 3 \\ -10 & 0 & 10 \\ -3 & 0 & 3 \end{bmatrix}$$
**Application:** Used extensively in computer vision tasks where the exact edge orientation $\theta$ is needed for feature extraction, such as in the Histogram of Oriented Gradients (HOG) algorithm for pedestrian detection.

---

## 13. Deep Dive: Zero-Padding and Linear Convolution

When performing filtering via the DFT (frequency domain multiplication), we must be careful about boundary conditions. The DFT inherently assumes the image is **periodic** (it wraps around like a torus).

If we directly multiply the DFTs of an image and a filter, we perform **Circular Convolution**. This means pixels filtering off the right edge will wrap around and affect the left edge, creating severe boundary artifacts.

**The Solution: Zero-Padding**
To perform true **Linear Convolution** using the DFT, we must zero-pad both the image and the filter. 
If the image is $M \times N$ and the filter is $K \times L$, we must pad both of them with zeros to a new size of at least:
$$P \ge M + K - 1$$
$$Q \ge N + L - 1$$
Only after padding to this size can we take the $P \times Q$ DFT, multiply them, and take the IDFT to get an artifact-free filtered image.
''')

with open("lecture_27.tex", "r", encoding="utf-8") as f:
    tex = f.read()

tex = tex.replace(r"\end{document}", r'''
\section{Extended Topics: Mathematical Properties of the 2D DFT}
\subsection{Translation (Spatial Shift)}
Shifting an image corresponds to a phase shift in the frequency domain. 
\begin{equation}
f[m - m_0, n - n_0] \longleftrightarrow F[k,l] e^{-j\frac{2\pi}{M}km_0} e^{-j\frac{2\pi}{N}ln_0}
\end{equation}
The magnitude spectrum $|F[k,l]|$ remains identical; only the phase changes.

\subsection{Rotation and Scaling}
If an image is rotated by $\theta$, its spectrum is also rotated by $\theta$.
Scaling an image causes inverse scaling in the frequency domain:
\begin{equation}
f(a\cdot x, b\cdot y) \longleftrightarrow \frac{1}{|ab|} F\left(\frac{u}{a}, \frac{v}{b}\right)
\end{equation}
Tiny, sharp details (narrow spatial width) correspond to very high frequencies.

\section{Extended Topics: Advanced Edge Detection Operators}
\subsection{The Prewitt Operator}
Provides a standard average rather than a weighted average.
\begin{equation}
H_x = \begin{bmatrix} -1 & 0 & 1 \\ -1 & 0 & 1 \\ -1 & 0 & 1 \end{bmatrix}, \quad H_y = \begin{bmatrix} -1 & -1 & -1 \\ 0 & 0 & 0 \\ 1 & 1 & 1 \end{bmatrix}
\end{equation}

\subsection{The Scharr Operator}
Provides better rotational symmetry than Sobel.
\begin{equation}
H_x = \begin{bmatrix} -3 & 0 & 3 \\ -10 & 0 & 10 \\ -3 & 0 & 3 \end{bmatrix}
\end{equation}

\section{Deep Dive: Zero-Padding and Linear Convolution}
To perform true \textbf{Linear Convolution} using the DFT, we must zero-pad both the image and the filter. If the image is $M \times N$ and the filter is $K \times L$, we must pad both to:
\begin{align}
P &\ge M + K - 1 \\
Q &\ge N + L - 1
\end{align}
Only then can we multiply the DFTs and avoid circular convolution artifacts.

\end{document}
''')

with open("lecture_27.tex", "w", encoding="utf-8") as f:
    f.write(tex)
