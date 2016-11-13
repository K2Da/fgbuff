class CommentStore {
    constructor(page_url) {
        riot.observable(this)
        this.page_url = page_url
        this.read()
    }

    read() {
        var self = this
        window.superagent
            .post('/api/comment/read')
            .send({page_url: self.page_url})
            .end((err, res) => {
                self.comments = res.body
                self.trigger('refresh', self)
            })
    }

    write(text) {
        var self = this
        window.superagent
            .post('/api/comment/write')
            .send({page_url: self.page_url, text : text})
            .end((err, res) => { self.read() })
    }

    comment_list() {
        return this.comments.map(
            (c) => {
                return c.text.replace(/[&'`"<>]/g, function(match) {
                    return {
                        '&': '&amp;',
                        "'": '&#x27;',
                        '`': '&#x60;',
                        '"': '&quot;',
                        '<': '&lt;',
                        '>': '&gt;',
                    }[match]
                })
            }
        ).join('<br />')
    }
}