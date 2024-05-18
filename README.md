# Introduce
这是一个可以通过配置`needItem.json`就可以动态显示不同表单组件的**streamlit**项目。

`needItem.json`名字可以自定义.只需要保证传递给`FormCpt`对象的参数满足配置需要即可。

随意的设置不同的表单组件和其属性，不用频繁修改代码。

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


# run demo
```bash
streamlit run demo.py
```