<player-input>
    <input
        class    = 'awesomplete form-control'
        type     = 'text'
        value    = { opts.url }
        onchange = { this.onPlayerChange }
    />

    var self = this
    this.store = opts.store
    this.participant = opts.participant

    this.on('mount', () => {
        var input = this.root.firstElementChild
        new Awesomplete(input, {list: '#player_li', minChars: 1, autoFirst: true })
        input.addEventListener('awesomplete-selectcomplete', this.onPlayerChange)
    })

    onPlayerChange(e) {
        let player = this.store.player_by_url(e.srcElement.value)
        let name   = (this.participant.name == '' || this.participant.name == null)
            ? e.srcElement.value
            : this.participant.name
        if (player != null) {
            this.store.update(
                'challo_participant', this.participant.id, [['player_id', player.id], ['name', name]]
            )
        }
    }
</player-input>
