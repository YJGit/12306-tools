# 概述  
12306的一些工具  
目前功能:  
&nbsp;&nbsp;&nbsp;&nbsp;命令行查票

# 开发环境  
Windows10    
Python3.x  

# 使用方法  
## Clone  
```
git clone https://github.com/YJGit/12306-tools.git  
cd 12306-tools  
```
## Set up  
在当前目录打开Windows PowerShell  
```
.\setup.py install  
```
## 执行命令  
在任意目录打开cmd或者PowerShell均可执行  
```
tickets -h  //显示帮助
tickets [-gdtkz] <from> <to> <date>  //查询余票  
tickets  //按照conf.ini配置进行查询  
```  
此时直接在Windows左下角直接输入tickets回车也可执行，当然这样的查询参数是按照conf.ini配置里的  

# 一些结果展示  
查询成功：  
![](http://ouebtut1h.bkt.clouddn.com/12306-%E5%8C%97%E4%BA%AC-%E6%88%90%E9%83%BD-2018-01-31.PNG)  
![](http://ouebtut1h.bkt.clouddn.com/12306-%E5%8C%97%E4%BA%AC-%E5%90%89%E9%A6%96-2018-02-10.PNG)  
查询失败： 
![](http://ouebtut1h.bkt.clouddn.com/12306-%E5%8C%97%E4%BA%AC-%E6%88%90%E9%83%BD-2018-02-31-error.PNG)  

# 源码说明  
参考文章https://www.shiyanlou.com/courses/623/labs/2072/document  
目录如下：  
&nbsp;&nbsp;&nbsp;&nbsp;conf.ini  
&nbsp;&nbsp;&nbsp;&nbsp;parse_station.py  
&nbsp;&nbsp;&nbsp;&nbsp;stations.py    
&nbsp;&nbsp;&nbsp;&nbsp;setup.py  
&nbsp;&nbsp;&nbsp;&nbsp;tickets.py  

conf.ini里为一些默认的配置  
parse_station.py主要是获取车站的数据，将车站名和车站的code联系起来，查询url里需要的是车站的code  
stations.py是parse_station.py获取的数据，当然前面"stations="为人为加入的  
setup.py为脚本，能够是tickets在任何目录运行  
tickets.py为主函数文件，目前实现的是一共进行5次尝试，若都不成功，则给出一些可能的错误提示，可以参见之前的截图  

# 注意事项  
1. conf.ini里写了tickets_query_url，原因是其会改变，应当注意(这个原因在失败查询给出的提示中并没给出)，至于如何改变，变成什么样，可以参见之前提供的参考文章  
2. 注意将tickets.py第36行代码conf.read(r"E:\projects\12306-tools\\12306-tools\conf.ini", encoding="utf-8-sig")的conf.ini路径改成你的绝对路径，否则会报错(注意r必须保留)    
