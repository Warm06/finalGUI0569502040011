import streamlit as st
import pandas as pd

# ==========================================
# ตั้งค่าหน้าเว็บไซต์
# ==========================================

st.set_page_config(
    page_title="แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์",
    page_icon="🚗",
    layout="wide"
)

# ==========================================
# อ่านข้อมูลจาก car_output.csv
# ==========================================

df = pd.read_csv("car_output.csv")

# ==========================================
# กำหนดราคารถยนต์
# ==========================================

car_price = 1000000

# ==========================================
# คำนวณยอดชำระรวม
# ==========================================

df["total_payment"] = car_price + df["total_rate"]

# ==========================================
# คำนวณค่างวดต่อเดือน
# ==========================================

df["monthly_payment"] = (
    df["total_payment"] / (df["year"] * 12)
)

# ==========================================
# หาข้อมูลสำหรับ Dashboard
# ==========================================

lowest_interest = df["total_rate"].min()

highest_interest = df["total_rate"].max()

lowest_monthly = df["monthly_payment"].min()

highest_payment = df["total_payment"].max()

# บริษัทที่มีดอกเบี้ยต่ำสุด
lowest_interest_company = df.loc[
    df["total_rate"].idxmin(),
    "company_name"
]

# บริษัทที่มีค่างวดต่ำสุด
lowest_monthly_company = df.loc[
    df["monthly_payment"].idxmin(),
    "company_name"
]

# ==========================================
# หัวข้อ Dashboard
# ==========================================

st.title("🚗 แดชบอร์ดเปรียบเทียบสินเชื่อรถยนต์")

st.write(
    "เปรียบเทียบอัตราดอกเบี้ย ยอดชำระรวม "
    "และค่างวดต่อเดือนของแต่ละบริษัท"
)

st.divider()

# ==========================================
# ส่วนแสดงข้อมูลสรุป
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "ราคารถยนต์",
        f"฿{car_price:,.2f}"
    )

with col2:
    st.metric(
        "ดอกเบี้ยต่ำสุด",
        f"฿{lowest_interest:,.2f}",
        f"บริษัท {lowest_interest_company}"
    )

with col3:
    st.metric(
        "ค่างวดต่ำสุด",
        f"฿{lowest_monthly:,.2f}",
        f"บริษัท {lowest_monthly_company}"
    )

with col4:
    st.metric(
        "ยอดชำระสูงสุด",
        f"฿{highest_payment:,.2f}"
    )

st.divider()

# ==========================================
# เปรียบเทียบดอกเบี้ยและค่างวด
# ==========================================

col1, col2 = st.columns(2)

# ------------------------------------------
# กราฟดอกเบี้ยรวม
# ------------------------------------------

with col1:

    st.subheader("📊 เปรียบเทียบดอกเบี้ยรวม")

    interest_chart = df.set_index(
        "company_name"
    )[["total_rate"]]

    st.bar_chart(interest_chart)

# ------------------------------------------
# กราฟค่างวดต่อเดือน
# ------------------------------------------

with col2:

    st.subheader("📊 เปรียบเทียบค่างวดต่อเดือน")

    monthly_chart = df.set_index(
        "company_name"
    )[["monthly_payment"]]

    st.bar_chart(monthly_chart)

st.divider()

# ==========================================
# ตารางเปรียบเทียบข้อมูล
# ==========================================

st.subheader("📋 ตารางเปรียบเทียบเงื่อนไขสินเชื่อรถยนต์")

# สร้างตารางสำหรับแสดงผล
display_df = df.copy()

# จัดรูปแบบตัวเลข
display_df["rate"] = display_df["rate"].map(
    lambda x: f"{x:.2f}%"
)

display_df["total_rate"] = display_df["total_rate"].map(
    lambda x: f"{x:,.2f}"
)

display_df["total_payment"] = display_df["total_payment"].map(
    lambda x: f"{x:,.2f}"
)

display_df["monthly_payment"] = display_df["monthly_payment"].map(
    lambda x: f"{x:,.2f}"
)

# เปลี่ยนชื่อหัวตารางเป็นภาษาไทย
display_df.columns = [
    "บริษัท",
    "ดอกเบี้ย/ปี",
    "จำนวนปี",
    "ดอกเบี้ยรวม (บาท)",
    "ยอดชำระรวม (บาท)",
    "ค่างวด/เดือน (บาท)"
]

# แสดงตาราง
st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

# ==========================================
# สรุปข้อมูล
# ==========================================

st.divider()

st.subheader("📝 สรุปข้อมูล")

st.write(
    f"🚗 ราคารถยนต์ที่ใช้ในการคำนวณ: "
    f"**฿{car_price:,.2f}**"
)

st.write(
    f"💰 บริษัทที่มีดอกเบี้ยรวมต่ำสุด: "
    f"**บริษัท {lowest_interest_company}** "
    f"จำนวน **฿{lowest_interest:,.2f}**"
)

st.write(
    f"💳 บริษัทที่มีค่างวดต่อเดือนต่ำสุด: "
    f"**บริษัท {lowest_monthly_company}** "
    f"จำนวน **฿{lowest_monthly:,.2f} ต่อเดือน**"
)
    display_df,
    use_container_width=True,
    hide_index=True
)
