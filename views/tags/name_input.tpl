<name-input>
    <input
        class    = 'awesomplete form-control'
        type     = 'text'
        value    = { this.participant.name }
        onchange = { this.onNameChange }
    />

    var self = this
    this.store = opts.store
    this.participant = opts.participant

    this.on('mount', () => {
        var input = this.root.firstElementChild
        new Awesomplete(input, {list: '#player_li', minChars: 1, autoFirst: true })
        input.addEventListener('awesomplete-selectcomplete', this.onNameChange)
    })

    onNameChange(e) {
        e.preventUpdate = false
        parent.store.update(
            'challo_participant', self.participant.id, [['name', e.srcElement.value.trim()]]
        )
    }
</name-input>
