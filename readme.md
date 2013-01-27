#Blog powered by web.py and MongoDB

#Introduce

学习Python的第一个Web框架就是[web.py](http://webpy.org/)，没想到它的作者Aaron Swartz已经于2013年1月11日自杀。 2012年年末计划用Python将此博客重写，其中Web框架经过一翻[选型](http://wiki.woodpecker.org.cn/moin/PyWebFrameList)，便确定使用web.py。本打算利用周末时间，希望能在年前完成，但因迫近年关诸事繁忙，现在才刚刚搭建起基本的项目框架。真是诸行无常，现在唯一能纪念的，就是作为一个程序员，学习吸收Aaron Swartz的思想，尽快的完成这个项目，并发布到github，也算是对web.py的一种推介，对Aaron Swartz的一种追思。

[@程序员杂志](http://e.weibo.com/programmermag)： 震惊！Aaron Swartz自杀身亡，年仅26。他是Reddit的联合创始人，web.py的设计者，14岁参与创造了RSS 1.0规范，又与John Gruber共同设计了Markdown。2011年曾因下载480万篇JSTOR学术论文而被捕。[http://t.cn/zjrzsyb](http://t.cn/zjrzsyb)

这个周末，已经开始搭建基本的项目开发框架，其中会有很多未考虑周全的地方，尤其是对Python新手，需要在今后持续的理论学习后进行改进。

#Structure

使用tree输出目录结构，并进行一些处理后，主要项目结构如下：

	blog/
	├── dist										#发布目录
	├── doc											#文档目录
	├── src											#源代码目录
	│   ├── app.py									#主程序，直接运行 python app.py即可
	│   ├── config									#配置模块
	│   │   ├── setting.py							#主要配置，包括博客设置，日志，数据库等
	│   │   └── url.py								#URL配置，web.py相关，在app.py中会用到
	│   ├── controller								#业务处理模块
	│   │   ├── blog.py								#URL分发处理代码，如Index，Entry,Page等，后端的业务逻辑交给entry.py等处理
	│   │   ├── entry.py							#entry业务处理代码，与数据库的交互等
	│   │   └── page.py								#page业务处理代码，与数据库的交互等
	│   ├── db
	│   │   └── blog.json							#博客演示数据，由mongoexport导出
	│   ├── logs									#开发调试日志目录
	│   ├── publish									#静态资源发布目录
	│   │   └── entries								#Entries发布目录，以年、月建立
	│   │       └── 2013
	│   │           └── 01
	│   ├── static									#静态资源目录，web.py相关，主要响应images,css,js等
	│   │   ├── css
	│   │   ├── favicon.ico
	│   │   ├── img
	│   │   └── js
	│   ├── template								#模板目录，包括主模板、小工具、模块、布局以及一些杂项模板（站点统计、广告）
	│   │   ├── archive.html						#归档页面模板
	│   │   ├── entry.html							#Entry页面模板
	│   │   ├── error.html							#错误页面模板
	│   │   ├── index.html							#首页模板
	│   │   ├── page.html							#Page页面模板
	│   │   ├── search.html							#搜索页面模板
	│   │   ├── templates							#子模板目录
	│   │   │   ├── layout							#布局，主要是页首、页尾、边栏等
	│   │   │   ├── misc							#杂项模板
	│   │   │   └── modules							#模块模板
	│   │   └── widgets								#小工具模板
	│   └── util									#实用工具类，如Dict到Object转换工具，错误处理，日志处理等
	│       ├── d2o.py
	│       ├── error.py
	│       ├── __init__.py
	│       └── logger.py
	└── test
	
	31 directories, 61 files



#Demostration
##Import demo database 

演示程序中，已经使用mongodump导出了博客的部分数据，主要是blog.entries。

导出数据：

	mongoexport -v -d blog -c entries -o /data/mongo/blog.json
	
导入数据：
	
	mongoimport -v -d blog -c entries -o /workspace/blog/db/blog.json

注意：

因项目结构在是Windows平台上搭建，使用的MongoDB也在Windows上，blog.json导出后在Linux平台上导入前需要使用dos2unix进行格式转换。

##run app

	$ python app.py 
或

	$ ./app.py

打开浏览器，访问，控制台输出信息如下：
	
	[dylan@www src]$ ./app.py 
	http://0.0.0.0:8080/
	14.122.105.167:60718 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /" - 200 OK
	14.122.105.167:60719 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/css/styles.css" - 200 
	14.122.105.167:60718 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/js/jquery.js" - 200 
	14.122.105.167:60719 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/js/bootstrap.js" - 200 
	14.122.105.167:60724 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/css/bootstrap.css" - 200 
	14.122.105.167:60726 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/css/customize.css" - 200 
	14.122.105.167:60727 - - [21/Jan/2013 00:04:55] "HTTP/1.1 GET /static/css/bootstrap-responsive.css" - 200 
	14.122.105.167:60718 - - [21/Jan/2013 00:04:56] "HTTP/1.1 GET /static/img/glyphicons-halflings-white.png" - 200 
	14.122.105.167:60718 - - [21/Jan/2013 00:04:57] "HTTP/1.1 GET /favicon.ico" - 200 OK
	14.122.105.167:60718 - - [21/Jan/2013 00:05:04] "HTTP/1.1 GET /entries/the-importance-of-complex-passwords.html" - 200 OK
	

#Developing source code

[source code of blog@githut](https://github.com/dylanninin/blog)

#Todo List

	[dylan@www src]$ mongo
	MongoDB shell version: 2.2.2
	connecting to: test
	> use blog
	switched to db blog
	> db.todo.find({},{priority:1,todo:1})
	{"priority" : 1, "todo" : "python standard library practice" }
	{"priority" : 1, "todo" : "web.py ... ..."}
	{"priority" : 1, "todo" : "MongoDB ... ..."}
	{"priority" : 1, "todo" : "PyMongo ... ..."}
	... ...
	{"priority" : 5, "todo" : "any thing else"}

#Reference
 * [web.py](http://webpy.org/)
 * [MongoDB](http://docs.mongodb.org/manual/reference/)
 * [PyMongo](http://api.mongodb.org/python/current/)
 * [Bootstrap](http://twitter.github.com/bootstrap)
 * [jquery](http://jquery.com/)