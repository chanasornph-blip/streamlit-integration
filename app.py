import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# 1) Page Setup
st.set_page_config(page_title="Numerical Integration (Trapezoidal Rule)")
st.title("Numerical Integration Explorer")
st.write("เว็บแอปสำหรับคำนวณหาค่าอินทิกรัลจำกัดเขตด้วยกฎคางหมู (Trapezoidal Rule) โดยเลือกจำนวนช่วงย่อย n แล้วเปรียบเทียบผลลัพธ์")

# 2) INPUT
with st.sidebar:
    st.header("Parameters")
    
    # เลือกฟังก์ชันที่ต้องการอินทิเกรต
    func_choice = st.selectbox(
        "เลือกฟังก์ชัน f(x)",
        ["f(x) = x^2", "f(x) = sin(x)", "f(x) = exp(x)"]
    )
    
    # รับค่าช่วงการอินทิเกรต a ถึง b และจำนวนช่วงย่อย n
    a = st.number_input("จุดเริ่มต้น (a)", value=0.0)
    b = st.number_input("จุดสิ้นสุด (b)", value=2.0)
    n = st.slider("จำนวนช่วงย่อย (n)", min_value=1, max_value=100, value=10, step=1)
    
    show_table = st.checkbox("แสดงตารางจุดคละและค่า y", value=True)

# ตรวจสอบเงื่อนไขข้อมูล (Validation)
if a >= b:
    st.warning("กรุณากำหนดค่า b ให้มากกว่า a (จุดสิ้นสุดต้องมากกว่าจุดเริ่มต้น)")
    st.stop()

# นิยามฟังก์ชันตามที่เลือก
if func_choice == "f(x) = x^2":
    f = lambda x: x**2
    exact_val = (b**3 - a**3) / 3
elif func_choice == "f(x) = sin(x)":
    f = lambda x: np.sin(x)
    exact_val = -np.cos(b) + np.cos(a)
else:
    f = lambda x: np.exp(x)
    exact_val = np.exp(b) - np.exp(a)

# 3) CALCULATION (Trapezoidal Rule)
x = np.linspace(a, b, n + 1)
y = f(x)
h = (b - a) / n

# คำนวณค่าประมาณด้วย Trapezoidal Rule: h/2 * [f(x0) + 2*sum(f(x_i)) + f(xn)]
trap_approx = (h / 2) * (y[0] + 2 * np.sum(y[1:-1]) + y[-1])
abs_error = abs(exact_val - trap_approx)

# 4) OUTPUT
col1, col2, col3 = st.columns(3)
col1.metric("Trapezoidal Approx.", f"{trap_approx:.6f}")
col2.metric("Exact Value", f"{exact_val:.6f}")
col3.metric("Absolute Error", f"{abs_error:.6e}")

# วาดกราฟแสดงฟังก์ชันและพื้นที่คางหมู
fig, ax = plt.subplots(figsize=(8, 4))

# กราฟเส้นโค้งจริง
x_dense = np.linspace(a, b, 200)
ax.plot(x_dense, f(x_dense), 'r-', label="f(x)", linewidth=2)

# วาดรูปคางหมูแต่ละช่วง
for i in range(n):
    xs = [x[i], x[i], x[i+1], x[i+1]]
    ys = [0, y[i], y[i+1], 0]
    ax.fill(xs, ys, edgecolor='blue', facecolor='cyan', alpha=0.3)

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_title(f"Trapezoidal Rule Approximation (n = {n})")
ax.grid(True, alpha=0.3)
ax.legend()

st.pyplot(fig)
plt.close(fig)

# แสดงตารางข้อมูลและปุ่มดาวน์โหลด CSV
if show_table:
    data = pd.DataFrame({"x": x, "f(x)": y})
    st.dataframe(data, hide_index=True)
    
    csv_bytes = data.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Data CSV",
        csv_bytes,
        file_name="trapezoidal_data.csv",
        mime="text/csv"
    )