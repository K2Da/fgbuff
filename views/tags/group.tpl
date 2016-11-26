<group>
    <h2>{ this.group.name }</h2>
    <button type="button" class="btn btn-primary" onclick={ onClickAddRound }>add round bottom</button>
    <button type="button" class="btn btn-primary" onclick={ onClickStretchRound }>stretch round top</button>
    <button type="button" class="btn btn-primary" onclick={ onClickFillRounds }>fill rounds</button>
    <button type="button" class="btn btn-primary" onclick={ onClickClearMatches }>clear matches</button>
    <button type="button" class="btn btn-primary" onclick={ onClickDeleteGroup }>delete group</button>

    <h3>{ this.store.pool_editor(this.group_id).current_total_round }</h3>

    <div style="width: { this.store.max_round(this.group_id) * match_width }px">
        <h3>winners</h3>
        <bracket store={ this.store } group_id={ this.group_id } type="win"></bracket>

        <h3>losers</h3>
        <bracket store={ this.store } group_id={ this.group_id } type="lose"></bracket>
    </div>

    this.store    = opts.store
    this.group_id = opts.group_id
    this.group    = this.store.group(this.group_id)

    onClickAddRound(e) { self.store.add_round(this.group_id, true) }
    onClickStretchRound(e) { self.store.add_round(this.group_id, false) }
    onClickFillRounds(e) { self.store.fill_rounds(this.group_id) }
    onClickClearMatches(e) { self.store.clear_matches(this.group_id) }
    onClickDeleteGroup(e) { self.store.delete_group(this.group_id) }
</group>
