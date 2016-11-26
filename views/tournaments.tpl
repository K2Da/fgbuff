% from operator import attrgetter
% rebase('base.tpl', title='Tournaments')

<h4 class="display-4">Tournaments</h4>

% include('labels.tpl')

<table class="table">
% for t in sorted(pool.tournaments.values(), key=attrgetter('end_at_desc')):
    <tr>
        <td>{{!t.link_or_name}}</td>
        <td>{{!t.flag_span}}</td>
        <td style="vertical-align: middle;"><small>{{!t.labels_short}}</small></td>
        <td>{{t.date_string}}</td>
        <td>{{!t.tournament_link}}</td>
    </tr>
% end
</table>
