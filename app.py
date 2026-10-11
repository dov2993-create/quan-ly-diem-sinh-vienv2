```python
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. CẤU HÌNH TRANG WEB
# ==========================================
st.set_page_config(
    page_title="Quản lý điểm sinh viên",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 QUẢN LÝ ĐIỂM SINH VIÊN")
st.markdown("---")

# ==========================================
# 2. KHAI BÁO DỮ LIỆU SINH VIÊN
# ==========================================
data = {
    "Họ tên": [
        "Nguyễn Văn An",
        "Trần Thị Bình",
        "Lê Hoàng Cường",
        "Phạm Minh Dũng",
        "Hoàng Thị Hà",
        "Võ Quốc Huy",
        "Đặng Ngọc Lan",
        "Bùi Thành Nam",
        "Đỗ Thị Phương",
        "Phan Minh Tuấn"
    ],
    "Chuyên cần": [9, 8, 7, 10, 9, 6, 8, 7, 10, 8],
    "Giữa kỳ":    [8, 7, 6, 9, 8, 5, 7, 6, 9, 8],
    "Cuối kỳ":    [9, 8, 7, 9, 8, 6, 8, 5, 10, 9]
}

df = pd.DataFrame(data)

# ==========================================
# 3. TÍNH ĐIỂM TỔNG KẾT VÀ XẾP LOẠI
# ==========================================
# Trọng số: Chuyên cần 20%, Giữa kỳ 30%, Cuối kỳ 50%
df["Tổng kết"] = (
    df["Chuyên cần"] * 0.2
    + df["Giữa kỳ"] * 0.3
    + df["Cuối kỳ"] * 0.5
).round(2)


def xep_loai(diem):
    if diem >= 8.5:
        return "Giỏi"
    elif diem >= 7:
        return "Khá"
    elif diem >= 5:
        return "Trung bình"
    else:
        return "Yếu"


df["Xếp loại"] = df["Tổng kết"].apply(xep_loai)

# ==========================================
# 4. HIỂN THỊ BẢNG ĐIỂM
# ==========================================
st.subheader("📋 Bảng điểm chi tiết")

st.dataframe(
    df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# 5. THỐNG KÊ KẾT QUẢ HỌC TẬP
# ==========================================
st.subheader("📊 Thống kê kết quả")

diem_trung_binh = df["Tổng kết"].mean()
diem_cao_nhat = df["Tổng kết"].max()
diem_thap_nhat = df["Tổng kết"].min()

sinh_vien_cao_nhat = df.loc[
    df["Tổng kết"] == diem_cao_nhat, "Họ tên"
].tolist()

sinh_vien_thap_nhat = df.loc[
    df["Tổng kết"] == diem_thap_nhat, "Họ tên"
].tolist()

so_sinh_vien_dat = (df["Tổng kết"] >= 5).sum()
so_sinh_vien = len(df)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Điểm trung bình lớp",
    f"{diem_trung_binh:.2f}"
)

col2.metric(
    "Điểm cao nhất",
    f"{diem_cao_nhat:.2f}"
)

col3.metric(
    "Điểm thấp nhất",
    f"{diem_thap_nhat:.2f}"
)

col4.metric(
    "Sinh viên đạt",
    f"{so_sinh_vien_dat}/{so_sinh_vien}"
)

st.write("**Sinh viên có điểm cao nhất:** " + ", ".join(sinh_vien_cao_nhat))
st.write("**Sinh viên có điểm thấp nhất:** " + ", ".join(sinh_vien_thap_nhat))
st.write("**Tỷ lệ đạt:** " + f"{so_sinh_vien_dat / so_sinh_vien * 100:.1f}%")

# ==========================================
# 6. TRA CỨU ĐIỂM THEO SINH VIÊN
# ==========================================
st.markdown("---")
st.subheader("🔎 Tra cứu điểm sinh viên")

ten_sinh_vien = st.selectbox(
    "Chọn sinh viên:",
    df["Họ tên"].tolist()
)

sinh_vien = df[df["Họ tên"] == ten_sinh_vien].iloc[0]

st.write(f"**Họ tên:** {sinh_vien['Họ tên']}")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Chuyên cần", f"{sinh_vien['Chuyên cần']:.1f}")
col2.metric("Giữa kỳ", f"{sinh_vien['Giữa kỳ']:.1f}")
col3.metric("Cuối kỳ", f"{sinh_vien['Cuối kỳ']:.1f}")
col4.metric("Tổng kết", f"{sinh_vien['Tổng kết']:.2f}")

st.info(f"Xếp loại học tập: **{sinh_vien['Xếp loại']}**")

# ==========================================
# 7. BIỂU ĐỒ ĐIỂM TỔNG KẾT
# ==========================================
st.markdown("---")
st.subheader("📈 Biểu đồ điểm tổng kết của sinh viên")

fig, ax = plt.subplots(figsize=(12, 5))

bars = ax.bar(
    df["Họ tên"],
    df["Tổng kết"],
    color="cornflowerblue",
    edgecolor="black"
)

ax.set_title("ĐIỂM TỔNG KẾT CỦA SINH VIÊN")
ax.set_xlabel("Họ tên sinh viên")
ax.set_ylabel("Điểm tổng kết")
ax.set_ylim(0, 10)
ax.tick_params(axis="x", rotation=45)
ax.grid(axis="y", linestyle="--", alpha=0.4)

for bar in bars:
    height = bar.get_height()
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        height + 0.1,
        f"{height:.2f}",
        ha="center",
        va="bottom",
        fontsize=8
    )

plt.tight_layout()
st.pyplot(fig)
plt.close(fig)

# ==========================================
# 8. THỐNG KÊ XẾP LOẠI
# ==========================================
st.subheader("📚 Thống kê số lượng theo xếp loại")

thong_ke = df["Xếp loại"].value_counts()

fig2, ax2 = plt.subplots(figsize=(8, 4))

thong_ke.plot(
    kind="bar",
    ax=ax2,
    color="mediumseagreen",
    edgecolor="black"
)

ax2.set_title("SỐ LƯỢNG SINH VIÊN THEO XẾP LOẠI")
ax2.set_xlabel("Xếp loại")
ax2.set_ylabel("Số lượng sinh viên")
ax2.grid(axis="y", linestyle="--", alpha=0.4)

plt.tight_layout()
st.pyplot(fig2)
plt.close(fig2)

# ==========================================
# 9. TẢI XUỐNG BẢNG ĐIỂM
# ==========================================
st.markdown("---")
st.subheader("📥 Xuất dữ liệu")

csv_data = df.to_csv(index=False).encode("utf-8-sig")

st.download_button(
    label="Tải bảng điểm CSV",
    data=csv_data,
    file_name="bang_diem_sinh_vien.csv",
    mime="text/csv"
)

# ==========================================
# 10. THÔNG TIN NGƯỜI TẠO
# ==========================================
st.markdown("---")
st.caption("Người tạo: Đỗ Trần Quang Việt | MSSV: [051208000848]")
```
