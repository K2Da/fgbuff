<players>
    <table class='table'>
        <tr each={ participant, i in self.store.participants() }>
            <td>{ i + 1 }</td>
            <td>
                <a onclick={ this.onDelete }>del</a>
            </td>
            <td>
                <name-input
                    store       = { self.store }
                    url         = { self.store.player_url(participant.player_id)}
                    participant = { participant }
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
    this.store = opts.store

    onRankChange(e) {
        parent.store.update(
            'challo_participant', e.item.participant.id, [['final_rank', e.srcElement.value == 0 ? null : e.srcElement.value]]
        )
    }


    onDelete(e) {
        parent.store.remove('challo_participant', e.item.participant.id)
    }
</players>
