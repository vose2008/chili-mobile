create table bbs_newsList (
    news_id int unsigned not null primary key,
    news_name char(24) not null,
    author_id int unsigned not null,
    author_name char(18) not null,
    reply mediumint not null,
    lastreply_time datetime not null,
    lastreply_author char(18) not null,
    hit int unsigned not null
)
