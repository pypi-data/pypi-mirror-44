# stock_grpc目前实现的接口有12个

## 客户端安装方式
    pip install sense-data

## 配置settings.ini文件，用于配置rpc的IP地址和端口，比如：

[data_rpc]

host = localhost

port = 5001

## 使用方法，初始化一个实例，调用方法
    from sense_data import *
    sen = SenseDataService()

    ## 1-公司别名，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司的别名，输出形式为model，或model组成的列表
    sen.get_company_alias(stock_code)
    比如：
    sen.get_company_alias('000045')
    sen.get_company_alias([])
    sen.get_company_alias(['000045','000046'])

    ## 2-子公司，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到子公司信息，输出形式为model，或model组成的列表
    sen.get_subcompany(stock_code)

    ## 3-实时股价，输入股票代码字符串，输出最新的股票数据，数据形式为model
    sen.get_stock_price_tick(stock_code)

    ## 4-每日股价，输入股票代码字符串，输出该股票历史信息
    sen.get_stock_price_day(*args)
    有三种查询方式，sen.get_stock_price_day('000020')，输出有史以来的所有数据，数据形式为model列表；
    sen.get_stock_price_day('000020', '2018-12-2')，输出指定某一天的数据，数据形式为model；
    sen.get_stock_price_day('000020', '2018-12-2', '2019-1-4')，输出指定时间段的数据，数据形式为model列表；

    ## 5-公司基本信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到公司基本信息，输出形式为model，或model组成的列表
    sen.get_company_info(stock_code)

    ## 6-董监高信息，输入股票代码，允许的输入形式为股票字符串，或股票字符串+职位，输出懂事和监事的信息，每个人的数据形式是model，然后将对象存入列表中
    sen.get_chairman_supervisor(*args)
    比如：
    sen.get_chairman_supervisor('000045') 输出该公司所有的董监高人员信息
    sen.get_chairman_supervisor('000045', '懂事') 输出该公司所有的懂事人员信息

    ## 7-股东信息，输入股票代码，输出十大股东信息，每个股东的数据形式是model，然后将对象存入列表中
    sen.get_stockholder('000045')

    ## 8-行业概念信息，输入股票代码，允许的输入形式为字符串，或字符串列表（列表为空返回所有数据），得到股票对应的行业概念信息，输出形式为model，或model组成的列表
    sen.get_industry_concept(stock_code)

    ## 9-返回前一个交易收盘日期，无参数，返回值形如'2019-1-28 03:00:00'的时间戳，是int型数据，李军用
    sen.get_trade_date()

    ## 10-返回四大板块（深市主板、沪市主板、创业板和中小板）的股票涨跌幅，无参数，输出板块涨跌幅model，暂时不用了
    sen.get_market_rise_fall()

    ## 11-返回60左右个行业的股票涨跌幅数据，无参数，输出涨跌幅model，暂时不用了
    sen.get_industry_rise_fall()

    ## 12-返回股市中概念板块的涨跌幅数据，无参数，输出涨跌幅model，暂时不用了
    sen.get_concept_rise_fall()

    ## 13-给个实体名字（人名，子公司名）查询其在相关上市公司扮演的角色信息，输出形式为model组成的列表
    sen.get_entity_role('重庆富桂电子有限公司')

# 所有数据的model内容见sense_data/dictobj.py中的定义










