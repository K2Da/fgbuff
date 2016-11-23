class Store {
    constructor() {
        riot.observable(this)
        var self = this
        window.superagent
            .get('/api/tournament/' + TOURNAMENT_URL)
            .end((err, res) => {
                self.pool = res.body
                self.pool_editors = {}
                self.pool.challo_group.forEach((row) => {
                    self.pool_editors[row.id] = new DoubleElimination(self, row.id)
                })
                self.trigger('refresh', self)
                self.tournament = self.pool.fg_tournament[0]
            })
    }

    push_store_to_server() {
        var self = this
        window.superagent
            .post('/api/update')
            .send(self.pool)
            .end((err, res) => { alert(res.text) })
    }

    last_at_losers(id) {
        this.pool.challo_match.sort((a, b) => a.round - b.round)
        let last_match = this.pool.challo_match.find(
            (row) => row.player1_id == id || row.player2_id == id
        )
        return last_match && last_match.round < 0
            ? last_match.round
            : 0
    }

    last_at_winners(id) {
        this.pool.challo_match.sort((a, b) => b.round - a.round)
        let last_match = this.pool.challo_match.find(
            (row) => row.player1_id == id || row.player2_id == id
        )
        return last_match && last_match.round > 0
            ? last_match.round
            : 0
    }

    rounds(group_id, type) {
        let rounds = Array.from(
            this.pool.challo_match.filter((x, i, self) => x['group_id'] == group_id),
            (s) => s['round']
        )
        rounds = rounds.filter((x, i, self) =>
            self.indexOf(x) === i && (type == 'win' && x > 0 || type == 'lose' && x < 0)
        )
        return rounds.sort((a, b) => (a - b) * (type == 'win' ? 1 : -1))
    }

    max_round(group_id) {
        let abss = Array.from(this.pool.challo_match, (s) => s['group_id'] == group_id ? Math.abs(s['round']) : 0)
        return Math.max.apply(null, abss)
    }

    matches(group_id, round) {
        return this.pool.challo_match
            .filter((x, i, self) => x.group_id == group_id && x.round == round)
            .sort((a, b) => b.id - a.id)
    }

    participants() {
        let ret = []
        this.pool.challo_participant.forEach((row) => {
            ret.push(row)
        })
        let self = this
        return ret.sort((a, b) => {
            let al = self.last_at_losers(a.id)
            let bl = self.last_at_losers(b.id)
            let aw = self.last_at_winners(a.id)
            let bw = self.last_at_winners(b.id)
            if (al == 0 && aw != 0) al = -100
            if (bl == 0 && bw != 0) bl = -100
            a = (al == 0 && aw == 0) ? 1000 - a.id : al * -10 + aw
            b = (bl == 0 && bw == 0) ? 1000 - b.id : bl * -10 + bw
            return b - a
        })
    }

    player_url(player_id) {
        let player = this.player_by_id(player_id)
        return player ? player.url : ''
    }

    players() {
        let ret = []
        this.pool.fg_player.forEach((row) => { ret.push(row) })
        return ret.sort((a, b) => a.url > b.url ? -1 : 1 )
    }

    player_by_url(url) {
        return this.pool.fg_player.find((row) => row['url'] == url)
    }

    update(table, id, values) {
        let rows = this.pool[table]
        rows.forEach((row) => {
            if (row['id'] == id) {
                values.forEach((kv) => { row[kv[0]] = kv[1] })
            }
        })
    }

    remove(table, id) {
        let rows = this.pool[table]
        rows.splice(rows.indexOf(rows.find((row) => row['id'] == id)), 1)
    }

    update_match(id, values) {
        this.update('challo_match', id, values)
        let match = this.match_by_id(id)
        if (match == null || match.scores_csv == null) return
        let scores = match.scores_csv.split('-')
        if (scores.length == 2) {
            if (scores[0] > scores[1]) {
                match.winner_id = match.player1_id
            }
            if (scores[0] < scores[1]) {
                match.winner_id = match.player2_id
            }
        }
    }

    match_by_id(id) {
        return this.pool.challo_match.find((row) => row['id'] == id)
    }

    participant_by_id(id) {
        return this.pool.challo_participant.find((row) => row['id'] == id)
    }

    player_by_id(id) {
        return this.pool.fg_player.find((row) => row['id'] == id)
    }

    participant_by_name(name) {
        return this.pool.challo_participant.find((row) => row['name'] == name)
    }

    player_by_participant_id(id) {
        var participant = this.participant_by_id(id)
        return this.player_by_id(participant.player_id)
    }

    add_participant(count) {
        for (let i = 0; i < count; i++) {
            this.pool.challo_participant.push({
                tournament_id : this.tournament.id,
                id            : this.max_id('challo_participant') + 1,
                name          : null,
                final_rank    : null,
                player_id     : null,
            })
        }
    }

    refresh() {
        this.trigger('refresh', self)
    }

    groups() {
        return this.pool.challo_group.sort((a, b) => a.id - b.id)
    }

    group(group_id) {
        return this.pool.challo_group.find((row) => row.id == group_id)
    }

    add_round(group_id, move) { this.pool_editors[group_id].add_round(move) }
    fill_rounds(group_id) { this.pool_editors[group_id].fill_rounds() }
    delete_group(group_id) { this.pool_editors[group_id].delete_group() }

    clear_matches(group_id) { this.pool_editors[group_id].clear_matches() }

    pool_editor(group_id) {
        return this.pool_editors[group_id]
    }

    max_id(table) {
        let max = 0
        this.pool[table].forEach((row) => {
            if (row.id > max) {
                max = row.id
            }
        })
        return max
    }
}

class PoolEditor {
    constructor(store, group_id) {
        this.store      = store
        this.pool       = store.pool
        this.group_id   = group_id
        this.group      = this.pool.challo_group.find((row) => row.id == group_id)
        this.tournament = this.pool.fg_tournament[0]
    }

    add_round() { }

    remove_round() { }

    delete_group(group_id) {
        this.pool.challo_group = this.pool.challo_group.filter((x, i, self) => x['id'] != this.group_id)
        this.pool.challo_match = this.pool.challo_match.filter((x, i, self) => x['group_id'] != this.group_id)
    }

    match_count_in_round(round) {
        self = this
        let arr = this.pool.challo_match.filter((match) => match.group_id == self.group_id && match.round == round)
        return arr.length
    }

    add_groups(count) {
        for (let i = 0; i < count; i++) {
            this.pool.challo_group.push({
                tournament_id : this.tournament.id,
                id            : this.max_id('challo_group') + 1,
                min_round     : 0,
                max_round     : 0,
                name          : 'Main Tournament',
            })
        }
    }

    add_matches(round, count) {
        for (let i = 0; i < count; i++) {
            this.pool.challo_match.push({
                tournament_id : this.tournament.id,
                group_id      : this.group.id,
                id            : this.max_id('challo_match') + 1,
                round         : round,
                player1_id    : null,
                player2_id    : null,
                winner_id     : null,
                scores_csv    : null,
            })
        }
    }

    clear_matches() {
        this.group_matches().forEach((row) => {
            row.player1_id = null
            row.player2_id = null
            row.winner_id  = null
            row.scores_csv = null
        })
    }

    max_id(table) {
        return this.store.max_id(table)
    }

    group_matches() {
        return this.pool.challo_match.filter((x, i, self) => x['group_id'] == this.group_id)
    }
}

class DoubleElimination extends PoolEditor {
    constructor(store, group_id) {
        super(store, group_id)
        this.current_total_round = this.get_total_round()
        if (this.pool.challo_group.length == 0) {
            this.add_groups(group_id)
        }
    }

    add_round(move) {
        if (move) { this.update_round(this.current_total_round, this.current_total_round + 1) }
        this.current_total_round++
        this.fill_rounds()
    }

    fill_rounds() {
        let match_counts = this.match_numbers_by_total_rounds(this.current_total_round)
        let max = 0
        let min = 0
        for (let round in match_counts) {
            round = Number(round)
            if (round > max) max = round
            if (round < min) min = round
            this.add_matches(
                round, match_counts[round] - this.match_count_in_round(round)
            )
        }
        this.store.update('challo_group', this.group.id, [['max_round', max], ['min_round', min]])
    }

    get_participants_count(match_counts) {
        console.log(match_counts)
        if (match_counts[1] != match_counts[-1] * 2) {
            return match_counts[1] * 2 + match_counts[-1]
        } else {
            return match_counts[1] * 2
        }
    }

    update_round(from, to) {
        var w_diff = this.max_winners_round(to) - this.max_winners_round(from)
        var l_diff = this.max_losers_round(to) - this.max_losers_round(from)

        this.group_matches().forEach((row) => {
            if (row.round > 0) {
                row.round += w_diff
            }
            if (row.round < 0) {
                row.round -= l_diff
            }
        })
    }

    get_total_round() {
        var matches = this.group_matches().sort((a, b) => a.round - b.round)
        if (matches.length == 0) {
            return 0
        }
        if (matches[0].round == 1) {
            return 1
        }
        return Math.abs(matches[0].round) + 1
    }

    match_numbers_by_total_rounds(total_rounds) {
        var win_max  = this.max_winners_round(total_rounds)
        var lose_max = this.max_losers_round(total_rounds)

        var match_count = {}
        for (let win = 0; win < win_max; win++) {
            match_count[win_max - win] = win == 0 ? 2 : Math.pow(2, win - 1)
        }
        for (let lose = 0; lose < lose_max; lose++) {
            match_count[-(lose_max - lose)] = Math.pow(2, Math.floor(lose/2))
        }
        return match_count
    }

    max_winners_round(total_rounds) {
        return Math.ceil(total_rounds/2) + 1
    }

    max_losers_round(total_rounds) {
        return total_rounds - 1
    }
}
