from st_aggrid import AgGrid
import pandas as pd
import streamlit as st


import MeCab
mecab = MeCab.Tagger()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
font_path = 'Corporate-Logo-Bold-ver2.otf'
import altair as alt
#import datetime
from datetime import datetime, timedelta, timezone


st.set_page_config(layout="wide")
st.title(':face_with_monocle:  政治家に届けたい！子育ての実情アンケートの結果（仮）')
#st.subheader('「この政治家、どういう考えの人なんだろ？？」と思っても、議会の議事録とか眺めるのしんどいよね…:dizzy_face:')
#st.markdown('　SNSとかで発信している政治家も最近は増えてきてますが、何やってるかよく分からない人の方が多いというのが実際のところではないでしょうか。一応議会とかに出席してあれこれやってるんだろうけど、その議事録とか見るのはだらだら長くてしんどい。')
st.markdown('　子育ての実状に関するアンケートを実施して、この結果について文字解析の技術でざっくりと可視化してみてみました（いわゆるワードクラウドというやつ）。')
#st.markdown('　対象はわたしの住んでる東京都中央区議会、期間は2022年3月時点で入手できた2015年5月から2021年10月まで。')
#st.markdown('　python + streamlitで作ってます。超初心者の習作なもので色々ツッコミどころはあるかと思います。こうすればもっと良いよ！とか教えてもらえると嬉しいです。一緒にやろうよ！という人がいてくれるともっと嬉しいです。コメント、ツッコミはお気軽に。')
#st.markdown('**作った人：[ほづみゆうき](https://twitter.com/ninofku)**')

logs = pd.read_csv('./komarigoto3.csv', encoding='UTF-8')#dataframeとしてcsvを読み込み
pref_list = pd.read_csv('./pref.csv', encoding='UTF-8')
#pref_list = pref_list_temp['都道府県']

oya_list = pd.read_csv('./oya_nendai.csv', encoding='UTF-8')

ko_list = pd.read_csv('./ko_nendai.csv', encoding='UTF-8')

st.header(':fork_and_knife: 使い方')
st.markdown('　寄せられた回答のワードクラウドが自動的に表示されます。')
st.markdown('　都道府県とか年代で結果を絞って見たければ、絞り込み条件を設定してみてください。')

#st.header(':fork_and_knife: 検索条件')

st.header(':cake: 結果表示')
st.markdown('初期表示では全国の声が表示されています。都道府県などの絞りたいときは以下に条件を入れてください。')

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

#stpwds = ["様","辺","なし","分","款","皆","さん","議会","文","場所","現在","ら","方々","こちら","性","化","場合","対象","一方","皆様","考え","それぞれ","意味","とも","内容","とおり","目","事業","つ","見解","検討","本当","議論","民","地域","万","確認","実際","先ほど","前","後","利用","説明","次","あたり","部分","状況","わけ","話","答弁","資料","半ば","とき","支援","形","今回","中","対応","必要","今後","質問","取り組み","終了","暫時","午前","たち","九十","八十","七十","六十","五十","四十","三十","問題","提出","進行","付託","議案","動議","以上","程度","異議","開会","午後","者","賛成","投票","再開","休憩","質疑","ただいま","議事","号","二十","平成","等","会","日","月","年","年度","委員","中央","点","区","委員会","賛成者","今","中央区","もの","こと","ふう","ところ","ほう","これ","私","わたし","僕","あなた","みんな","ただ","ほか","それ", "もの", "これ", "ところ","ため","うち","ここ","そう","どこ", "つもり", "いつ","あと","もん","はず","こと","そこ","あれ","なに","傍点","まま","事","人","方","何","時","一","二","三","四","五","六","七","八","九","十"]
stpwds = ["子ども","子供","児童","園","子","皆","制度","文","場所","現在","ら","方々","こちら","性","化","場合","対象","一方","皆様","考え","それぞれ","意味","とも","内容","とおり","目","事業","つ","見解","検討","本当","議論","民","地域","万","確認","実際","先ほど","前","後","利用","説明","次","あたり","部分","状況","わけ","話","答弁","資料","半ば","とき","支援","形","今回","中","対応","必要","今後","質問","取り組み","終了","暫時","午前","たち","九十","八十","七十","六十","五十","四十","三十","問題","提出","進行","付託","議案","動議","以上","程度","異議","開会","午後","者","賛成","投票","再開","休憩","質疑","ただいま","議事","号","二十","平成","等","会","日","月","年","年度","委員","中央","点","区","委員会","賛成者","今","中央区","もの","こと","ふう","ところ","ほう","これ","私","わたし","僕","あなた","みんな","ただ","ほか","それ", "もの", "これ", "ところ","ため","うち","ここ","そう","どこ", "つもり", "いつ","あと","もん","はず","こと","そこ","あれ","なに","傍点","まま","事","人","方","何","時","一","二","三","四","五","六","七","八","九","十"]


wc = WordCloud(stopwords=stpwds, 
    width=1000, 
    height=1000, 
    background_color='white',
    colormap='Dark2', 
    #colormap='coolwarm', 
    font_path = font_path
)
wc.generate(words)
wc.to_file('wc.png')
st.image('wc.png')
st.markdown('補足：更新するたびに表示位置などはビミョーに変わります。対象は名詞だけで、「それぞれ」や「問題」など、頻繁に使われるけど中身のないキーワードは除外してます。')

#with st.expander("■ 年度単位での発言文字数の推移", False):
##st.markdown('　#### :chart_with_upwards_trend: 年度単位での発言文字数の推移')
#    st.markdown('　それぞれの年度でどの程度発言されているのかを推移を示したものです。')
#    #チャート作成
#    st.bar_chart(logs_contents_temp_moji)
#    #集計文字数表示
#    st.metric(label="発言文字数", value=len(text))

option_selected_l = st.text_input('キーワード入力してね。', '')

selected_l = logs_contents_temp_show[(logs_contents_temp_show['内容'].str.contains(option_selected_l))


    #table作成
with st.expander("■ 解析対象の文字列", False):
    #st.markdown('　#### :open_book: 解析対象の文字列')
    st.markdown('　上記の解析結果の対象となった文字列です。もうちょい細かく見たいこともあるかと思い表示させてみました（改行がうまくできてなくてすいません…）')
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
#    AgGrid(logs_contents_temp_show)
#st.header(':paperclip: 情報参照元')
#st.markdown('分析の元になっているデータは、[中央区議会 Webサイト](https://www.kugikai.city.chuo.lg.jp/index.html)の「会議録検索」からHTMLファイルをごっそりダウンロードして、その上であれこれ苦心して加工して作成しました。注意して作業はしたつもりですが、一部のデータが欠損等している可能性もありますのでご承知おきください。もし不備等ありましたら[ほづみゆうき](https://twitter.com/ninofku)まで声掛けいただけるとありがたいです。')
st.header(':paperclip: 作成責任者')
st.markdown('このサイトは、みらい子育て全国ネットワーク(https://miraco-net.com/)が作成しました。')

