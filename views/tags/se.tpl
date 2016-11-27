<SE>
    <input
        ref      = 'group_name'
        type     = "text"
        value    = "{ this.group.name }"
        onchange = { this.onNameChange }
    /><br />
    <input
        ref      = 'group_type'
        type     = 'text'
        value    = '{ this.group.ttype }'
        onchange = { this.onTypeChange }
    /><br />
    <button type="button" class="btn btn-primary" onclick={ onClickAddRound }>add round bottom</button>
    <button type="button" class="btn btn-primary" onclick={ onClickStretchRound }>stretch round top</button>
    <button type="button" class="btn btn-primary" onclick={ onClickFillRounds }>fill rounds</button>
    <button type="button" class="btn btn-primary" onclick={ onClickClearMatches }>clear matches</button>
    <button type="button" class="btn btn-primary" onclick={ onClickDeleteGroup }>delete group</button>

    <h3>{ this.store.pool_editor(this.group_id).current_total_round }</h3>

    <div style="width: { this.store.max_round(this.group_id) * match_width }px">
        <h3>winners</h3>
        <bracket store={ this.store } group_id={ this.group_id } type="win"></bracket>
    </div>

    self = this
    this.store    = opts.store
    this.editor   = opts.store.pool_editor(opts.group_id)
    this.group_id = opts.group_id
    this.group    = this.store.group(this.group_id)

    onClickAddRound(e) { self.store.pool_editor(self.group_id).add_round(true) }
    onClickStretchRound(e) { self.store.pool_editor(self.group_id).add_round(false) }
    onClickFillRounds(e) { self.store.pool_editor(self.group_id).fill_rounds() }
    onClickClearMatches(e) { self.store.pool_editor(self.group_id).clear_matches() }
    onClickDeleteGroup(e) { self.store.delete_group(this.group_id) }

    onNameChange(e) {
        this.store.update(
            'challo_group', this.group_id, [['name', this.refs.group_name.value]]
        )
    }
    onTypeChange(e) {
        this.store.update(
            'challo_group', this.group_id, [['ttype', this.refs.group_type.value]]
        )
    }
</SE>
