

## Create virtualenv
-----------------

	1
    $ pip install virtualenv --index-url http://pypi.tuna.tsinghua.edu.cn/simple
    $ virtualenv env
    $ source ../env/bin/activate

## Install packages
-----------------````

    1. 如果没有python，安装python：
       $ https://www.python.org/downloads/
    2. 安装包管理工具，先安装setuptools(easy_install)和pip
    3. 安装第三方包：
       $ pip install -r requirements.txt
       $ 安装pycrypto:http://www.voidspace.org.uk/python/modules.shtml#pycrypto
    4. requests文档：http://www.python-requests.org/en/latest/
    6. windows 64 安装MySQLdb：
       下载地址：https://pypi.python.org/pypi/MySQL-python/1.2.5
       linux安装MySQL-python-1.2.3报错：ImportError: No module named setuptools
       解决：http://blog.csdn.net/chidy/article/details/7694750
      
        1、先安装mysql-devel.x86_64
        # yum install mysql-devel.x86_64
        2、在次执行安装mysql-ptyhon
        #pip install mysql-python 
        
## Test Code
-----------------

    1. git clone http://gitlab.zhulebei.com/long.jin/ZhuLeBei_Test
    2. git add .       #添加修改代码
    3. git commit -m 'test'        #提交修改代码
    4. git pull origin master     #push之前一定要先pull代码,否则可能会覆盖别人代码!
    5. git push origin master          #提交到远程仓库
    6. 分支：
        * 在本地新建一个分支： git branch Branch1
        * 切换到你的新分支: git checkout Branch1
        * 将新分支发布在github上： git push origin Branch1
        * 在本地删除一个分支： git branch -d Branch1
        * 在github远程端删除一个分支： git push origin :Branch1   (分支名前的冒号代表删除)
       
    
## Test Report
-----------------

    1. http://tungwaiyip.info/software/HTMLTestRunner.html
    2. 下载源码：HTMLTestRunner.py
    3. 将文件放到python环境变量（sys.path） 如：/usr/lib/python2.7/site-packages
    4. import HTMLTestRunner 可以使用了
    5. 解决中文乱码的问题：
        a. 打开HTMLTestRunner.py
        b. 找到 uo = o.decode('latin-1') 和 ue = e.decode('latin-1')
        c. 修改位 utf-8 编码，done

## 常见问题记录
-----------------

    1. 解决request请求HTTPS地址报错的问题：
        错误：InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring
             SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.
             readthedocs.org/en/latest/security.html#insecureplatformwarning.
        解决：pip install pyopenssl ndg-httpsclient pyasn1
             如果是ubuntu：apt-get install libffi-dev libssl-dev
        出处：http://stackoverflow.com/questions/29134512/insecureplatformwarning-a-true-sslcontext-object-is-not-available-this-prevent
    
    2. mac和windows跨平台编码不同报错：
        错误：SyntaxError: Non-ASCII character '\xe5' in file G:/gongzuo/icaopan/OpenAPI/api_suit.py on line 14,
             but no encoding declared; see http://python.org/dev/peps/pep-0263/ for details
        解决：a. 把编码声明放到第一行：# -*- coding: utf-8 -*-    
             b. 修改pycharm > Default Setting > File Encoding : IDE Encdoing位：utf-8 、Project Encoding：utf-8，properties files：utf8
    3. pip使用报错【cannot import name HTTPSHandler】
        解决：yum安装openssl和openssl-devel。然后重新编译python。
        
    4. 解决jenkins URL解析中文乱码问题
        解决：设置tomcat容器server.xml文件，在Connector标签后增加URIEncoding='UTF-8 （对请求参数进行utf8的编码）
        参考：http://blog.csdn.net/taijianyu/article/details/43826739
    5. pycharm 2016.2版本报错RuntimeWarning:
        解决:http://stackoverflow.com/questions/38569992/pycharm-import-runtimewarning-after-updating-to-2016-2
    6. windows安装pycrypto,编译报错,需要vs2008环境
        解决:[下载不需要编辑的pycrypto]http://www.voidspace.org.uk/python/modules.shtml#pycrypto
    7. Jenkins pull仓库时报错:error: insufficient permission for adding an object to repository database .git/objects
        原因：
        git库权限的问题
        $ ls -la，查看git库的所有者
        解决：
        在git库目录下：
        $sudo chown -R git:git git库（9x25oecore.git'）


## unittest常用方法：
    assertEqual(a, b)     a == b      
    assertNotEqual(a, b)     a != b      
    assertTrue(x)     bool(x) is True      
    assertFalse(x)     bool(x) is False      
    assertIs(a, b)     a is b     2.7
    assertIsNot(a, b)     a is not b     2.7
    assertIsNone(x)     x is None     2.7
    assertIsNotNone(x)     x is not None     2.7
    assertIn(a, b)     a in b     2.7
    assertNotIn(a, b)     a not in b     2.7
    assertIsInstance(a, b)     isinstance(a, b)     2.7
    assertNotIsInstance(a, b)     not isinstance(a, b)     2.7

### 其他的unittest方法，用于执行更具体的检查：
    Method     Checks that     New in
    assertAlmostEqual(a, b)     round(a-b, 7) == 0      
    assertNotAlmostEqual(a, b)     round(a-b, 7) != 0      
    assertGreater(a, b)     a > b     2.7
    assertGreaterEqual(a, b)     a >= b     2.7
    assertLess(a, b)     a < b     2.7
    assertLessEqual(a, b)     a <= b     2.7
    assertRegexpMatches(s, re)     regex.search(s)     2.7
    assertNotRegexpMatches(s, re)     not regex.search(s)     2.7
    assertItemsEqual(a, b)     sorted(a) == sorted(b) and works with unhashable objs     2.7
    assertDictContainsSubset(a, b)     all the key/value pairs in a exist in b     2.7
    assertMultiLineEqual(a, b)     strings     2.7
    assertSequenceEqual(a, b)     sequences     2.7
    assertListEqual(a, b)     lists     2.7
    assertTupleEqual(a, b)     tuples     2.7
    assertSetEqual(a, b)     sets or frozensets     2.7
    assertDictEqual(a, b)     dicts     2.7
    assertMultiLineEqual(a, b)     strings     2.7
    assertSequenceEqual(a, b)     sequences     2.7
    assertListEqual(a, b)     lists     2.7
    assertTupleEqual(a, b)     tuples     2.7
    assertSetEqual(a, b)     sets or frozensets     2.7
    assertDictEqual(a, b)     dicts     2.7


## selenium方法
    * 获取元素中的值
    element = driver.find_element_by_xpath("//*[@id='lobby-left-container']/div[2]/div/table/tbody/tr[1]/td[2]/div")
    data_id = element.get_attribute("data-id")
    selenium-python常用函数：http://blog.sina.com.cn/s/articlelist_3053349671_5_1.html


#### 等待条件
    - title_is
    - title_contains
    - presence_of_element_located
    - visibility_of_element_located
    - visibility_of
    - presence_of_all_elements_located
    - text_to_be_present_in_element
    - text_to_be_present_in_element_value
    - frame_to_be_available_and_switch_to_it
    - invisibility_of_element_located
    - element_to_be_clickable – it is Displayed and Enabled.
    - staleness_of
    - element_to_be_selected
    - element_located_to_be_selected
    - element_selection_state_to_be
    - element_located_selection_state_to_be
    - alert_is_present

## 在linux-server下运行webdriver，安装：Xvfb、firefox

    1. 下载firefox
        - http://ftp.mozilla.org/pub/firefox/releases/
    2. 安装Xvfb
        - yum install xorg-x11-server-Xvfb

    3. 添加环境变量：~/.bash_profile
        - export DISPLAY=:1
        - export BROWSER_PATH=/usr/lib64/firefox/
        PATH=$PATH:$BROWSER_PATH
    4. 启动Xvfb和firefox：
        - Xvfb :1 -screen 0 1366x768x16 &
        - export DISPLAY=:1
        - firefox &
    5. 参考：http://www.puritys.me/docs-blog/article-262-%E5%AE%89%E8%A3%9D-XVFB-%E5%81%9A-Selenium-%E6%B8%AC%E8%A9%A6.html


## 使用phantomJS驱动测试

    1. 安装phantomJS：brew install phantomjs  或 官网：http://phantomjs.org/download.html
    2. 配置phantomjs PATH系统变量
    2. example:
        '''
        from selenium import webdriver

        driver = webdriver.PhantomJS(executable_path = "%s/phantomjs-2.1.1/bin/phantomjs" % WebConfig.PHANTOMJS) # or add to your PATH
        driver.set_window_size(1024, 768) # optional
        driver.get('https://google.com/')
        driver.save_screenshot('screen.png') # save a screenshot to disk
        sbtn = driver.find_element_by_css_selector('button.gbqfba')
        sbtn.click()
        '''

## Jpype相关，python调用JAVA jar包

    1. 使用Jpype，mac环境报错：java not requireXXX

        > 解决：
        >> -进入/Library/Java/JavaVirtualMachines/jdk.1.8.<…>/Contents/目录
        >> -备份Info.list 文件
        >> -将
           '''
           <key>JVMCapabilities</key>
                <array>
                <string>CommandLine</string>
                </array>
            替换为：
            <key>JVMCapabilities</key>
                <array>
                <string>JNI</string>
                <string>BundledApp</string>
                <string>CommandLine</string>
                </array>
             '''
        >> -重启电脑


    2. java打包错误导致调用失败:找不到引用的外部类
        > 原因：打包方式错误
        > 解决：打的jar包，把依赖包也都放到jar包里
        >>- 参考：http://blog.sina.com.cn/s/blog_3fe961ae0102uy42.html

    3. python调用java，中文转码问题
        > 解决：
        >> python中使用UTF-8编码（非unicode）如：str="中文"
        >> java中，最后将字符串转成UTF-8的字节编码形式的字符串
        '''
        String newStr = sf.toString();
        String newStr1 = new String(newStr.getBytes("iso8859-1"), "utf-8");
        '''
        参考：http://blog.csdn.net/xfei365/article/details/50847681


## webdriver遇到的那些坑

    1. 如果button有渐变效果，需要等待渐变效果开始或结束，否则后面的操作可能导致失败。                   #坑0.5小时
    2. 当存在多个相同元素时，用find_element会返回第一个元素，比如申请渠道页面的保存按钮，这时可能操作的元素不是自己想要的。     #坑3小时
    3. send_key和下拉列表都可以滚动页面，click不行，需要自己指定滚动到click的元素。               #坑2小时


## 关于Jenkins2.1 Pipline持续交付

    - 安装
        1. tomcat8、jenkins2.19.2
        2. 更新：jenkins放到webapp下

    - Steps库手册
        1. [Pipeline Steps库官方参考手册](https://jenkins.io/doc/pipeline/steps/)

    - 升级依赖插件
	    1. [groovy.hpi](http://updates.jenkins-ci.org/download/plugins/groovy/1.29/groovy.hpi)

    - 学习Groovy

    - 问题解决
        1. 报错：java.lang.NoSuchMethodError: No such DSL method 'node' found among steps [archive, 很多,params]
           解决：升级Pipeline: Job、Pipeline: Shared Groovy Libraries，Pipeline: Job等等,最主要的是Pipeline插件和相关依赖升级。


    - 迁移
        1. 任务迁移：

