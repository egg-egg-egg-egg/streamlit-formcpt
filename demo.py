import argparse
import json
import os
from typing import List,Dict

import streamlit as st
import pandas as pd

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


# 侧边栏组件
with st.sidebar:
    st.title("查看报名信息")

    # 输入家长手机号
    phone = st.text_input("输入手机号查询",placeholder="输入手机号")
    
    if st.button("查询") and len(phone)==11:
        infos_dir = "./infos"
        # 读取一个目录下的所有json文件
        filenames = os.listdir(infos_dir)
        for filename in filenames:
            with open(f"{infos_dir}/{filename}",'r',encoding="utf8") as f:
                info:dict = json.load(f)
                
            if info["家长手机号"] != phone:
                continue

            image_path = info["上传孩子寸照"]
            
            # 读取infos["上传孩子寸照"]路径中的图片
            with open(info["上传孩子寸照"],'rb') as f:
                st.image(f.read(),caption="孩子寸照")
            info.pop("上传孩子寸照")
            info.pop("家长手机号")
            
            # info的key作为index,value作为孩子信息字段
            df = pd.DataFrame(info,index=[0]).T#.style.set_properties(**{'text-align': 'left'})
            df.columns = ["孩子信息"]
            # 将info输出为一个表格
            infoTable = st.table(df)