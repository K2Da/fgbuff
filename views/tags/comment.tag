<comment>
    <form class="form-inline float-xs-right">
        <button type="button"
            class="btn btn-outline-danger" data-container="body" data-toggle="popover" data-placement="bottom"
            data-content={ this.comments } title="comments">
                { this.store.comments.length }
        </button>
        <input name="input_comment" class="form-control" type="text" placeholder="Comment">
        <button class="btn btn-outline-success" onclick={ this.write }>push</button>
    </form>

    this.page_url = opts.page_url
    this.store = new CommentStore(this.page_url)
    RiotControl.addStore(this.store)
    self = this
    this.wrote = false

    RiotControl.on('refresh', (store) => {
        self.store = store
        this.comments = store.comment_list()
        self.update()
        if (this.wrote) {
            $('[data-toggle="popover"]').popover('show')
            this.wrote = false
        }
    })

    write(e) {
        this.store.write(this.input_comment.value)
        this.input_comment.value = ''
        this.wrote = true
        $('[data-toggle="popover"]').popover('hide')
    }

    $(function () {
        $('[data-toggle="popover"]').popover({ html : true })
    })
</comment>