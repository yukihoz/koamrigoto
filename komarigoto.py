from st_aggrid import AgGrid
import pandas as pd
import streamlit as st
import numpy as np

from PIL import Image

import MeCab
mecab = MeCab.Tagger()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
font_path = 'Corporate-Logo-Bold-ver2.otf'
import altair as alt
#import datetime
from datetime import datetime, timedelta, timezone


st.set_page_config(layout="wide")
bannar = Image.open('bannar.png')
st.image(bannar)
#st.title(':face_with_monocle:  政治家に届けたい！子育ての実情アンケートの結果（仮）')
st.markdown('みらい子育て全国ネットワークでは、参院選に先立って2022年4月から6月にかけて「政治家に届けたい！子育ての実情アンケート」としてインターネット経由で妊娠中〜就学中のお子さんを子育て中の方々の声を集めてきました（のべ3,371件）。')
st.markdown('このwebサイトではアンケートの回答結果をテキスト解析した結果を見ることができる他、寄せられた回答結果の中身を読むことができます。また、都道府県や年代などで絞り込みを行うこともできます。')
st.markdown('参院選の候補者の皆様におかれましては、子育て世代がどのようなことに困っているのか、どういったことを解決してほしいとのかについて考えるきっかけとしていただければ幸いです。')
#st.markdown('**作った人：[ほづみゆうき](https://twitter.com/ninofku)**')

logs = pd.read_csv('./komarigoto.csv', encoding='UTF-8')#dataframeとしてcsvを読み込み
pref_list = pd.read_csv('./pref.csv', encoding='UTF-8')
#pref_list = pref_list_temp['都道府県']

oya_list = pd.read_csv('./oya_nendai.csv', encoding='UTF-8')

ko_list = pd.read_csv('./ko_nendai.csv', encoding='UTF-8')

st.header(':fork_and_knife: 使い方')
st.markdown('　寄せられた回答結果のテキスト解析結果（ワードクラウド）が自動的に表示されます。')
st.markdown('　都道府県や年代で結果を絞って見たければ、絞り込み条件を設定してみてください。')

#st.header(':fork_and_knife: 検索条件')

st.header(':cake: 結果表示')
st.markdown('初期表示では全国の回答結果が表示されています。都道府県などの絞りたいときは以下に条件を入れてください。')

with st.expander("条件での絞り込み（任意）", False):
    st.markdown(' ##### :round_pushpin:「都道府県」での絞り込み')
    st.markdown('都道府県で絞りたいときはチェックを入れて選択してください。チェックなしだと全国の声が表示されてます。')
    shibori = st.checkbox('都道府県で絞り込む')
    if shibori:
             option_selected_g = st.selectbox(
            'もう1度、全国で見たいときは上のチェックを外します。',
            pref_list
    )
# 議員選択
#option_selected_g = st.selectbox(
#    '政治家の名前をどれか選択してください。選んだ政治家の結果が表示されます。',
#    pref_list
#)

#親選択
    st.markdown(' ##### :woman:「親の年代」での絞り込み')
    option_selected_oya = st.multiselect(
    '親の年代で結果を絞りたい場合は使ってみてください。初期値では全部が選択されてます。',
    oya_list,
    ['19歳以下','20〜29歳','30〜39歳','40〜49歳','50〜59歳','60〜69歳','70歳以上'])
    option_selected_oya = '|'.join(option_selected_oya)

#委員会選択のテキスト化（後の条件付けのため
    f = open('temp_oya.txt', 'w')#textに書き込み
    f.writelines(option_selected_oya)
    f.close()
    option_selected_oya_txt = open("temp_oya.txt", encoding="utf8").read()

#子選択
    st.markdown(' ##### :boy:「子ども」での絞り込み')
    option_selected_ko = st.multiselect(
    '小学生や中学生など、子どもの段階によって結果を絞りたい場合に使ってみてください。初期値では全部が選択されてます。',
    ko_list,
    ['未就学(保育園、幼稚園等)','小学生','中学生','高校生','大学生・大学院生','就職・その他'])
    #['妊娠中','未就学(保育園、幼稚園等)','小学生','中学生','高校生','大学生・大学院生','就職・その他'])
    option_selected_ko = '|'.join(option_selected_ko)

#委員会選択のテキスト化（後の条件付けのため
f = open('temp_ko.txt', 'w')#textに書き込み
f.writelines(option_selected_ko)
f.close()
option_selected_ko_txt = open("temp_ko.txt", encoding="utf8").read()


logs_contents_temp = logs[(logs['親の年代'].str.contains(option_selected_oya_txt)) & (logs['子ども世代'].str.contains(option_selected_ko_txt))]

if shibori:
    logs_contents_temp = logs[(logs['都道府県'].str.contains(option_selected_g, na=False)) & (logs['親の年代'].str.contains(option_selected_oya_txt)) & (logs['子ども世代'].str.contains(option_selected_ko_txt))]
# # #後々の絞り込み条件のため残す logs_contents_temp = logs[(logs['都道府県'].str.contains(option_selected_g)) & (logs['委員会'].str.contains(option_selected_i_txt)) & (logs['内容分類']== "質問" ) & (logs['年度'] >= start_year) & (logs['年度'] <= end_year)]

logs_contents_temp_show = logs_contents_temp[["都道府県","自治体","親の年代","性別","子どもの数","子ども世代","意見","備考"]]
#logs_contents_temp_moji = logs_contents_temp.groupby('年度').sum()# 年度ごとの文字数
##文字カウント
#logs_contents_temp_moji = logs_contents_temp_moji['文字数']


# ワードクラウド作成
logs_contents = logs_contents_temp["意見"]

f = open('temp.txt', 'w')#textに書き込み
f.writelines(logs_contents)
f.close()

text = open("temp.txt", encoding="utf8").read()

results = mecab.parse(text)
result = results.split('\n')[:-2][0]

nouns = []
for result in results.split('\n')[:-2]:
        if '名詞' in result.split('\t')[4]:
            nouns.append(result.split('\t')[0])
words = ' '.join(nouns)

#st.markdown('　#### :face_with_monocle: 文字解析の結果')
JST = timezone(timedelta(hours=+9), 'JST')
#dt_now = datetime.datetime.now()
dt_now = datetime.now(JST)

#st.write('**[政治家名]**',option_selected_g, '**[対象年度]**',start_year,'-',end_year,'**[作成日時]**',dt_now)
#stpwds = ["子ども","子供","児童","園","子","皆","制度","文","場所","現在","ら","方々","こちら","性","化","場合","対象","一方","皆様","考え","それぞれ","意味","とも","内容","とおり","目","事業","つ","見解","検討","本当","議論","民","地域","万","確認","実際","先ほど","前","後","利用","説明","次","あたり","部分","状況","わけ","話","答弁","資料","半ば","とき","支援","形","今回","中","対応","必要","今後","質問","取り組み","終了","暫時","午前","たち","九十","八十","七十","六十","五十","四十","三十","問題","提出","進行","付託","議案","動議","以上","程度","異議","開会","午後","者","賛成","投票","再開","休憩","質疑","ただいま","議事","号","二十","平成","等","会","日","月","年","年度","委員","中央","点","区","委員会","賛成者","今","中央区","もの","こと","ふう","ところ","ほう","これ","私","わたし","僕","あなた","みんな","ただ","ほか","それ", "もの", "これ", "ところ","ため","うち","ここ","そう","どこ", "つもり", "いつ","あと","もん","はず","こと","そこ","あれ","なに","傍点","まま","事","人","方","何","時","一","二","三","四","五","六","七","八","九","十"]
stpwds = ["はず","まま","子ども","子供","児童","子","ため","こと","たち","いつ","うち","もの","それ","これ","こども","ところ","子育て"]

mask = np.array(Image.open('mask.png'))


wc = WordCloud(stopwords=stpwds, 
    width=1000, 
    height=1000, 
    background_color='white',
    colormap='Dark2',
    mask=mask,
    #colormap='coolwarm', 
    font_path = font_path
)
wc.generate(words)
wc.to_file('wc.png')
st.image('wc.png')
st.markdown('補足：更新するたびに表示位置などはビミョーに変わります。対象は名詞だけで、「それぞれ」や「問題」など、頻繁に使われるけど中身のないキーワードは除外してます。')

st.subheader(':coffee: 意見の詳細')
option_selected_l = st.text_input('上記の解析結果の対象となった意見の詳細です。以下にキーワードを入れると、絞り込みを行えます', '')

logs_contents_temp_show = logs_contents_temp_show[(logs_contents_temp_show['意見'].str.contains(option_selected_l))]

    #table作成
#with st.expander("■ 解析対象の文字列", False):
    #st.markdown('　#### :open_book: 解析対象の文字列')
grid_options = {
    "columnDefs":[
    {
        "headerName":"都道府県",
        "field":"都道府県",
        "suppressSizeToFit":True,
        "autoHeight":True,
        "maxWidth":100,
    },
    {
        "headerName":"自治体",
        "field":"自治体",
        "suppressSizeToFit":True,
        "autoHeight":True,

    },
    {
        "headerName":"親の年代",
        "field":"親の年代",
        "suppressSizeToFit":True,
        "autoHeight":True,

    },
    {
        "headerName":"性別",
        "field":"性別",
        "suppressSizeToFit":True,
        "autoHeight":True,

    },
    {
        "headerName":"子どもの数",
        "field":"子どもの数",
        "suppressSizeToFit":True,
        "autoHeight":True,
    },
    {
        "headerName":"子ども世代",
        "field":"子ども世代",
        "suppressSizeToFit":True,
        "autoHeight":True,

    },
    {
        "headerName":"性別",
        "field":"性別",
        "suppressSizeToFit":True,
        "autoHeight":True,

    },
    {
        "headerName":"意見",
        "field":"意見",
        "wrapText":True,
        "autoHeight":True,
        "suppressSizeToFit":True,
        "maxWidth":400,
        "minWidth":400,
    },
    {
        "headerName":"備考",
        "field":"備考",
        "wrapText":True,
        "autoHeight":True,
        "suppressSizeToFit":True,
        "maxWidth":200,
        "minWidth":200,

    },
    ],
}
AgGrid(logs_contents_temp_show, grid_options)

st.header(':paperclip: 作成責任者')
st.markdown('みらい子育て全国ネットワーク（#GoTo候補者2022）：https://miraco-net.com/project/seisaku/27910/')

st.markdown('【SNSアカウント一覧】')
st.markdown('・Webサイト: https://miraco-net.com/')
st.markdown('・Facebook https://www.facebook.com/hoikuenhairitai')
st.markdown('・Twitter https://twitter.com/hoikuenhairitai')
st.markdown('・Instagram https://www.instagram.com/miraco_net/')
