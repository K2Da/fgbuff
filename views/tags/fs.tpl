<FS>
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
    <button type="button" class="btn btn-primary" onclick={ onClickAddMatch }>add match</button>
    <button type="button" class="btn btn-primary" onclick={ onClickDeleteGroup }>delete group</button>

    <div style="width: { this.store.max_round(this.group_id) * match_width }px">
        <table>
            <tr>
                <td each={ round in self.store.rounds(this.group_id, 'win') } style="width: { match_width }px;" valign="top">
                    <matches group_id={ parent.group_id } round={ 1 } store={ parent.store }></matches>
                </td>
            </tr>
        </table>
        <br />
    </div>

    self = this
    this.store    = opts.store
    this.editor   = opts.store.pool_editor(opts.group_id)
    this.group_id = opts.group_id
    this.group    = this.store.group(this.group_id)

    onClickAddMatch(e) { self.store.pool_editor(this.group_id).add_match() }
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
</FS>
