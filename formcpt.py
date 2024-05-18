from typing import List,Dict
import streamlit as st

# 表单池
form_cpt = {
    "text":st.text_input,
    "file":st.file_uploader,
    "selectbox":st.selectbox
    }

# TODO表单配置规范
pass


class FormCpt:
    def __init__(self,needItem:List[Dict]):
        self.form_cpt = form_cpt
        self.needItem = needItem
        

    def __call__(self,*args,**kwargs):
        for item in self.needItem:
            cpt = form_cpt[item["type"]]
            cpt(
                item["lable"], 
                key=item['lable'],
                **(item.get("paras",dict()))
            )
            
    
    def __bool__(self):
        # 未填写的信息显示错误
        infos = {}
        checkstatus = True
        for item in self.needItem:
            info = st.session_state[item["lable"]]
            # 判断是否必填
            if item.get("fill",True) and not info:
                st.error(f"请填写: {item['lable']}")
                checkstatus = False
                break
            infos[item["lable"]] = info
            
        self._infos = infos
        return checkstatus
    
    @property
    def infos(self):
        return self._infos

    def save(self):
        if self.checkstatus:
            # 保存数据
            st.session_state.form_data = self.infos
            st.success("表单填写成功")
        else:
            st.error("表单填写失败")

    # TODO 表单数据读取
    def read(self):
        pass

    # TODO 表单数据展示
    def show_data(self):
        pass
            