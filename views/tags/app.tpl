<app>
    <div style="padding: 1em;">
        <p>{ self.store.msg }</p>
        <button type="button" class="btn btn-primary" onclick={ onClickPush }>push</button>
        <button type="button" class="btn btn-primary" onclick={ onClickAddParticipant }>add participant</button>
        <button type="button" class="btn btn-primary" onclick={ onClickAddGroup }>add group</button>

        <div style="width: 600px">
            <players app={ this } store={ this.store }></players>
        </div>

        <div each={ self.store.groups() }>
            <de store={ parent.store } group_id={ id } if={ ttype == 'DE' }></de>
            <se store={ parent.store } group_id={ id } if={ ttype == 'SE' }></se>
            <fs store={ parent.store } group_id={ id } if={ ttype == 'FS' }></fs>
        </div>
        <participants-li store={ self.store }></participants-li>
    </div>

    <style>
        :scope { display: block; }
        .custom-select {
            padding: 0.1rem 1.5rem 0.1rem 0.5rem
        }
        .form-control {
            padding: 0.2rem 0.5rem 0.2rem 0.5rem
        }
    </style>

    this.title = opts.title
    var self = this

    RiotControl.on('refresh', (store) => {
        self.store = store
        self.update()
    })

    onClickPush(e) { self.store.push_store_to_server() }
    onClickAddParticipant(e) { self.store.add_participant(1) }
    onClickAddGroup(e) { self.store.add_group() }
</app>
