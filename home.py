import streamlit as st
import pandas as pd
import datetime
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe
import calendar
from pytz import timezone

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

credentials = Credentials.from_service_account_file(
    'duty-387503-69ca976b8f4f.json',
    scopes=scopes
)

gc = gspread.authorize(credentials)

SP_SHEET_KEY = '1rJhhD8Z92qa5Koa8SY9u4v8GgmnuW4mPnQHUo26mBLE'
NL_SHEET_KEY = '1Yj38mvHd84fQKZbLUUymrPiYV6336ViA-U7jLciEG6g'
sh = gc.open_by_key(SP_SHEET_KEY)
nl = gc.open_by_key(NL_SHEET_KEY)
HD_NAME = 'holidays'
NL_NAME = 'namelist'
A1st_NAME = 'A_1st'
A2nd_NAME = 'A_2nd'
hds = sh.worksheet(HD_NAME)
names = nl.worksheet(NL_NAME)
A1st = sh.worksheet(A1st_NAME)
A2nd = sh.worksheet(A2nd_NAME)
holidayslist = hds.get_all_values()
namelist = names.get_all_values()
A1stlist = A1st.get_all_values()
A2ndlist = A2nd.get_all_values()
df_names = pd.DataFrame(namelist[1:],columns=namelist[0])
df_holidays = pd.DataFrame(holidayslist[1:],columns=holidayslist[0])
df_A1st = pd.DataFrame(A1stlist[1:],columns=A1stlist[0])
df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
hds_arr =  holidayslist[1:]
namelist1 = df_names['1年目名簿']
namelist2 = df_names['2年目名簿']
timelist1 = df_A1st['Time']
timelist2 = df_A2nd['Time']
dtnow = datetime.datetime.now()
now = dtnow.astimezone(timezone('Asia/Tokyo')).strftime('%Y/%m/%d %H:%M:%S')
year = int(dtnow.strftime('%Y'))
month = int(dtnow.strftime('%m'))+1
if month == 13:
    year = year+1
    month = 1
namelist_link = '[研修医名簿](https://docs.google.com/spreadsheets/d/1Yj38mvHd84fQKZbLUUymrPiYV6336ViA-U7jLciEG6g/edit?usp=sharing)'
Table1_link = '[1年目振り分け表](https://docs.google.com/spreadsheets/d/1Ry_BkXERLYMfQ4_mdOT3XdA-PeB76k6cBHjunToLCoE/edit?usp=sharing)'
Table2_link = '[2年目振り分け表](https://docs.google.com/spreadsheets/d/1jFIYV1Ey36-5_0iWMwZtB9g7VtJjplXAH50tj4Hu4MI/edit?usp=sharing)'

def page_home():
    st.title('Home')
    """
    ##### 回答フォームは左上のメニューから該当のフォームで回答してください。
    ##### (スマホで回答する方は少し上にスクロールして出てくる＞をタップして)
    #### ＊くれぐれも、他人の名前で回答しないようにお願いします。
    #####
    ##### 日当直決め担当者は以下の要領で行ってください。
    ##### 1．左上のメニューから管理者ページにアクセスし、祝日の登録、名簿の確認を行って下さい。
    ##### 2．下記のリンクから振り分け表にアクセスし、表を完成させてください。
    """
    st.markdown(Table1_link, unsafe_allow_html=True)
    st.markdown(Table2_link, unsafe_allow_html=True)
    """
    ### ＊回答状況＊
    """
    st.write("間違いや再回答をした場合は、以下の履歴を参考に回答を削除してください。")
    st.write("＊トラブル回避のため自動的な上書き機能は廃止されました。また、1つずつしか削除できないようにしています。")
    df_A1st = pd.DataFrame(A1stlist[1:],columns=A1stlist[0])
    with st.form("delete1"):
        st.write(df_A1st)
        id1 = st.selectbox("注意して、削除したい回答の時間を選択してください。",timelist1)
        deleted = st.form_submit_button("Delete")
        if deleted:
            df_A1st = pd.DataFrame(A1stlist[1:],columns=A1stlist[0])
            df_A1st = df_A1st[df_A1st['Time']!=id1]
            A1st.clear()
            set_with_dataframe(A1st,df_A1st,row=1,col=1)
            st.write("選択したデータを削除しました。")
            st.write("＊もう一度削除する際は、必ずページを再読み込みしてください。")
            st.write(df_A1st) 
    df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
    with st.form("delete2"):
        st.write(df_A2nd)
        id2 = st.selectbox("注意して、削除したい回答の時間を選択してください。",timelist2)
        deleted = st.form_submit_button("Delete")
        if deleted:
            df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
            df_A2nd = df_A2nd[df_A2nd['Time']!=id2]
            A2nd.clear()
            set_with_dataframe(A2nd,df_A2nd,row=1,col=1)
            st.write("選択したデータを削除しました。")
            st.write("＊もう一度削除する際は、必ずページを再読み込みしてください。")
            st.write(df_A2nd)
    

def page_form1():
    st.title('1年目_日当直回答フォーム')
    """
    ###### 【日直・当直アンケート記載注意点】
    ######  休日は日直・当直それぞれあるので、回答をお願いします！！				
    ######  <内科ローテ>　外来研修、午前/午後救急に当直明けを被せないで下さい！　(午後救急の後の当直は自己責任で！)　循環器・呼吸器は水曜日に、研修医の重大な御仕事(シンチ、ブロンコ)があるので火曜日は原則当直を入れないで下さい！
    ######  <外科ローテ>　原則的に当直前と当直明けにオペ日を被せないようにして下さい！　チームの手術日（曜日）を確認して解答お願いします！				
    ######  <麻酔科ローテ>　ICU研修がある場合、その期間には当直を被せないで下さい！								
    ######  <精神科ローテ>　当直・当直明けでの早退・欠勤を避けるため、土曜日直・土曜当直・日曜日直しか入れないです！御了承下さい！
    """
    with st.form("my_form"):
        cal = calendar.Calendar().itermonthdays2(year,month)
        cal_arr = list(cal)
        new_cal_arr = []
        new_hds_arr = []
        for x in cal_arr:
            if x[0] == 0:
                del x
            else:
                if x[1] == 0:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (月)")
                elif x[1] == 1:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (火)")
                elif x[1] == 2:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (水)")
                elif x[1] == 3:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (木)")
                elif x[1] == 4:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (金)")
                elif x[1] == 5:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (土)")
                elif x[1] == 6:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (日)")
        for y in cal_arr:
            if y[0] == 0:
                del y
            else:
                if y[1] == 5:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (土)")
                elif y[1] == 6:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (日)")
                else:
                    del y
        for z in hds_arr:
            new_hds_arr.append(str(z[0]))            
                
        
        yourname = st.selectbox(
            'あなたの名前を選んでください',
            namelist1
            )

        comment = st.text_input(
            'ご要望等あればご記載ください。'
        )

        left_col, right_col = st.columns(2)

        with left_col:

            '当直がNGな日を選んでください',
                
            NG_list1 = []
            for x in new_cal_arr:
                checked1 = st.checkbox(str(x),key="cb1"+str(x))
                if checked1:
                    NG_list1.append(str(x))


        with right_col:
            '日直がNGな日を選んでください',
                
            NG_list2 = []
            for y in new_hds_arr:
                checked2 = st.checkbox(str(y),key="cb2"+str(y))
                if checked2:
                    NG_list2.append(str(y))

        demandsA1 = st.multiselect("当直の希望日があれば入力ください（参考程度です）",new_cal_arr)
        demandsB1 = st.multiselect("日直の希望日があれば入力ください（参考程度です）",new_hds_arr)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Time: ", now)
            st.write("Name: ", yourname)
            st.write('Your comment: ', comment)
            st.write('You selected: ', NG_list1, NG_list2)
            st.write("上記の内容で提出しました。")
            df_A1st = pd.DataFrame(A1stlist[1:],columns=A1stlist[0])
            data1 = [[now,yourname,comment,NG_list1,NG_list2,demandsA1,demandsB1]]
            columns1 = ['Time','Name','Comment','NG1','NG2','OK1','OK2']
            nd = pd.DataFrame(data=data1,columns=columns1)
            df_A1st = pd.concat([df_A1st,nd],axis=0,)
            set_with_dataframe(A1st,df_A1st,row=1,col=1)
            st.write(df_A1st) 
        

def page_form2():
    st.title('2年目_日当直回答フォーム')
    """
    ###### 【日直・当直アンケート記載注意点】
    ######  休日は日直・当直それぞれあるので、回答をお願いします！！				
    ######  <内科ローテ>　外来研修、午前/午後救急に当直明けを被せないで下さい！　(午後救急の後の当直は自己責任で！)　循環器・呼吸器は水曜日に、研修医の重大な御仕事(シンチ、ブロンコ)があるので火曜日は原則当直を入れないで下さい！
    ######  <外科ローテ>　原則的に当直前と当直明けにオペ日を被せないようにして下さい！　チームの手術日（曜日）を確認して解答お願いします！				
    ######  <麻酔科ローテ>　ICU研修がある場合、その期間には当直を被せないで下さい！								
    ######  <精神科ローテ>　当直・当直明けでの早退・欠勤を避けるため、土曜日直・土曜当直・日曜日直しか入れないです！御了承下さい！
    """
    with st.form("my_form"):
        cal = calendar.Calendar().itermonthdays2(year,month)
        cal_arr = list(cal)
        new_cal_arr = []
        new_hds_arr = []
        for x in cal_arr:
            if x[0] == 0:
                del x
            else:
                if x[1] == 0:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (月)")
                elif x[1] == 1:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (火)")
                elif x[1] == 2:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (水)")
                elif x[1] == 3:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (木)")
                elif x[1] == 4:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (金)")
                elif x[1] == 5:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (土)")
                elif x[1] == 6:
                    new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (日)")
        for y in cal_arr:
            if y[0] == 0:
                del y
            else:
                if y[1] == 5:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (土)")
                elif y[1] == 6:
                    new_hds_arr.append(str(year)+"/"+str(month)+"/"+str(y[0])+" (日)")
                else:
                    del y
        for z in hds_arr:
            new_hds_arr.append(str(z[0]))            
                
        
        yourname = st.selectbox(
            'あなたの名前を選んでください',
            namelist2
            )

        comment = st.text_input(
            'ご要望等あればご記載ください。'
        )

        left_col, right_col = st.columns(2)

        with left_col:

            '当直がNGな日を選んでください',
                
            NG_list1 = []
            for x in new_cal_arr:
                checked1 = st.checkbox(str(x),key="cb1"+str(x))
                if checked1:
                    NG_list1.append(str(x))


        with right_col:
            '日直がNGな日を選んでください',
                
            NG_list2 = []
            for y in new_hds_arr:
                checked2 = st.checkbox(str(y),key="cb2"+str(y))
                if checked2:
                    NG_list2.append(str(y))

        demandsA2 = st.multiselect("当直の希望日があれば入力ください（参考程度です）",new_cal_arr)
        demandsB2 = st.multiselect("日直の希望日があれば入力ください（参考程度です）",new_hds_arr)

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("Time: ", now)
            st.write("Name: ", yourname)
            st.write('Your comment: ', comment)
            st.write('You selected: ', NG_list1, NG_list2)
            st.write("上記の内容で提出しました")
            df_A2nd = pd.DataFrame(A2ndlist[1:],columns=A2ndlist[0])
            data2 = [[now,yourname,comment,NG_list1,NG_list2,demandsA2,demandsB2]]
            columns2 = ['Time','Name','Comment','NG1','NG2','OK1','OK2']
            nd = pd.DataFrame(data=data2,columns=columns2)
            df_A2nd = pd.concat([df_A2nd,nd],axis=0,)
            set_with_dataframe(A2nd,df_A2nd,row=1,col=1)
            st.write(df_A2nd)

def page_manager():
    st.title('管理者ページ')
    cal = calendar.Calendar().itermonthdays2(year,month)
    cal_arr = list(cal)
    new_cal_arr = []
    for x in cal_arr:
        if x[0] == 0:
            del x
        else:
            if x[1] == 0:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (月)")
            elif x[1] == 1:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (火)")
            elif x[1] == 2:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (水)")
            elif x[1] == 3:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (木)")
            elif x[1] == 4:
                new_cal_arr.append(str(year)+"/"+str(month)+"/"+str(x[0])+" (金)")
            elif x[1] == 5:
                del x
            elif x[1] == 6:
                del x
    
    with st.form("holidays"):
        newholidays = st.multiselect(
            '土日を除いた祝日を選んでください。Submitを忘れずに。*祝日のない月であっても、空欄でSubmitしてください。',
            new_cal_arr
        )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")
        if submitted:
            st.write("祝日: ", newholidays, "として登録しました。")
            df_holidays = pd.DataFrame({'holidays':newholidays})
            hds.clear()
            set_with_dataframe(hds,df_holidays,row=1,col=1)
            
            st.write(df_holidays)


    "名簿を確認して、編集が必要であれば以下のリンクからGoogleSheetを編集してください。"
    st.dataframe(df_names)
    st.markdown(namelist_link, unsafe_allow_html=True)


selected_page = st.sidebar.radio(
    "メニュー", 
    ["HOME", 
     "1年目の回答フォーム", "2年目の回答フォーム", "管理者ページ"
     ]
    )

if selected_page == "HOME":
    page_home()
elif selected_page == "1年目の回答フォーム":
    page_form1()
elif selected_page == "2年目の回答フォーム":
    page_form2()
elif selected_page == "管理者ページ":
    page_manager()
else:
    pass




