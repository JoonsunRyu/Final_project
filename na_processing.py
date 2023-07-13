import pandas as pd
import numpy as np

##### Data frame 호출 #####
def df_open():
    df = pd.read_csv('./data/df_json.csv', encoding = 'UTF-8')  # csv파일 경로는 각자 환경에 따라 맞춰주면 됨
    return df

df_json = df_open()


##### 열 삭제 #####
def col_delete():
    df_json.drop(['Unnamed: 0', 'id', 'size', 'drug_S', 'width', 'height', 'mark_code_front', 'mark_code_back', 'line_front',
                  'line_back', 'mark_code_front_anal', 'mark_code_back_anal', 'mark_code_front_img', 'mark_code_back_img',
                  'color_class2', 'file_name', 'dl_company_en', 'di_company_mf', 'di_company_mf_en', 'img_regist_ts',
                  'change_date', 'back_color', 'light_color', 'camera_la', 'camera_lo', 'print_back'],
                  axis = 1, inplace = True)
    return df_json

df_json = col_delete()


##### fillna #####
# 0으로 채우기
def fill_zero():
    df_json['leng_long'].fillna(0, inplace = True)
    df_json['leng_short'].fillna(0, inplace = True)
    df_json['thick'].fillna(0, inplace = True)
    return df_json

df_json = fill_zero()

# unknown으로 채우기
def fill_unknown():
    df_json.fillna('unknown', inplace = True)
    return df_json

df_json = fill_unknown()
# print(df_json.isna().sum())  # 확인용


#### 문자열 처리 - by 정규표현식 ####
def preprocessing():
    df_json['di_edi_code'] = df_json['di_edi_code'].astype(str)  # str이랑 섞여있는것들 str타입으로 변경

    # ,구분자 처리
    df_json['dl_name'] = df_json['dl_name'].str.replace(',', ' ') 
    df_json['dl_name_en'] = df_json['dl_name_en'].str.replace(',', ' ')
    df_json['print_front'] = df_json['print_front'].str.replace(',', ' ')
    df_json['dl_custom_shape'] = df_json['dl_custom_shape'].str.replace(',', '|')
    df_json['di_class_no'] = df_json['di_class_no'].str.replace(',', '|')
    df_json['di_edi_code'] = df_json['di_edi_code'].str.replace(',', '|')
    df_json['color_class1'] = df_json['color_class1'].str.replace(',', '|')
    df_json['form_code_name'] = df_json['form_code_name'].str.replace(',', '|')

    # .구분자 처리
    df_json['di_class_no'] = df_json['di_class_no'].str.replace('.', '|')
    df_json['dl_material'] = df_json['dl_material'].str.replace('.', '|')
    df_json['dl_material_en'] = df_json['dl_material_en'].str.replace('.', '|')
    df_json['dl_name'] = df_json['dl_name'].str.replace(',', '|')
    df_json['dl_name_en'] = df_json['dl_name_en'].str.replace(',', '|')

    # 공백처리
    df_json['di_edi_code'] = df_json['di_edi_code'].astype(str).replace(r'\.0$', '', regex = True)
    df_json['leng_short'] = df_json['leng_short'].replace(r'\s', '', regex = True)
    df_json['leng_long'] = df_json['leng_long'].replace(r'\s', '', regex = True)
    df_json['thick'] = df_json['thick'].replace(r'\s', '', regex = True)

    # name 분리
    df_json['dl_name_korean'] = df_json['dl_name'].str.extract(r'([가-힣]+)', expand = False)
    df_json['dl_name_nonkorean'] = df_json['dl_name'].str.extract(r'([^가-힣]+)', expand = False)

    # chart 삭제
    df_json.drop('chart', axis = 1, inplace = True)
    df_json['dl_name_nonkorean'] = df_json['dl_name_nonkorean'].fillna('unknown')
    # df.to_csv('data_ho.csv')
    return df_json

df_json = preprocessing()


##### csv로 저장하기 #####
# df_json.to_csv('./data/df_pre-processing.csv', encoding = 'UTF-8', index = False)