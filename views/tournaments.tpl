% from operator import attrgetter
% rebase('base.tpl', title='Tournaments')

<h4 class="display-4">Tournaments</h4>
<table class="table">
% for t in sorted(pool.tournaments.values(), key=attrgetter('end_at_desc')):
    <tr>
        <td>{{!t.link_or_name}}</a></td>
        <!-- <td>{{t.type}}</td> -->
        <td>{{!t.end_at}}</td>
        <td>{{!t.challonge_link}}</td>
    </tr>
% end
</table>
