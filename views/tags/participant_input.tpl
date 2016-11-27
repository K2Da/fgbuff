<participant-input>
    <input
        class    = 'awesomplete form-control'
        ref      = 'player_name'
        type     = 'text'
        value    = { this.name }
        onchange = { this.onParticipantChange }
    />

    var self = this
    this.store          = opts.store
    this.participant_id = opts.participant_id
    this.match          = opts.match
    this.side           = opts.side
    this.awesomplete    = null

    let participant = self.store.participant_by_id(self.match[self.side])
    self.name = participant ? participant.name : ''

    onParticipantChange(e) {
        let participant = this.store.participant_by_name(e.srcElement.value)
        if (participant != null) {
            this.store.update_match(this.match.id, [[this.side, participant.id]])
        }
    }

    this.on('mount', () => {
        var input = self.refs.player_name
        self.awesomplete = new Awesomplete(input, { list: self.store.participant_names(), minChars: 1, autoFirst: true })
        input.addEventListener('awesomplete-selectcomplete', self.onParticipantChange)
    })
</participant-input>

