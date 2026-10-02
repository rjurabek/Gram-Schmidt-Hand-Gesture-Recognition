<div align="center">

  <h1>🖐️ Hand Gesture Recognition & Local Coordinate System</h1>
  <p><b>Real-time hand gesture classification and local coordinate space estimation using OpenCV, MediaPipe, and NumPy.</b></p>

  <p>
    <a href="#about-the-project">About</a> •
    <a href="#key-features">Key Features</a> •
    <a href="#how-it-works">How It Works</a> •
    <a href="#getting-started">Getting Started</a> •
    <a href="#gestures-recognized">Gestures</a>
  </p>

  <hr />

</div>

<h2 id="about-the-project">📌 About The Project</h2>

<p>
  This repository provides a Python implementation for real-time hand gesture recognition along with 
  estimating a local 2D/3D coordinate basis on the hand. By using the <b>Gram-Schmidt Orthonormalization Process</b>, 
  the application projects a localized coordinate frame onto key palm landmarks (Wrist, Index MCP, and Pinky MCP).
</p>

<h2 id="key-features">✨ Key Features</h2>

<ul>
  <li><b>Orthonormal Basis Computation:</b> Computes local $X$ and $Y$ axis vectors on the hand using Gram-Schmidt.</li>
  <li><b>Rule-Based Gesture Recognition:</b> Fast and lightweight distance-based finger extension logic.</li>
  <li><b>Real-Time Visual Overlay:</b> Draws hand skeletons, tracking bounds, coordinate axes, and recognized gesture status.</li>
</ul>

<h2 id="how-it-works">🧮 How It Works</h2>

<p>
  The system computes two vectors originating from the wrist landmark:
</p>

<pre><code>v1 = Index_MCP - Wrist
v2 = Pinky_MCP - Wrist</code></pre>

<p>
  The <b>Gram-Schmidt algorithm</b> orthogonalizes $v_2$ relative to $v_1$ and normalizes both to unit length, 
  forming a stable local coordinate system anchored to the palm regardless of hand orientation.
</p>

<h2 id="gestures-recognized">🖐️ Recognized Gestures</h2>

<table>
  <thead>
    <tr>
      <th>Gesture Label</th>
      <th>Description</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>OPEN HAND</code></td>
      <td>All four fingers extended</td>
    </tr>
    <tr>
      <td><code>FIST</code></td>
      <td>All four fingers curled into the palm</td>
    </tr>
    <tr>
      <td><code>PEACE</code></td>
      <td>Index and Middle fingers extended</td>
    </tr>
    <tr>
      <td><code>ONE</code></td>
      <td>Index finger extended only</td>
    </tr>
    <tr>
      <td><code>THUMBS UP</code></td>
      <td>Fist position with thumb extended away from wrist</td>
    </tr>
    <tr>
      <td><code>UNKNOWN</code></td>
      <td>Unrecognized position or transition state</td>
    </tr>
  </tbody>
</table>

<h2 id="getting-started">🚀 Getting Started</h2>

<h3>Prerequisites</h3>

<p>Install the required Python dependencies:</p>

<pre><code>pip install opencv-python mediapipe numpy</code></pre>

<h3>Usage</h3>

<p>Run the main script to start your webcam feed:</p>

<pre><code>python index.py</code></pre>

<p>Press <b><code>q</code></b> or <b><code>ESC</code></b> in the window to quit.</p>
