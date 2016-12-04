% from operator import attrgetter
% rebase('base.tpl', title='Players')

<h4 class="display-4">Players</h4>

% include('labels.tpl')

<table class="table">
% for p in sorted(pool.players.values(), key=attrgetter('rank_sort')):
    % count = len(p.participant_ids)
    % if count == 0:
        % continue
    % else:
    % ranks = p.rank_dic
    <tr>
        <td class="text-xs-right">{{!p.flag_span}}</td>
        <td><a href="/player/{{p.url}}">{{p.name}}</a></td>
        <td class="text-xs-left">{{'🥇 x ' + str(ranks[1]) if ranks[1] else ''}}</td>
        <td class="text-xs-left">{{'🥈 x ' + str(ranks[2]) if ranks[2] else ''}}</td>
        <td class="text-xs-left">{{'🥉 x ' + str(ranks[3]) if ranks[3] else ''}}</td>
        <td class="text-xs-right">in {{count}} tournaments</td>
        <td class="text-xs-center">{{p.win}} win - {{p.lose}} lose</td>
    </tr>
    % end
% end
</table>
