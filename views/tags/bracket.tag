<bracket>
    <table>
        <tr>
            <td each={ round, i in self.store.rounds(this.type) } style="width: { match_width }px;" valign="top">
                <matches round={ round } store={ parent.store }></matches>
            </td>
        </tr>
    </table>
    <style scoped>
        :scope { display: block }
        .table td, .table th {
            padding: 0.2em;
            vertical-align: top;
        }
    </style>

    var self   = this
    this.store = opts.store
    this.type  = opts.type
</bracket>
