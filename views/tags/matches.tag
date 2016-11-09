<matches>
    <table>
        <colgroup>
            <col width="14px" >
            <col width="200px">
            <col width="50px" >
            <col width="200px">
        </colgroup>
        <tr each={ this.store.matches(this.round) }>
            <td><a onclick={ this.onDelete }>-</a></td>
            <td>
                <participant-input
                    side           = 'player1_id'
                    store          = { parent.store }
                    participant_id = { player1_id }
                    match          = { this }
                />
            </td>
            <td>
                <input
                    class    = 'form-control'
                    value    = { scores_csv }
                    onchange = { this.onScoreChange }
                    style    = 'width: 4em; text-align: center;'
                    match_id = { id }
                />
            </td>
            <td>
                <participant-input
                    side           = 'player2_id'
                    store          = { parent.store }
                    participant_id = { player2_id }
                    match          = { this }
                />
            </td>
        </tr>
    </table>

    var self   = this
    this.store = opts.store
    this.round = opts.round

    onScoreChange(e) {
        console.log(e.item.id)
        this.store.update_match(e.item.id, [['scores_csv', e.srcElement.value]])
    }

    onDelete(e) {
        this.store.remove('challo_match', e.item.id)
    }
</matches>
