# 介绍
这是一个可以通过配置`needItem.json`就可以动态显示不同表单组件的**streamlit**项目。

`needItem.json`名字可以自定义.只需要保证传递给`FormCpt`对象的参数满足配置需要即可。

随意的设置不同的表单组件和其属性，不用频繁修改代码。

# 如何使用
- 安装依赖
```bash
pip install -r requirements.txt
```

- 使用表单
```python
import streamlit as st
import formcpt as fcpt

form = fcpt.FormCpt("needItem.json",nowshow=False) # 文件名可以随意

form() # 或者form.show() 或者 直接设置nowshow=True

# 判断表单是否填完整
if form:
    st.write("表单填写完整")
else:
    st.write("表单填写不完整")


# 无论表单信息是否完整，都可以查看已经填写的信息
st.write(form.infos)
```

# 文件说明
说实话别看这么多文件，只有 formcpt.py和needItem.json要用到。


- demo.py 是一个使用示例
- formcpt.py 表单组件
- needItem.json 参考配置文件
- requirements.txt 依赖库文件
- .streamlit/config.toml st的配置文件

这个项目结构确实有点乱。
# 如何配置动态表单

每一个表单的lable应该是独一无二的。

动态表单目前有三种类型：
- 文本输入框:text
- 下拉框:selectbox
- 上传文件:file

## 文本输入框
前三个key必须配置
```json
{
    "lable":"家长手机号",
    "type":"text",
    "description":"",
    "fill":false,// 不填默认true
    "paras":{}
}
```

## 下拉框
前四个key必须配置
```json
{
    "lable":"孩子性别",
    "type":"selectbox",
    "description":"",
    "paras":{
        "options":["男","女"],
        "placeholder":"请选择性别",  // 下拉框的提示文字
        "multiple":false,  // 是否多选
        "index":null  // 下拉框的默认选项,null表示没有默认,0表示第一个,1表示第二个
    }
}
```

## 上传文件
前四个key必须配置
```json
{
    "lable":"上传孩子寸照",
    "type":"file",
    "description":"",
    "paras":{
        "type":["png","jpg","jpeg"]
    }
}
```

# 表单池

在formcpt.py中有一个表单池，修改key和value就可以自定义表单池了。

```python
import streamlit as st
import formcpt as fcpt

fcpt.form_cpt["number"] = st.number_input

f = fcpt.FormCpt([{
        "lable":"age",
        "type":"number",
        "description":"填写你的年龄",
        "fill":True,
        "paras":{}  # 可以填st.number_input中的参数以key:value的形式
    }],nowshow=True)

```


# run demo
```bash
streamlit run demo.py
```