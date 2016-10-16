% from operator import attrgetter
% rebase('base.tpl', title=fg_tournament['name'])
<div class="col-xs-12">
    <h4 class="display-4">{{fg_tournament['name']}}</h4>
</div>

<div class="col-xs-12 col-lg-4">
    <h5>Participants</h5>
    <table class="table">
    % for p in sorted(pool.participants.values(), key=lambda p: p.rank_for_sort):
        <tr>
            <td>{{!p.link_or_text}}</td>
            <td>{{p.rank_text}}</td>
        </tr>
    % end
    </table>
</div>

<div class="col-xs-12 col-lg-8">
    <h5>Matches</h5>
    <table class="table">
    <% group = None %>
    % for m in sorted(pool.matches.values(), key=attrgetter('tournament_id', 'group_id', 'sort_key', 'id_desc')):
        % if group is None or group != m.group:
            <thead>
                <tr>
                    <th colspan="5">{{m.group.name}}</th>
                </tr>
            </thead>
            <tbody>
        % end
        <tr>
            <% p1 = '<b><u>{0}</u></b>' if m.p1_win else '{0}' %>
            <% p2 = '<b><u>{0}</u></b>' if m.p2_win else '{0}' %>
            <td class="text-xs-center">{{m.round_name}}</td>
            <td class="text-xs-right">{{!p1.format(m.player1.link_or_text)}}</td>
            <td class="text-xs-center">{{m.scores_csv}}</td>
            <td class="text-xs-left">{{!p2.format(m.player2.link_or_text)}}</td>
        </tr>
        <% group = m.group %>
    % end
        </tbody>
    </table>
</div>
