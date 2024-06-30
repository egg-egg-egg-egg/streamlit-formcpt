from typing import List,Dict
import streamlit as st
import json
# 表单池
form_cpt = {
    "text":st.text_input,
    "file":st.file_uploader,
    "selectbox":st.selectbox
    }

# TODO表单配置规范
pass


class FormCpt:
    def __init__(self,needItem:List[Dict]|str,nowshow=False):
        if isinstance(needItem,str):
            with open(needItem,encoding="utf8") as f:
                needItem = json.load(f)
        needItem = {item['lable']:item for item in needItem} if isinstance(needItem,List) else needItem

        self.form_cpt = form_cpt
        self.needItem = needItem
        if nowshow:
            self.show()
            

    def __call__(self,*args,**kwargs):
        for key in self.needItem:
            item = self.needItem[key]
            cpt = form_cpt[item["type"]]
            cpt(
                item["lable"], 
                # key=item['lable'],
                **(item.get("paras",dict()))
            )
    
    def show(self,*args,**kwargs):
        self()
    
    def __bool__(self):
        return self.check()
    
    def check(self):
        """
        检查是否按要求填完
        """
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

    # TODO 保存数据
    def save(self):
        if not self: # 填写失败
            st.error("表单填写失败")
            return False
        st.success("表单填写成功")

    # TODO 表单数据读取
    def read(self):
        pass

    # TODO 表单数据展示
    def show_data(self):
        pass

    # TODO 每个表单数据的验证
    def form_valid(self):
        pass
            