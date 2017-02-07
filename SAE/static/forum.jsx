var Router = ReactRouter;
var Route = ReactRouter.Route;
var RouteHandler = ReactRouter.RouteHandler;
var Link = ReactRouter.Link;
var StateMixin = ReactRouter.State;

// topic list 部分
var  TopicList = React.createClass({
    getInitialState:function(){
        return { NewsData: [] }
    },
    componentDidMount:function(){
        $.ajax({
            url: "http://lajiao.sinaapp.com/api/bbs/topic",
            dataType: "json",
            success:function(data){
                this.setState({ NewsData: data});
            }.bind(this),
            error:function(xhr, status, err){
                console.error( this.props.url, status, err.toString() );
            }.bind(this)
        });
    },
    componentDidUpdate:function(){
    },
    render:function(){
        var newsNode = this.state.NewsData.map(
            function( news , index ){
                return (
                    <Topic data={news} key={index} />
                );
            }
        );
        return (
            <div className="React-topicList">
                <div className="mdl-card__title">
                    <h3 className="mdl-card__title-text">论坛</h3>
                </div>
                <ul className="topic-list">
                    {newsNode}
                </ul>
            </div>
        );
    }
});

var Topic = React.createClass ({
    onClick:function(){
        $(".forum-card__module").addClass("forum-card__module--animation");
    },
    render:function(){
        return (
            <li className="topic-list__item">
                    <span onClick={this.onClick} className="topic-list__topic">
                        <Link className="topic-list__topic-link" to="topic_detail" params={{id:this.props.data.topic_link}}>{this.props.data.topic}</Link>
                    </span>
                    <span className="topic-list__author">{this.props.data.author}</span>
                    <span className="topic-list__reply">{this.props.data.reply}</span>
            </li>
        );
    }
});

// topic detail 部分
var TopicDetail = React.createClass({
    back:function(){
        window.history.back()
    },
    getInitialState:function(){
        return { Detail:[] }
    },
    componentWillMount:function(){
        $("main")[0].scrollTop = 0;
        $(".forum-card__slide").addClass("forum-card__slide--out");
        $(".custom-menu").addClass("custom-menu--back");
        // GlobalDrawerEvent in material.min.js
        $(".mdl-layout__drawer-button")[0].removeEventListener('click',GlobalDrawerEvent);
        $(".mdl-layout__drawer-button")[0].addEventListener('click',this.back);
    },
    componentDidMount:function(){
        $.ajax({
            url: "http://lajiao.sinaapp.com/api/bbs/topic/detail/"+this.props.params.id,
            dataType: "json",
            success: function(data){
                this.setState( {Detail:data} )
            }.bind(this),
            error: function(xhr, status, err){
                console.error( this.props.url, status, err.toString() );
            }.bind(this)
        });
    },
    componentDidUpdate:function(){
    },
    componentWillUnmount:function(){
        $(".forum-card__slide").removeClass("forum-card__slide--out");
        $(".forum-card__module").removeClass("forum-card__module--animation");
        $(".custom-menu").removeClass("custom-menu--back");
        $(".mdl-layout__drawer-button")[0].removeEventListener('click',this.back);
        $(".mdl-layout__drawer-button")[0].addEventListener('click',GlobalDrawerEvent);
    },
    render:function(){
        var top_floor = this.state.Detail.shift();
        if( top_floor ){
            function content(){ return {__html:top_floor.content} }
            var other_floors = this.state.Detail.map(
                function( floor , index ){
                    return (
                        <Floor data={floor} key={index} />
                    );
                }
            );
            return(
                <div className="React-topicDetail">
                    <div className="loading sliding">
                        <div className="loading__spinner"></div>
                    </div>
                    <div className="topic-detail">
                        <div className="topic-detail__floor" >
                            <h1 className="topic-detail__title">{ top_floor.topic }</h1>
                            <a className="topic-detail__avatar-link" href={top_floor.author_link}>
                                <img className="topic-detail__avatar" src={top_floor.avatar} alt="author" />
                            </a>
                            <span className="topic-detail__author-name">
                                <a className="topic-detail__author-link" href={top_floor.author_link}>{top_floor.author}</a>
                            </span>
                            <span className="topic-detail__reply-time">于 {top_floor.reply_time}</span>
                            <span className="topic-detail__hits-and-reply">已有 {top_floor.hits}次点击  回复{top_floor.reply}条</span>
                            <div className="topic-detail__content" dangerouslySetInnerHTML={ content() } />
                        </div>
                        { other_floors }
                    </div>
                </div>
            );
        }
        else {
            return (
                <div className="React-topicDetail">
                    <div className="loading">
                        <div className="loading__spinner"></div>
                    </div>
                </div>
            )
        }
    }
});

var Floor = React.createClass({
    render:function(){
        function content(content){ return {__html:content} }
        return (
            <div className="topic-detail__floor" >
                <div className="topic-detail-comment__author-info">
                    <a className="topic-detail-comment__avatar-link" href={this.props.data.author_link}>
                        <img className="topic-detail-comment__avatar" src={this.props.data.avatar} alt={this.props.data.author} />
                    </a>
                </div>
                <div className="topic-detail-comment__floor-info">
                    <a className="topic-detail-comment__author">{this.props.data.author}</a>
                    <span className="topic-detail-comment__time">{this.props.data.reply_time}</span>
                    <span className="topic-detail-comment__floor-counter">#{this.props.data.floor}</span>
                </div>
                <div className="topic-detail-comment__content" dangerouslySetInnerHTML={ content(this.props.data.content) } />
            </div>
        );
    }
});

// ------ render ------ render ------ render ------ render ------ 
/*
React.render(
    <TopicList url="topic.json" />,
    document.getElementById("topicList")
);
*/
// -------------- React Router --------------------- Router --------------
var Forum = React.createClass({
    render:function(){
        return (
            <RouteHandler />
        );
    }
})

var routes = (
    <Route handler={Forum}>
        <Route name="topic_list" path="/" handler={TopicList} />
        <Route name="topic_detail" path="/t/:id" handler={TopicDetail} />
    </Route>
)

Router.run( 
    routes,
    Router.HashLocation,
    function(Root){
        React.render(
            <Root />,document.getElementById("module")
        );
    }
)
