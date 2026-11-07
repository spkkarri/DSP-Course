"""
Lecture 31 companion demo: fixed-point quantization and overflow.
Requires only Python's standard library.

Run:
    python lecture_27_fixed_point_demo.py
"""

def q15_encode(x):
    """Round to signed Q1.15, saturating to the representable range."""
    scaled = round(x * (1 << 15))
    return max(-32768, min(32767, scaled))

def q15_decode(code):
    return code / (1 << 15)

def q15_saturating_add(a, b):
    """Add two Q1.15 integer codes with signed 16-bit saturation."""
    return max(-32768, min(32767, a + b))

def signed_8bit_wrap(value):
    """Return the two's-complement signed 8-bit wrap-around result."""
    value &= 0xFF
    return value - 256 if value >= 128 else value

def main():
    print("Q1.15 representation")
    for x in (0.625, 0.3, -0.75, 1.0):
        code = q15_encode(x)
        print(f"x={x:>7.4f} -> code={code:>6d}, decoded={q15_decode(code): .8f}")

    print("\\n8-bit overflow example")
    exact = 120 + 20
    print(f"Exact sum: {exact}")
    print(f"8-bit wrap-around: {signed_8bit_wrap(exact)}")
    print(f"8-bit saturation:  {min(127, max(-128, exact))}")

    print("\\nThree-tap moving average with Q1.15 samples")
    samples = [q15_encode(v) for v in (0.25, 0.50, -0.25, 0.75, 0.0)]
    history = [0, 0]
    for n, current in enumerate(samples):
        # Keep the accumulator in a wider Python integer; narrow only after /3.
        accumulator = current + history[0] + history[1]
        output_code = q15_encode(q15_decode(round(accumulator / 3)))
        print(
            f"n={n}: x={q15_decode(current): .5f}, "
            f"acc={accumulator:>7d}, y={q15_decode(output_code): .5f}"
        )
        history = [current, history[0]]

if __name__ == "__main__":
    main()
