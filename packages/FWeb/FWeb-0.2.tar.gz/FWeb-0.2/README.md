# FWeb - 我心目中的Python Web框架

## 理念
一个轻量的，结构完整的Python Web框架。适用于小型项目或组合进某一项工程中。

## 起因
本人高中学生一个，估计再有几个月就消失了。之前使用过Django和Flask，经常幻想自己的Web框架会怎么设计。

建立这个项目，目的是学习相关技术，了解一下。希望能实现到应用级别，但也可能中道荒废。

# 已实现
* 支持WGSI
* 函数式路由
* 二分法路由
* lambda可作为路由参数
* 四次路由（即请求响应经过 初始化函数->检查器->页面函数->错误处理函数）
* HTTP头、GET、POST、COOKIE解析
* 基于异常处理的HTTP状态码响应
* HTTP无状态设计（即服务器的返回取决于请求的数据，而非请求方法）

# 从头开始创建一个FWeb项目

## 建立项目
一个基本的项目，需要包含：1个入口py文件，数个页面py文件，静态文件目录（可选），模板文件目录（可选）。

创建`/app.py`，内容为：
```Python
from FWeb.App import WebApp
from werkzeug.serving import run_simple # 使用了werkzeug来启动WSGI服务。其并非本项目作品。仅作为一个 HTTP服务器<-->Python WSGI应用 连接器使用。

import error
import pages

app = WebApp(
    "view", # 模板文件的文件夹名
    "static", # 静态文件的文件夹名
    pages, # 页面模块
    error # 错误页面模块
)

if __name__ == '__main__':
    run_simple('127.0.0.1', 80, app, use_debugger=True, use_reloader=True) # 启动服务器
```

目录结构为
```
/
|---app.py
|---pages.py
|---error.py
|---view
    |---main.css
    |---...
|---static
    |---index.html
    |---...
```

### 函数页面模块路由
app.py可以使用如下指明模块与url的关系
```Python
def map(url):
    if url.startswith("/api"):
        return api
    elif url.startswith("/user"):
        return user
    else:
        return pages


app = WebApp(
    "view",
    "static",
    map,
    error
)
```
## 创建一个页面模块
上文所述的`pages`、`api`、`user `等模块都为类似形式
```Python
from FWeb.App import WebPage, WebPageHandler, HttpRedirect, HttpError

page = WebPage()
# WebPage是一个列表，记录了
# @page.init() 初始化 在最初运行一次，无返回值
# @page.i(url) 检查器 在所有页面函数前运行，可返回True/False表示检查是否通过
# @page.p(url) 页面函数 执行页面
# @page.e(error_code) 错误页处理 无返回值


@page.init()
def init(p: WebPageHandler):
    print("init")


@page.i("/user")
def check_user_login(p: WebPageHandler):
    # balabala
    return True


@page.p("/")
def index(p: WebPageHandler):
    p.echo("hi,FWeb\n") # 向响应缓冲区追加文本
    return "hello world" # 向响应缓冲区追加文本，结束函数


@page.p("/user")
def user(p: WebPageHandler):
    return {"username": "FWeb"} # 向响应缓冲区追加Json，结束函数

@page.p("/asdadas")
def asdadas(p: WebPageHandler):
    raise HttpError(500)


@page.p("/redirect/<any:url>") # 类似Flask的url匹配方式，末尾有详解
def redirect(p: WebPageHandler):
    raise HttpRedirect(p.get_url_data("url", default="")) # 1.使用异常处理实现错误码的响应 2.内建数据获取函数，后文讲解


@page.p(lambda x: {"name": "hahaha"} if x.startswith("/hello") else False) # 使用lambda表达式进行路由
def hello(p: WebPageHandler):
    return "hello," + str(p.get_url_data("name"))


@page.e(404)
def not_found(p: WebPageHandler):
    print("没找到？？？")

```

检查器和页面函数都可以使用URL表达式（类似Flask）和lambda表达式处理。
1. URL表达式
   1. 可选是否带有参数名 `<int:aa>` 参数名为aa，`<int:>``<int>`无参数名。参数被称之为url_data
   2. 可选的匹配符
      1. `<str:*>`任意字符串，但不包含"/"
      2. `<int:*>`整数
      3. `<float:*>`小数
      4. `<any:*>`任意字符，包含"/"
2. lambda表达式
   1. 一个形如f(url)->dict/Flase的函数
   2. 可返回字典并用作url_data，或者任意可以被bool(任务是True的内容)
   3. 返回False表示不匹配


参数获取函数：

存在性检查：
* isset_get_data(self, key)
* isset_post_data(self, key)
* isset_pos_pro_data(self, key)
* isset_cookie_data(self, key)
* isset_url_data(self, key)

格式化获取
* get_get_data(self, key, Type=str, default=None)
* get_post_data(self, key, Type=str, default=None)
* get_pos_pro_data(self, key, Type=str, default=None)
* get_cookie_data(self, key, Type=str, default=None)
* get_url_data(self, key, Type=str, default=None)

post为简单的post参数，由表单提交。post_pro包含完整的multipart/form-data形式的POST数据（包括一键多值）。
