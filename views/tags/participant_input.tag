<participant-input>
    <input class='awesomplete form-control'
        type     = 'text'
        column   = { opts.side }
        value    = { this.name }
        onchange = { this.onParticipantChange }
    />

    var self = this
    this.store          = opts.store
    this.participant_id = opts.participant_id
    this.match          = opts.match
    this.side           = opts.side

    this.on('mount', () => {
        var input = this.root.firstElementChild
        new Awesomplete(input, { list: '#participants_li', minChars: 1, autoFirst: true })
        input.addEventListener('awesomplete-selectcomplete', this.onParticipantChange)
    })

    onParticipantChange(e) {
        let participant = this.store.participant_by_name(e.srcElement.value)
        if (participant != null) {
            console.log(this.match)
            this.store.update_match(this.match.id, [[this.side, participant.id]])
        }
    }

    this.on('update', () => {
        let participant = self.store.participant_by_id(self.participant_id)
        self.name = participant ? participant.name : ''
    })
</participant-input>

