<app>
    <div style="padding: 1em;">
        <button type="button" class="btn btn-primary" onclick={onClickPush}>push</button>
        <button type="button" class="btn btn-primary" onclick={onClickAddParticipant}>add participant</button>
        <button type="button" class="btn btn-primary" onclick={onClickAddRound}>add round</button>
        <button type="button" class="btn btn-primary" onclick={onClickRemoveRound}>remove round</button>
        <button type="button" class="btn btn-primary" onclick={onClickRefresh}>refresh</button>

        <div style="width: 600px">
            <players store={ self.store }></players>
        </div>

        <participants-li store={ self.store }></participants-li>

        <div style="width: { self.store.max_round() * match_width }px">
            <h3>winners</h3>
            <bracket store={ self.store } type="win"></bracket>
            <h3>losers</h3>
            <bracket store={ self.store } type="lose"></bracket>
        </div>
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
    onClickAddRound(e) { self.store.add_round() }
    onClickRemoveRound(e) { self.store.remove_round() }
    onClickAddParticipant(e) { self.store.add_participant() }
    onClickRefresh(e) {}
</app>
