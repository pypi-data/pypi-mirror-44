// TODO: 1、回复其他人，并且发送提醒。点击自己的是删除，点击别人的是回复 2、显示笔记

$(document).ready(function () {
    axios.defaults.xsrfCookieName = 'csrftoken';
    axios.defaults.xsrfHeaderName = 'X-CSRFToken';

    function remove_location_params() {
        window.history.pushState({}, document.title, "/feed");
    }

    var new_feed = new Vue({
        el: '#new-feed',
        data: {
            content: '',
            success_message: '',
            error_message: '',
            selected_files: null,
        },

        methods: {
            on_upload_image_change: function (e) {
                if (e.target.files.length > 9) {
                    alert('最多只能传9张图片');
                    return;
                }

                this.selected_files = e.target.files;
                if (this.content.length === 0) {
                    this.content = '分享图片';
                }
            },

            post_new_feed: function (e) {
                e.target.disabled = true;
                var url = e.target.getAttribute("data-confirm");

                if (new_feed.content === '') {
                    alert('内容不能为空');
                } else {
                    var form_data = new FormData();
                    form_data.append('content', new_feed.content);
                    if (new_feed.selected_files) {
                        for (var i = 0; i < new_feed.selected_files.length; i++) {
                            var file = new_feed.selected_files[i];
                            form_data.append('files', file, file.name);
                        }
                    }

                    axios.post(url, form_data).then(function (resp) {
                        var data = resp.data;

                        if (data['rc'] === 0) {
                            new_feed.success_message = data['message'];

                            new_feed.content = '';
                            new_feed.selected_files = null;
                            setTimeout(function () {
                                new_feed.success_message = '';
                            }, 2000);

                            var new_feeds = JSON.parse(data['new_feeds']);
                            feeds.feeds.unshift(new_feeds);
                            window.history.go();
                        } else {
                            alert(data['message']);
                        }

                    });

                }
                e.target.disabled = false;
            }
        }
    });

    var feeds = new Vue({
        el: '#feeds',
        data: {
            feeds: [],
            page: 1,
            type: 0,   // 0 所有，1 单个用户, 2 同班同学（假的）
            user_id: 0,
            display_id: 0,
            request_user_id: 0,
            can_manage: false // 当前用户是否可以管理日志
        },

        methods: {
            load_all_page: function (e) {
                e.preventDefault();
                feeds.user_id = 0;
                feeds.type = 0;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            load_feedstar_page: function (e) {
                feeds.type = 4;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            load_classmates_page: function (user_id) {
                feeds.user_id = user_id;
                feeds.type = 2;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            load_my_page: function (user_id) {
                feeds.user_id = user_id;
                feeds.type = 1;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            remove_feed: function (feed_id) {
                for (var i = 0; i < this.feeds.length; i++) {
                    var feed = this.feeds[i];
                    if (feed.id === feed_id) {
                        this.feeds.splice(i, 1);
                    }
                }
            }
        }
    });

    var loader = new Vue({
        el: '#feeds-loader',
        data: {
            status: 0
        },

        methods: {
            load_more_page: function (e) {
                e.preventDefault();

                feeds.page++;
                loader.status = 1;
                load_page_data();
            }
        }
    });

    Vue.component('image-list', {
        template: '#image-list',
        props: ['name'],
    });

    Vue.component('feed', {
        template: '#feed-template',
        props: ['id', 'publisher_data','publisher_name', 'publisher_avatar', 'content', 'emojis', 'comments', 'created_at',
            'input_show',
            'link_name', 'link_link', 'images', 'is_stick', 'stick_expired_at', 'is_star', 'star_at'],
        data: function () {
            return {
                data_id: this.id,
                data_publisher: this.publisher_data,

                data_content: this.content,
                data_emojis: this.emojis,
                data_comments: this.comments,
                data_created_at: this.created_at,
                data_input_show: this.input_show,
                data_link_name: this.link_name,
                data_link_link: this.link_link,
                data_is_star: this.is_star,
                data_is_stick: this.is_stick,
                new_comment: '',
                data_images: this.images,
                is_truncate: true,
                image_showbox_url: null,
                image_download_link: null,
                OwO: null,
                comment_to_user: null,
                _comment_to_user_name: null,
            };
        },

        updated: function () {
            if (this.data_input_show === true) {
                this.OwO = new OwO({
                    logo: 'OωO表情',
                    container: this.$el.getElementsByClassName('OwO')[0],
                    target: this.$el.getElementsByClassName('OwO-textarea')[0],
                    api: '../static/bee_django_social_feed/OwO.json',
                    position: 'down',
                    width: '100%',
                    maxHeight: '250px'
                });
            }
        },

        computed: {
            // 当前登录用户，是否给该条feed点过赞了？
            is_request_user_emoji: function () {
                var rc = false;

                if (typeof(this.data_emojis) === "undefined") {
                    return rc;
                }

                this.data_emojis.forEach(function (i) {
                    if (i.user_id === feeds.request_user_id) {
                        rc = true;
                    }
                });

                return rc;
            },

            // 该条feed 是否有人点赞了？
            has_emojis: function () {
                if (typeof(this.data_emojis) === "undefined") {
                    return false;
                } else {
                    return this.data_emojis.length > 0;
                }
            },

            // 是否有评论了
            has_comments: function () {
                if (typeof(this.data_comments) === "undefined") {
                    return false;
                } else {
                    return this.data_comments.length > 0;
                }
            },

            // 是否有链接名称
            has_link_name: function () {
                if (typeof(this.data_link_name) === "undefined") {
                    return false;
                } else {
                    return this.data_link_name != null;
                }
            },

            // 是否有链接内容
            has_link_link: function () {
                if (typeof(this.data_link_link) === "undefined") {
                    return false;
                } else {
                    return this.data_link_link != null;
                }
            },

            // 是否有传图片
            images_count: function () {
                if (typeof(this.data_images) === "undefined") {
                    return 0;
                } else {
                    if (this.data_images === null) {
                        return 0;
                    } else {
                        return this.data_images.length;
                    }
                }
            },
        },

        methods: {
            load_user_page: function (user_id, e) {
                e.preventDefault();
                feeds.user_id = user_id;
                feeds.type = 1;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            load_feed_data: function (feed_id) {
                feeds.type = 3;
                feeds.display_id = feed_id;
                feeds.page = 1;
                feeds.feeds = [];
                remove_location_params();
                load_page_data();
            },

            show_image: function (image) {
                this.image_showbox_url = image.medium_url;
                this.image_download_link = image.image;
            },

            fold_image: function () {
                this.image_showbox_url = null;
                this.image_download_link = null;
            },

            // 显示被截短的日志全文
            fold_content: function () {
                this.is_truncate = false;
            },

            // 收起日志全文
            unfold_content: function () {
                this.is_truncate = true;
            },

            // 点赞
            post_emoji: function (feed_id) {
                var this_feed = this;
                $.post('/feed/feeds/' + String(feed_id) + '/emoji')
                    .done(function (data) {
                        this_feed.data_emojis = this_feed.data_emojis.concat(JSON.parse(data['new_emoji']));
                    })
            },

            // 显示feed的评论输入框
            show_comment_input: function (to_user,to_user_name) {
                if (to_user) {
                    this.comment_to_user = to_user;
                    this._comment_to_user_name=to_user_name;
                } else {
                    this.comment_to_user = null;
                    this._comment_to_user_name=null
                }
                this.data_input_show = !this.data_input_show;

            },

            // 发表对feed的评论
            post_comment: function (feed_id, comment) {
                if (comment) {
                    var this_feed = this;
                    if (this.comment_to_user) {
                        var to_user_id = this.comment_to_user.id;
                    } else {
                        var to_user_id = null;
                    }
                    var post_data = {
                        comment: comment,
                        to_user_id: to_user_id
                    };
                    $.post('/feed/feeds/' + String(feed_id) + '/comment', post_data)
                        .done(function (data) {
                            this_feed.data_comments = this_feed.data_comments.concat(JSON.parse(data['new_comments']));
                            this_feed.new_comment = '';
                            this_feed.data_input_show = false;
                        })
                } else {
                    alert("请输入一点文字");
                }
            },

            // 判断评论是否有to_user
            comment_to_user_exists: function () {
                return this.comment_to_user != null;
            },

            comment_to_user_name: function () {
                var user_name = this._comment_to_user_name;
                return "回复 " + user_name + " :"
            },

            // 给feed加精
            star_feed: function (feed_id) {
                var this_feed = this;
                var url = "/feed/feeds/" + String(feed_id) + "/star";
                axios.post(url).then(function (resp) {
                    var data = resp['data'];
                    this_feed.data_is_star = true;
                    alert(data['message']);
                });
            },

            // 取消feed加精
            unstar_feed: function (feed_id) {
                var this_feed = this;
                var url = "/feed/feeds/" + String(feed_id) + "/unstar";
                axios.post(url).then(function (resp) {
                    var data = resp['data'];
                    this_feed.data_is_star = false;
                    alert(data['message']);
                });
            },

            // 给feed置顶
            stick_feed: function (feed_id) {
                var this_feed = this;
                var url = "/feed/feeds/" + String(feed_id) + "/stick";
                axios.post(url).then(function (resp) {
                    var data = resp['data'];
                    this_feed.data_is_stick = true;
                    alert(data['message']);
                    window.history.go();
                });
            },

            // 取消feed的置顶状态
            unstick_feed: function (feed_id) {
                var this_feed = this;
                var url = "/feed/feeds/" + String(feed_id) + "/unstick";
                axios.post(url).then(function (resp) {
                    var data = resp['data'];
                    this_feed.data_is_stick = false;
                    alert(data['message']);
                });
            },

            // 删除feed
            delete_feed: function (feed_id) {
                if (confirm('确定删除?')) {
                    var this_feed = this;
                    var url = "/feed/feeds/" + String(feed_id) + "/delete";
                    axios.post(url).then(function (resp) {
                        var data = resp['data'];
                        if (data['rc'] === 0) {
                            alert(data['message']);
                            feeds.remove_feed(feed_id);
                        } else if (data['rc'] === -1) {
                            alert(data['message']);
                        }
                    });
                }

            },

            // 是否可以删除
            can_delete_feed: function (publisher_data) {
                if (feeds.can_manage) {
                    return true;
                } else {
                    return feeds.request_user_id === publisher_data.id;
                }
            },

            // 是否可以加精
            can_star_feed: function (publisher_data) {
                return feeds.can_manage;
            },

            // 是否可以置顶
            can_stick_feed: function (publisher_data) {
                return feeds.can_manage;
            },

            // 删除feed的评论
            delete_comment: function (comment_id) {
                if (confirm('确定删除评论？')) {
                    var _this = this;
                    var url = "/feed/feed_comment/" + String(comment_id) + '/delete';
                    axios.post(url).then(function (resp) {
                        var data = resp['data'];
                        if (data['rc'] === 0) {
                            alert(data['message']);
                            _this.remove_comment(comment_id);
                        } else if (data['rc'] === -1) {
                            alert(data['message']);
                        }
                    });
                }
            },

            // 回复评论
            reply_comment: function (comment_id, user_data) {

            },

            // 从this.comments里面移除comment_id对应的comment
            remove_comment: function (comment_id) {
                var comments = this.data_comments;
                for (var i = 0; i < comments.length; i++) {
                    var comment = comments[i];
                    if (comment.id === comment_id) {
                        comments.splice(i, 1);
                    }
                }
            },

            // 是否可以删除评论
            can_delete_comment: function (publisher_data) {
                if (feeds.can_manage) {
                    return true;
                } else {
                    return feeds.request_user_id === publisher_data.id;
                }
            },

            // 点击评论处理事件 如果点自己的就是删除，点别人的就是回复
            on_click_comment: function(comment) {
                if (comment.user_id === feeds.request_user_id) {
                    this.delete_comment(comment.id);
                } else {
                    this.show_comment_input(comment.user_data, comment.user_name);
                }
            }
        },

        watch: {
            emojis(val) {
                this.data_emojis = val;
            },

            data_emojis(val) {
                this.$emit('update:emojis', val);
            },

            input_show(val) {
                this.data_input_show = val;
            },

            data_input_show(val) {
                this.$emit('update:input_show', val);
            },

            comments(val) {
                this.data_comments = val;
            },

            data_comments(val) {
                this.$emit('update:comments', val);
            },

            images(val) {
                this.data_images = val;
            },

            data_images(val) {
                this.$emit('update:images', val);
            },

            is_star(val) {
                this.data_is_star = val;
            },

            data_is_star(val) {
                this.$emit('update:is_star', val);
            },

            is_stick(val) {
                this.data_is_stick = val;
            },

            data_is_stick(val) {
                this.$emit('update:is_stick', val);
            }
        }
    });

    Vue.component('star', {
        template: '#star',
    });

    Vue.component('unstar', {
        template: '#unstar',
    });

    Vue.component('stick', {
        template: '#stick',
    });

    Vue.component('unstick', {
        template: '#unstick',
    });

    Vue.component('emoji-button', {
        template: '#emoji-button',
        props: ['feel']
    });

    Vue.component('emoji-did', {
        template: '#emoji-did'
    });

    Vue.component('comment-button', {
        template: '#comment-button',
        props: ['show_input']
    });

    moment.locale('zh-cn');
    Vue.filter('formatDate', function (value) {
        if (value) {
            return moment(String(value)).fromNow();
        }
    });

    Vue.filter('truncate', function (text, length, clamp) {
        text = text || '';
        clamp = clamp || '...';
        length = length || 140;

        if (text.length <= length) return text;

        var tcText = text.slice(0, length - clamp.length);
        var last = tcText.length - 1;


        while (last > 0 && tcText[last] !== ' ' && tcText[last] !== clamp[0]) last -= 1;

        // Fix for case when text dont have any `space`
        last = last || length - clamp.length;

        tcText = tcText.slice(0, last);

        return tcText + clamp;
    });


    // 拉取指定页面的feeds
    var load_page_data = function () {
        var options = {
            page: feeds.page,
            type: feeds.type,
            user_id: feeds.user_id,
            display_id: feeds.display_id,
        };

        var url_string = window.location.href;
        var url = new URL(url_string);
        var data_type = url.searchParams.get('type');
        var data_display_id = url.searchParams.get('display_id');
        if (data_type && data_display_id) {
            options.type = data_type;
            options.display_id = data_display_id;
        }

        $.get('/feed/feeds', options)
            .done(function (data) {
                var new_feeds = JSON.parse(data['feeds']);
                feeds.request_user_id = data['request_user_id'];
                feeds.can_manage = data['can_manage'];
                if (new_feeds.length === 0) {
                    feeds.page = data['page'];
                    loader.status = 3;
                } else {
                    feeds.feeds = feeds.feeds.concat(new_feeds);
                    feeds.page = data['page'];
                    loader.status = 0;
                }

                // console.log('第' + feeds.page + '页拉取完毕');
            })
            .fail(function () {
                loader.status = 2;
            })
    };
    load_page_data();

    // 下拉翻页的处理
    window.onscroll = function (e) {
        var bottomOfWindow = (window.scrollY || window.pageYOffset || document.documentElement.scrollTop)
            + window.innerHeight >= document.documentElement.offsetHeight;

        if (bottomOfWindow) {
            loader.load_more_page(e);
        }
    }
});