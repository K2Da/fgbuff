% from operator import attrgetter
% rebase('base.tpl', title='Players')

<h4 class="display-4">Players</h4>
<table class="table">
% for p in sorted(pool.players.values(), key=attrgetter('sort_key')):
    <tr>
        <td><a href="/player/{{p.url}}">{{p.name}}</a></td>
        <td class="text-xs-center">{{p.win}} - {{p.lose}}</td>
    </tr>
% end
</table>
