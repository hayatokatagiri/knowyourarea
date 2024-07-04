# import
import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# サーバーを立ち上げるにはターミナルで以下のコマンドを実行
# streamlit run src/app.py

# ページ設定
st.set_page_config(page_title="KnowYourArea")

# データの読み込み
df = pd.read_csv(
    "data/2020_2010_kokucho_shochiiki_tanba_sasayama_foranalysis.csv",
    encoding="cp932")

# "CITYNAME"列の値が"篠山市"の行を"丹波篠山市"に置き換える
df.loc[df["CITYNAME"] == "篠山市", "CITYNAME"] = "丹波篠山市"


# main処理
st.html("<h1><center>KnowYourArea</center></h1>")
st.html("<h2><center>兵庫県丹波地域版</center></h2>")
st.html("<center>兵庫県丹波地域（丹波篠山・丹波市）の自治会ごとの人口動態を可視化したサイトです。</h2>")

# area_name = st.text_input('地域名を入力', '住山')  # area_nameに地域名が格納される
# st.write('入力された地域名：', area_name)

# "CITY"列と"NAME"列を連結して新しい列"CITY_NAME"を作成
df["CITY_NAME"] = df["CITYNAME"] + " - " + df["NAME"]
st.write("エリア名（自治会名）を選択してください。")
# ユーザーにエリア名を選択させるためのプルダウンメニュー
selected_city_name = st.selectbox("エリア名", df["CITY_NAME"].unique())

# 選択されたCITY_NAMEから対応するNAMEを抽出
area_name = df[df["CITY_NAME"] == selected_city_name]["NAME"].values[0]


# 入力されたエリア名に一致する行を取得
area_data = df[df["NAME"] == area_name]

# 基礎データ（2020）
st.html("<h3><center>基礎データ（2020）</center></h3>")
# 当該地域の2020年における人口総数
area_pop = df.loc[df["NAME"] == area_name, "人口総数20"].values[0]
st.write('人口総数(人)：', area_pop)

# 当該地域の2020年における65歳以上高齢化率
area_age65 = df.loc[df["NAME"] == area_name, "高齢化率20"].values[0]
area_age65 = round(area_age65, 2) * 100
st.write('高齢化率(%)：', area_age65)
# 第一次産業比率
prime_indst = df.loc[df["NAME"] == area_name, "第一次産業比率20"].values[0]
prime_indst = round(prime_indst, 2) * 100
st.write('第一次産業比率(%)：', prime_indst)
# 第二次産業比率
second_indst = df.loc[df["NAME"] == area_name, "第二次産業比率20"].values[0]
second_indst = round(second_indst, 2) * 100
st.write('第二次産業比率(%)：', second_indst)
# 第三次産業比率
third_indst = df.loc[df["NAME"] == area_name, "第三次産業比率20"].values[0]
third_indst = round(third_indst, 2) * 100
st.write('第三次産業比率(%)：', third_indst)
# 持ち家比率
ownhouse = df.loc[df["NAME"] == area_name, "持ち家比率20"].values[0]
ownhouse = round(ownhouse, 2) * 100
st.write('持ち家比率(%)：', ownhouse)

# 入力されたエリア名に一致する行を取得
area_data = df[df["NAME"] == area_name]

# 入力されたエリア名が存在しない場合の処理
if area_data.empty:
    print(f"エリア名 '{area_name}' は存在しません。")
else:
    # 年齢階級のリスト
    age_groups = [
        "0_4", "5_9", "10_14", "15_19", "20_24", "25_29", "30_34", "35_39",
        "40_44", "45_49", "50_54", "55_59", "60_64", "65_69", "70_74", "75_79",
        "80_84", "85_89", "90_94", "95_99", "over100"
    ]

    # 男性人口と女性人口のリスト
    male_population = [-area_data[f"男20_{age}"].values[0]
                       for age in age_groups]
    female_population = [
        area_data[f"女20_{age}"].values[0] for age in age_groups]

    # プロットの設定
    fig_pyramid, ax = plt.subplots(figsize=(10, 8))

    # バーチャートをプロット
    ax.barh(age_groups, male_population, color='#00ced1', label='Male')
    ax.barh(age_groups, female_population, color='#ff69b4', label='Female')

    # ラベルとタイトルの設定
    ax.set_xlabel('Population')
    ax.set_ylabel('Age Group')
    # ax.set_title(f'Population Pyramid')
    ax.legend()

    # x軸のラベルを正の値にするための設定
    ax.set_xticklabels([str(abs(int(x))) for x in ax.get_xticks()])

    # グリッドラインを追加
    ax.grid(True)

# 人口推移
# 年と人口のデータ
years = [2010, 2015, 2020]
population = [
    area_data["人口総数10"].values[0],
    area_data["人口総数15"].values[0],
    area_data["人口総数20"].values[0]
]

# 折れ線グラフの設定
fig_poptrans, ax_poptrans = plt.subplots(figsize=(10, 6))
# 折れ線グラフをプロット
ax_poptrans.plot(years, population, marker='o', linestyle='-', color='b')

# ラベルとタイトルの設定
ax_poptrans.set_xlabel('Year')
ax_poptrans.set_ylabel('Population')
ax_poptrans.grid(True)

# 高齢化率の推移
aging_rates = [
    area_data["高齢化率10"].values[0],
    area_data["高齢化率15"].values[0],
    area_data["高齢化率20"].values[0]
]

# 折れ線グラフの設定
fig_aging, ax_aging = plt.subplots(figsize=(10, 6))

# 折れ線グラフをプロット
ax_aging.plot(years, aging_rates, marker='o', linestyle='-', color='g')

# ラベルとタイトルの設定
ax_aging.set_xlabel('Year')
ax_aging.set_ylabel('Aging Rate')
ax_aging.grid(True)

# Y軸の目盛りを設定
ax_aging.set_yticks([0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7])
# X軸のメモリを2010年、2015年、2020年のみに設定
ax_aging.set_xticks(years)


# X軸のメモリを2010年、2015年、2020年のみに設定
ax_poptrans.set_xticks(years)

# グラフを表示
st.html("<h3><center>人口ピラミッド（2020）</center></h3>")
st.pyplot(fig_pyramid)

st.html("<h3><center>人口総数推移（2010-20）</center></h3>")
st.pyplot(fig_poptrans)

st.html("<h3><center>高齢化率推移（2010-2020）</center></h3>")
st.pyplot(fig_aging)

st.html("<h3><center>丹波地域国勢調査（2010-2020）</center></h3>")
st.dataframe(df)

st.markdown('<p style="font-size:small; text-align:center;">(C)Hayato Katagiri All Rights Reserverd.</p>',
            unsafe_allow_html=True)
st.markdown('<p style="font-size:small; text-align:center;">【データ出典】国勢調査小地域データ(2010年-2020年)</p>',
            unsafe_allow_html=True)
