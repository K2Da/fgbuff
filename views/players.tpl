% from operator import attrgetter
% rebase('base.tpl', title='Players')

<h4 class="display-4">Players</h4>

% include('labels.tpl')

<table class="table">
% for p in sorted(pool.players.values(), key=attrgetter('sort_key')):
    % count = len(p.participant_ids)
    % if count == 0:
        % break
    % else:
    <tr>
        <td class="text-xs-right">{{!p.flag_span}}</td>
        <td><a href="/player/{{p.url}}">{{p.name}}</a></td>
        <td class="text-xs-right">{{len(p.participant_ids)}}</td>
        <td class="text-xs-center">{{p.win}} - {{p.lose}}</td>
    </tr>
    % end
% end
</table>
