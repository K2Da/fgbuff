<players>
    <button type="button" class="btn btn-primary" onclick={onClickRefresh}>
        refresh
    </button>
    <table class='table'>
        <tr each={ participant, i in self.store.participants() }>
            <td>{ i + 1 }</td>
            <td>
                <a onclick={ this.onDelete }>del</a>
            </td>
            <td>
                <input
                    class    = 'form-control'
                    value    = { participant.name }
                    onchange = { this.onNameChange }
                    style    = 'width: 10em; text-align: left;'
                />
            </td>
            <td>
                <player-input
                    store       = { self.store }
                    url         = { self.store.player_url(participant.player_id)}
                    participant = { this }
                >
                </player-input>
            </td>
            <td>
                <input
                    class    = 'form-control'
                    type     = 'number'
                    value    = { participant.final_rank }
                    onchange = { this.onRankChange }
                    style    = 'width: 5em; text-align: right;'
                />
            </td>
            <td>
                { self.store.last_at_winners(participant.id) } / { self.store.last_at_losers(participant.id) }
            </td>
        </tr>
        <ul id='player_li' style='display: none;'>
            <li each={ self.store.players() }>{ url }</li>
        </ul>
    </table>

    <style scoped>
        :scope { display: block }
        .table td, .table th {
            padding: 0.2em;
            vertical-align: middle;
        }

    </style>

    var self = this
    self.store = opts.store

    onRankChange(e) {
        e.preventUpdate = true
        this.store.update(
            'challo_participant', e.item.participant.id, [['final_rank', e.srcElement.value]]
        )
    }

    onNameChange(e) {
        e.preventUpdate = false
        this.store.update(
            'challo_participant', e.item.participant.id, [['name', e.srcElement.value.trim()]]
        )
    }

    onDelete(e) {
        this.store.remove('challo_participant', e.item.participant.id)
    }

    onClickRefresh(e) {
    }
</players>
