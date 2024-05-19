import streamlit as st
import pandas as pd
import os
import json


st.set_page_config(
    page_title="查询报名信息", 
    page_icon="./favicon.ico" if os.path.exists("../favicon.ico") else "🔍"
    )


def queryInfo(key:str="孩子身份证号"):
    
    query = st.text_input(f"输入{key}查询",placeholder=f"请输入{key}")
    
    if st.button("查询",key="query"):

        info_path = os.path.join("./infos",f"{query}.json")
        # 查询infos目录下是否存在文件名为f"{query}.json"的文件
        if not os.path.exists(info_path):
            st.warning(f"暂无报名信息")
            return
        
        with open(info_path,'r',encoding="utf8") as f:
            info:dict = json.load(f)
        
        image_path = info["上传孩子寸照"] #os.path.abspath(info["上传孩子寸照"])
        
        col1,col2 = st.columns(2)
        
        col1.image(image_path,caption="孩子寸照")

        info.pop("上传孩子寸照")
        
        # info的key作为index,value作为孩子信息字段
        df = pd.DataFrame(info,index=[0]).T#.style.set_properties(**{'text-align': 'left'})
        df.columns = ["孩子信息"]
        # 将info输出为一个表格
        infoTable = col2.table(df)


queryInfo()

