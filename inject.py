import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

injection = '''
                    <section class="card">
                        <div class="card-title">Core Theory: IIR Filter Structures</div>
                        <div class="theory-text">
                            Infinite Impulse Response (IIR) filters are recursive systems characterized by a feedback loop. Since the difference equation involves both past inputs and past outputs, the way we arrange the arithmetic operations and memory delays drastically affects the system's performance, memory requirements, and stability under quantization.
                        </div>

                        <div class="math-card">
                            <strong>General Transfer Function</strong>
                            \\\\[ H(z) = \\frac{\\sum_{k=0}^{M} b_k z^{-k}}{1 + \\sum_{k=1}^{N} a_k z^{-k}} \\\\]
                            This represents the standard rational transfer function of an IIR filter. It expresses the system in terms of feedforward coefficients \\( b_k \\) (creating zeros) and feedback coefficients \\( a_k \\) (creating poles).
                        </div>

                        <div class="math-card">
                            <strong>Direct Form I &amp; II</strong>
                            \\\\[ \\text{DF-I: } y[n] = \\sum_{k=0}^{M} b_k x[n-k] - \\sum_{k=1}^{N} a_k y[n-k] \\\\]
                            \\\\[ \\text{DF-II State Eq: } v[n] = x[n] - \\sum_{k=1}^{N} a_k v[n-k] \\\\]
                            Direct Form I implements the numerator and denominator as separate delay lines, requiring \\( M + N \\) delays. Direct Form II is canonical, sharing the delay line and requiring only \\( \\max(M, N) \\) delays, thus minimizing memory footprint.
                        </div>

                        <div class="math-card">
                            <strong>Cascade &amp; Parallel Forms</strong>
                            \\\\[ H(z) = G \\prod_{k=1}^{K} H_k(z) \\quad \\text{(Cascade)} \\\\]
                            \\\\[ H(z) = C + \\sum_{k=1}^{K} H_k(z) \\quad \\text{(Parallel)} \\\\]
                            High-order polynomials suffer from extreme <span style="color: #8b5cf6;">coefficient sensitivity</span>. Cascade form factors the transfer function into a product of 2nd-order sections (biquads). Parallel form uses partial fraction expansion to create a sum of 2nd-order sections, grouping complex poles into real sections, enabling simultaneous processing.
                        </div>
                        
                        <div class="math-card">
                            <strong>Lattice-Ladder Structure</strong>
                            \\\\[ |K_m| < 1 \\quad \\forall m \\\\]
                            Uses PARCOR reflection coefficients \\( K_m \\) instead of direct delays. Highly modular and robust, it guarantees stability as long as all reflection coefficients have a magnitude strictly less than 1.
                        </div>

                        <table style="width:100%; border-collapse:collapse; font-size:0.8rem;">
                            <thead>
                                <tr style="background-color: #0f172a; text-align: left;">
                                    <th style="padding: 8px; border: 1px solid #334155;">Concept</th>
                                    <th style="padding: 8px; border: 1px solid #334155;">Formula</th>
                                    <th style="padding: 8px; border: 1px solid #334155;">Notes</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr style="background-color: #1e293b;">
                                    <td style="padding: 8px; border: 1px solid #334155;">General \\( H(z) \\)</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">\\( H(z) = \\frac{\\sum b_k z^{-k}}{1 + \\sum a_k z^{-k}} \\)</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">Rational transfer function (poles &amp; zeros)</td>
                                </tr>
                                <tr style="background-color: #0f172a;">
                                    <td style="padding: 8px; border: 1px solid #334155;">Biquad Section (Cascade)</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">\\( H_k(z) = \\frac{b_{k0} + b_{k1} z^{-1} + b_{k2} z^{-2}}{1 + a_{k1} z^{-1} + a_{k2} z^{-2}} \\)</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">2nd-order building block, groups complex poles</td>
                                </tr>
                                <tr style="background-color: #1e293b;">
                                    <td style="padding: 8px; border: 1px solid #334155;">Parallel Section</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">\\( H_k(z) = \\frac{\\gamma_{k0} + \\gamma_{k1} z^{-1}}{1 + a_{k1} z^{-1} + a_{k2} z^{-2}} \\)</td>
                                    <td style="padding: 8px; border: 1px solid #334155;">Derived via partial fraction expansion</td>
                                </tr>
                            </tbody>
                        </table>

                        <div class="accordion">
                            <div class="accordion-header">
                                <div class="accordion-title">
                                    <span class="accordion-icon">▶</span>
                                    Q1: How many delay elements are required for \\( H(z) = \\frac{1 + 2z^{-1} + z^{-2}}{1 - 0.5z^{-1} + 0.25z^{-2}} \\)?
                                </div>
                            </div>
                            <div class="accordion-content">
                                <p>
                                    In <strong>Direct Form I</strong>, we need separate delays for the numerator (\\( M=2 \\)) and denominator (\\( N=2 \\)). Total delays = \\( M + N = 4 \\).<br>
                                    In <strong>Direct Form II</strong>, delays are shared. Total delays = \\( \\max(M, N) = \\max(2, 2) = 2 \\).
                                </p>
                            </div>
                        </div>

                        <div class="accordion">
                            <div class="accordion-header">
                                <div class="accordion-title">
                                    <span class="accordion-icon">▶</span>
                                    Q2: Decompose \\( H(z) = \\frac{1}{(1 - 0.5z^{-1})(1 - 0.25z^{-1})} \\) into a Parallel Form.
                                </div>
                            </div>
                            <div class="accordion-content">
                                <ol>
                                    <li>Use Partial Fraction Expansion. Let \\( p_1 = 0.5 \\) and \\( p_2 = 0.25 \\).</li>
                                    <li>\\( H(z) = \\frac{A}{1 - 0.5z^{-1}} + \\frac{B}{1 - 0.25z^{-1}} \\)</li>
                                    <li>\\( A = H(z)(1 - 0.5z^{-1}) \\big|_{z^{-1}=2} = \\frac{1}{1 - 0.25(2)} = \\frac{1}{1 - 0.5} = 2 \\)</li>
                                    <li>\\( B = H(z)(1 - 0.25z^{-1}) \\big|_{z^{-1}=4} = \\frac{1}{1 - 0.5(4)} = \\frac{1}{1 - 2} = -1 \\)</li>
                                    <li>Parallel Form: \\( H(z) = \\frac{2}{1 - 0.5z^{-1}} - \\frac{1}{1 - 0.25z^{-1}} \\)</li>
                                </ol>
                            </div>
                        </div>
                    </section>

'''

if "Core Theory: IIR Filter Structures" in content:
    print("Content already injected, doing nothing to avoid duplication.")
else:
    new_content = content.replace('                    <!-- L13 Section 2: Overlap-Add Simulator -->', injection + '                    <!-- L13 Section 2: Overlap-Add Simulator -->')
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Content successfully injected.")

