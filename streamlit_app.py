import streamlit as st
import json
import argparse
import os

# 创建一个解析对象
parser = argparse.ArgumentParser(description='选择测试环境')

# 向该对象中添加你要关注的命令行参数和选项
parser.add_argument('--env', default='prod', help='设置环境参数')

# 进行解析
args = parser.parse_args()


st.set_page_config(
    page_title="报名系统", 
    page_icon="favicon.ico"
    )
st.title("全国青少年中开展综合素质测评报名")


if st.session_state.get("needItem", True):
    # 读取json数据,根据参数选择数据文件
    item_file = 'testItem.json' if args.env == 'test' else 'needItem.json'
    with open(item_file,encoding="utf8") as f:
        needItem = json.load(f)
        st.session_state["needItem"] = needItem
    
    # 如果不存在infos,photos文件夹则创建
    os.makedirs("infos", exist_ok=True)
    os.makedirs("photos", exist_ok=True)

    st.session_state["tab_assemb"] = {
        "text":st.text_input,
        "image":st.file_uploader,
        "selectbox":st.selectbox
        }


def showTableList():
    # 根据needItem.json中的内容，动态添加相应的输入框
    tab_assemb = st.session_state["tab_assemb"]
    for item in st.session_state["needItem"]:
        assemb = tab_assemb[item["type"]]
        assemb(
            item["lable"], 
            key=item['lable'],
            **item["paras"]
        )
    

def submitInfo():
    infos = {}
    for item in needItem:
        info = st.session_state[item["lable"]]
        
        if not info:
            st.error(f"请填写: {item['lable']}")
            # 保存之前预选信息
            break
        infos[item["lable"]] = info
    # 判断信息是否完整
    if len(infos) == len(needItem):# 保存数据
        
        # 需要有个配置项文件，表示以什么数据作为文件名
        filename = infos['孩子身份证号']

        img_data = infos["上传孩子寸照"].read()
        # 保存图片到photos文件夹
        with open(f"./photos/{filename}.jpg",'wb') as f:
            f.write(img_data)
        
        # 显示图片
        # st.image(img_data)
        # 保存数据
        with open(f"./infos/{filename}.json",'w',encoding="utf8") as f:
            infos.pop("上传孩子寸照")
            json.dump(infos,f,ensure_ascii=False)
        st.info("提交成功")

        if args.env == 'test':
            st.write(infos)

with st.form("tableList"):
        
    showTableList()

    # Every form must have a submit button.
    submitted = st.form_submit_button("提交信息")
    if submitted:
        submitInfo()