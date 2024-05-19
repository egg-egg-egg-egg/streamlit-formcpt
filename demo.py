import argparse
import json
import os
from typing import List,Dict

import streamlit as st

import formcpt as fcpt

# 创建一个解析对象
parser = argparse.ArgumentParser(description='选择测试环境')

# 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('--env', default='needItem.json', help='设置环境参数')

# 进行解析
args = parser.parse_args()

st.set_page_config(
    page_title="报名系统", 
    page_icon="favicon.ico" if os.path.exists("favicon.ico") else "😊"
    )
st.title("全国青少年中开展综合素质测评报名")

# 前往查询页面
st.page_link("pages/demo_query.py", label="查询报名信息", icon="🔍")

if st.session_state.get("init", True):
    # 读取json数据
    item_file = args.env
    with open(item_file,encoding="utf8") as f:
        needItem:List[Dict] = json.load(f)
        st.session_state["needItem"] = needItem 
    form = fcpt.FormCpt(st.session_state["needItem"])
    st.session_state["form"] = form
    # 如果不存在infos,photos文件夹则创建
    os.makedirs("infos", exist_ok=True)
    os.makedirs("photos", exist_ok=True)
    
    st.session_state["init"] = False
    

def submitInfo():
    # 未填写的信息显示错误
    form:fcpt.FormCpt = st.session_state["form"]
    # 判断信息是否完整
    if form:# 保存数据
        infos = form.infos

        # 表单数据的操作逻辑自定义    
        # TODO 需要有个配置项文件，表示以什么数据作为文件名
        filename = infos['孩子身份证号']
        name = infos["上传孩子寸照"].name
        # 提取filetype中的文件后缀
        imagename = "./photos/"+ filename + "." + name.split(".")[-1]
        img_data = infos["上传孩子寸照"].read()
        with open(f"{imagename}",'wb') as f:
            f.write(img_data)

        # 保存数据
        with open(f"./infos/{filename}.json",'w',encoding="utf8") as f:
            infos["上传孩子寸照"] = imagename
            json.dump(infos,f,ensure_ascii=False)
        st.info("提交成功")

        if args.env != "needItem.json":
            st.write(infos)
            st.write(bool(args.env))
        

with st.form("tableList"):
        
    form = st.session_state["form"]
    form()

    # Every form must have a submit button.
    submitted = st.form_submit_button("提交信息")
    if submitted:
        submitInfo()
